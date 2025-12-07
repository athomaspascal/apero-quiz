package com.quizz.examplefeature;

import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

interface QuizSessionRepository extends JpaRepository<QuizSession, Long> {
    Optional<QuizSession> findBySessionCode(String sessionCode);
}

