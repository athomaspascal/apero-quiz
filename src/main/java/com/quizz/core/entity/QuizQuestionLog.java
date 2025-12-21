package com.quizz.core.entity;

import jakarta.persistence.*;
import org.jspecify.annotations.Nullable;

import java.time.LocalDateTime;

@Entity
@Table(name = "quiz_question_log")
public class QuizQuestionLog {

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE)
    @Column(name = "log_id")
    private Long id;

    @ManyToOne
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    @ManyToOne
    @JoinColumn(name = "quiz_id", nullable = false)
    private Quiz quiz;

    @Column(name = "question_id_ref")
    private Long questionIdRef;

    @Column(name = "question_text", length = 1000, nullable = false)
    private String questionText;

    @Column(name = "option1", length = 500)
    private String option1;

    @Column(name = "option2", length = 500)
    private String option2;

    @Column(name = "option3", length = 500)
    private String option3;

    @Column(name = "option4", length = 500)
    private String option4;

    @Column(name = "correct_answer", length = 500, nullable = false)
    private String correctAnswer;

    @Column(name = "user_answer", length = 500)
    private String userAnswer;

    @Column(name = "is_correct", nullable = false)
    private boolean isCorrect;

    @Column(name = "time_taken_seconds")
    private Integer timeTakenSeconds;

    @Column(name = "asked_at", nullable = false)
    private LocalDateTime askedAt;

    @Column(name = "session_code", length = 20)
    private String sessionCode;

    public QuizQuestionLog() {
    }

    public QuizQuestionLog(User user, Quiz quiz, Long questionIdRef, String questionText,
                           String option1, String option2, String option3, String option4,
                           String correctAnswer, String userAnswer, boolean isCorrect,
                           Integer timeTakenSeconds, String sessionCode) {
        this.user = user;
        this.quiz = quiz;
        this.questionIdRef = questionIdRef;
        this.questionText = questionText;
        this.option1 = option1;
        this.option2 = option2;
        this.option3 = option3;
        this.option4 = option4;
        this.correctAnswer = correctAnswer;
        this.userAnswer = userAnswer;
        this.isCorrect = isCorrect;
        this.timeTakenSeconds = timeTakenSeconds;
        this.askedAt = LocalDateTime.now();
        this.sessionCode = sessionCode;
    }

    public @Nullable Long getId() {
        return id;
    }

    public User getUser() {
        return user;
    }

    public void setUser(User user) {
        this.user = user;
    }

    public Quiz getQuiz() {
        return quiz;
    }

    public void setQuiz(Quiz quiz) {
        this.quiz = quiz;
    }

    public Long getQuestionIdRef() {
        return questionIdRef;
    }

    public void setQuestionIdRef(Long questionIdRef) {
        this.questionIdRef = questionIdRef;
    }

    public String getQuestionText() {
        return questionText;
    }

    public void setQuestionText(String questionText) {
        this.questionText = questionText;
    }

    public String getOption1() {
        return option1;
    }

    public void setOption1(String option1) {
        this.option1 = option1;
    }

    public String getOption2() {
        return option2;
    }

    public void setOption2(String option2) {
        this.option2 = option2;
    }

    public String getOption3() {
        return option3;
    }

    public void setOption3(String option3) {
        this.option3 = option3;
    }

    public String getOption4() {
        return option4;
    }

    public void setOption4(String option4) {
        this.option4 = option4;
    }

    public String getCorrectAnswer() {
        return correctAnswer;
    }

    public void setCorrectAnswer(String correctAnswer) {
        this.correctAnswer = correctAnswer;
    }

    public String getUserAnswer() {
        return userAnswer;
    }

    public void setUserAnswer(String userAnswer) {
        this.userAnswer = userAnswer;
    }

    public boolean isCorrect() {
        return isCorrect;
    }

    public void setCorrect(boolean correct) {
        isCorrect = correct;
    }

    public Integer getTimeTakenSeconds() {
        return timeTakenSeconds;
    }

    public void setTimeTakenSeconds(Integer timeTakenSeconds) {
        this.timeTakenSeconds = timeTakenSeconds;
    }

    public LocalDateTime getAskedAt() {
        return askedAt;
    }

    public void setAskedAt(LocalDateTime askedAt) {
        this.askedAt = askedAt;
    }

    public String getSessionCode() {
        return sessionCode;
    }

    public void setSessionCode(String sessionCode) {
        this.sessionCode = sessionCode;
    }
}

