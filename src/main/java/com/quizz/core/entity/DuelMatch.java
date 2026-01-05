package com.quizz.core.entity;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "duel_match")
public class DuelMatch {

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE)
    @Column(name = "duel_id")
    private Long id;

    @ManyToOne
    @JoinColumn(name = "player1_id", nullable = false)
    private User player1;

    @ManyToOne
    @JoinColumn(name = "player2_id")
    private User player2;

    @ManyToOne
    @JoinColumn(name = "quiz_id")
    private Quiz quiz;

    @Column(name = "status", nullable = false)
    @Enumerated(EnumType.STRING)
    private DuelStatus status = DuelStatus.SEARCHING;

    @Column(name = "player1_score")
    private Integer player1Score;

    @Column(name = "player2_score")
    private Integer player2Score;

    @Column(name = "player1_ready")
    private boolean player1Ready = false;

    @Column(name = "player2_ready")
    private boolean player2Ready = false;

    @Column(name = "player1_rematch")
    private boolean player1Rematch = false;

    @Column(name = "player2_rematch")
    private boolean player2Rematch = false;

    @Column(name = "rematch_count")
    private int rematchCount = 0;

    @Column(name = "created_at", nullable = false)
    private LocalDateTime createdAt;

    @Column(name = "started_at")
    private LocalDateTime startedAt;

    @Column(name = "finished_at")
    private LocalDateTime finishedAt;

    @Column(name = "countdown_started_at")
    private LocalDateTime countdownStartedAt;

    public enum DuelStatus {
        SEARCHING,      // Waiting for opponent
        MATCHED,        // Opponent found, waiting for acceptance
        COUNTDOWN,      // Both accepted, countdown started
        IN_PROGRESS,    // Quiz in progress
        FINISHED,       // Quiz finished
        REMATCH_PENDING,// Waiting for rematch decision
        CANCELLED       // Duel cancelled
    }

    protected DuelMatch() {
    }

    public DuelMatch(User player1) {
        this.player1 = player1;
        this.createdAt = LocalDateTime.now();
        this.status = DuelStatus.SEARCHING;
    }

    // Getters and Setters
    public Long getId() {
        return id;
    }

    public User getPlayer1() {
        return player1;
    }

    public void setPlayer1(User player1) {
        this.player1 = player1;
    }

    public User getPlayer2() {
        return player2;
    }

    public void setPlayer2(User player2) {
        this.player2 = player2;
    }

    public Quiz getQuiz() {
        return quiz;
    }

    public void setQuiz(Quiz quiz) {
        this.quiz = quiz;
    }

    public DuelStatus getStatus() {
        return status;
    }

    public void setStatus(DuelStatus status) {
        this.status = status;
    }

    public Integer getPlayer1Score() {
        return player1Score;
    }

    public void setPlayer1Score(Integer player1Score) {
        this.player1Score = player1Score;
    }

    public Integer getPlayer2Score() {
        return player2Score;
    }

    public void setPlayer2Score(Integer player2Score) {
        this.player2Score = player2Score;
    }

    public boolean isPlayer1Ready() {
        return player1Ready;
    }

    public void setPlayer1Ready(boolean player1Ready) {
        this.player1Ready = player1Ready;
    }

    public boolean isPlayer2Ready() {
        return player2Ready;
    }

    public void setPlayer2Ready(boolean player2Ready) {
        this.player2Ready = player2Ready;
    }

    public boolean isPlayer1Rematch() {
        return player1Rematch;
    }

    public void setPlayer1Rematch(boolean player1Rematch) {
        this.player1Rematch = player1Rematch;
    }

    public boolean isPlayer2Rematch() {
        return player2Rematch;
    }

    public void setPlayer2Rematch(boolean player2Rematch) {
        this.player2Rematch = player2Rematch;
    }

    public int getRematchCount() {
        return rematchCount;
    }

    public void setRematchCount(int rematchCount) {
        this.rematchCount = rematchCount;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public LocalDateTime getStartedAt() {
        return startedAt;
    }

    public void setStartedAt(LocalDateTime startedAt) {
        this.startedAt = startedAt;
    }

    public LocalDateTime getFinishedAt() {
        return finishedAt;
    }

    public void setFinishedAt(LocalDateTime finishedAt) {
        this.finishedAt = finishedAt;
    }

    public LocalDateTime getCountdownStartedAt() {
        return countdownStartedAt;
    }

    public void setCountdownStartedAt(LocalDateTime countdownStartedAt) {
        this.countdownStartedAt = countdownStartedAt;
    }

    public boolean isBothPlayersReady() {
        return player1Ready && player2Ready;
    }

    public boolean isBothPlayersWantRematch() {
        return player1Rematch && player2Rematch;
    }

    public boolean canRematch() {
        return rematchCount < 2;
    }

    public void resetForRematch() {
        this.status = DuelStatus.COUNTDOWN;
        this.player1Score = null;
        this.player2Score = null;
        this.player1Ready = false;
        this.player2Ready = false;
        this.player1Rematch = false;
        this.player2Rematch = false;
        this.startedAt = null;
        this.finishedAt = null;
        this.countdownStartedAt = LocalDateTime.now();
        this.rematchCount++;
    }
}

