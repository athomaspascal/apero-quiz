package com.quizz.examplefeature;

import jakarta.persistence.*;
import org.jspecify.annotations.Nullable;

import java.time.LocalDateTime;
import java.util.UUID;

@Entity
@Table(name = "quiz_session")
public class QuizSession {

    public static final int SESSION_CODE_LENGTH = 8;

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE)
    @Column(name = "session_id")
    private Long id;

    @Column(name = "session_code", nullable = false, unique = true, length = SESSION_CODE_LENGTH)
    private String sessionCode;

    @ManyToOne
    @JoinColumn(name = "quiz_id", nullable = false)
    private Quiz quiz;

    @Column(name = "created_at", nullable = false)
    private LocalDateTime createdAt;

    @Column(name = "status", nullable = false)
    @Enumerated(EnumType.STRING)
    private SessionStatus status = SessionStatus.WAITING;

    @Column(name = "host_user_id")
    private Long hostUserId;

    protected QuizSession() {
    }

    public QuizSession(Quiz quiz, Long hostUserId) {
        this.quiz = quiz;
        this.hostUserId = hostUserId;
        this.sessionCode = generateSessionCode();
        this.createdAt = LocalDateTime.now();
        this.status = SessionStatus.WAITING;
    }

    private String generateSessionCode() {
        return UUID.randomUUID().toString().substring(0, SESSION_CODE_LENGTH).toUpperCase();
    }

    public @Nullable Long getId() {
        return id;
    }

    public String getSessionCode() {
        return sessionCode;
    }

    public Quiz getQuiz() {
        return quiz;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public SessionStatus getStatus() {
        return status;
    }

    public void setStatus(SessionStatus status) {
        this.status = status;
    }

    public Long getHostUserId() {
        return hostUserId;
    }

    public enum SessionStatus {
        WAITING,    // En attente des participants
        ACTIVE,     // Session en cours
        COMPLETED   // Session terminée
    }
}

