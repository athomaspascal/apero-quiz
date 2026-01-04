package com.quizz.core.repository;

import com.quizz.core.entity.PlayerTrace;
import com.quizz.core.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Repository
public interface PlayerTraceRepository extends JpaRepository<PlayerTrace, Long> {

    // Find all traces for a specific user
    List<PlayerTrace> findByUserOrderByTimestampDesc(User user);

    // Find all traces by action type
    List<PlayerTrace> findByActionTypeOrderByTimestampDesc(String actionType);

    // Find traces within a time range
    List<PlayerTrace> findByTimestampBetweenOrderByTimestampDesc(LocalDateTime start, LocalDateTime end);

    // Find the last login for a user
    Optional<PlayerTrace> findFirstByUserAndActionTypeOrderByTimestampDesc(User user, String actionType);

    // Get all active sessions (users who logged in but not logged out)
    @Query("SELECT DISTINCT t.user FROM PlayerTrace t WHERE t.actionType = 'LOGIN' " +
           "AND NOT EXISTS (SELECT 1 FROM PlayerTrace t2 WHERE t2.user = t.user " +
           "AND t2.actionType = 'LOGOUT' AND t2.timestamp > t.timestamp) " +
           "AND t.timestamp > :since")
    List<User> findActiveUsers(@Param("since") LocalDateTime since);

    // Count active users
    @Query("SELECT COUNT(DISTINCT t.user) FROM PlayerTrace t WHERE t.actionType = 'LOGIN' " +
           "AND NOT EXISTS (SELECT 1 FROM PlayerTrace t2 WHERE t2.user = t.user " +
           "AND t2.actionType = 'LOGOUT' AND t2.timestamp > t.timestamp) " +
           "AND t.timestamp > :since")
    Long countActiveUsers(@Param("since") LocalDateTime since);

    // Get recent quiz starts
    @Query("SELECT t FROM PlayerTrace t WHERE t.actionType = 'START_QUIZ' " +
           "AND t.timestamp > :since ORDER BY t.timestamp DESC")
    List<PlayerTrace> findRecentQuizStarts(@Param("since") LocalDateTime since);

    // Get quiz statistics by mode
    @Query("SELECT t.quizMode, COUNT(t) FROM PlayerTrace t WHERE t.actionType = 'START_QUIZ' " +
           "AND t.timestamp > :since GROUP BY t.quizMode")
    List<Object[]> getQuizStatsByMode(@Param("since") LocalDateTime since);

    // Get most played quizzes
    @Query("SELECT t.quiz.name, COUNT(t) as playCount FROM PlayerTrace t " +
           "WHERE t.actionType = 'START_QUIZ' AND t.timestamp > :since " +
           "GROUP BY t.quiz.name ORDER BY playCount DESC")
    List<Object[]> getMostPlayedQuizzes(@Param("since") LocalDateTime since);
}

