package com.quizz.core.ui;

import com.quizz.base.ui.component.ViewToolbar;
import com.quizz.core.entity.Quiz;
import com.quizz.core.entity.QuizParticipant;
import com.quizz.core.entity.QuizQuestion;
import com.quizz.core.entity.QuizSession;
import com.quizz.core.entity.User;
import com.quizz.core.service.QuizAnswerService;
import com.quizz.core.service.QuizQuestionService;
import com.quizz.core.service.QuizService;
import com.quizz.core.service.QuizSessionService;
import com.quizz.core.service.QuizQuestionLogService;
import com.quizz.core.service.TranslationService;
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
    private final QuizQuestionLogService questionLogService;
    private final TranslationService translationService;

    private Long quizId;
    private Quiz currentQuiz; // Store current quiz for logging
    private String quizName; // Store quiz name for toolbar
    private ViewToolbar toolbar; // ViewToolbar reference
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
    private final Paragraph playerInfoLabel; // Display player name and team

    // Timer components
    private final ProgressBar timeProgressBar;
    private final Paragraph timeLabel;
    private final Paragraph scoreLabel;
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
                     QuizSessionService sessionService, QuizAnswerService answerService,
                     QuizQuestionLogService questionLogService, TranslationService translationService) {
        this.quizQuestionService = quizQuestionService;
        this.quizService = quizService;
        this.sessionService = sessionService;
        this.answerService = answerService;
        this.questionLogService = questionLogService;
        this.translationService = translationService;

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

        timeLabel = new Paragraph(translationService.translate("quiz.timer.initial"));
        timeLabel.getStyle()
            .set("font-weight", "bold")
            .set("text-align", "center")
            .set("margin", "0");

        // Score label with smaller font
        scoreLabel = new Paragraph(translationService.translate("quiz.yourScore") + ": 0 / 0");
        scoreLabel.getStyle()
            .set("font-size", "0.875rem")
            .set("text-align", "center")
            .set("margin", "0")
            .set("color", "var(--lumo-secondary-text-color)");
        scoreLabel.setVisible(false); // Hide until first answer

        // Container for timer and score labels side by side
        HorizontalLayout timerScoreLayout = new HorizontalLayout(timeLabel, scoreLabel);
        timerScoreLayout.setWidthFull();
        timerScoreLayout.setJustifyContentMode(HorizontalLayout.JustifyContentMode.BETWEEN);
        timerScoreLayout.setAlignItems(HorizontalLayout.Alignment.CENTER);
        timerScoreLayout.getStyle().set("margin", "0");

        // Player info label (will be populated in beforeEnter if in team mode)
        playerInfoLabel = new Paragraph();
        playerInfoLabel.getStyle()
            .set("font-size", "0.875rem")
            .set("text-align", "center")
            .set("margin", "var(--lumo-space-xs) 0")
            .set("color", "var(--lumo-primary-text-color)")
            .set("font-weight", "500");
        playerInfoLabel.setVisible(false); // Will be shown if in team mode

        Div timerContainer = new Div();
        timerContainer.addClassNames(LumoUtility.Margin.Bottom.LARGE);
        timerContainer.add(timerScoreLayout, playerInfoLabel, timeProgressBar);

        previousButton = new Button(translationService.translate("quiz.previous"), event -> showPreviousQuestion());
        previousButton.addThemeVariants(ButtonVariant.LUMO_TERTIARY);

        nextButton = new Button(translationService.translate("quiz.next"));
        nextButton.addThemeVariants(ButtonVariant.LUMO_PRIMARY);
        nextButton.setEnabled(false);

        stopButton = new Button(translationService.translate("quiz.stop"));
        stopButton.addThemeVariants(ButtonVariant.LUMO_ERROR);
        stopButton.getStyle().set("margin-left", "auto");


        progressText = new Paragraph();
        progressText.addClassNames(LumoUtility.Margin.Top.MEDIUM);

        Div buttonLayout = new Div(previousButton, nextButton, stopButton);
        buttonLayout.addClassNames(LumoUtility.Display.FLEX, LumoUtility.Gap.MEDIUM);

        // Bouton de retour en haut à gauche (visible uniquement quand le menu latéral n'est pas affiché)
        Button backButton = new Button(translationService.translate("quiz.backToList"), VaadinIcon.ARROW_LEFT.create());
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

            // Store quiz for logging
            this.currentQuiz = quiz;

            // Store quiz name for toolbar
            this.quizName = quiz.getName();

            // Add ViewToolbar at the top
            if (toolbar != null) {
                remove(toolbar);
            }
            toolbar = new ViewToolbar(quizName);
            addComponentAsFirst(toolbar);

            // Démarrer une nouvelle run (invalide toute tâche précédente)
            startNewRun();

            // Seed aléatoire stable pour cette run (utile pour éviter l'impression de "toujours les mêmes")
            initOrRotateRunSeed(true);

            // Charger toutes les questions en une fois (pas par index)
            List<QuizQuestion> allQuestions = new ArrayList<>(quizQuestionService.getQuestionsByQuizId(quizId));

            // Check if we're coming from a session or starting a simple quiz
            // Get current participant if in a session
            Object sessionCodeAttr = VaadinSession.getCurrent().getAttribute("activeSessionCode");
            String sessionCode = sessionCodeAttr != null ? sessionCodeAttr.toString() : null;
            QuizSession session = null;
            boolean isSessionQuiz = false;

            if (sessionCode != null) {
                session = sessionService.getSessionByCode(sessionCode);

                // Verify the session is still active and valid
                if (session != null && session.getQuiz() != null
                    && session.getQuiz().getId() != null
                    && session.getQuiz().getId().equals(quizId)) {
                    isSessionQuiz = true;
                    User currentUser = VaadinSession.getCurrent().getAttribute(User.class);

                    if (currentUser != null && currentUser.getId() != null) {
                        var participants = sessionService.getParticipants(session);
                        currentParticipant = participants.stream()
                            .filter(p -> p.getUser() != null && p.getUser().getId() != null
                                      && p.getUser().getId().equals(currentUser.getId()))
                            .findFirst()
                            .orElse(null);
                    }
                } else {
                    // Session doesn't exist or quiz ID doesn't match - clear the session code
                    logger.info("Clearing stale activeSessionCode. Session: {}, Quiz ID mismatch or session not found", sessionCode);
                    VaadinSession.getCurrent().setAttribute("activeSessionCode", null);
                    session = null;
                }
            }

            // If NOT in a session quiz, ensure we clear any stale session data
            if (!isSessionQuiz) {
                VaadinSession.getCurrent().setAttribute("activeSessionCode", null);
                currentParticipant = null;
                logger.info("Starting simple quiz (non-session) for quiz ID: {}", quizId);
                // Hide player info for simple quiz
                playerInfoLabel.setVisible(false);
            } else {
                // Update player info label for session quiz
                if (currentParticipant != null) {
                    User currentUser = VaadinSession.getCurrent().getAttribute(User.class);
                    if (currentUser != null) {
                        String playerInfo = "👤 " + currentUser.getName();

                        // Add team info if in team mode
                        if (session != null && session.isTeamMode() && currentParticipant.getTeamName() != null && !currentParticipant.getTeamName().isEmpty()) {
                            String teamName = currentParticipant.getTeamName();
                            // Capitalize first letter of team name
                            String displayTeamName = teamName.substring(0, 1).toUpperCase() + teamName.substring(1);
                            playerInfo += " | 🏆 " + displayTeamName;
                        }

                        playerInfoLabel.setText(playerInfo);
                        playerInfoLabel.setVisible(true);
                        logger.info("Displaying player info: {}", playerInfo);
                    }
                } else {
                    playerInfoLabel.setVisible(false);
                }
            }

            // If in a session, use the session's questions (same for all participants)
            if (isSessionQuiz && session != null && session.getSelectedQuestionIds() != null && !session.getSelectedQuestionIds().isEmpty()) {
                // Load questions from session
                this.randomQuestions = loadQuestionsFromSession(session, allQuestions);
                logger.debug("Loaded {} questions from session {}", randomQuestions.size(), session.getSessionCode());
            } else {
                // Select questions randomly
                this.randomQuestions = selectQuestionsAvoidingSeen(allQuestions, new Random(currentRunSeed));

                // If in a session, save the selected questions
                if (isSessionQuiz && session != null) {
                    saveQuestionsToSession(session, randomQuestions);
                    logger.info("Saved {} questions to session {}", randomQuestions.size(), session.getSessionCode());
                }
            }

            // Set total questions to the number we're actually showing
            this.totalQuestions = Math.min(MAX_QUESTIONS, this.randomQuestions.size());

            logger.debug("Starting quiz - ID: {}, Total questions: {}, Selected questions: {}, seed: {}",
                quizId, totalQuestions, randomQuestions.size(), currentRunSeed);

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

        nextButton.setText(translationService.translate("quiz.next"));
        nextButton.setVisible(true);
        nextButton.setEnabled(false);

        stopButton.setText(translationService.translate("quiz.stop"));
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

        logger.debug("Starting new timer - timerId: {} runId: {}", thisTimerId, runIdSnapshot);

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
                    timeLabel.setText(translationService.translate("quiz.timer.elapsed", elapsedSeconds, TIME_LIMIT_SECONDS));

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

        answerFeedback.setText(translationService.translate("quiz.timeUp"));
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

            // Update toolbar with question progress
            if (toolbar != null) {
                remove(toolbar);
            }
            toolbar = new ViewToolbar(quizName + " - " + translationService.translate("quiz.progress", (currentQuestionIndex + 1), totalQuestions));
            addComponentAsFirst(toolbar);

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

            progressText.setText(translationService.translate("quiz.progress", (currentQuestionIndex + 1), totalQuestions));

            previousButton.setEnabled(currentQuestionIndex > 0);
            nextButton.setEnabled(false); // Disable next button until an answer is selected

            if (currentQuestionIndex >= totalQuestions - 1) {
                nextButton.setText(translationService.translate("quiz.finish"));
            } else {
                nextButton.setText(translationService.translate("quiz.next"));
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

            // Update the score display
            updateScoreDisplay();

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
                    logger.error("Error recording answer: " + e.getMessage());
                }
            }

            // LOG QUESTION AND ANSWERS FOR DEBUGGING - Always log for all users
            try {
                User currentUser = VaadinSession.getCurrent().getAttribute(User.class);
                Object sessionCodeAttr = VaadinSession.getCurrent().getAttribute("activeSessionCode");
                String sessionCode = sessionCodeAttr != null ? sessionCodeAttr.toString() : null;

                if (currentUser != null && currentQuiz != null && currentQuestion != null) {
                    questionLogService.logQuestion(
                        currentUser,
                        currentQuiz,
                        currentQuestion,
                        selectedAnswer,
                        elapsedSeconds,
                        sessionCode
                    );

                    logger.debug("QUESTION LOGGED - User: {}, Quiz: {}, Question ID: {}, Question: {}, Correct Answer: {}, User Answer: {}, Options: {}",
                        currentUser.getEmail(),
                        currentQuiz.getName(),
                        currentQuestion.getId(),
                        currentQuestion.getQuestion(),
                        currentQuestion.getAnswer(),
                        selectedAnswer,
                        currentQuestion.getOptions()
                    );
                }
            } catch (Exception e) {
                logger.error("Error logging question: " + e.getMessage(), e);
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

    private void updateScoreDisplay() {
        if (scoreLabel != null) {
            int answeredQuestions = currentQuestionIndex + 1;
            scoreLabel.setText(translationService.translate("quiz.yourScore") + ": " + correctAnswers + " / " + answeredQuestions);
            scoreLabel.setVisible(true); // Show after first answer
        }
    }

    private void displayFinalScore() {
        // Stop the timer
        stopTimer();

        showFinalScore();
    }

    private void showFinalScore() {
        //questionTitle.setText("Quiz Completed!");

        // Update toolbar to show completion
        if (toolbar != null) {
            remove(toolbar);
        }
        toolbar = new ViewToolbar(quizName + " - " + translationService.translate("quiz.completed"));
        addComponentAsFirst(toolbar);

        double percentage = (totalQuestions > 0) ? ((double) correctAnswers / totalQuestions) * 100 : 0;
        String scoreMessage = translationService.translate("quiz.finalScore.message", correctAnswers, totalQuestions, String.format("%.1f", percentage), elapsedSeconds);

        // Add performance message
        String performanceMessage;
        if (percentage >= 90) {
            performanceMessage = translationService.translate("quiz.performance.excellent");
        } else if (percentage >= 70) {
            performanceMessage = translationService.translate("quiz.performance.great");
        } else if (percentage >= 50) {
            performanceMessage = translationService.translate("quiz.performance.good");
        } else {
            performanceMessage = translationService.translate("quiz.performance.keepLearning");
        }

        // Combine score and performance message on the same line
        questionText.setText(scoreMessage + " - " + performanceMessage);

        // Hide the separate feedback div
        answerFeedback.setVisible(false);

        optionsContainer.setVisible(false);
        previousButton.setVisible(false);
        stopButton.setVisible(false);
        progressText.setVisible(false);

        // Hide the progress bar to save space
        timeProgressBar.setVisible(false);

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
            nextButton.setText(translationService.translate("quiz.viewLeaderboard"));
            nextButton.setVisible(true);
            nextButton.setEnabled(true);

            // Remplacer le handler proprement
            if (nextClickReg != null) nextClickReg.remove();
            nextClickReg = nextButton.addClickListener(event -> {
                VaadinSession.getCurrent().setAttribute("activeSessionCode", null);
                getUI().ifPresent(ui -> ui.navigate("quiz-session/" + sessionCode));
            });

            // Check if current user is the host of the session
            boolean isHost = currentUser != null && currentUser.getId() != null &&
                             session != null && currentUser.getId().equals(session.getHostUserId());

            // Debug logs to troubleshoot isHost detection
            logger.info("showFinalScore - Checking isHost: currentUser={}, currentUserId={}, session={}, sessionHostUserId={}, isHost={}",
                currentUser != null ? currentUser.getName() : "null",
                currentUser != null ? currentUser.getId() : "null",
                session != null ? session.getSessionCode() : "null",
                session != null ? session.getHostUserId() : "null",
                isHost);

            // Hide the Restart Session button - it will be shown in QuizSessionView after the scoreboard
            // This ensures the button appears at the bottom of the scoreboard, not on the quiz completion page
            logger.info("Session quiz completed - user will see Restart Session button on the scoreboard page (QuizSessionView)");
            stopButton.setVisible(false);
        } else {
            nextButton.setText(translationService.translate("quiz.backToList"));
            nextButton.setVisible(true);
            nextButton.setEnabled(true);

            if (nextClickReg != null) nextClickReg.remove();
            nextClickReg = nextButton.addClickListener(event -> getUI().ifPresent(ui -> ui.navigate("")));

            stopButton.setText(translationService.translate("quiz.restart"));
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
            progressText.setText(translationService.translate("quiz.progress", 1, totalQuestions));


            answerFeedback.setVisible(false);
            answerFeedback.setText("");

            // Re-show and reset the progress bar
            timeProgressBar.setVisible(true);
            timeProgressBar.setValue(0);
            timeProgressBar.setMax(TIME_LIMIT_SECONDS);
            timeProgressBar.getStyle().set("--lumo-primary-color", "#1976d2");
            timeLabel.setText(translationService.translate("quiz.timer.initial"));

            // Hide the score label until first answer
            scoreLabel.setVisible(false);

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

    private void startNewRoundForSession(QuizSession session, String sessionCode) {
        logger.info("Host starting new round for session: {}", sessionCode);

        // Reset all participants scores and completed status
        sessionService.resetParticipants(session);

        // Clear the selected questions so new questions will be chosen
        session.setSelectedQuestionIds(null);
        sessionService.updateSession(session);

        // Set session back to WAITING status
        sessionService.updateSessionStatus(session, QuizSession.SessionStatus.WAITING);

        // Clear active session from current user's session
        VaadinSession.getCurrent().setAttribute("activeSessionCode", null);

        // Navigate back to the quiz session view where host can start for everyone
        getUI().ifPresent(ui -> ui.navigate("quiz-session/" + sessionCode));
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
                    logger.error("Error recording answer: " + e.getMessage());
                }
            }

            // LOG QUESTION AND ANSWERS FOR DEBUGGING
            try {
                User currentUser = VaadinSession.getCurrent().getAttribute(User.class);
                Object sessionCodeAttr = VaadinSession.getCurrent().getAttribute("activeSessionCode");
                String sessionCode = sessionCodeAttr != null ? sessionCodeAttr.toString() : null;

                if (currentUser != null && currentQuiz != null && currentQuestion != null) {
                    questionLogService.logQuestion(
                        currentUser,
                        currentQuiz,
                        currentQuestion,
                        selectedAnswer,
                        elapsedSeconds,
                        sessionCode
                    );

                    logger.info("QUESTION LOGGED (STOP) - User: {}, Quiz: {}, Question ID: {}, Correct Answer: {}, User Answer: {}",
                        currentUser.getEmail(),
                        currentQuiz.getName(),
                        currentQuestion.getId(),
                        currentQuestion.getAnswer(),
                        selectedAnswer
                    );
                }
            } catch (Exception e) {
                logger.error("Error logging question on stop: " + e.getMessage(), e);
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

        H3 reviewTitle = new H3(translationService.translate("quiz.review.title"));
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
            H3 qNumber = new H3(translationService.translate("quiz.review.questionNumber", (i + 1)));
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

            String answerText = userAnswer.isEmpty() ? translationService.translate("quiz.review.noAnswer") : userAnswer;
            String answerPrefix = isCorrect ? "✓ " + translationService.translate("quiz.review.yourAnswer") + ": " : "✗ " + translationService.translate("quiz.review.yourAnswer") + ": ";
            userAnswerDiv.setText(answerPrefix + answerText);

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
                correctAnswerDiv.setText("✓ " + translationService.translate("quiz.review.correctAnswer") + ": " + correctAnswer);
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

        // Update the seen set in session
        VaadinSession.getCurrent().setAttribute(getSeenIdsSessionKey(), seenIds);

        return selected;
    }

    private List<QuizQuestion> loadQuestionsFromSession(QuizSession session, List<QuizQuestion> allQuestions) {
        String questionIdsStr = session.getSelectedQuestionIds();
        if (questionIdsStr == null || questionIdsStr.isEmpty()) {
            return new ArrayList<>();
        }

        // Parse comma-separated IDs
        String[] idStrs = questionIdsStr.split(",");
        List<Long> questionIds = new ArrayList<>();
        for (String idStr : idStrs) {
            try {
                questionIds.add(Long.parseLong(idStr.trim()));
            } catch (NumberFormatException e) {
                logger.error("Invalid question ID in session: {}", idStr);
            }
        }

        // Find questions by IDs in the same order
        List<QuizQuestion> questions = new ArrayList<>();
        for (Long questionId : questionIds) {
            allQuestions.stream()
                .filter(q -> q.getId() != null && q.getId().equals(questionId))
                .findFirst()
                .ifPresent(questions::add);
        }

        return questions;
    }

    private void saveQuestionsToSession(QuizSession session, List<QuizQuestion> questions) {
        // Convert question IDs to comma-separated string
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < questions.size(); i++) {
            QuizQuestion q = questions.get(i);
            if (q.getId() != null) {
                if (i > 0) {
                    sb.append(",");
                }
                sb.append(q.getId());
            }
        }

        session.setSelectedQuestionIds(sb.toString());
        sessionService.updateSession(session);
    }

    private String getSeenIdsSessionKey() {
        return SEEN_QUESTION_IDS_SESSION_KEY_PREFIX + quizId;
    }

    // Ancienne signature conservée si appelée ailleurs dans le fichier
    private List<QuizQuestion> selectQuestionsAvoidingSeen(List<QuizQuestion> allQuestions) {
        return selectQuestionsAvoidingSeen(allQuestions, new Random(System.nanoTime()));
    }

}
