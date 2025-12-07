package com.quizz.core.repository;

import com.quizz.core.entity.QuizParticipant;
import com.quizz.core.entity.QuizSession;
import com.quizz.core.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

public interface QuizParticipantRepository extends JpaRepository<QuizParticipant, Long> {
    List<QuizParticipant> findBySession(QuizSession session);
    Optional<QuizParticipant> findBySessionAndUser(QuizSession session, User user);
}

