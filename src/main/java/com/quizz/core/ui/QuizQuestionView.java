package com.quizz.core.ui;

import com.quizz.core.entity.Quiz;
import com.quizz.core.entity.QuizParticipant;
import com.quizz.core.entity.QuizQuestion;
import com.quizz.core.entity.QuizSession;
import com.quizz.core.entity.User;
import com.quizz.core.service.QuizAnswerService;
import com.quizz.core.service.QuizQuestionService;
import com.quizz.core.service.QuizService;
import com.quizz.core.service.QuizSessionService;
import com.vaadin.flow.component.UI;
import com.vaadin.flow.component.button.Button;
import com.vaadin.flow.component.button.ButtonVariant;
import com.vaadin.flow.component.html.Div;
import com.vaadin.flow.component.html.H3;
import com.vaadin.flow.component.html.Main;
import com.vaadin.flow.component.html.Paragraph;
import com.vaadin.flow.component.icon.VaadinIcon;
import com.vaadin.flow.component.DetachEvent;
import com.vaadin.flow.component.orderedlayout.HorizontalLayout;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import com.vaadin.flow.component.progressbar.ProgressBar;
import com.vaadin.flow.router.*;
import com.vaadin.flow.server.VaadinSession;
import com.vaadin.flow.theme.lumo.LumoUtility;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;
import java.util.Timer;
import java.util.TimerTask;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.ScheduledFuture;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicLong;


@Route("quiz-questions/:quizId")
@PageTitle("Quiz Questions")
class  QuizQuestionView extends Main implements BeforeEnterObserver {

    private static final Logger logger = LoggerFactory.getLogger(QuizQuestionView.class);
    private static final int MAX_QUESTIONS = 5; // Limit to 5 questions
    private static final int TIME_LIMIT_SECONDS = 60; // 1 minute time limit
    private static final String SEEN_QUESTION_IDS_SESSION_KEY_PREFIX = "seenQuestionIds:quiz:";
    private static final String QUIZ_RUN_SEED_SESSION_KEY_PREFIX = "quizRunSeed:quiz:";

    private final QuizQuestionService quizQuestionService;
    private final QuizService quizService;
    private final QuizSessionService sessionService;
    private final QuizAnswerService answerService;

    private Long quizId;
    private int currentQuestionIndex = 0;
    private QuizQuestion currentQuestion;
    private int correctAnswers = 0;
    private int totalQuestions = 0;
    private List<QuizQuestion> randomQuestions = new ArrayList<>();
    private QuizParticipant currentParticipant = null;
    private List<String> userAnswers = new ArrayList<>(); // Store user's answers

    //private final H2 questionTitle;
    private final H3 questionText;
    private final VerticalLayout optionsContainer;
    private String selectedAnswer = null;
    private List<Button> optionButtons = new ArrayList<>();
    private final Button nextButton;
    private final Button previousButton;
    private final Button stopButton;
    private final Paragraph progressText;
    private final Div answerFeedback;

    // Timer components
    private final ProgressBar timeProgressBar;
    private final Paragraph timeLabel;
    private Timer timer;
    private long startTime;
    private volatile int elapsedSeconds = 0; // volatile pour assurer la synchronisation entre threads
    private volatile long currentTimerId = 0; // ID unique pour chaque timer
    private volatile boolean isRestarting = false; // Flag to prevent double-clicks

    // --- Orchestration propre des tâches asynchrones (timer + délais UI) ---
    private final ScheduledExecutorService scheduler = Executors.newSingleThreadScheduledExecutor(r -> {
        Thread t = new Thread(r, "quiz-scheduler");
        t.setDaemon(true);
        return t;
    });
    private final AtomicLong runSeq = new AtomicLong(0);
    private volatile long activeRunId = 0;
    private volatile ScheduledFuture<?> pendingDelayFuture;

    HorizontalLayout windowLayout = new HorizontalLayout();
    private Div horizontalContainer = new Div();

    private volatile boolean quizCompleted = false;

    // Garde les registrations pour pouvoir retirer proprement les listeners
    private com.vaadin.flow.shared.Registration nextClickReg;
    private com.vaadin.flow.shared.Registration stopClickReg;

    QuizQuestionView(QuizQuestionService quizQuestionService, QuizService quizService,
                     QuizSessionService sessionService, QuizAnswerService answerService) {
        this.quizQuestionService = quizQuestionService;
        this.quizService = quizService;
        this.sessionService = sessionService;
        this.answerService = answerService;

        //questionTitle = new H2();
        //questionTitle.addClassNames(LumoUtility.Margin.Bottom.MEDIUM);

        questionText = new H3();
        questionText.addClassNames(LumoUtility.Margin.Bottom.MEDIUM);

        optionsContainer = new VerticalLayout();
        optionsContainer.setPadding(false);
        optionsContainer.setSpacing(true);
        optionsContainer.addClassNames(LumoUtility.Margin.Bottom.MEDIUM);

        answerFeedback = new Div();
        answerFeedback.addClassNames(LumoUtility.Margin.Bottom.MEDIUM);
        answerFeedback.setVisible(false);

        // Timer components
        timeProgressBar = new ProgressBar();
        timeProgressBar.setMin(0);
        timeProgressBar.setMax(TIME_LIMIT_SECONDS);
        timeProgressBar.setValue(0);
        timeProgressBar.setWidth("100%");
        timeProgressBar.getStyle().set("--lumo-primary-color", "#1976d2");

        timeLabel = new Paragraph("Time: 0s / 60s");
        timeLabel.getStyle()
            .set("font-weight", "bold")
            .set("text-align", "center")
            .set("margin", "0");

        Div timerContainer = new Div();
        timerContainer.addClassNames(LumoUtility.Margin.Bottom.LARGE);
        timerContainer.add(timeLabel, timeProgressBar);

        previousButton = new Button("Previous", event -> showPreviousQuestion());
        previousButton.addThemeVariants(ButtonVariant.LUMO_TERTIARY);

        nextButton = new Button("Next");
        nextButton.addThemeVariants(ButtonVariant.LUMO_PRIMARY);
        nextButton.setEnabled(false);

        stopButton = new Button("Stop Quiz");
        stopButton.addThemeVariants(ButtonVariant.LUMO_ERROR);
        stopButton.getStyle().set("margin-left", "auto");


        progressText = new Paragraph();
        progressText.addClassNames(LumoUtility.Margin.Top.MEDIUM);

        Div buttonLayout = new Div(previousButton, nextButton, stopButton);
        buttonLayout.addClassNames(LumoUtility.Display.FLEX, LumoUtility.Gap.MEDIUM);

        // Bouton de retour en haut à gauche (visible uniquement quand le menu latéral n'est pas affiché)
        Button backButton = new Button("Back to Quiz List", VaadinIcon.ARROW_LEFT.create());
        backButton.addThemeVariants(ButtonVariant.LUMO_TERTIARY);
        backButton.addClickListener(event -> {
            stopTimer(); // Arrêter le timer avant de quitter
            getUI().ifPresent(ui -> ui.navigate(""));
        });
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

        VerticalLayout content = new VerticalLayout(
            timerContainer,
            //questionTitle,
            questionText,
            optionsContainer,
            answerFeedback,
            buttonLayout,
            progressText
        );
        content.addClassNames(
            LumoUtility.Padding.LARGE,
            LumoUtility.MaxWidth.SCREEN_MEDIUM
        );

        setSizeFull();
        addClassNames(
            LumoUtility.BoxSizing.BORDER,
            LumoUtility.Display.FLEX,
            LumoUtility.FlexDirection.COLUMN,
            LumoUtility.Padding.MEDIUM
        );
        add(backButton, content);

        // Nettoyage quand la vue est détachée
        addDetachListener((DetachEvent detachEvent) -> {
            // Ne pas shutdown le scheduler ici: Vaadin peut détacher/réattacher la vue.
            // On annule simplement les tâches en cours pour éviter des callbacks après navigation.
            startNewRun();
            cancelPendingDelay();
            stopTimer();
        });
    }

    @Override
    public void beforeEnter(BeforeEnterEvent event) {
        String quizIdParam = event.getRouteParameters().get("quizId").orElse(null);
        if (quizIdParam == null) {
            event.rerouteTo("");
            return;
        }

        try {
            this.quizId = Long.parseLong(quizIdParam);
            Quiz quiz = quizService.getById(quizId);
            if (quiz == null) {
                event.rerouteTo("");
                return;
            }

            // Démarrer une nouvelle run (invalide toute tâche précédente)
            startNewRun();

            // Seed aléatoire stable pour cette run (utile pour éviter l'impression de "toujours les mêmes")
            initOrRotateRunSeed(true);

            // Charger toutes les questions en une fois (pas par index)
            List<QuizQuestion> allQuestions = new ArrayList<>(quizQuestionService.getQuestionsByQuizId(quizId));

            // Sélectionne 5 questions en évitant (si possible) celles déjà vues par cet utilisateur pendant cette session
            this.randomQuestions = selectQuestionsAvoidingSeen(allQuestions, new Random(currentRunSeed));

            // Set total questions to the number we're actually showing
            this.totalQuestions = Math.min(MAX_QUESTIONS, this.randomQuestions.size());

            logger.info("Starting quiz - ID: {}, Total questions: {}, Selected questions: {}, seed: {}",
                quizId, totalQuestions, randomQuestions.size(), currentRunSeed);

            // Get current participant if in a session
            Object sessionCodeAttr = VaadinSession.getCurrent().getAttribute("activeSessionCode");
            String sessionCode = sessionCodeAttr != null ? sessionCodeAttr.toString() : null;

            if (sessionCode != null) {
                QuizSession session = sessionService.getSessionByCode(sessionCode);
                User currentUser = VaadinSession.getCurrent().getAttribute(User.class);

                if (session != null && currentUser != null && currentUser.getId() != null) {
                    var participants = sessionService.getParticipants(session);
                    currentParticipant = participants.stream()
                        .filter(p -> p.getUser() != null && p.getUser().getId() != null
                                  && p.getUser().getId().equals(currentUser.getId()))
                        .findFirst()
                        .orElse(null);
                }
            }

            quizCompleted = false;

            // restaurer l'état des boutons (au cas où la vue revient depuis l'écran final)
            optionsContainer.setVisible(true);
            previousButton.setVisible(true);
            stopButton.setVisible(true);
            progressText.setVisible(true);

            restoreDefaultButtonHandlers();

            // Load first question
            displayQuestion();

            // Start the timer
            startTimer();
        } catch (NumberFormatException e) {
            event.rerouteTo("");
        }
    }

    private void restoreDefaultButtonHandlers() {
        // Retire les listeners actuels (si on était sur écran final)
        if (nextClickReg != null) {
            nextClickReg.remove();
        }
        if (stopClickReg != null) {
            stopClickReg.remove();
        }

        nextButton.setText("Next");
        nextButton.setVisible(true);
        nextButton.setEnabled(false);

        stopButton.setText("Stop Quiz");
        stopButton.setVisible(true);
        stopButton.setEnabled(true);
        stopButton.removeThemeVariants(ButtonVariant.LUMO_CONTRAST);
        stopButton.addThemeVariants(ButtonVariant.LUMO_ERROR);
        stopButton.setIcon(null);

        nextClickReg = nextButton.addClickListener(e -> showNextQuestion());
        stopClickReg = stopButton.addClickListener(e -> stopQuiz());
    }

    private void startTimer() {
        startTimer(UI.getCurrent());
    }

    private void startTimer(UI ui) {
        // Stop any existing timer first to avoid multiple timers
        if (timer != null) {
            logger.warn("Timer already exists when starting new timer - cancelling old one");
            timer.cancel();
            timer = null;
        }

        if (ui == null) {
            logger.error("Cannot start timer - UI is null");
            return;
        }

        startTime = System.currentTimeMillis();
        elapsedSeconds = 0;
        currentTimerId = System.currentTimeMillis();
        final long thisTimerId = currentTimerId;
        final long runIdSnapshot = activeRunId;

        logger.info("Starting new timer - timerId: {} runId: {}", thisTimerId, runIdSnapshot);

        timer = new Timer();
        timer.scheduleAtFixedRate(new TimerTask() {
            @Override
            public void run() {
                // Ignorer si ce n'est pas le timer actuel
                if (thisTimerId != currentTimerId || runIdSnapshot != activeRunId) {
                    return;
                }

                ui.access(() -> {
                    // double-check côté UI thread
                    if (runIdSnapshot != activeRunId) {
                        return;
                    }

                    elapsedSeconds++;

                    timeProgressBar.setValue(elapsedSeconds);
                    timeLabel.setText("Time: " + elapsedSeconds + "s / " + TIME_LIMIT_SECONDS + "s");

                    if (elapsedSeconds >= TIME_LIMIT_SECONDS * 0.8) {
                        timeProgressBar.getStyle().set("--lumo-primary-color", "#d32f2f");
                    } else if (elapsedSeconds >= TIME_LIMIT_SECONDS * 0.5) {
                        timeProgressBar.getStyle().set("--lumo-primary-color", "#ff9800");
                    }

                    if (elapsedSeconds >= TIME_LIMIT_SECONDS) {
                        stopTimer();
                        finishQuizTimeUp(runIdSnapshot);
                    }
                });
            }
        }, 1000, 1000);
    }

    private void finishQuizTimeUp(long runIdSnapshot) {
        // Disable all interactions
        optionButtons.forEach(btn -> btn.setEnabled(false));
        nextButton.setEnabled(false);
        previousButton.setEnabled(false);

        answerFeedback.setText("⏰ Time's up! Quiz finished.");
        answerFeedback.getStyle()
            .set("color", "var(--lumo-error-text-color)")
            .set("font-weight", "bold")
            .set("padding", "var(--lumo-space-m)")
            .set("background-color", "var(--lumo-error-color-10pct)")
            .set("border-radius", "var(--lumo-border-radius-m)");
        answerFeedback.setVisible(true);

        // Afficher le score final après 2s, mais seulement si la run est toujours active
        scheduleIfRunActive(runIdSnapshot, 2000, this::showFinalScore);
    }

    private void finishQuizTimeUp() {
        // conservée pour compat: redirection vers la version run-aware
        finishQuizTimeUp(activeRunId);
    }

    private void displayQuestion() {
        if (currentQuestionIndex < randomQuestions.size()) {
            currentQuestion = randomQuestions.get(currentQuestionIndex);

            //questionTitle.setText("Question " + (currentQuestionIndex + 1));
            questionText.setText(currentQuestion.getQuestion());

            // Clear previous options
            optionsContainer.removeAll();
            optionButtons.clear();
            selectedAnswer = null;

            // Randomize options order so the correct answer isn't always in the same place
            List<String> shuffledOptions = new ArrayList<>(currentQuestion.getOptions());
            Collections.shuffle(shuffledOptions);

            // Create large buttons for each option
            for (String option : shuffledOptions) {
                Button optionButton = new Button(option);
                optionButton.setWidth("100%");
                optionButton.getStyle()
                    .set("height", "60px")
                    .set("text-align", "left")
                    .set("font-size", "16px")
                    .set("padding", "0 20px")
                    .set("white-space", "normal")
                    .set("background-color", "#e3f2fd")  // Light blue background
                    .set("color", "#1976d2")  // Dark blue text
                    .set("border", "2px solid #90caf9");  // Light blue border

                optionButton.addClickListener(event -> {
                    // Toggle selection
                    if (selectedAnswer != null && selectedAnswer.equals(option)) {
                        // Deselect
                        selectedAnswer = null;
                        optionButton.setIcon(null);
                        optionButton.getStyle()
                            .set("background-color", "#e3f2fd")  // Light blue
                            .set("color", "#1976d2")  // Dark blue text
                            .set("border", "2px solid #90caf9");  // Light blue border
                        nextButton.setEnabled(false);
                    } else {
                        // Select this option, deselect others
                        selectedAnswer = option;

                        // Reset all buttons to light blue
                        for (Button btn : optionButtons) {
                            btn.setIcon(null);
                            btn.getStyle()
                                .set("background-color", "#e3f2fd")  // Light blue
                                .set("color", "#1976d2")  // Dark blue text
                                .set("border", "2px solid #90caf9");  // Light blue border
                        }

                        // Highlight selected button in light green
                        optionButton.getStyle()
                            .set("background-color", "#81c784")  // Light green
                            .set("color", "white")
                            .set("border", "2px solid #66bb6a");  // Medium green border

                        nextButton.setEnabled(true);
                    }
                });

                optionButtons.add(optionButton);
                optionsContainer.add(optionButton);
            }

            answerFeedback.setVisible(false);
            answerFeedback.setText("");

            progressText.setText("Question " + (currentQuestionIndex + 1) + " of " + totalQuestions);

            previousButton.setEnabled(currentQuestionIndex > 0);
            nextButton.setEnabled(false); // Disable next button until an answer is selected

            if (currentQuestionIndex >= totalQuestions - 1) {
                nextButton.setText("Finish");
            } else {
                nextButton.setText("Next");
            }
        }
    }

    private void showNextQuestion() {
        // Après un restart il arrive que Next soit cliqué alors que la vue est encore en transition.
        // On sécurise: pas de question => rien à faire.
        if (quizCompleted) {
            logger.debug("Ignoring Next click because quizCompleted=true");
            return;
        }
        if (currentQuestion == null) {
            logger.warn("Ignoring Next click because currentQuestion is null (quizId={}, idx={})", quizId, currentQuestionIndex);
            return;
        }

        // Check answer and update score if an option is selected
        if (selectedAnswer != null) {
            boolean isCorrect = selectedAnswer.equals(currentQuestion.getAnswer());

            if (isCorrect) {
                // Show checkmark icon ONLY on the correct answer when user selected it
                for (Button btn : optionButtons) {
                    String btnText = btn.getText();
                    if (btnText.equals(selectedAnswer)) {
                        btn.setIcon(VaadinIcon.CHECK.create());
                        btn.setIconAfterText(true);
                        btn.getElement().getStyle().set("color", "#2e7d32"); // Dark green for icon
                        break;
                    }
                }
            } else {
                // Show "times" icon ONLY on the wrong answer selected by user
                for (Button btn : optionButtons) {
                    String btnText = btn.getText();
                    if (btnText.equals(selectedAnswer)) {
                        btn.setIcon(VaadinIcon.CLOSE.create());
                        btn.setIconAfterText(true);
                        btn.getElement().getStyle().set("color", "#c62828"); // Dark red for icon
                        break;
                    }
                }
            }

            // Store the user's answer
            userAnswers.add(selectedAnswer);

            if (isCorrect) {
                correctAnswers++;
            }

            // Hide the feedback message (user only sees the icons)
            answerFeedback.setVisible(false);

            // Record the answer if we have a participant
            if (currentParticipant != null && currentQuestion != null) {
                try {
                    // Calculate time taken for this question
                    int timeTaken = elapsedSeconds;

                    // Save the answer to database
                    answerService.recordAnswer(currentParticipant, currentQuestion, selectedAnswer, timeTaken);
                } catch (Exception e) {
                    // Log error but don't interrupt the quiz
                    System.err.println("Error recording answer: " + e.getMessage());
                }
            }

            // Pause 1 seconde (run-aware) avant de passer à la question suivante
            final long runIdSnapshot = activeRunId;
            scheduleIfRunActive(runIdSnapshot, 1000, this::proceedToNextQuestion);

        } else {
            // No answer selected, store empty string
            userAnswers.add("");
            proceedToNextQuestion();
        }
    }

    private void proceedToNextQuestion() {
        if (currentQuestionIndex < totalQuestions - 1) {
            currentQuestionIndex++;
            displayQuestion();
        } else {
            // Quiz finished - show final score
            displayFinalScore();
        }
    }

    private void displayFinalScore() {
        // Stop the timer
        stopTimer();

        showFinalScore();
    }

    private void showFinalScore() {
        //questionTitle.setText("Quiz Completed!");

        double percentage = (totalQuestions > 0) ? ((double) correctAnswers / totalQuestions) * 100 : 0;
        String scoreMessage = String.format("Your Score: %d/%d (%.1f%%) - Time: %ds",
            correctAnswers, totalQuestions, percentage, elapsedSeconds);

        questionText.setText(scoreMessage);

        // Add performance message
        String performanceMessage;
        if (percentage >= 90) {
            performanceMessage = "Excellent! Outstanding performance! 🎉";
        } else if (percentage >= 70) {
            performanceMessage = "Great job! Well done! 👍";
        } else if (percentage >= 50) {
            performanceMessage = "Good effort! Keep practicing! 📚";
        } else {
            performanceMessage = "Keep learning and try again! 💪";
        }

        answerFeedback.setText(performanceMessage);
        answerFeedback.getStyle().set("color", "#1976d2");
        answerFeedback.getStyle().set("font-size", "1.2em");
        answerFeedback.getStyle().set("font-weight", "bold");
        answerFeedback.setVisible(true);

        optionsContainer.setVisible(false);
        previousButton.setVisible(false);
        stopButton.setVisible(false);
        progressText.setVisible(false);

        // Check if this is part of a session
        Object sessionCodeAttr = VaadinSession.getCurrent().getAttribute("activeSessionCode");
        String sessionCode = sessionCodeAttr != null ? sessionCodeAttr.toString() : null;

        if (sessionCode != null) {
            // Save score to session
            QuizSession session = sessionService.getSessionByCode(sessionCode);
            User currentUser = VaadinSession.getCurrent().getAttribute(User.class);

            if (session != null && currentUser != null && currentUser.getId() != null) {
                var participants = sessionService.getParticipants(session);
                var participant = participants.stream()
                    .filter(p -> p.getUser() != null && p.getUser().getId() != null
                              && p.getUser().getId().equals(currentUser.getId()))
                    .findFirst();

                participant.ifPresent(p ->
                    sessionService.updateParticipantScore(p, correctAnswers)
                );
            }

            // Change next button to "View Leaderboard"
            nextButton.setText("View Leaderboard");
            nextButton.setVisible(true);
            nextButton.setEnabled(true);

            // Remplacer le handler proprement
            if (nextClickReg != null) nextClickReg.remove();
            nextClickReg = nextButton.addClickListener(event -> {
                VaadinSession.getCurrent().setAttribute("activeSessionCode", null);
                getUI().ifPresent(ui -> ui.navigate("quiz-session/" + sessionCode));
            });

            // Bouton Restart
            stopButton.setText("Restart Quiz");
            stopButton.setVisible(true);
            stopButton.setEnabled(true);
            stopButton.removeThemeVariants(ButtonVariant.LUMO_ERROR);
            stopButton.addThemeVariants(ButtonVariant.LUMO_CONTRAST);
            stopButton.setIcon(VaadinIcon.REFRESH.create());

            if (stopClickReg != null) stopClickReg.remove();
            stopClickReg = stopButton.addClickListener(event -> restartQuiz());
        } else {
            nextButton.setText("Back to Quiz List");
            nextButton.setVisible(true);
            nextButton.setEnabled(true);

            if (nextClickReg != null) nextClickReg.remove();
            nextClickReg = nextButton.addClickListener(event -> getUI().ifPresent(ui -> ui.navigate("")));

            stopButton.setText("Restart Quiz");
            stopButton.setVisible(true);
            stopButton.setEnabled(true);
            stopButton.removeThemeVariants(ButtonVariant.LUMO_ERROR);
            stopButton.addThemeVariants(ButtonVariant.LUMO_CONTRAST);
            stopButton.setIcon(VaadinIcon.REFRESH.create());

            if (stopClickReg != null) stopClickReg.remove();
            stopClickReg = stopButton.addClickListener(event -> restartQuiz());
        }

        // Display all questions with answers on the right side
        displayAllQuestionsWithAnswersOnRight();
    }

    private void restartQuiz() {
        if (isRestarting) {
            logger.warn("Restart already in progress - ignoring duplicate click");
            return;
        }
        isRestarting = true;

        // Invalider toutes les tâches en cours et démarrer une nouvelle run
        startNewRun();

        try {
            quizCompleted = false;

            // Reset all state variables
            currentQuestionIndex = 0;
            correctAnswers = 0;
            selectedAnswer = null;
            userAnswers.clear();
            elapsedSeconds = 0;
            currentQuestion = null;

            // Nouvelle seed pour forcer une sélection différente
            initOrRotateRunSeed(true);

            // Rétablir handlers et apparence standard des boutons
            restoreDefaultButtonHandlers();

            // Clear the UI
            optionsContainer.removeAll();
            optionButtons.clear();

            // Charger toutes les questions
            List<QuizQuestion> allQuestions = new ArrayList<>(quizQuestionService.getQuestionsByQuizId(quizId));

            // Sélectionne une nouvelle série en évitant les déjà vues (tant qu'il reste des questions)
            randomQuestions = selectQuestionsAvoidingSeen(allQuestions, new Random(currentRunSeed));
            totalQuestions = Math.min(MAX_QUESTIONS, randomQuestions.size());

            optionsContainer.setVisible(true);
            previousButton.setVisible(true);
            previousButton.setEnabled(false);

            progressText.setVisible(true);
            progressText.setText("Question 1 of " + totalQuestions);


            answerFeedback.setVisible(false);
            answerFeedback.setText("");

            timeProgressBar.setValue(0);
            timeProgressBar.setMax(TIME_LIMIT_SECONDS);
            timeProgressBar.getStyle().set("--lumo-primary-color", "#1976d2");
            timeLabel.setText("Time: 0s / " + TIME_LIMIT_SECONDS + "s");

            getElement().executeJs(
                "const reviewSection = this.querySelector('#review-section');" +
                "if (reviewSection && reviewSection.parentElement) {" +
                "  reviewSection.parentElement.removeChild(reviewSection);" +
                "}"
            );

            displayQuestion();
            startTimer();
        } finally {
            isRestarting = false;
        }
    }

    private void startNewRun() {
        activeRunId = runSeq.incrementAndGet();
        cancelPendingDelay();
        stopTimer();
    }

    private void cancelPendingDelay() {
        ScheduledFuture<?> f = pendingDelayFuture;
        if (f != null) {
            f.cancel(false);
            pendingDelayFuture = null;
        }
    }

    private void scheduleIfRunActive(long runIdSnapshot, long delayMs, Runnable uiTask) {
        cancelPendingDelay();
        pendingDelayFuture = scheduler.schedule(() -> {
            if (runIdSnapshot != activeRunId) {
                return;
            }
            getUI().ifPresent(ui -> ui.access(() -> {
                if (runIdSnapshot != activeRunId) {
                    return;
                }
                uiTask.run();
            }));
        }, delayMs, TimeUnit.MILLISECONDS);
    }

    private void showPreviousQuestion() {
        if (currentQuestionIndex > 0) {
            currentQuestionIndex--;
            displayQuestion();
        }
    }

    private void stopQuiz() {
        // Stop the timer
        stopTimer();

        // Save the current answer if one was selected
        if (selectedAnswer != null) {
            boolean isCorrect = selectedAnswer.equals(currentQuestion.getAnswer());

            if (isCorrect) {
                // Show checkmark icon ONLY on the correct answer when user selected it
                for (Button btn : optionButtons) {
                    String btnText = btn.getText();
                    if (btnText.equals(selectedAnswer)) {
                        btn.setIcon(VaadinIcon.CHECK.create());
                        btn.setIconAfterText(true);
                        btn.getElement().getStyle().set("color", "#2e7d32"); // Dark green for icon
                        break;
                    }
                }
            } else {
                // Show "times" icon ONLY on the wrong answer selected by user
                for (Button btn : optionButtons) {
                    String btnText = btn.getText();
                    if (btnText.equals(selectedAnswer)) {
                        btn.setIcon(VaadinIcon.CLOSE.create());
                        btn.setIconAfterText(true);
                        btn.getElement().getStyle().set("color", "#c62828"); // Dark red for icon
                        break;
                    }
                }
            }

            // Store the user's answer
            userAnswers.add(selectedAnswer);

            if (isCorrect) {
                correctAnswers++;
            }

            // Record the answer if we have a participant
            if (currentParticipant != null && currentQuestion != null) {
                try {
                    answerService.recordAnswer(currentParticipant, currentQuestion, selectedAnswer, elapsedSeconds);
                } catch (Exception e) {
                    System.err.println("Error recording answer: " + e.getMessage());
                }
            }
        } else {
            // No answer selected for current question, store empty string
            userAnswers.add("");
        }

        // Fill remaining questions with empty answers
        while (userAnswers.size() < totalQuestions) {
            userAnswers.add("");
        }

        // Pause 1 seconde (run-aware) avant d'afficher le score final
        final long runIdSnapshot = activeRunId;
        scheduleIfRunActive(runIdSnapshot, 1000, this::showFinalScore);
    }

    private void stopTimer() {
        if (timer != null) {
            timer.cancel();
            timer.purge();
            timer = null;
        }
    }

    private void displayAllQuestionsWithAnswersOnRight() {
        // Remove old horizontal container if present
        remove(horizontalContainer);
        horizontalContainer.removeAll();

        // Create the review container (displayed below the main content)
        VerticalLayout reviewContainer = new VerticalLayout();
        reviewContainer.setId("review-section");
        reviewContainer.addClassNames(
            LumoUtility.Padding.MEDIUM,
            LumoUtility.Gap.MEDIUM
        );
        reviewContainer.getStyle()
            .set("background-color", "var(--lumo-contrast-5pct)")
            .set("border-radius", "var(--lumo-border-radius-m)")
            .set("width", "100%")
            .set("max-height", "600px")
            .set("overflow-y", "auto")
            .set("margin-top", "var(--lumo-space-l)");

        H3 reviewTitle = new H3("📋 Questions Review");
        reviewTitle.getStyle().set("margin-top", "0");
        reviewContainer.add(reviewTitle);

        // Display each question with the user's answer (vertical layout)
        for (int i = 0; i < randomQuestions.size(); i++) {
            QuizQuestion question = randomQuestions.get(i);
            String userAnswer = i < userAnswers.size() ? userAnswers.get(i) : "";
            String correctAnswer = question.getAnswer();
            boolean isCorrect = userAnswer.equals(correctAnswer);

            // Question container
            Div questionContainer = new Div();
            questionContainer.addClassNames(LumoUtility.Padding.MEDIUM);
            questionContainer.getStyle()
                .set("background-color", "white")
                .set("border-radius", "var(--lumo-border-radius-m)")
                .set("border-left", "4px solid " + (isCorrect ? "#4caf50" : "#f44336"))
                .set("margin-bottom", "var(--lumo-space-s)");

            // Question number and text
            H3 qNumber = new H3("Question " + (i + 1));
            qNumber.getStyle().set("margin-top", "0");

            Paragraph qText = new Paragraph(question.getQuestion());
            qText.getStyle().set("font-weight", "500");

            // User's answer
            Div userAnswerDiv = new Div();
            userAnswerDiv.getStyle()
                .set("padding", "var(--lumo-space-s)")
                .set("margin", "var(--lumo-space-s) 0")
                .set("border-radius", "var(--lumo-border-radius-s)")
                .set("background-color", isCorrect ? "#e8f5e9" : "#ffebee")
                .set("color", isCorrect ? "#2e7d32" : "#c62828")
                .set("font-weight", "bold");

            String answerPrefix = isCorrect ? "✓ Your answer: " : "✗ Your answer: ";
            userAnswerDiv.setText(answerPrefix + (userAnswer.isEmpty() ? "(No answer)" : userAnswer));

            questionContainer.add(qNumber, qText, userAnswerDiv);

            // Show correct answer if user was wrong
            if (!isCorrect) {
                Div correctAnswerDiv = new Div();
                correctAnswerDiv.getStyle()
                    .set("padding", "var(--lumo-space-s)")
                    .set("margin", "var(--lumo-space-s) 0")
                    .set("border-radius", "var(--lumo-border-radius-s)")
                    .set("background-color", "#e8f5e9")
                    .set("color", "#2e7d32")
                    .set("font-weight", "bold");
                correctAnswerDiv.setText("✓ Correct answer: " + correctAnswer);
                questionContainer.add(correctAnswerDiv);
            }

            reviewContainer.add(questionContainer);
        }

        // Add the review below the main content
        add(reviewContainer);
    }

    private Set<Long> getSeenQuestionIdsForCurrentQuiz() {
        if (quizId == null) {
            return new HashSet<>();
        }
        Object attr = VaadinSession.getCurrent().getAttribute(SEEN_QUESTION_IDS_SESSION_KEY_PREFIX + quizId);
        if (attr instanceof Set<?> s) {
            //noinspection unchecked
            return (Set<Long>) s;
        }
        Set<Long> created = new HashSet<>();
        VaadinSession.getCurrent().setAttribute(SEEN_QUESTION_IDS_SESSION_KEY_PREFIX + quizId, created);
        return created;
    }

    private long currentRunSeed = 0L;

    private void initOrRotateRunSeed(boolean rotate) {
        if (quizId == null) {
            currentRunSeed = System.nanoTime();
            return;
        }
        String key = QUIZ_RUN_SEED_SESSION_KEY_PREFIX + quizId;
        Object attr = VaadinSession.getCurrent().getAttribute(key);
        Long existing = (attr instanceof Long l) ? l : null;

        if (!rotate && existing != null) {
            currentRunSeed = existing;
            return;
        }

        // Seed: mélange nanoTime + un peu d'entropie liée à l'UI/session
        long newSeed = System.nanoTime() ^ System.currentTimeMillis() ^ (long) System.identityHashCode(this);
        currentRunSeed = newSeed;
        VaadinSession.getCurrent().setAttribute(key, newSeed);
    }

    private List<QuizQuestion> selectQuestionsAvoidingSeen(List<QuizQuestion> allQuestions, Random rnd) {
        if (allQuestions == null || allQuestions.isEmpty()) {
            return List.of();
        }

        // Mélange d'abord toutes les questions avec la seed de run.
        // Ça casse fortement l'effet "les premières (ORDER BY id) reviennent".
        List<QuizQuestion> shuffled = new ArrayList<>(allQuestions);
        Collections.shuffle(shuffled, rnd);

        Set<Long> seenIds = getSeenQuestionIdsForCurrentQuiz();

        // On prend d'abord les non-vues (si on a des IDs)
        List<QuizQuestion> selected = new ArrayList<>(MAX_QUESTIONS);
        for (QuizQuestion q : shuffled) {
            if (selected.size() >= MAX_QUESTIONS) break;
            Long id = q.getId();
            if (id != null && !seenIds.contains(id)) {
                selected.add(q);
            }
        }

        // Si pas assez, on complète avec le reste (vues ou sans id)
        if (selected.size() < MAX_QUESTIONS) {
            for (QuizQuestion q : shuffled) {
                if (selected.size() >= MAX_QUESTIONS) break;
                if (!selected.contains(q)) {
                    selected.add(q);
                }
            }
        }

        // Si on n'a rien pu sélectionner en non-vues (par ex. tout vu), on reset le seen et on garde la sélection
        boolean anyUnseen = selected.stream().anyMatch(q -> q.getId() != null && !seenIds.contains(q.getId()));
        if (!anyUnseen && !seenIds.isEmpty()) {
            seenIds.clear();
        }

        // Marquer comme vues
        for (QuizQuestion q : selected) {
            if (q.getId() != null) {
                seenIds.add(q.getId());
            }
        }

        return List.copyOf(selected);
    }

    // Ancienne signature conservée si appelée ailleurs dans le fichier
    private List<QuizQuestion> selectQuestionsAvoidingSeen(List<QuizQuestion> allQuestions) {
        return selectQuestionsAvoidingSeen(allQuestions, new Random(System.nanoTime()));
    }

}
