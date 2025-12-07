package com.quizz.core.dto;

import java.util.List;

/**
 * DTO for participant answer statistics
 */
public class ParticipantAnswerStats {

    private Long participantId;
    private String participantName;
    private long totalAnswers;
    private long correctAnswers;
    private long incorrectAnswers;
    private double scorePercentage;
    private Double averageTimePerQuestion;
    private List<QuestionAnswerDetail> answerDetails;

    public ParticipantAnswerStats() {
    }

    public ParticipantAnswerStats(Long participantId, String participantName,
                                   long totalAnswers, long correctAnswers,
                                   double scorePercentage, Double averageTimePerQuestion) {
        this.participantId = participantId;
        this.participantName = participantName;
        this.totalAnswers = totalAnswers;
        this.correctAnswers = correctAnswers;
        this.incorrectAnswers = totalAnswers - correctAnswers;
        this.scorePercentage = scorePercentage;
        this.averageTimePerQuestion = averageTimePerQuestion;
    }

    public Long getParticipantId() {
        return participantId;
    }

    public void setParticipantId(Long participantId) {
        this.participantId = participantId;
    }

    public String getParticipantName() {
        return participantName;
    }

    public void setParticipantName(String participantName) {
        this.participantName = participantName;
    }

    public long getTotalAnswers() {
        return totalAnswers;
    }

    public void setTotalAnswers(long totalAnswers) {
        this.totalAnswers = totalAnswers;
    }

    public long getCorrectAnswers() {
        return correctAnswers;
    }

    public void setCorrectAnswers(long correctAnswers) {
        this.correctAnswers = correctAnswers;
    }

    public long getIncorrectAnswers() {
        return incorrectAnswers;
    }

    public void setIncorrectAnswers(long incorrectAnswers) {
        this.incorrectAnswers = incorrectAnswers;
    }

    public double getScorePercentage() {
        return scorePercentage;
    }

    public void setScorePercentage(double scorePercentage) {
        this.scorePercentage = scorePercentage;
    }

    public Double getAverageTimePerQuestion() {
        return averageTimePerQuestion;
    }

    public void setAverageTimePerQuestion(Double averageTimePerQuestion) {
        this.averageTimePerQuestion = averageTimePerQuestion;
    }

    public List<QuestionAnswerDetail> getAnswerDetails() {
        return answerDetails;
    }

    public void setAnswerDetails(List<QuestionAnswerDetail> answerDetails) {
        this.answerDetails = answerDetails;
    }

    /**
     * Nested class for detailed answer information
     */
    public static class QuestionAnswerDetail {
        private Long questionId;
        private String questionText;
        private String userAnswer;
        private String correctAnswer;
        private boolean correct;
        private Integer timeTakenSeconds;

        public QuestionAnswerDetail() {
        }

        public QuestionAnswerDetail(Long questionId, String questionText,
                                     String userAnswer, String correctAnswer,
                                     boolean correct, Integer timeTakenSeconds) {
            this.questionId = questionId;
            this.questionText = questionText;
            this.userAnswer = userAnswer;
            this.correctAnswer = correctAnswer;
            this.correct = correct;
            this.timeTakenSeconds = timeTakenSeconds;
        }

        public Long getQuestionId() {
            return questionId;
        }

        public void setQuestionId(Long questionId) {
            this.questionId = questionId;
        }

        public String getQuestionText() {
            return questionText;
        }

        public void setQuestionText(String questionText) {
            this.questionText = questionText;
        }

        public String getUserAnswer() {
            return userAnswer;
        }

        public void setUserAnswer(String userAnswer) {
            this.userAnswer = userAnswer;
        }

        public String getCorrectAnswer() {
            return correctAnswer;
        }

        public void setCorrectAnswer(String correctAnswer) {
            this.correctAnswer = correctAnswer;
        }

        public boolean isCorrect() {
            return correct;
        }

        public void setCorrect(boolean correct) {
            this.correct = correct;
        }

        public Integer getTimeTakenSeconds() {
            return timeTakenSeconds;
        }

        public void setTimeTakenSeconds(Integer timeTakenSeconds) {
            this.timeTakenSeconds = timeTakenSeconds;
        }
    }
}

