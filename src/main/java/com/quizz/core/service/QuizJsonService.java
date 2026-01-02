package com.quizz.core.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import com.quizz.core.entity.QuizQuestionsData;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.core.io.ClassPathResource;
import org.springframework.stereotype.Service;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.List;

@Service
public class QuizJsonService {

    private static final Logger logger = LoggerFactory.getLogger(QuizJsonService.class);
    private final ObjectMapper objectMapper;

    public QuizJsonService() {
        this.objectMapper = new ObjectMapper();
        this.objectMapper.registerModule(new JavaTimeModule());
    }

    /**
     * Met à jour le niveau de difficulté d'une question dans le fichier JSON
     */
    public void updateQuestionDifficultyLevel(String quizName, int questionId, Integer difficultyLevel) throws IOException {
        // Lire le fichier JSON
        File jsonFile = getJsonFile();
        QuizQuestionsData data = objectMapper.readValue(jsonFile, QuizQuestionsData.class);

        // Trouver le quiz et la question
        boolean updated = false;
        for (QuizQuestionsData.QuizData quiz : data.getQuizzes()) {
            if (quiz.getName().equals(quizName)) {
                for (QuizQuestionsData.QuestionData question : quiz.getQuestions()) {
                    if (question.getId() == questionId) {
                        question.setDifficulty_level(difficultyLevel);
                        question.setDateUpdate(LocalDateTime.now());
                        updated = true;
                        logger.info("Updated difficulty level for question ID {} in quiz '{}' to level {}", 
                                questionId, quizName, difficultyLevel);
                        break;
                    }
                }
                break;
            }
        }

        if (updated) {
            // Créer un backup avant de sauvegarder
            createBackup(jsonFile);
            
            // Sauvegarder le fichier JSON
            objectMapper.writerWithDefaultPrettyPrinter().writeValue(jsonFile, data);
            logger.info("JSON file updated successfully");
        } else {
            logger.warn("Question not found: quiz='{}', questionId={}", quizName, questionId);
        }
    }

    /**
     * Récupère toutes les données du fichier JSON
     */
    public QuizQuestionsData loadQuizData() throws IOException {
        File jsonFile = getJsonFile();
        return objectMapper.readValue(jsonFile, QuizQuestionsData.class);
    }

    /**
     * Récupère les questions d'un quiz spécifique
     */
    public List<QuizQuestionsData.QuestionData> getQuizQuestions(String quizName) throws IOException {
        QuizQuestionsData data = loadQuizData();
        
        for (QuizQuestionsData.QuizData quiz : data.getQuizzes()) {
            if (quiz.getName().equals(quizName)) {
                return quiz.getQuestions();
            }
        }
        
        return List.of();
    }

    /**
     * Obtient le chemin du fichier JSON
     */
    private File getJsonFile() throws IOException {
        // En développement, utiliser le fichier dans src/main/resources
        Path resourcePath = Paths.get("src/main/resources/quiz-questions.json");
        if (Files.exists(resourcePath)) {
            return resourcePath.toFile();
        }
        
        // En production, utiliser le classpath
        ClassPathResource resource = new ClassPathResource("tools/quiz-questions.json");
        return resource.getFile();
    }

    /**
     * Crée un backup du fichier JSON
     */
    private void createBackup(File jsonFile) {
        try {
            String timestamp = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyyMMdd-HHmmss"));
            Path backupPath = Paths.get("quiz-questions-backup-" + timestamp + ".json");
            Files.copy(jsonFile.toPath(), backupPath, StandardCopyOption.REPLACE_EXISTING);
            logger.info("Backup created: {}", backupPath.getFileName());
        } catch (IOException e) {
            logger.error("Failed to create backup", e);
        }
    }
}

