package com.quizz.core.ui;

import com.quizz.core.entity.QuizParticipant;
import com.quizz.core.entity.QuizSession;
import com.quizz.core.entity.User;
import com.quizz.core.service.QuizSessionService;
import com.quizz.core.service.UserService;
import com.vaadin.flow.component.UI;
import com.vaadin.flow.component.button.Button;
import com.vaadin.flow.component.button.ButtonVariant;
import com.vaadin.flow.component.html.*;
import com.vaadin.flow.component.icon.VaadinIcon;
import com.vaadin.flow.component.orderedlayout.HorizontalLayout;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import com.vaadin.flow.router.*;
import com.vaadin.flow.server.VaadinSession;
import com.vaadin.flow.server.auth.AnonymousAllowed;
import com.vaadin.flow.theme.lumo.LumoUtility;

@Route("quiz-session/:sessionCode")
@PageTitle("Quiz Session")
@AnonymousAllowed
public class QuizSessionView extends VerticalLayout implements BeforeEnterObserver {

    private final QuizSessionService sessionService;
    private final UserService userService;
    private QuizSession session;
    private String sessionCode;

    public QuizSessionView(QuizSessionService sessionService, UserService userService) {
        this.sessionService = sessionService;
        this.userService = userService;

        setSizeFull();
        addClassNames(LumoUtility.Padding.MEDIUM);
    }

    @Override
    public void beforeEnter(BeforeEnterEvent event) {
        sessionCode = event.getRouteParameters().get("sessionCode").orElse(null);

        if (sessionCode == null) {
            event.rerouteTo("");
            return;
        }

        session = sessionService.getSessionByCode(sessionCode);

        if (session == null) {
            add(new H2("Session not found"));
            add(new Paragraph("The session code '" + sessionCode + "' is invalid or has expired."));
            add(new Button("Back to Quiz List", e -> getUI().ifPresent(ui -> ui.navigate(""))));
            return;
        }

        User currentUser = VaadinSession.getCurrent().getAttribute(User.class);
        if (currentUser == null) {
            // Redirect to login
            event.rerouteTo(com.quizz.core.security.LoginView.class);
            return;
        }

        // Join the session
        sessionService.joinSession(session, currentUser);

        buildUI();
    }

    private void buildUI() {
        removeAll();

        // Bouton de retour en haut à gauche (visible uniquement quand le menu latéral n'est pas affiché)
        Button backButton = new Button("Back to Quiz List", VaadinIcon.ARROW_LEFT.create());
        backButton.addThemeVariants(ButtonVariant.LUMO_TERTIARY);
        backButton.addClickListener(event -> getUI().ifPresent(ui -> ui.navigate("quiz-list")));
        backButton.getStyle()
            .set("position", "absolute")
            .set("top", "10px")
            .set("left", "10px");

        // Hide back button when side menu is visible
        backButton.addAttachListener(attachEvent -> {
            getUI().ifPresent(ui -> {
                ui.getPage().executeJs(
                    "const checkMenu = () => {" +
                    "  const drawer = document.querySelector('vaadin-app-layout vaadin-drawer-toggle');" +
                    "  const sideNav = document.querySelector('vaadin-side-nav');" +
                    "  if (drawer && window.getComputedStyle(drawer).display !== 'none') {" +
                    "    $0.style.display = 'none';" +
                    "  } else if (sideNav && window.getComputedStyle(sideNav).display !== 'none') {" +
                    "    $0.style.display = 'none';" +
                    "  } else {" +
                    "    $0.style.display = '';" +
                    "  }" +
                    "};" +
                    "checkMenu();" +
                    "window.addEventListener('resize', checkMenu);" +
                    "setTimeout(checkMenu, 100);" +
                    "setTimeout(checkMenu, 500);",
                    backButton.getElement()
                );
            });
        });

        H2 title = new H2("Quiz Session: " + session.getQuiz().getName());
        title.addClassNames(LumoUtility.Margin.Bottom.MEDIUM);

        Div sessionInfo = new Div();
        sessionInfo.addClassNames(
            LumoUtility.Background.CONTRAST_5,
            LumoUtility.Padding.MEDIUM,
            LumoUtility.BorderRadius.MEDIUM,
            LumoUtility.Margin.Bottom.LARGE
        );

        H3 codeTitle = new H3("Session Code: " + session.getSessionCode());
        codeTitle.addClassNames(LumoUtility.Margin.NONE);

        Paragraph statusText = new Paragraph("Status: " + session.getStatus());
        statusText.addClassNames(LumoUtility.Margin.Top.SMALL, LumoUtility.Margin.Bottom.NONE);

        sessionInfo.add(codeTitle, statusText);

        // Participants list
        H3 participantsTitle = new H3("Participants");
        Div participantsList = new Div();
        participantsList.addClassNames(
            LumoUtility.Display.FLEX,
            LumoUtility.FlexDirection.COLUMN,
            LumoUtility.Gap.SMALL
        );

        updateParticipantsList(participantsList);

        // Action buttons
        HorizontalLayout actions = new HorizontalLayout();
        actions.addClassNames(LumoUtility.Margin.Top.LARGE);

        User currentUser = VaadinSession.getCurrent().getAttribute(User.class);
        boolean isHost = currentUser != null && currentUser.getId() != null &&
                         currentUser.getId().equals(session.getHostUserId());

        if (isHost && session.getStatus() == QuizSession.SessionStatus.WAITING) {
            Button startButton = new Button("Start Quiz for All", event -> startQuizSession());
            startButton.addThemeVariants(ButtonVariant.LUMO_PRIMARY, ButtonVariant.LUMO_SUCCESS);
            actions.add(startButton);
        }

        if (session.getStatus() == QuizSession.SessionStatus.ACTIVE ||
            session.getStatus() == QuizSession.SessionStatus.WAITING) {
            Button joinButton = new Button("Start My Quiz", event -> startPersonalQuiz());
            joinButton.addThemeVariants(ButtonVariant.LUMO_PRIMARY);
            actions.add(joinButton);
        }

        if (session.getStatus() == QuizSession.SessionStatus.COMPLETED) {
            showLeaderboard();
        }

        Button refreshButton = new Button("Refresh", event -> {
            updateParticipantsList(participantsList);
            getUI().ifPresent(UI::push);
        });
        refreshButton.addThemeVariants(ButtonVariant.LUMO_TERTIARY);
        actions.add(refreshButton);

        add(backButton, title, sessionInfo, participantsTitle, participantsList, actions);
    }

    private void updateParticipantsList(Div participantsList) {
        participantsList.removeAll();

        var participants = sessionService.getParticipants(session);

        if (participants.isEmpty()) {
            participantsList.add(new Paragraph("No participants yet. Share the session code!"));
        } else {
            for (QuizParticipant participant : participants) {
                Div participantCard = new Div();
                participantCard.addClassNames(
                    LumoUtility.Background.CONTRAST_5,
                    LumoUtility.Padding.SMALL,
                    LumoUtility.BorderRadius.SMALL,
                    LumoUtility.Display.FLEX,
                    LumoUtility.JustifyContent.BETWEEN,
                    LumoUtility.AlignItems.CENTER
                );

                Span name = new Span(participant.getUser().getName());
                Span status = new Span(participant.isCompleted() ?
                    "✓ Completed - Score: " + participant.getScore() :
                    "In progress...");

                if (participant.isCompleted()) {
                    status.addClassNames(LumoUtility.TextColor.SUCCESS);
                }

                participantCard.add(name, status);
                participantsList.add(participantCard);
            }
        }
    }

    private void startQuizSession() {
        sessionService.updateSessionStatus(session, QuizSession.SessionStatus.ACTIVE);
        buildUI();
    }

    private void startPersonalQuiz() {
        User currentUser = VaadinSession.getCurrent().getAttribute(User.class);
        if (currentUser != null) {
            // Store session code in session for tracking
            VaadinSession.getCurrent().setAttribute("activeSessionCode", session.getSessionCode());
            getUI().ifPresent(ui -> ui.navigate("quiz-questions/" + session.getQuiz().getId()));
        }
    }

    private void showLeaderboard() {
        H3 leaderboardTitle = new H3("🏆 Final Leaderboard");
        leaderboardTitle.addClassNames(LumoUtility.Margin.Top.XLARGE);

        Div leaderboard = new Div();
        leaderboard.addClassNames(
            LumoUtility.Background.PRIMARY_10,
            LumoUtility.Padding.MEDIUM,
            LumoUtility.BorderRadius.MEDIUM
        );

        var participants = sessionService.getParticipants(session);
        participants.sort((p1, p2) -> Integer.compare(p2.getScore(), p1.getScore()));

        int rank = 1;
        for (QuizParticipant participant : participants) {
            if (participant.isCompleted()) {
                Div rankCard = new Div();
                rankCard.addClassNames(
                    LumoUtility.Background.BASE,
                    LumoUtility.Padding.MEDIUM,
                    LumoUtility.BorderRadius.SMALL,
                    LumoUtility.Margin.Bottom.SMALL,
                    LumoUtility.Display.FLEX,
                    LumoUtility.JustifyContent.BETWEEN
                );

                String medal = rank == 1 ? "🥇" : rank == 2 ? "🥈" : rank == 3 ? "🥉" : String.valueOf(rank);

                Span rankSpan = new Span(medal + " " + participant.getUser().getName());
                rankSpan.addClassNames(LumoUtility.FontSize.LARGE, LumoUtility.FontWeight.SEMIBOLD);

                Span scoreSpan = new Span("Score: " + participant.getScore());
                scoreSpan.addClassNames(LumoUtility.FontSize.LARGE, LumoUtility.TextColor.PRIMARY);

                rankCard.add(rankSpan, scoreSpan);
                leaderboard.add(rankCard);
                rank++;
            }
        }

        add(leaderboardTitle, leaderboard);
    }
}

