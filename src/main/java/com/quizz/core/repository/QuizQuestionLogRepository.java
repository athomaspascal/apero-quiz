package com.quizz.core.repository;

import com.quizz.core.entity.QuizQuestionLog;
import com.quizz.core.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface QuizQuestionLogRepository extends JpaRepository<QuizQuestionLog, Long> {

    List<QuizQuestionLog> findByUserOrderByAskedAtDesc(User user);

    List<QuizQuestionLog> findBySessionCodeOrderByAskedAt(String sessionCode);

    List<QuizQuestionLog> findByQuestionIdRef(Long questionIdRef);
}

