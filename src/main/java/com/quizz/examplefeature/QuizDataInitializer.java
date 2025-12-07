package com.quizz.examplefeature;

import com.fasterxml.jackson.databind.ObjectMapper;
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
        // Only initialize if no quizzes exist
        if (quizService.list(org.springframework.data.domain.Pageable.unpaged()).isEmpty()) {
            logger.info("Initializing quiz data from JSON file...");
            initializeQuizData();
        }
    }

    private void initializeQuizData() {
        try {
            ObjectMapper objectMapper = new ObjectMapper();
            ClassPathResource resource = new ClassPathResource("quiz-questions.json");
            QuizQuestionsData data = objectMapper.readValue(resource.getInputStream(), QuizQuestionsData.class);

            // Create each quiz from the JSON data
            for (QuizQuestionsData.QuizData quizData : data.getQuizzes()) {
                Quiz quiz = quizService.createQuiz(quizData.getName());

                // Add all questions for this quiz
                for (QuizQuestionsData.QuestionData questionData : quizData.getQuestions()) {
                    quizQuestionService.createQuestion(quiz,
                        questionData.getQuestion(),
                        questionData.getOptions(),
                        questionData.getAnswer());
                }

                logger.info("Quiz '{}' initialized with {} questions", quizData.getName(), quizData.getQuestions().size());
            }

            logger.info("All quiz data initialized successfully");
        } catch (IOException e) {
            logger.error("Failed to initialize quiz data from JSON file", e);
        }
    }
}

