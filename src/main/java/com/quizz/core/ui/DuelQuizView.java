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

    private DuelMatch currentDuel;
    private VerticalLayout mainContent;
    private ScheduledExecutorService executor;
    private ScheduledFuture<?> pollingTask;
    private ScheduledFuture<?> countdownTask;

    public DuelQuizView(DuelService duelService, TranslationService translationService) {
        this.duelService = duelService;
        this.translationService = translationService;

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
        Optional<DuelMatch> activeDuel = duelService.getActiveDuel(currentUser);

        if (activeDuel.isPresent()) {
            currentDuel = activeDuel.get();
            updateView();
        } else {
            showInitialView();
        }
    }

    @Override
    protected void onAttach(AttachEvent attachEvent) {
        super.onAttach(attachEvent);
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
        currentDuel = duelService.startSearching(currentUser);
        updateView();
    }

    private void updateView() {
        if (currentDuel == null) {
            showInitialView();
            return;
        }

        UI ui = getUI().orElse(null);
        if (ui != null) {
            ui.access(() -> {
                mainContent.removeAll();

                switch (currentDuel.getStatus()) {
                    case SEARCHING:
                        showSearchingView();
                        break;
                    case MATCHED:
                        showMatchedView();
                        break;
                    case COUNTDOWN:
                        showCountdownView();
                        break;
                    case IN_PROGRESS:
                        navigateToQuiz();
                        break;
                    case REMATCH_PENDING:
                        showRematchView();
                        break;
                    case FINISHED:
                        showFinishedView();
                        break;
                    case CANCELLED:
                        showCancelledView();
                        break;
                }

                ui.push();
            });
        }
    }

    private void showSearchingView() {
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
    }

    private void showMatchedView() {
        User currentUser = VaadinSession.getCurrent().getAttribute(User.class);
        User opponent = currentUser.getId().equals(currentDuel.getPlayer1().getId())
            ? currentDuel.getPlayer2()
            : currentDuel.getPlayer1();

        H2 title = new H2(translationService.translate("duelquiz.matched"));
        Paragraph opponentInfo = new Paragraph(
            translationService.translate("duelquiz.opponent") + ": " + opponent.getName()
        );
        Paragraph quizInfo = new Paragraph(
            translationService.translate("duelquiz.quiz") + ": " + currentDuel.getQuiz().getName()
        );

        Button acceptButton = new Button(translationService.translate("duelquiz.accept"), event -> {
            currentDuel = duelService.acceptMatch(currentDuel.getId(), currentUser);
            updateView();
        });
        acceptButton.addThemeVariants(ButtonVariant.LUMO_PRIMARY, ButtonVariant.LUMO_LARGE);

        Button declineButton = new Button(translationService.translate("duelquiz.decline"), event -> {
            duelService.cancelDuel(currentDuel.getId());
            currentDuel = null;
            showInitialView();
        });
        declineButton.addThemeVariants(ButtonVariant.LUMO_ERROR);

        mainContent.add(title, opponentInfo, quizInfo, acceptButton, declineButton);
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
        logger.info("Navigating to quiz: {}, duelId: {}",
            currentDuel.getQuiz().getId(), currentDuel.getId());
        stopPolling();

        // Store duel ID in session for QuizQuestionView to retrieve
        VaadinSession.getCurrent().setAttribute("activeDuelId", currentDuel.getId());

        getUI().ifPresent(ui -> {
            ui.navigate(QuizQuestionView.class,
                new RouteParameters("quizId", String.valueOf(currentDuel.getQuiz().getId())));
        });
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

        VerticalLayout player1Layout = new VerticalLayout();
        player1Layout.setAlignItems(FlexComponent.Alignment.CENTER);
        player1Layout.add(
            new H3(currentDuel.getPlayer1().getName()),
            new H1(String.valueOf(currentDuel.getPlayer1Score()))
        );

        Span vsSpan = new Span("VS");
        vsSpan.getStyle().set("font-size", "32px").set("font-weight", "bold");

        VerticalLayout player2Layout = new VerticalLayout();
        player2Layout.setAlignItems(FlexComponent.Alignment.CENTER);
        player2Layout.add(
            new H3(currentDuel.getPlayer2().getName()),
            new H1(String.valueOf(currentDuel.getPlayer2Score()))
        );

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

