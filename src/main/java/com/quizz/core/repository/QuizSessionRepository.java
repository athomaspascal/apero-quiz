package com.quizz.core.repository;

import com.quizz.core.entity.QuizSession;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface QuizSessionRepository extends JpaRepository<QuizSession, Long> {
    Optional<QuizSession> findBySessionCode(String sessionCode);
}

