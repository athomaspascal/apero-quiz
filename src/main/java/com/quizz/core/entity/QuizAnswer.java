package com.quizz.core.entity;

import jakarta.persistence.*;
import org.jspecify.annotations.Nullable;

import java.time.LocalDateTime;

/**
 * Entity to record each participant's answer to a quiz question
 */
@Entity
@Table(name = "quiz_answer",
       uniqueConstraints = @UniqueConstraint(columnNames = {"participant_id", "question_id"}))
public class QuizAnswer {

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE)
    @Column(name = "answer_id")
    private Long id;

    @ManyToOne
    @JoinColumn(name = "participant_id", nullable = false)
    private QuizParticipant participant;

    @ManyToOne
    @JoinColumn(name = "question_id", nullable = false)
    private QuizQuestion question;

    @Column(name = "user_answer", nullable = false, length = 200)
    private String userAnswer;

    @Column(name = "is_correct", nullable = false)
    private boolean correct;

    @Column(name = "answered_at", nullable = false)
    private LocalDateTime answeredAt;

    @Column(name = "time_taken_seconds")
    private Integer timeTakenSeconds;

    protected QuizAnswer() {
    }

    public QuizAnswer(QuizParticipant participant, QuizQuestion question, String userAnswer) {
        this.participant = participant;
        this.question = question;
        this.userAnswer = userAnswer;
        this.correct = question.getAnswer().equals(userAnswer);
        this.answeredAt = LocalDateTime.now();
    }

    public QuizAnswer(QuizParticipant participant, QuizQuestion question, String userAnswer, int timeTakenSeconds) {
        this(participant, question, userAnswer);
        this.timeTakenSeconds = timeTakenSeconds;
    }

    public @Nullable Long getId() {
        return id;
    }

    public QuizParticipant getParticipant() {
        return participant;
    }

    public QuizQuestion getQuestion() {
        return question;
    }

    public String getUserAnswer() {
        return userAnswer;
    }

    public void setUserAnswer(String userAnswer) {
        this.userAnswer = userAnswer;
        this.correct = question.getAnswer().equals(userAnswer);
    }

    public boolean isCorrect() {
        return correct;
    }

    public LocalDateTime getAnsweredAt() {
        return answeredAt;
    }

    public Integer getTimeTakenSeconds() {
        return timeTakenSeconds;
    }

    public void setTimeTakenSeconds(Integer timeTakenSeconds) {
        this.timeTakenSeconds = timeTakenSeconds;
    }

    @Override
    public boolean equals(Object obj) {
        if (obj == null || !getClass().isAssignableFrom(obj.getClass())) {
            return false;
        }
        if (obj == this) {
            return true;
        }

        QuizAnswer other = (QuizAnswer) obj;
        return getId() != null && getId().equals(other.getId());
    }

    @Override
    public int hashCode() {
        return getClass().hashCode();
    }
}

