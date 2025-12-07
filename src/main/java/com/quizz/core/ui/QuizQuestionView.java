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
import com.vaadin.flow.component.html.H2;
import com.vaadin.flow.component.html.H3;
import com.vaadin.flow.component.html.Main;
import com.vaadin.flow.component.html.Paragraph;
import com.vaadin.flow.component.orderedlayout.HorizontalLayout;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import com.vaadin.flow.component.progressbar.ProgressBar;
import com.vaadin.flow.component.radiobutton.RadioButtonGroup;
import com.vaadin.flow.router.*;
import com.vaadin.flow.server.VaadinSession;
import com.vaadin.flow.theme.lumo.LumoUtility;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Timer;
import java.util.TimerTask;

@Route("quiz-questions/:quizId")
@PageTitle("Quiz Questions")
class  QuizQuestionView extends Main implements BeforeEnterObserver {

    private static final int MAX_QUESTIONS = 5; // Limit to 5 questions
    private static final int TIME_LIMIT_SECONDS = 60; // 1 minute time limit

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

    private final H2 questionTitle;
    private final H3 questionText;
    private final RadioButtonGroup<String> optionsGroup;
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
    private int elapsedSeconds = 0;
    HorizontalLayout windowLayout = new HorizontalLayout();
    private Div horizontalContainer = new Div();


    QuizQuestionView(QuizQuestionService quizQuestionService, QuizService quizService,
                     QuizSessionService sessionService, QuizAnswerService answerService) {
        this.quizQuestionService = quizQuestionService;
        this.quizService = quizService;
        this.sessionService = sessionService;
        this.answerService = answerService;

        questionTitle = new H2();
        questionTitle.addClassNames(LumoUtility.Margin.Bottom.MEDIUM);

        questionText = new H3();
        questionText.addClassNames(LumoUtility.Margin.Bottom.MEDIUM);

        optionsGroup = new RadioButtonGroup<>();
        optionsGroup.addClassNames(LumoUtility.Margin.Bottom.MEDIUM);
        optionsGroup.getStyle().set("--lumo-primary-color", "#1976d2");
        optionsGroup.getStyle().set("--lumo-primary-color-50pct", "rgba(25, 118, 210, 0.5)");
        optionsGroup.getStyle().set("--lumo-primary-color-10pct", "rgba(25, 118, 210, 0.1)");

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

        nextButton = new Button("Next", event -> showNextQuestion());
        nextButton.addThemeVariants(ButtonVariant.LUMO_PRIMARY);
        nextButton.setEnabled(false); // Disabled by default until an answer is selected

        stopButton = new Button("Stop Quiz", event -> stopQuiz());
        stopButton.addThemeVariants(ButtonVariant.LUMO_ERROR);
        stopButton.getStyle().set("margin-left", "auto");

        // Enable next button when an answer is selected
        optionsGroup.addValueChangeListener(event ->
            nextButton.setEnabled(event.getValue() != null)
        );

        progressText = new Paragraph();
        progressText.addClassNames(LumoUtility.Margin.Top.MEDIUM);

        Div buttonLayout = new Div(previousButton, nextButton, stopButton);
        buttonLayout.addClassNames(LumoUtility.Display.FLEX, LumoUtility.Gap.MEDIUM);

        VerticalLayout content = new VerticalLayout(
            timerContainer,
            questionTitle,
            questionText,
            optionsGroup,
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
        add(content);
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

            // Load all questions and select 5 randomly
            int totalAvailableQuestions = quizQuestionService.getTotalQuestionsByQuizId(quizId);
            List<QuizQuestion> allQuestions = new ArrayList<>();
            for (int i = 0; i < totalAvailableQuestions; i++) {
                QuizQuestion question = quizQuestionService.getQuestionByQuizIdAndIndex(quizId, i);
                if (question != null) {
                    allQuestions.add(question);
                }
            }

            // Shuffle and take only MAX_QUESTIONS (5)
            Collections.shuffle(allQuestions);
            this.randomQuestions = allQuestions.stream()
                .limit(MAX_QUESTIONS)
                .toList();

            // Set total questions to the number we're actually showing
            this.totalQuestions = Math.min(MAX_QUESTIONS, this.randomQuestions.size());

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

            // Load first question
            displayQuestion();

            // Start the timer
            startTimer();
        } catch (NumberFormatException e) {
            event.rerouteTo("");
        }
    }

    private void startTimer() {
        startTime = System.currentTimeMillis();
        elapsedSeconds = 0;

        timer = new Timer();
        timer.scheduleAtFixedRate(new TimerTask() {
            @Override
            public void run() {
                UI ui = getUI().orElse(null);
                if (ui != null) {
                    ui.access(() -> {
                        elapsedSeconds++;

                        // Update progress bar and label
                        timeProgressBar.setValue(elapsedSeconds);
                        timeLabel.setText("Time: " + elapsedSeconds + "s / " + TIME_LIMIT_SECONDS + "s");

                        // Change color based on time remaining
                        if (elapsedSeconds >= TIME_LIMIT_SECONDS * 0.8) {
                            timeProgressBar.getStyle().set("--lumo-primary-color", "#d32f2f");
                        } else if (elapsedSeconds >= TIME_LIMIT_SECONDS * 0.5) {
                            timeProgressBar.getStyle().set("--lumo-primary-color", "#ff9800");
                        }

                        // Time's up!
                        if (elapsedSeconds >= TIME_LIMIT_SECONDS) {
                            stopTimer();
                            finishQuizTimeUp();
                        }
                    });
                }
            }
        }, 1000, 1000); // Update every second
    }

    private void stopTimer() {
        if (timer != null) {
            timer.cancel();
            timer = null;
        }
    }

    private void finishQuizTimeUp() {
        // Disable all interactions
        optionsGroup.setEnabled(false);
        nextButton.setEnabled(false);
        previousButton.setEnabled(false);

        // Show time's up message
        answerFeedback.setText("⏰ Time's up! Quiz finished.");
        answerFeedback.getStyle()
            .set("color", "var(--lumo-error-text-color)")
            .set("font-weight", "bold")
            .set("padding", "var(--lumo-space-m)")
            .set("background-color", "var(--lumo-error-color-10pct)")
            .set("border-radius", "var(--lumo-border-radius-m)");
        answerFeedback.setVisible(true);

        // Show final score after a short delay
        new Timer().schedule(new TimerTask() {
            @Override
            public void run() {
                UI ui = getUI().orElse(null);
                if (ui != null) {
                    ui.access(() -> showFinalScore());
                }
            }
        }, 2000);
    }

    private void displayQuestion() {
        if (currentQuestionIndex < randomQuestions.size()) {
            currentQuestion = randomQuestions.get(currentQuestionIndex);

            questionTitle.setText("Question " + (currentQuestionIndex + 1));
            questionText.setText(currentQuestion.getQuestion());
            optionsGroup.setItems(currentQuestion.getOptions());
            optionsGroup.setValue(null);
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
        // Check answer and update score if an option is selected
        if (optionsGroup.getValue() != null) {
            String selectedAnswer = optionsGroup.getValue();
            boolean isCorrect = selectedAnswer.equals(currentQuestion.getAnswer());

            // Store the user's answer
            userAnswers.add(selectedAnswer);

            if (isCorrect) {
                correctAnswers++;
                answerFeedback.setText("✓ Correct!");
                answerFeedback.getStyle().set("color", "green");
            } else {
                answerFeedback.setText("✗ Incorrect. The correct answer is: " + currentQuestion.getAnswer());
                answerFeedback.getStyle().set("color", "red");
            }
            answerFeedback.setVisible(true);

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
        } else {
            // No answer selected, store empty string
            userAnswers.add("");
        }

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
        questionTitle.setText("Quiz Completed!");

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

        optionsGroup.setVisible(false);
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

            // Remove all existing click listeners and add new one
            nextButton.getElement().removeProperty("click");
            nextButton.getElement().executeJs("this.removeAllListeners('click')");
            nextButton.addClickListener(event -> {
                VaadinSession.getCurrent().setAttribute("activeSessionCode", null);
                getUI().ifPresent(ui -> ui.navigate("quiz-session/" + sessionCode));
            });
        } else {
            // Regular quiz - show back button
            nextButton.setText("Back to Quiz List");
            nextButton.setVisible(true);
            nextButton.setEnabled(true);

            // Remove all existing click listeners and add new one
            nextButton.getElement().removeProperty("click");
            nextButton.getElement().executeJs("this.removeAllListeners('click')");
            nextButton.addClickListener(event ->
                getUI().ifPresent(ui -> ui.navigate(""))
            );
        }

        // Display all questions with answers on the right side
        displayAllQuestionsWithAnswersOnRight();
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
        if (optionsGroup.getValue() != null) {
            String selectedAnswer = optionsGroup.getValue();
            boolean isCorrect = selectedAnswer.equals(currentQuestion.getAnswer());

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

        // Show final score
        showFinalScore();
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
}
