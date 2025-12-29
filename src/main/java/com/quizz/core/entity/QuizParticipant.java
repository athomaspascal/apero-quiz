package com.quizz.core.entity;

import jakarta.persistence.*;
import org.jspecify.annotations.Nullable;

@Entity
@Table(name = "quiz_participant")
public class QuizParticipant {

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE)
    @Column(name = "participant_id")
    private Long id;

    @ManyToOne
    @JoinColumn(name = "session_id", nullable = false)
    private QuizSession session;

    @ManyToOne
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    @Column(name = "score", nullable = false)
    private int score = 0;

    @Column(name = "completed", nullable = false)
    private boolean completed = false;

    @Column(name = "team_name", length = 100)
    private String teamName;

    protected QuizParticipant() {
    }

    public QuizParticipant(QuizSession session, User user) {
        this.session = session;
        this.user = user;
        this.score = 0;
        this.completed = false;
    }

    public @Nullable Long getId() {
        return id;
    }

    public QuizSession getSession() {
        return session;
    }

    public User getUser() {
        return user;
    }

    public int getScore() {
        return score;
    }

    public void setScore(int score) {
        this.score = score;
    }

    public boolean isCompleted() {
        return completed;
    }

    public void setCompleted(boolean completed) {
        this.completed = completed;
    }

    public String getTeamName() {
        return teamName;
    }

    public void setTeamName(String teamName) {
        this.teamName = teamName;
    }
}

