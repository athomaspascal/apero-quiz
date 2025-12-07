package com.quizz.core.repository;

import com.quizz.core.entity.QuizAnswer;
import com.quizz.core.entity.QuizParticipant;
import com.quizz.core.entity.QuizQuestion;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;
import java.util.Optional;

/**
 * Repository for managing quiz answers
 */
public interface QuizAnswerRepository extends JpaRepository<QuizAnswer, Long> {

    /**
     * Find all answers given by a participant
     */
    List<QuizAnswer> findByParticipant(QuizParticipant participant);

    /**
     * Find all answers for a specific question
     */
    List<QuizAnswer> findByQuestion(QuizQuestion question);

    /**
     * Find a specific answer by participant and question
     */
    Optional<QuizAnswer> findByParticipantAndQuestion(QuizParticipant participant, QuizQuestion question);

    /**
     * Count correct answers for a participant
     */
    @Query("SELECT COUNT(a) FROM QuizAnswer a WHERE a.participant = :participant AND a.correct = true")
    long countCorrectAnswersByParticipant(@Param("participant") QuizParticipant participant);

    /**
     * Count total answers for a participant
     */
    long countByParticipant(QuizParticipant participant);

    /**
     * Find all correct answers by a participant
     */
    List<QuizAnswer> findByParticipantAndCorrect(QuizParticipant participant, boolean correct);

    /**
     * Get average time taken per question for a participant
     */
    @Query("SELECT AVG(a.timeTakenSeconds) FROM QuizAnswer a WHERE a.participant = :participant AND a.timeTakenSeconds IS NOT NULL")
    Double getAverageTimeTakenByParticipant(@Param("participant") QuizParticipant participant);
}

