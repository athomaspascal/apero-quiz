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
import com.vaadin.flow.server.StreamResource;

import java.io.ByteArrayInputStream;
import java.io.InputStream;
import java.util.Properties;
import java.util.concurrent.ScheduledFuture;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Route("quiz-session/:sessionCode")
@PageTitle("Quiz Session")
@AnonymousAllowed
@SuppressWarnings({"deprecation", "removal"})
public class QuizSessionView extends Main implements BeforeEnterObserver {

    private static final Logger logger = LoggerFactory.getLogger(QuizSessionView.class);

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

        // If team mode is enabled and user hasn't selected a team yet, force selection
        if (session.isTeamMode()) {
            QuizParticipant participant = sessionService.getParticipant(session, currentUser);
            if (participant != null && (participant.getTeamName() == null || participant.getTeamName().isEmpty())) {
                // Force team selection immediately after joining
                showTeamSelectionDialogOnJoin(currentUser);
            }
        }
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

        // Auto-refresh for ALL players (including host) to show new participants joining
        if (participantsListDiv != null) {
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
            // Add Team Mode section
            VerticalLayout teamModeSection = new VerticalLayout();
            teamModeSection.setPadding(false);
            teamModeSection.setSpacing(true);
            teamModeSection.setWidthFull();

            com.vaadin.flow.component.checkbox.Checkbox teamModeCheckbox = new com.vaadin.flow.component.checkbox.Checkbox(
                translationService.translate("quizSession.teamMode.enable")
            );
            teamModeCheckbox.setValue(session.isTeamMode());

            // Team selection checkboxes
            VerticalLayout teamSelectionLayout = new VerticalLayout();
            teamSelectionLayout.setPadding(false);
            teamSelectionLayout.setSpacing(false);
            teamSelectionLayout.setVisible(session.isTeamMode());

            H4 teamSelectionTitle = new H4(translationService.translate("quizSession.teamMode.selectTeams"));
            teamSelectionTitle.getStyle().set("margin", "var(--lumo-space-s) 0");

            String[] availableTeams = {"stark", "lannister", "targaryen", "baratheon", "tyrell", "martell", "arryn", "tully", "greyjoy"};
            java.util.Set<String> selectedTeamsSet = new java.util.HashSet<>();
            if (session.getSelectedTeams() != null && !session.getSelectedTeams().isEmpty()) {
                selectedTeamsSet.addAll(java.util.Arrays.asList(session.getSelectedTeams().split(",")));
            }

            HorizontalLayout teamsCheckboxLayout = new HorizontalLayout();
            teamsCheckboxLayout.setSpacing(true);
            teamsCheckboxLayout.getStyle().set("flex-wrap", "wrap");

            java.util.Map<String, com.vaadin.flow.component.checkbox.Checkbox> teamCheckboxes = new java.util.HashMap<>();

            for (String team : availableTeams) {
                com.vaadin.flow.component.checkbox.Checkbox teamCheckbox = new com.vaadin.flow.component.checkbox.Checkbox(
                    translationService.translate("quizSession.teamMode.team." + team)
                );
                teamCheckbox.setValue(selectedTeamsSet.contains(team));
                teamCheckboxes.put(team, teamCheckbox);
                teamsCheckboxLayout.add(teamCheckbox);
            }

            teamSelectionLayout.add(teamSelectionTitle, teamsCheckboxLayout);

            teamModeCheckbox.addValueChangeListener(event -> {
                boolean teamMode = event.getValue();
                session.setTeamMode(teamMode);
                teamSelectionLayout.setVisible(teamMode);
                if (!teamMode) {
                    session.setSelectedTeams(null);
                }
                sessionService.updateSession(session);
            });

            // Update selected teams when checkboxes change
            teamCheckboxes.forEach((team, checkbox) -> {
                checkbox.addValueChangeListener(event -> {
                    java.util.List<String> selectedTeamsList = new java.util.ArrayList<>();
                    teamCheckboxes.forEach((t, cb) -> {
                        if (cb.getValue()) {
                            selectedTeamsList.add(t);
                        }
                    });
                    session.setSelectedTeams(selectedTeamsList.isEmpty() ? null : String.join(",", selectedTeamsList));
                    sessionService.updateSession(session);
                });
            });

            teamModeSection.add(teamModeCheckbox, teamSelectionLayout);
            contentWrapper.add(teamModeSection);

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

                // Name and team
                VerticalLayout nameTeamLayout = new VerticalLayout();
                nameTeamLayout.setPadding(false);
                nameTeamLayout.setSpacing(false);
                nameTeamLayout.getStyle().set("gap", "2px");

                // Create horizontal layout for name and flag
                HorizontalLayout nameAndFlagLayout = new HorizontalLayout();
                nameAndFlagLayout.setSpacing(true);
                nameAndFlagLayout.setDefaultVerticalComponentAlignment(HorizontalLayout.Alignment.CENTER);
                nameAndFlagLayout.getStyle().set("gap", "8px");

                Span name = new Span(participant.getUser().getName());
                name.addClassNames(LumoUtility.FontWeight.SEMIBOLD);
                nameAndFlagLayout.add(name);

                // Add country flag if available
                User participantUser = participant.getUser();
                logger.info("Checking country flag for participant: {}", participantUser.getName());
                if (participantUser.getCountry() != null) {
                    logger.info("Participant has country: {}", participantUser.getCountry().getCountryName());
                    String flagSvg = participantUser.getCountry().getCountryFlag();
                    logger.info("Flag SVG length: {}", flagSvg != null ? flagSvg.length() : 0);
                    if (flagSvg != null && !flagSvg.isEmpty()) {
                        logger.info("Creating flag display for country: {}", participantUser.getCountry().getCountryName());
                        Div flagContainer = new Div();
                        flagContainer.getStyle()
                            .set("width", "30px")
                            .set("height", "20px")
                            .set("display", "flex")
                            .set("align-items", "center")
                            .set("justify-content", "center")
                            .set("border", "1px solid #e0e0e0")
                            .set("border-radius", "3px")
                            .set("box-shadow", "0 1px 2px rgba(0,0,0,0.1)");

                        // Create StreamResource from SVG content
                        StreamResource flagResource = new StreamResource("flag.svg",
                            () -> new ByteArrayInputStream(flagSvg.getBytes(java.nio.charset.StandardCharsets.UTF_8)));
                        flagResource.setContentType("image/svg+xml");

                        Image flagImage = new Image(flagResource, "Country flag");
                        flagImage.setWidth("30px");
                        flagImage.setHeight("20px");
                        flagImage.getStyle()
                            .set("object-fit", "contain");

                        flagContainer.add(flagImage);
                        nameAndFlagLayout.add(flagContainer);
                        logger.info("Flag container added to layout for participant: {}", participantUser.getName());
                    } else {
                        logger.warn("Flag SVG is null or empty for country: {}", participantUser.getCountry().getCountryName());
                    }
                } else {
                    logger.warn("Participant {} has no country associated", participantUser.getName());
                }

                nameTeamLayout.add(nameAndFlagLayout);

                if (session.isTeamMode() && participant.getTeamName() != null) {
                    Span team = new Span(translationService.translate("quizSession.teamMode.teamSelected",
                        translationService.translate("quizSession.teamMode.team." + participant.getTeamName())));
                    team.getStyle()
                        .set("font-size", "var(--lumo-font-size-s)")
                        .set("color", "var(--lumo-secondary-text-color)");
                    nameTeamLayout.add(team);
                }

                Span status = new Span(participant.isCompleted() ?
                    translationService.translate("quizSession.completed", participant.getScore()) :
                    translationService.translate("quizSession.inProgress"));

                if (participant.isCompleted()) {
                    status.addClassNames(LumoUtility.TextColor.SUCCESS);
                }

                participantCard.add(nameTeamLayout, status);
                participantsList.add(participantCard);
            }
        }
    }

    private void startQuizSession() {
        // Check if team mode is enabled and host has selected a team
        if (session.isTeamMode()) {
            User currentUser = VaadinSession.getCurrent().getAttribute(User.class);
            QuizParticipant hostParticipant = sessionService.getParticipant(session, currentUser);

            if (hostParticipant == null || hostParticipant.getTeamName() == null || hostParticipant.getTeamName().isEmpty()) {
                // Host must select a team first
                showTeamSelectionDialogForHost(currentUser);
                return;
            }
        }

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
            // Check if team mode is enabled
            if (session.isTeamMode()) {
                // Show team selection dialog
                showTeamSelectionDialog(currentUser);
            } else {
                // Store session code in session for tracking
                VaadinSession.getCurrent().setAttribute("activeSessionCode", session.getSessionCode());
                getUI().ifPresent(ui -> ui.navigate("quiz-questions/" + session.getQuiz().getId()));
            }
        }
    }

    private void showTeamSelectionDialog(User currentUser) {
        Dialog dialog = new Dialog();
        dialog.setHeaderTitle(translationService.translate("quizSession.teamMode.selectTeam"));
        dialog.setWidth("400px");
        dialog.setCloseOnOutsideClick(false);
        dialog.setCloseOnEsc(false);

        VerticalLayout content = new VerticalLayout();
        content.setSpacing(true);
        content.setPadding(false);

        // Get participant to check if team already selected
        QuizParticipant participant = sessionService.getParticipant(session, currentUser);

        Paragraph instruction = new Paragraph(translationService.translate("quizSession.teamMode.selectTeamMessage"));
        instruction.getStyle().set("color", "var(--lumo-secondary-text-color)");

        com.vaadin.flow.component.radiobutton.RadioButtonGroup<String> teamRadioGroup =
            new com.vaadin.flow.component.radiobutton.RadioButtonGroup<>();
        teamRadioGroup.setLabel(translationService.translate("quizSession.teamMode"));

        // Get available teams
        if (session.getSelectedTeams() != null && !session.getSelectedTeams().isEmpty()) {
            String[] teams = session.getSelectedTeams().split(",");
            java.util.Map<String, String> teamItems = new java.util.LinkedHashMap<>();
            for (String team : teams) {
                teamItems.put(team, translationService.translate("quizSession.teamMode.team." + team));
            }
            teamRadioGroup.setItems(teamItems.keySet());
            teamRadioGroup.setItemLabelGenerator(team -> teamItems.get(team));

            // Pre-select team if already chosen
            if (participant != null && participant.getTeamName() != null) {
                teamRadioGroup.setValue(participant.getTeamName());
            }
        }

        HorizontalLayout buttonLayout = new HorizontalLayout();
        buttonLayout.setSpacing(true);

        Button confirmButton = new Button(translationService.translate("quizSession.teamMode.confirmTeam"), event -> {
            String selectedTeam = teamRadioGroup.getValue();
            if (selectedTeam != null && participant != null) {
                // Update participant's team
                sessionService.updateParticipantTeam(participant, selectedTeam);

                // Store session code and start quiz
                VaadinSession.getCurrent().setAttribute("activeSessionCode", session.getSessionCode());
                dialog.close();
                getUI().ifPresent(ui -> ui.navigate("quiz-questions/" + session.getQuiz().getId()));
            }
        });
        confirmButton.addThemeVariants(ButtonVariant.LUMO_PRIMARY);
        confirmButton.setEnabled(teamRadioGroup.getValue() != null);

        teamRadioGroup.addValueChangeListener(event -> {
            confirmButton.setEnabled(event.getValue() != null);
        });

        // No cancel button - team selection is mandatory in team mode
        buttonLayout.add(confirmButton);

        content.add(instruction, teamRadioGroup, buttonLayout);
        dialog.add(content);
        dialog.open();
    }

    private void showTeamSelectionDialogOnJoin(User currentUser) {
        Dialog dialog = new Dialog();
        dialog.setHeaderTitle(translationService.translate("quizSession.teamMode.selectTeam"));
        dialog.setWidth("400px");
        dialog.setCloseOnOutsideClick(false);
        dialog.setCloseOnEsc(false);

        VerticalLayout content = new VerticalLayout();
        content.setSpacing(true);
        content.setPadding(false);

        // Get participant
        QuizParticipant participant = sessionService.getParticipant(session, currentUser);

        Paragraph instruction = new Paragraph(translationService.translate("quizSession.teamMode.selectTeamMessage"));
        instruction.getStyle().set("color", "var(--lumo-secondary-text-color)");

        com.vaadin.flow.component.radiobutton.RadioButtonGroup<String> teamRadioGroup =
            new com.vaadin.flow.component.radiobutton.RadioButtonGroup<>();
        teamRadioGroup.setLabel(translationService.translate("quizSession.teamMode"));

        // Get available teams
        if (session.getSelectedTeams() != null && !session.getSelectedTeams().isEmpty()) {
            String[] teams = session.getSelectedTeams().split(",");
            java.util.Map<String, String> teamItems = new java.util.LinkedHashMap<>();
            for (String team : teams) {
                teamItems.put(team, translationService.translate("quizSession.teamMode.team." + team));
            }
            teamRadioGroup.setItems(teamItems.keySet());
            teamRadioGroup.setItemLabelGenerator(team -> teamItems.get(team));

            // Pre-select team if already chosen
            if (participant != null && participant.getTeamName() != null) {
                teamRadioGroup.setValue(participant.getTeamName());
            }
        }

        HorizontalLayout buttonLayout = new HorizontalLayout();
        buttonLayout.setSpacing(true);

        Button confirmButton = new Button(translationService.translate("quizSession.teamMode.confirmTeam"), event -> {
            String selectedTeam = teamRadioGroup.getValue();
            if (selectedTeam != null && participant != null) {
                // Update participant's team
                sessionService.updateParticipantTeam(participant, selectedTeam);

                // Close dialog and refresh UI
                dialog.close();
                buildUI();
            }
        });
        confirmButton.addThemeVariants(ButtonVariant.LUMO_PRIMARY);
        confirmButton.setEnabled(teamRadioGroup.getValue() != null);

        teamRadioGroup.addValueChangeListener(event -> {
            confirmButton.setEnabled(event.getValue() != null);
        });

        // No cancel button - team selection is mandatory in team mode
        buttonLayout.add(confirmButton);

        content.add(instruction, teamRadioGroup, buttonLayout);
        dialog.add(content);
        dialog.open();
    }

    private void showTeamSelectionDialogForHost(User currentUser) {
        Dialog dialog = new Dialog();
        dialog.setHeaderTitle(translationService.translate("quizSession.teamMode.selectTeam"));
        dialog.setWidth("400px");
        dialog.setCloseOnOutsideClick(false);
        dialog.setCloseOnEsc(false);

        VerticalLayout content = new VerticalLayout();
        content.setSpacing(true);
        content.setPadding(false);

        // Get participant
        QuizParticipant participant = sessionService.getParticipant(session, currentUser);

        Paragraph instruction = new Paragraph(translationService.translate("quizSession.teamMode.host.selectTeamBeforeStart"));
        instruction.getStyle()
            .set("color", "var(--lumo-error-color)")
            .set("font-weight", "bold");

        com.vaadin.flow.component.radiobutton.RadioButtonGroup<String> teamRadioGroup =
            new com.vaadin.flow.component.radiobutton.RadioButtonGroup<>();
        teamRadioGroup.setLabel(translationService.translate("quizSession.teamMode"));

        // Get available teams
        if (session.getSelectedTeams() != null && !session.getSelectedTeams().isEmpty()) {
            String[] teams = session.getSelectedTeams().split(",");
            java.util.Map<String, String> teamItems = new java.util.LinkedHashMap<>();
            for (String team : teams) {
                teamItems.put(team, translationService.translate("quizSession.teamMode.team." + team));
            }
            teamRadioGroup.setItems(teamItems.keySet());
            teamRadioGroup.setItemLabelGenerator(team -> teamItems.get(team));

            // Pre-select team if already chosen
            if (participant != null && participant.getTeamName() != null) {
                teamRadioGroup.setValue(participant.getTeamName());
            }
        }

        HorizontalLayout buttonLayout = new HorizontalLayout();
        buttonLayout.setSpacing(true);

        Button confirmButton = new Button(translationService.translate("quizSession.teamMode.confirmTeam"), event -> {
            String selectedTeam = teamRadioGroup.getValue();
            if (selectedTeam != null && participant != null) {
                // Update participant's team
                sessionService.updateParticipantTeam(participant, selectedTeam);

                // Now start the session
                dialog.close();
                sessionService.updateSessionStatus(session, QuizSession.SessionStatus.ACTIVE);
                buildUI();
            }
        });
        confirmButton.addThemeVariants(ButtonVariant.LUMO_PRIMARY);
        confirmButton.setEnabled(teamRadioGroup.getValue() != null);

        teamRadioGroup.addValueChangeListener(event -> {
            confirmButton.setEnabled(event.getValue() != null);
        });

        buttonLayout.add(confirmButton);

        content.add(instruction, teamRadioGroup, buttonLayout);
        dialog.add(content);
        dialog.open();
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
        var participants = sessionService.getParticipants(session);

        if (session.isTeamMode()) {
            // Team leaderboard
            H3 leaderboardTitle = new H3(translationService.translate("quizSession.leaderboard.teamTitle"));
            leaderboardTitle.addClassNames(LumoUtility.Margin.Top.XLARGE);

            Div leaderboard = new Div();
            leaderboard.addClassNames(
                LumoUtility.Background.PRIMARY_10,
                LumoUtility.Padding.MEDIUM,
                LumoUtility.BorderRadius.MEDIUM
            );

            // Calculate team scores
            java.util.Map<String, Integer> teamScores = new java.util.HashMap<>();
            java.util.Map<String, java.util.List<QuizParticipant>> teamMembers = new java.util.HashMap<>();

            for (QuizParticipant participant : participants) {
                if (participant.isCompleted() && participant.getTeamName() != null) {
                    String teamName = participant.getTeamName();
                    teamScores.put(teamName, teamScores.getOrDefault(teamName, 0) + participant.getScore());
                    teamMembers.computeIfAbsent(teamName, k -> new java.util.ArrayList<>()).add(participant);
                }
            }

            // Sort teams by score
            java.util.List<java.util.Map.Entry<String, Integer>> sortedTeams = new java.util.ArrayList<>(teamScores.entrySet());
            sortedTeams.sort((e1, e2) -> Integer.compare(e2.getValue(), e1.getValue()));

            int rank = 1;
            for (java.util.Map.Entry<String, Integer> entry : sortedTeams) {
                String teamName = entry.getKey();
                int teamScore = entry.getValue();

                Div teamCard = new Div();
                teamCard.addClassNames(
                    LumoUtility.Background.BASE,
                    LumoUtility.Padding.MEDIUM,
                    LumoUtility.BorderRadius.SMALL,
                    LumoUtility.Margin.Bottom.SMALL
                );

                String medal = rank == 1 ? "🥇" : rank == 2 ? "🥈" : rank == 3 ? "🥉" : String.valueOf(rank);

                HorizontalLayout teamHeader = new HorizontalLayout();
                teamHeader.setWidthFull();
                teamHeader.setJustifyContentMode(HorizontalLayout.JustifyContentMode.BETWEEN);

                Span teamRankSpan = new Span(medal + " " + translationService.translate("quizSession.teamMode.team." + teamName));
                teamRankSpan.addClassNames(LumoUtility.FontSize.LARGE, LumoUtility.FontWeight.SEMIBOLD);

                Span teamScoreSpan = new Span(translationService.translate("quizSession.leaderboard.teamScore",
                    translationService.translate("quizSession.teamMode.team." + teamName), String.valueOf(teamScore)));
                teamScoreSpan.addClassNames(LumoUtility.FontSize.LARGE, LumoUtility.TextColor.PRIMARY);

                teamHeader.add(teamRankSpan, teamScoreSpan);
                teamCard.add(teamHeader);

                // Add team members
                VerticalLayout membersLayout = new VerticalLayout();
                membersLayout.setPadding(false);
                membersLayout.setSpacing(false);
                membersLayout.getStyle().set("margin-left", "var(--lumo-space-m)").set("gap", "var(--lumo-space-xs)");

                java.util.List<QuizParticipant> members = teamMembers.get(teamName);
                members.sort((p1, p2) -> Integer.compare(p2.getScore(), p1.getScore()));

                for (QuizParticipant member : members) {
                    Span memberSpan = new Span(member.getUser().getName() + " - " +
                        translationService.translate("quizSession.leaderboard.score", member.getScore()));
                    memberSpan.getStyle()
                        .set("font-size", "var(--lumo-font-size-s)")
                        .set("color", "var(--lumo-secondary-text-color)");
                    membersLayout.add(memberSpan);
                }

                teamCard.add(membersLayout);
                leaderboard.add(teamCard);
                rank++;
            }

            add(leaderboardTitle, leaderboard);

        } else {
            // Individual leaderboard
            H3 leaderboardTitle = new H3(translationService.translate("quizSession.leaderboard.title"));
            leaderboardTitle.addClassNames(LumoUtility.Margin.Top.XLARGE);

            Div leaderboard = new Div();
            leaderboard.addClassNames(
                LumoUtility.Background.PRIMARY_10,
                LumoUtility.Padding.MEDIUM,
                LumoUtility.BorderRadius.MEDIUM
            );

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
}

