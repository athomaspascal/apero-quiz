package com.quizz.examplefeature;

import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

interface QuizParticipantRepository extends JpaRepository<QuizParticipant, Long> {
    List<QuizParticipant> findBySession(QuizSession session);
    Optional<QuizParticipant> findBySessionAndUser(QuizSession session, User user);
}

