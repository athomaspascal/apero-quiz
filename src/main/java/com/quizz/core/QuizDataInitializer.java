package com.quizz.core;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.quizz.core.entity.Quiz;
import com.quizz.core.entity.QuizQuestionsData;
import com.quizz.core.service.QuizQuestionService;
import com.quizz.core.service.QuizService;
import jakarta.annotation.PostConstruct;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.core.io.ClassPathResource;
import org.springframework.stereotype.Component;

import java.io.IOException;

@Component
public class QuizDataInitializer {

    private static final Logger logger = LoggerFactory.getLogger(QuizDataInitializer.class);

    private final QuizService quizService;
    private final QuizQuestionService quizQuestionService;

    public QuizDataInitializer(QuizService quizService, QuizQuestionService quizQuestionService) {
        this.quizService = quizService;
        this.quizQuestionService = quizQuestionService;
    }

    @PostConstruct
    public void init() {
        logger.info("=== QuizDataInitializer: Starting initialization check ===");

        // Only initialize if no quizzes exist
        var existingQuizzes = quizService.list(org.springframework.data.domain.Pageable.unpaged());
        logger.info("Found {} existing quizzes in database", existingQuizzes.size());

        if (existingQuizzes.isEmpty()) {
            logger.info("No quizzes found - initializing quiz data from JSON file...");
            initializeQuizData();
        } else {
            logger.info("Quizzes already exist - skipping initialization. Quiz names:");
            for (Quiz quiz : existingQuizzes) {
                logger.info("  - {} (ID: {}, Questions: {})",
                    quiz.getName(),
                    quiz.getId(),
                    quizQuestionService.getTotalQuestionsByQuizId(quiz.getId()));
            }
        }

        logger.info("=== QuizDataInitializer: Initialization check completed ===");
    }

    private void initializeQuizData() {
        try {
            logger.info("Starting to load quiz data from quiz-questions.json...");

            ObjectMapper objectMapper = new ObjectMapper();
            ClassPathResource resource = new ClassPathResource("quiz-questions.json");

            logger.info("Resource exists: {}", resource.exists());
            logger.info("Resource path: {}", resource.getPath());

            QuizQuestionsData data = objectMapper.readValue(resource.getInputStream(), QuizQuestionsData.class);

            logger.info("Successfully parsed JSON file. Found {} quizzes",
                data.getQuizzes() != null ? data.getQuizzes().size() : 0);

            // Create each quiz from the JSON data
            int quizCount = 0;
            for (QuizQuestionsData.QuizData quizData : data.getQuizzes()) {
                quizCount++;
                logger.info("Processing quiz #{}: '{}' with {} questions",
                    quizCount, quizData.getName(), quizData.getQuestions().size());

                Quiz quiz = new Quiz(quizData.getName());
                quiz.setImageFileName(quizData.getImageFileName());
                quiz = quizService.save(quiz);

                logger.info("Quiz '{}' saved with ID: {}", quizData.getName(), quiz.getId());

                // Add all questions for this quiz
                int questionCount = 0;
                for (QuizQuestionsData.QuestionData questionData : quizData.getQuestions()) {
                    questionCount++;
                    // Utiliser le niveau de difficulté s'il existe, sinon 1 par défaut
                    Integer difficultyLevel = questionData.getDifficulty_level() != 0
                        ? questionData.getDifficulty_level()
                        : 1;

                    quizQuestionService.createQuestion(quiz,
                        questionData.getQuestion(),
                        questionData.getOptions(),
                        questionData.getAnswer(),
                        difficultyLevel);

                    if (questionCount % 50 == 0) {
                        logger.info("  - Processed {} questions...", questionCount);
                    }
                }

                logger.info("Quiz '{}' initialized with {} questions", quizData.getName(), quizData.getQuestions().size());
            }

            logger.info("=== ALL QUIZ DATA INITIALIZED SUCCESSFULLY ===");
            logger.info("Total quizzes loaded: {}", quizCount);
        } catch (IOException e) {
            logger.error("=== FAILED TO INITIALIZE QUIZ DATA ===", e);
            logger.error("Error message: {}", e.getMessage());
            logger.error("Error type: {}", e.getClass().getName());
        } catch (Exception e) {
            logger.error("=== UNEXPECTED ERROR DURING QUIZ INITIALIZATION ===", e);
            logger.error("Error message: {}", e.getMessage());
            logger.error("Error type: {}", e.getClass().getName());
        }
    }
}

