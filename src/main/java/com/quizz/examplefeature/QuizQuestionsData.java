package com.quizz.examplefeature;

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
        private List<QuestionData> questions;

        public QuizData() {
        }

        public String getName() {
            return name;
        }

        public void setName(String name) {
            this.name = name;
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
        private String question;
        private List<String> options;
        private String answer;

        public QuestionData() {
        }

        public int getId() {
            return id;
        }

        public void setId(int id) {
            this.id = id;
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
    }
}

