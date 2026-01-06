package com.quizz.core.ui;

import com.quizz.base.ui.component.ViewToolbar;
import com.quizz.core.entity.DuelMatch;
import com.quizz.core.entity.User;
import com.quizz.core.service.DuelService;
import com.quizz.core.service.TranslationService;
import com.vaadin.flow.component.AttachEvent;
import com.vaadin.flow.component.DetachEvent;
import com.vaadin.flow.component.UI;
import com.vaadin.flow.component.button.Button;
import com.vaadin.flow.component.button.ButtonVariant;
import com.vaadin.flow.component.html.*;
import com.vaadin.flow.component.notification.Notification;
import com.vaadin.flow.component.orderedlayout.FlexComponent;
import com.vaadin.flow.component.orderedlayout.HorizontalLayout;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import com.vaadin.flow.router.Menu;
import com.vaadin.flow.router.PageTitle;
import com.vaadin.flow.router.Route;
import com.vaadin.flow.router.RouteParameters;
import com.vaadin.flow.server.VaadinSession;
import com.vaadin.flow.theme.lumo.LumoUtility;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.time.Duration;
import java.time.LocalDateTime;
import java.util.Optional;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledFuture;
import java.util.concurrent.TimeUnit;

@Route("duel-quiz")
@PageTitle("Duel Quiz")
@Menu(order = 2, icon = "vaadin:trophy", title = "menu.duelquiz")
public class DuelQuizView extends Main {

    private static final Logger logger = LoggerFactory.getLogger(DuelQuizView.class);
    private static final int COUNTDOWN_SECONDS = 5;

    private final DuelService duelService;
    private final TranslationService translationService;
    private final com.quizz.core.service.UserActivityService userActivityService;

    private DuelMatch currentDuel;
    private VerticalLayout mainContent;
    private ScheduledExecutorService executor;
    private ScheduledFuture<?> pollingTask;
    private ScheduledFuture<?> countdownTask;

    public DuelQuizView(DuelService duelService, TranslationService translationService,
                       com.quizz.core.service.UserActivityService userActivityService) {
        logger.info("=== DuelQuizView Constructor CALLED ===");
        this.duelService = duelService;
        this.translationService = translationService;
        this.userActivityService = userActivityService;
        logger.info("DuelQuizView services injected successfully");

        setSizeFull();
        addClassNames(LumoUtility.BoxSizing.BORDER, LumoUtility.Display.FLEX,
                     LumoUtility.FlexDirection.COLUMN, LumoUtility.Padding.MEDIUM,
                     LumoUtility.Gap.MEDIUM);

        add(new ViewToolbar(translationService.translate("duelquiz.title")));

        mainContent = new VerticalLayout();
        mainContent.setSizeFull();
        mainContent.setAlignItems(FlexComponent.Alignment.CENTER);
        mainContent.setJustifyContentMode(FlexComponent.JustifyContentMode.CENTER);

        add(mainContent);

        // Check if user already has an active duel
        User currentUser = VaadinSession.getCurrent().getAttribute(User.class);
        logger.info("Current user: {}", currentUser != null ? currentUser.getName() : "null");
        Optional<DuelMatch> activeDuel = duelService.getActiveDuel(currentUser);

        if (activeDuel.isPresent()) {
            logger.info("Active duel found for user, showing match view");
            currentDuel = activeDuel.get();
            updateView();
        } else {
            logger.info("No active duel, showing initial view");
            showInitialView();
        }
        logger.info("=== DuelQuizView Constructor COMPLETED ===");
    }

    @Override
    protected void onAttach(AttachEvent attachEvent) {
        super.onAttach(attachEvent);

        // Update user activity
        User currentUser = VaadinSession.getCurrent().getAttribute(User.class);
        if (currentUser != null) {
            userActivityService.updateActivity(currentUser, "DUEL_QUIZ_VIEW", "duel-quiz");
        }

        executor = Executors.newScheduledThreadPool(2);
        startPolling();
    }

    @Override
    protected void onDetach(DetachEvent detachEvent) {
        super.onDetach(detachEvent);
        stopPolling();
        if (executor != null && !executor.isShutdown()) {
            executor.shutdown();
        }
    }

    private void showInitialView() {
        mainContent.removeAll();

        H2 title = new H2(translationService.translate("duelquiz.welcome"));
        Paragraph description = new Paragraph(translationService.translate("duelquiz.description"));

        Button searchButton = new Button(translationService.translate("duelquiz.search"), event -> startSearching());
        searchButton.addThemeVariants(ButtonVariant.LUMO_PRIMARY, ButtonVariant.LUMO_LARGE);

        Button cancelButton = new Button(translationService.translate("duelquiz.back"), event ->
            getUI().ifPresent(ui -> ui.navigate("")));

        mainContent.add(title, description, searchButton, cancelButton);
    }

    private void startSearching() {
        User currentUser = VaadinSession.getCurrent().getAttribute(User.class);

        // Update user activity
        if (currentUser != null) {
            userActivityService.updateActivity(currentUser, "START_DUEL_SEARCH", "duel-quiz");
        }

        currentDuel = duelService.startSearching(currentUser);
        updateView();
    }

    private void updateView() {
        logger.info("=== updateView() CALLED ===");
        if (currentDuel == null) {
            logger.warn("currentDuel is NULL, showing initial view");
            showInitialView();
            return;
        }

        logger.info("Current duel status: {}, ID: {}", currentDuel.getStatus(), currentDuel.getId());

        // Special case: IN_PROGRESS status requires navigation OUTSIDE of ui.access()
        if (currentDuel.getStatus() == com.quizz.core.entity.DuelMatch.DuelStatus.IN_PROGRESS) {
            logger.info("Status is IN_PROGRESS, navigating to quiz");
            navigateToQuiz();
            return;
        }

        UI ui = getUI().orElse(null);
        if (ui == null) {
            logger.error("UI is NULL! Cannot update view");
            return;
        }

        logger.info("UI is present, calling ui.access()");
        ui.access(() -> {
            logger.info("Inside ui.access(), removing all content");
            mainContent.removeAll();

            logger.info("Switching on status: {}", currentDuel.getStatus());
            switch (currentDuel.getStatus()) {
                case SEARCHING:
                    logger.info("Showing SEARCHING view");
                    showSearchingView();
                    break;
                case MATCHED:
                    logger.info("Showing MATCHED view");
                    showMatchedView();
                    break;
                case COUNTDOWN:
                    logger.info("Showing COUNTDOWN view");
                    showCountdownView();
                    break;
                case REMATCH_PENDING:
                    logger.info("Showing REMATCH view");
                    showRematchView();
                    break;
                case FINISHED:
                    logger.info("Showing FINISHED view");
                    showFinishedView();
                    break;
                case CANCELLED:
                    logger.info("Showing CANCELLED view");
                    showCancelledView();
                    break;
                default:
                    logger.error("UNKNOWN STATUS: {} - showing initial view", currentDuel.getStatus());
                    showInitialView();
                    break;
            }

            logger.info("Calling ui.push()");
            ui.push();
        });
        logger.info("=== updateView() COMPLETED ===");
    }

    private void showSearchingView() {
        logger.info("=== showSearchingView() START ===");
        H2 title = new H2(translationService.translate("duelquiz.searching"));

        // Spinner (using CSS animation)
        Div spinner = new Div();
        spinner.addClassNames("spinner");
        spinner.getStyle()
            .set("width", "50px")
            .set("height", "50px")
            .set("border", "5px solid #f3f3f3")
            .set("border-top", "5px solid #3498db")
            .set("border-radius", "50%")
            .set("animation", "spin 1s linear infinite");

        // Add keyframes animation via JavaScript
        getElement().executeJs(
            "const style = document.createElement('style');" +
            "style.textContent = '@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }';" +
            "document.head.appendChild(style);"
        );

        Paragraph waitingText = new Paragraph(translationService.translate("duelquiz.searching.text"));

        Button cancelButton = new Button(translationService.translate("duelquiz.cancel"), event -> {
            duelService.cancelDuel(currentDuel.getId());
            currentDuel = null;
            showInitialView();
        });
        cancelButton.addThemeVariants(ButtonVariant.LUMO_ERROR);

        mainContent.add(title, spinner, waitingText, cancelButton);
        logger.info("=== showSearchingView() END - components added ===");
    }

    private void showMatchedView() {
        logger.info("=== showMatchedView() START ===");
        User currentUser = VaadinSession.getCurrent().getAttribute(User.class);
        User opponent = currentUser.getId().equals(currentDuel.getPlayer1().getId())
            ? currentDuel.getPlayer2()
            : currentDuel.getPlayer1();

        logger.info("Current user: {}, Opponent: {}", currentUser.getName(), opponent.getName());

        H2 title = new H2(translationService.translate("duelquiz.matched"));

        // Create opponent info with country flag
        HorizontalLayout opponentLayout = new HorizontalLayout();
        opponentLayout.setAlignItems(FlexComponent.Alignment.CENTER);
        opponentLayout.setSpacing(true);

        Span opponentLabel = new Span(translationService.translate("duelquiz.opponent") + ": " + opponent.getName());
        opponentLayout.add(opponentLabel);

        // Add country flag if available
        if (opponent.getCountry() != null && opponent.getCountry().getCountryFlag() != null
            && !opponent.getCountry().getCountryFlag().isEmpty()) {
            Div flagContainer = new Div();
            flagContainer.getStyle()
                .set("width", "30px")
                .set("height", "20px")
                .set("display", "flex")
                .set("align-items", "center")
                .set("justify-content", "center")
                .set("border", "1px solid #e0e0e0")
                .set("border-radius", "2px")
                .set("margin-left", "10px")
                .set("box-shadow", "0 1px 3px rgba(0,0,0,0.1)");

            // Set SVG content directly
            flagContainer.getElement().setProperty("innerHTML", opponent.getCountry().getCountryFlag());

            opponentLayout.add(flagContainer);
        }

        Paragraph quizInfo = new Paragraph(
            translationService.translate("duelquiz.quiz") + ": " + currentDuel.getQuiz().getName()
        );

        Button acceptButton = new Button(translationService.translate("duelquiz.accept"));
        acceptButton.addThemeVariants(ButtonVariant.LUMO_PRIMARY, ButtonVariant.LUMO_LARGE);

        acceptButton.addClickListener(event -> {
            // Change button appearance immediately
            acceptButton.setText(translationService.translate("duelquiz.waiting.acceptance"));
            acceptButton.setEnabled(false);
            acceptButton.removeThemeVariants(ButtonVariant.LUMO_PRIMARY);
            acceptButton.addThemeVariants(ButtonVariant.LUMO_CONTRAST);

            // Accept the match
            currentDuel = duelService.acceptMatch(currentDuel.getId(), currentUser);
            updateView();
        });

        Button declineButton = new Button(translationService.translate("duelquiz.decline"), event -> {
            duelService.cancelDuel(currentDuel.getId());
            currentDuel = null;
            showInitialView();
        });
        declineButton.addThemeVariants(ButtonVariant.LUMO_ERROR);

        mainContent.add(title, opponentLayout, quizInfo, acceptButton, declineButton);
        logger.info("=== showMatchedView() END - components added ===");
    }

    private void showCountdownView() {
        mainContent.removeAll();

        H2 title = new H2(translationService.translate("duelquiz.countdown.title"));
        H1 countdownDisplay = new H1();
        countdownDisplay.getStyle().set("font-size", "72px").set("color", "#3498db");

        Paragraph readyText = new Paragraph(translationService.translate("duelquiz.countdown.ready"));

        mainContent.add(title, countdownDisplay, readyText);

        // Start countdown
        if (countdownTask == null || countdownTask.isDone()) {
            startCountdown(countdownDisplay);
        }
    }

    private void startCountdown(H1 countdownDisplay) {
        LocalDateTime countdownStart = currentDuel.getCountdownStartedAt();
        if (countdownStart == null) {
            countdownStart = LocalDateTime.now();
        }

        final LocalDateTime finalCountdownStart = countdownStart;

        logger.info("Starting countdown for duel {} with quiz: {}",
            currentDuel.getId(),
            currentDuel.getQuiz() != null ? currentDuel.getQuiz().getName() : "null");

        countdownTask = executor.scheduleAtFixedRate(() -> {
            UI ui = getUI().orElse(null);
            if (ui != null) {
                ui.access(() -> {
                    long secondsElapsed = Duration.between(finalCountdownStart, LocalDateTime.now()).getSeconds();
                    long secondsRemaining = COUNTDOWN_SECONDS - secondsElapsed;

                    if (secondsRemaining > 0) {
                        countdownDisplay.setText(String.valueOf(secondsRemaining));
                    } else {
                        countdownDisplay.setText(translationService.translate("duelquiz.countdown.go"));
                        if (countdownTask != null) {
                            countdownTask.cancel(false);
                        }
                        // Start the quiz
                        logger.info("Countdown finished, starting quiz for duel {}", currentDuel.getId());
                        currentDuel = duelService.startQuiz(currentDuel.getId());
                        logger.info("Quiz started, status: {}, quiz: {}",
                            currentDuel.getStatus(),
                            currentDuel.getQuiz() != null ? currentDuel.getQuiz().getName() : "null");
                        updateView();
                    }
                    ui.push();
                });
            }
        }, 0, 1, TimeUnit.SECONDS);
    }

    private void navigateToQuiz() {
        logger.info("=== NAVIGATING TO DUEL QUIZ ===");
        logger.info("Current duel ID: {}", currentDuel.getId());
        logger.info("Quiz ID: {}", currentDuel.getQuiz().getId());
        logger.info("Quiz name: {}", currentDuel.getQuiz().getName());

        User currentUser = VaadinSession.getCurrent().getAttribute(User.class);
        logger.info("Current user: {}", currentUser != null ? currentUser.getName() : "null");

        stopPolling();

        // Store duel ID in session for QuizQuestionView to retrieve
        VaadinSession.getCurrent().setAttribute("activeDuelId", currentDuel.getId());
        logger.info("Stored activeDuelId in session: {}", currentDuel.getId());

        getUI().ifPresent(ui -> {
            logger.info("Attempting navigation to QuizQuestionView with quizId: {}", currentDuel.getQuiz().getId());
            ui.navigate(QuizQuestionView.class,
                new RouteParameters("quizId", String.valueOf(currentDuel.getQuiz().getId())));
            logger.info("Navigation command sent");
        });

        if (!getUI().isPresent()) {
            logger.error("ERROR: UI is not present! Cannot navigate.");
        }
    }

    private void showRematchView() {
        User currentUser = VaadinSession.getCurrent().getAttribute(User.class);
        User opponent = currentUser.getId().equals(currentDuel.getPlayer1().getId())
            ? currentDuel.getPlayer2()
            : currentDuel.getPlayer1();

        H2 title = new H2(translationService.translate("duelquiz.finished"));

        // Display scores
        HorizontalLayout scoresLayout = new HorizontalLayout();
        scoresLayout.setSpacing(true);
        scoresLayout.setAlignItems(FlexComponent.Alignment.CENTER);

        // Player 1 layout with country flag
        VerticalLayout player1Layout = new VerticalLayout();
        player1Layout.setAlignItems(FlexComponent.Alignment.CENTER);

        HorizontalLayout player1NameLayout = new HorizontalLayout();
        player1NameLayout.setAlignItems(FlexComponent.Alignment.CENTER);
        player1NameLayout.setSpacing(true);
        H3 player1Name = new H3(currentDuel.getPlayer1().getName());
        player1NameLayout.add(player1Name);

        // Add country flag for player 1
        if (currentDuel.getPlayer1().getCountry() != null && currentDuel.getPlayer1().getCountry().getCountryFlag() != null
            && !currentDuel.getPlayer1().getCountry().getCountryFlag().isEmpty()) {
            Div flag1Container = new Div();
            flag1Container.getStyle()
                .set("width", "30px")
                .set("height", "20px")
                .set("display", "flex")
                .set("align-items", "center")
                .set("justify-content", "center")
                .set("border", "1px solid #e0e0e0")
                .set("border-radius", "2px")
                .set("margin-left", "10px")
                .set("box-shadow", "0 1px 3px rgba(0,0,0,0.1)");
            flag1Container.getElement().setProperty("innerHTML", currentDuel.getPlayer1().getCountry().getCountryFlag());
            player1NameLayout.add(flag1Container);
        }

        H1 player1Score = new H1(String.valueOf(currentDuel.getPlayer1Score()));
        player1Score.getStyle().set("color", "#1976d2").set("margin", "0");
        player1Layout.add(player1NameLayout, player1Score);

        Span vsSpan = new Span("VS");
        vsSpan.getStyle().set("font-size", "32px").set("font-weight", "bold");

        // Player 2 layout with country flag
        VerticalLayout player2Layout = new VerticalLayout();
        player2Layout.setAlignItems(FlexComponent.Alignment.CENTER);

        HorizontalLayout player2NameLayout = new HorizontalLayout();
        player2NameLayout.setAlignItems(FlexComponent.Alignment.CENTER);
        player2NameLayout.setSpacing(true);
        H3 player2Name = new H3(currentDuel.getPlayer2().getName());
        player2NameLayout.add(player2Name);

        // Add country flag for player 2
        if (currentDuel.getPlayer2().getCountry() != null && currentDuel.getPlayer2().getCountry().getCountryFlag() != null
            && !currentDuel.getPlayer2().getCountry().getCountryFlag().isEmpty()) {
            Div flag2Container = new Div();
            flag2Container.getStyle()
                .set("width", "30px")
                .set("height", "20px")
                .set("display", "flex")
                .set("align-items", "center")
                .set("justify-content", "center")
                .set("border", "1px solid #e0e0e0")
                .set("border-radius", "2px")
                .set("margin-left", "10px")
                .set("box-shadow", "0 1px 3px rgba(0,0,0,0.1)");
            flag2Container.getElement().setProperty("innerHTML", currentDuel.getPlayer2().getCountry().getCountryFlag());
            player2NameLayout.add(flag2Container);
        }

        H1 player2Score = new H1(String.valueOf(currentDuel.getPlayer2Score()));
        player2Score.getStyle().set("color", "#1976d2").set("margin", "0");
        player2Layout.add(player2NameLayout, player2Score);

        scoresLayout.add(player1Layout, vsSpan, player2Layout);

        // Determine winner
        String resultMessage;
        if (currentDuel.getPlayer1Score() > currentDuel.getPlayer2Score()) {
            resultMessage = translationService.translate("duelquiz.winner") + ": " + currentDuel.getPlayer1().getName();
        } else if (currentDuel.getPlayer2Score() > currentDuel.getPlayer1Score()) {
            resultMessage = translationService.translate("duelquiz.winner") + ": " + currentDuel.getPlayer2().getName();
        } else {
            resultMessage = translationService.translate("duelquiz.draw");
        }

        Paragraph result = new Paragraph(resultMessage);
        result.getStyle().set("font-size", "24px").set("font-weight", "bold");

        Paragraph rematchInfo = new Paragraph(
            translationService.translate("duelquiz.rematch.available") +
            " (" + (currentDuel.getRematchCount() + 1) + "/3)"
        );

        Button rematchButton = new Button(translationService.translate("duelquiz.rematch"), event -> {
            currentDuel = duelService.requestRematch(currentDuel.getId(), currentUser);
            if (currentDuel.getStatus() == DuelMatch.DuelStatus.COUNTDOWN) {
                Notification.show(translationService.translate("duelquiz.rematch.accepted"),
                    3000, Notification.Position.TOP_CENTER);
                updateView();
            } else {
                Notification.show(translationService.translate("duelquiz.rematch.waiting"),
                    3000, Notification.Position.TOP_CENTER);
            }
        });
        rematchButton.addThemeVariants(ButtonVariant.LUMO_PRIMARY);

        Button exitButton = new Button(translationService.translate("duelquiz.exit"), event -> {
            currentDuel = null;
            getUI().ifPresent(ui -> ui.navigate(""));
        });

        mainContent.add(title, scoresLayout, result, rematchInfo, rematchButton, exitButton);
    }

    private void showFinishedView() {
        showRematchView(); // Same view but without rematch button
        // Find and remove rematch button
        mainContent.getChildren()
            .filter(component -> component instanceof Button)
            .map(component -> (Button) component)
            .filter(button -> button.getText().equals(translationService.translate("duelquiz.rematch")))
            .findFirst()
            .ifPresent(mainContent::remove);
    }

    private void showCancelledView() {
        mainContent.removeAll();

        H2 title = new H2(translationService.translate("duelquiz.cancelled"));
        Paragraph message = new Paragraph(translationService.translate("duelquiz.cancelled.message"));

        Button backButton = new Button(translationService.translate("duelquiz.back"), event -> {
            currentDuel = null;
            showInitialView();
        });
        backButton.addThemeVariants(ButtonVariant.LUMO_PRIMARY);

        mainContent.add(title, message, backButton);
    }

    private void startPolling() {
        if (pollingTask != null && !pollingTask.isDone()) {
            return;
        }

        pollingTask = executor.scheduleAtFixedRate(() -> {
            if (currentDuel != null && currentDuel.getId() != null) {
                Optional<DuelMatch> updated = duelService.getDuelById(currentDuel.getId());
                if (updated.isPresent()) {
                    DuelMatch oldStatus = currentDuel;
                    currentDuel = updated.get();

                    // Only update view if status changed
                    if (oldStatus.getStatus() != currentDuel.getStatus() ||
                        (currentDuel.getStatus() == DuelMatch.DuelStatus.MATCHED && !oldStatus.isBothPlayersReady() && currentDuel.isBothPlayersReady())) {
                        updateView();
                    }
                }
            }
        }, 1, 2, TimeUnit.SECONDS);
    }

    private void stopPolling() {
        if (pollingTask != null && !pollingTask.isDone()) {
            pollingTask.cancel(false);
        }
        if (countdownTask != null && !countdownTask.isDone()) {
            countdownTask.cancel(false);
        }
    }
}

