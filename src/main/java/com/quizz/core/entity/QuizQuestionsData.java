package com.quizz.core.entity;

import java.time.LocalDateTime;
import java.util.List;

public class QuizQuestionsData {
    private List<QuizData> quizzes;

    public QuizQuestionsData() {
    }

    public List<QuizData> getQuizzes() {
        return quizzes;
    }

    public void setQuizzes(List<QuizData> quizzes) {
        this.quizzes = quizzes;
    }

    public static class QuizData {
        private String name;
        private String imageFileName;
        private List<QuestionData> questions;

        public QuizData() {
        }

        public String getName() {
            return name;
        }

        public void setName(String name) {
            this.name = name;
        }

        public String getImageFileName() {
            return imageFileName;
        }

        public void setImageFileName(String imageFileName) {
            this.imageFileName = imageFileName;
        }

        public List<QuestionData> getQuestions() {
            return questions;
        }

        public void setQuestions(List<QuestionData> questions) {
            this.questions = questions;
        }
    }

    public static class QuestionData {
        private int id;
        private String uuid;
        private String question;
        private List<String> options;
        private String answer;
        private int difficulty_level = 1; // Valeur par défaut
        private LocalDateTime dateUpdate;

        public QuestionData() {
        }

        public int getId() {
            return id;
        }

        public void setId(int id) {
            this.id = id;
        }

        public String getUuid() {
            return uuid;
        }

        public void setUuid(String uuid) {
            this.uuid = uuid;
        }

        public String getQuestion() {
            return question;
        }

        public void setQuestion(String question) {
            this.question = question;
        }

        public List<String> getOptions() {
            return options;
        }

        public void setOptions(List<String> options) {
            this.options = options;
        }

        public String getAnswer() {
            return answer;
        }

        public void setAnswer(String answer) {
            this.answer = answer;
        }

        public int getDifficulty_level() {
            return difficulty_level;
        }

        public void setDifficulty_level(int difficulty_level) {
            this.difficulty_level = difficulty_level;
        }

        public LocalDateTime getDateUpdate() {
            return dateUpdate;
        }

        public void setDateUpdate(LocalDateTime dateUpdate) {
            this.dateUpdate = dateUpdate;
        }
    }
}

