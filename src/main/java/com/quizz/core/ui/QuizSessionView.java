package com.quizz.core.ui;

import com.quizz.base.ui.component.ViewToolbar;
import com.quizz.core.entity.QuizParticipant;
import com.quizz.core.entity.QuizSession;
import com.quizz.core.entity.User;
import com.quizz.core.service.QuizSessionService;
import com.quizz.core.service.TranslationService;
import com.quizz.core.util.QRCodeGenerator;
import com.vaadin.flow.component.AttachEvent;
import com.vaadin.flow.component.DetachEvent;
import com.vaadin.flow.component.UI;
import com.vaadin.flow.component.button.Button;
import com.vaadin.flow.component.button.ButtonVariant;
import com.vaadin.flow.component.dialog.Dialog;
import com.vaadin.flow.component.html.*;
import com.vaadin.flow.component.icon.VaadinIcon;
import com.vaadin.flow.component.orderedlayout.HorizontalLayout;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import com.vaadin.flow.router.*;
import com.vaadin.flow.server.VaadinSession;
import com.vaadin.flow.server.auth.AnonymousAllowed;
import com.vaadin.flow.theme.lumo.LumoUtility;

import java.io.InputStream;
import java.util.Properties;
import java.util.concurrent.ScheduledFuture;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

@Route("quiz-session/:sessionCode")
@PageTitle("Quiz Session")
@AnonymousAllowed
@SuppressWarnings({"deprecation", "removal"})
public class QuizSessionView extends Main implements BeforeEnterObserver {

    private final QuizSessionService sessionService;
    private final TranslationService translationService;
    private QuizSession session;

    // Auto-refresh for invited players
    private final ScheduledExecutorService scheduler = Executors.newSingleThreadScheduledExecutor();
    private ScheduledFuture<?> refreshTask;
    private Div participantsListDiv; // Keep reference for updates

    public QuizSessionView(QuizSessionService sessionService, TranslationService translationService) {
        this.sessionService = sessionService;
        this.translationService = translationService;


        // Set initial dynamic page title (quiz name will be applied after session resolves)
        getUI().ifPresent(ui -> ui.getPage().setTitle(translationService.translate("quizSession.pageTitle")));
    }

    @Override
    public void beforeEnter(BeforeEnterEvent event) {
        String sessionCode = event.getRouteParameters().get("sessionCode").orElse(null);

        if (sessionCode == null) {
            event.rerouteTo("");
            return;
        }

        session = sessionService.getSessionByCode(sessionCode);

        if (session == null) {
            add(new H2(translationService.translate("quizSession.notFound")));
            add(new Paragraph(translationService.translate("quizSession.invalidCode", sessionCode)));
            add(new Button(translationService.translate("quiz.backToList"), e -> getUI().ifPresent(ui -> ui.navigate(""))));
            return;
        }

        User currentUser = VaadinSession.getCurrent().getAttribute(User.class);
        if (currentUser == null) {
            // Save the intended URL to redirect after login
            VaadinSession.getCurrent().setAttribute("redirectAfterLogin", "quiz-session/" + sessionCode);
            // Redirect to login
            event.rerouteTo(com.quizz.core.security.LoginView.class);
            return;
        }

        // Join the session
        sessionService.joinSession(session, currentUser);

        // After session loaded, update the dynamic page title with quiz name
        getUI().ifPresent(ui -> ui.getPage().setTitle(translationService.translate("quizSession.title", session.getQuiz().getName())));

        buildUI();
    }

    @Override
    protected void onAttach(AttachEvent attachEvent) {
        super.onAttach(attachEvent);
        // Refresh title on attach (handles locale changes)
        if (session != null && session.getQuiz() != null) {
            getUI().ifPresent(ui -> ui.getPage().setTitle(translationService.translate("quizSession.title", session.getQuiz().getName())));
        } else {
            getUI().ifPresent(ui -> ui.getPage().setTitle(translationService.translate("quizSession.pageTitle")));
        }

        // Start auto-refresh for invited players
        startAutoRefreshIfNeeded();
    }

    @Override
    protected void onDetach(DetachEvent detachEvent) {
        super.onDetach(detachEvent);
        // Stop auto-refresh when view is detached
        stopAutoRefresh();
    }

    private void startAutoRefreshIfNeeded() {
        if (session == null) {
            return;
        }

        User currentUser = VaadinSession.getCurrent().getAttribute(User.class);
        boolean isHost = currentUser != null && currentUser.getId() != null &&
                         currentUser.getId().equals(session.getHostUserId());

        // Only auto-refresh for invited players (not host)
        if (!isHost && participantsListDiv != null) {
            UI ui = getUI().orElse(null);
            if (ui != null) {
                refreshTask = scheduler.scheduleAtFixedRate(() -> {
                    ui.access(() -> {
                        // Refresh session data
                        session = sessionService.getSessionByCode(session.getSessionCode());
                        if (session != null && participantsListDiv != null) {
                            updateParticipantsList(participantsListDiv);
                            ui.push();
                        }
                    });
                }, 2, 2, TimeUnit.SECONDS);
            }
        }
    }

    private void stopAutoRefresh() {
        if (refreshTask != null && !refreshTask.isCancelled()) {
            refreshTask.cancel(true);
            refreshTask = null;
        }
    }

    private void buildUI() {
        removeAll();

        User currentUser = VaadinSession.getCurrent().getAttribute(User.class);
        boolean isHost = currentUser != null && currentUser.getId() != null &&
                         currentUser.getId().equals(session.getHostUserId());

        // Add ViewToolbar with just the title
        add(new ViewToolbar(translationService.translate("quizSession.title", session.getQuiz().getName())));

        // Create a wrapper with width constraints
        VerticalLayout contentWrapper = new VerticalLayout();
        contentWrapper.setPadding(true);
        contentWrapper.setSpacing(true);
        contentWrapper.setWidthFull();
        contentWrapper.setMaxWidth("1200px");
        contentWrapper.getStyle()
            .set("margin", "0 auto")
            .set("box-sizing", "border-box");

        // Bouton de retour en haut à gauche (visible uniquement quand le menu latéral n'est pas affiché)
        Button backButton = new Button(translationService.translate("quiz.backToList"), VaadinIcon.ARROW_LEFT.create());
        backButton.addThemeVariants(ButtonVariant.LUMO_TERTIARY);
        backButton.addClickListener(event -> getUI().ifPresent(ui -> ui.navigate("quiz-list")));
        backButton.getStyle()
            .set("position", "absolute")
            .set("top", "10px")
            .set("left", "10px");

        // Hide back button when side menu is visible (lambda as expression to avoid warnings)
        backButton.addAttachListener(attachEvent -> getUI().ifPresent(ui -> ui.getPage().executeJs(
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
        )));

        Div sessionInfo = new Div();
        sessionInfo.addClassNames(
            LumoUtility.Background.CONTRAST_5,
            LumoUtility.Padding.MEDIUM,
            LumoUtility.BorderRadius.MEDIUM,
            LumoUtility.Margin.Bottom.LARGE
        );

        H3 codeTitle = new H3(translationService.translate("quizSession.code", session.getSessionCode()));
        codeTitle.addClassNames(LumoUtility.Margin.NONE);

        Paragraph statusText = new Paragraph(translationService.translate("quizSession.status", session.getStatus()));
        statusText.addClassNames(LumoUtility.Margin.Top.SMALL, LumoUtility.Margin.Bottom.NONE);

        sessionInfo.add(codeTitle, statusText);

        // Participants list
        H3 participantsTitle = new H3(translationService.translate("quizSession.participants"));

        participantsListDiv = new Div();
        participantsListDiv.addClassNames(
            LumoUtility.Display.FLEX,
            LumoUtility.FlexDirection.COLUMN,
            LumoUtility.Gap.SMALL
        );

        updateParticipantsList(participantsListDiv);

        // Create action buttons below participants list
        HorizontalLayout actionButtons = new HorizontalLayout();
        actionButtons.setSpacing(true);
        actionButtons.addClassNames(LumoUtility.Margin.Top.LARGE);
        actionButtons.setWidthFull();
        actionButtons.getStyle().set("flex-wrap", "wrap");

        if (isHost && session.getStatus() == QuizSession.SessionStatus.WAITING) {
            Button startButton = new Button(translationService.translate("quizSession.startAll"), event -> startQuizSession());
            startButton.addThemeVariants(ButtonVariant.LUMO_PRIMARY, ButtonVariant.LUMO_SUCCESS);
            actionButtons.add(startButton);
        }

        if (isHost && session.getStatus() == QuizSession.SessionStatus.COMPLETED) {
            Button resetButton = new Button(translationService.translate("quizSession.resetSession"), event -> resetQuizSession());
            resetButton.addThemeVariants(ButtonVariant.LUMO_PRIMARY);
            resetButton.setIcon(VaadinIcon.REFRESH.create());
            actionButtons.add(resetButton);
        }

        if (session.getStatus() == QuizSession.SessionStatus.ACTIVE ||
            session.getStatus() == QuizSession.SessionStatus.WAITING) {

            // Create a vertical layout to group button and help message
            VerticalLayout joinButtonContainer = new VerticalLayout();
            joinButtonContainer.setPadding(false);
            joinButtonContainer.setSpacing(false);
            joinButtonContainer.getStyle().set("gap", "var(--lumo-space-xs)");

            Button joinButton = new Button(translationService.translate("quizSession.startMine"), event -> startPersonalQuiz());
            joinButton.addThemeVariants(ButtonVariant.LUMO_PRIMARY);

            // Create help message
            Span helpMessage = new Span(translationService.translate("quizSession.waitForHostMessage"));
            helpMessage.getStyle()
                .set("font-size", "var(--lumo-font-size-s)")
                .set("color", "var(--lumo-secondary-text-color)")
                .set("font-style", "italic");

            if (session.getStatus() == QuizSession.SessionStatus.WAITING) {
                joinButton.setEnabled(false);
                joinButton.setTooltipText(translationService.translate("quizSession.waitingForHost"));
                // Show help message when waiting
                joinButtonContainer.add(joinButton, helpMessage);
            } else {
                // Active: no help message needed
                joinButtonContainer.add(joinButton);
            }

            actionButtons.add(joinButtonContainer);
        }

        Button showQRButton = new Button(translationService.translate("quizSession.showQRCode"), event -> showQRCodeDialog());
        showQRButton.setIcon(VaadinIcon.QRCODE.create());
        showQRButton.addThemeVariants(ButtonVariant.LUMO_TERTIARY);
        actionButtons.add(showQRButton);

        Button refreshButton = new Button(translationService.translate("common.refresh"), event -> {
            session = sessionService.getSessionByCode(session.getSessionCode());
            updateParticipantsList(participantsListDiv);
            getUI().ifPresent(UI::push);
        });
        refreshButton.addThemeVariants(ButtonVariant.LUMO_TERTIARY);
        actionButtons.add(refreshButton);

        if (session.getStatus() == QuizSession.SessionStatus.COMPLETED) {
            showLeaderboard();
        }

        contentWrapper.add(backButton, sessionInfo, participantsTitle, participantsListDiv, actionButtons);
        add(contentWrapper);

        // Start auto-refresh after UI is built
        startAutoRefreshIfNeeded();
    }

    private void updateParticipantsList(Div participantsList) {
        participantsList.removeAll();

        var participants = sessionService.getParticipants(session);

        if (participants.isEmpty()) {
            participantsList.add(new Paragraph(translationService.translate("quizSession.noParticipants")));
        } else {
            for (QuizParticipant participant : participants) {
                Div participantCard = new Div();
                participantCard.addClassNames(
                    LumoUtility.Background.CONTRAST_5,
                    LumoUtility.Padding.SMALL,
                    LumoUtility.BorderRadius.SMALL,
                    LumoUtility.Display.FLEX,
                    LumoUtility.JustifyContent.BETWEEN,
                    LumoUtility.AlignItems.CENTER,
                    LumoUtility.Gap.MEDIUM
                );

                Span name = new Span(participant.getUser().getName());
                Span status = new Span(participant.isCompleted() ?
                    translationService.translate("quizSession.completed", participant.getScore()) :
                    translationService.translate("quizSession.inProgress"));

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

    private void resetQuizSession() {
        // Reset all participants scores and completed status
        sessionService.resetParticipants(session);

        // Clear the selected questions so new questions can be chosen
        session.setSelectedQuestionIds(null);
        sessionService.updateSession(session);

        // Set session back to WAITING status
        sessionService.updateSessionStatus(session, QuizSession.SessionStatus.WAITING);

        // Rebuild UI to show the new state
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

    private void showQRCodeDialog() {
        Dialog dialog = new Dialog();
        dialog.setHeaderTitle(translationService.translate("session.share") + ": " + session.getQuiz().getName());
        dialog.setWidth("500px");

        VerticalLayout content = new VerticalLayout();
        content.setSpacing(true);
        content.setPadding(false);
        content.setAlignItems(VerticalLayout.Alignment.CENTER);

        H3 instructionTitle = new H3(translationService.translate("session.scan"));
        instructionTitle.getStyle().set("margin-top", "0");

        // Generate QR code with session URL
        Properties appProperties = new Properties();
        InputStream resourceAsStream = Thread.currentThread().getContextClassLoader().getResourceAsStream("application.properties");
        try {
            appProperties.load(resourceAsStream);
        } catch (Exception e) {
            throw new RuntimeException("Unable to load application properties", e);
        }

        String addressServer = appProperties.getProperty("server.address");
        String portServer = appProperties.getProperty("server.port");
        String sessionUrl = "http://" + addressServer + ":" + portServer + "/quiz-session/" + session.getSessionCode();

        Image qrCode = new Image(QRCodeGenerator.generateQRCode(sessionUrl, 150, 150), "QR Code");
        qrCode.setWidth("150px");
        qrCode.setHeight("150px");

        Div codeContainer = new Div();
        codeContainer.getStyle()
            .set("background", "var(--lumo-contrast-5pct)")
            .set("padding", "var(--lumo-space-m)")
            .set("border-radius", "var(--lumo-border-radius-m)")
            .set("text-align", "center");

        H2 sessionCodeDisplay = new H2("Code: " + session.getSessionCode());
        sessionCodeDisplay.getStyle()
            .set("margin", "0")
            .set("color", "var(--lumo-primary-color)")
            .set("font-family", "monospace");

        codeContainer.add(sessionCodeDisplay);

        Paragraph instructions = new Paragraph(
            translationService.translate("session.scan")
        );
        instructions.getStyle()
            .set("text-align", "center")
            .set("color", "var(--lumo-secondary-text-color)");

        Button closeButton = new Button(translationService.translate("common.cancel"), event -> dialog.close());

        content.add(instructionTitle, qrCode, codeContainer, instructions, closeButton);
        dialog.add(content);
        dialog.open();
    }

    private void showLeaderboard() {
        H3 leaderboardTitle = new H3(translationService.translate("quizSession.leaderboard.title"));
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

                Span scoreSpan = new Span(translationService.translate("quizSession.leaderboard.score", participant.getScore()));
                scoreSpan.addClassNames(LumoUtility.FontSize.LARGE, LumoUtility.TextColor.PRIMARY);

                rankCard.add(rankSpan, scoreSpan);
                leaderboard.add(rankCard);
                rank++;
            }
        }

        add(leaderboardTitle, leaderboard);
    }
}

