package com.quizz.examplefeature;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface QuizQuestionRepository extends JpaRepository<QuizQuestion, Long> {

    @Query("SELECT q FROM QuizQuestion q WHERE q.quiz.id = :quizId ORDER BY q.id")
    List<QuizQuestion> findByQuizId(@Param("quizId") Long quizId);

    long countByQuizId(Long quizId);
}

