package com.quizz.tools;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.ObjectNode;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.StandardCopyOption;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class AddDifficultyLevel {

    public static void main(String[] args) {
        System.out.println("Starting script to add difficulty_level attribute...");

        try {
            String inputFile = "src/main/resources/quiz-questions.json";
            File file = new File(inputFile);

            if (!file.exists()) {
                System.err.println("ERROR: File not found: " + inputFile);
                System.exit(1);
            }

            System.out.println("File found: " + inputFile);

            // Create backup
            String timestamp = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyyMMdd_HHmmss"));
            String backupFile = "src/main/resources/quiz-questions_backup_" + timestamp + ".json";
            Files.copy(file.toPath(), new File(backupFile).toPath(), StandardCopyOption.REPLACE_EXISTING);
            System.out.println("Backup created: " + backupFile);

            // Read JSON
            ObjectMapper mapper = new ObjectMapper();
            JsonNode root = mapper.readTree(file);

            if (!root.isArray()) {
                System.err.println("ERROR: JSON root is not an array");
                System.exit(1);
            }

            ArrayNode quizzes = (ArrayNode) root;
            System.out.println("Total quizzes: " + quizzes.size());

            int totalQuestions = 0;
            int modifiedQuestions = 0;

            // Process each quiz
            for (JsonNode quiz : quizzes) {
                String quizName = quiz.has("name") ? quiz.get("name").asText() : "Unknown";
                System.out.println("\nProcessing quiz: " + quizName);

                if (quiz.has("questions") && quiz.get("questions").isArray()) {
                    ArrayNode questions = (ArrayNode) quiz.get("questions");

                    for (JsonNode question : questions) {
                        totalQuestions++;

                        if (!question.has("difficulty_level")) {
                            ((ObjectNode) question).put("difficulty_level", 1);
                            modifiedQuestions++;
                        }
                    }
                }
            }

            System.out.println("\n" + "=".repeat(60));
            System.out.println("Total questions processed: " + totalQuestions);
            System.out.println("Questions modified: " + modifiedQuestions);

            // Write back to file
            System.out.println("\nWriting modified JSON to file...");
            mapper.writerWithDefaultPrettyPrinter().writeValue(file, root);

            System.out.println("\n✅ COMPLETED SUCCESSFULLY!");
            System.out.println("=".repeat(60));
            System.out.println("Backup: " + backupFile);
            System.out.println("Output: " + inputFile);
            System.out.println("=".repeat(60));

        } catch (IOException e) {
            System.err.println("❌ ERROR: " + e.getMessage());
            e.printStackTrace();
            System.exit(1);
        }
    }
}

