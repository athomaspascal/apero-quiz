package com.quizz.core.repository;

import com.quizz.core.entity.QuizParticipant;
import com.quizz.core.entity.QuizSession;
import com.quizz.core.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;
import java.util.Optional;

public interface QuizParticipantRepository extends JpaRepository<QuizParticipant, Long> {
    List<QuizParticipant> findBySession(QuizSession session);

    @Query("SELECT p FROM QuizParticipant p JOIN FETCH p.user u LEFT JOIN FETCH u.country WHERE p.session = :session")
    List<QuizParticipant> findBySessionWithUserAndCountry(@Param("session") QuizSession session);

    Optional<QuizParticipant> findBySessionAndUser(QuizSession session, User user);
}

