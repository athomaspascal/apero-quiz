package com.quizz.core.service;

import com.quizz.core.entity.PlayerTrace;
import com.quizz.core.entity.Quiz;
import com.quizz.core.entity.User;
import com.quizz.core.repository.PlayerTraceRepository;
import com.vaadin.flow.server.VaadinRequest;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
public class PlayerTraceService {

    private static final Logger logger = LoggerFactory.getLogger(PlayerTraceService.class);

    private final PlayerTraceRepository traceRepository;

    public PlayerTraceService(PlayerTraceRepository traceRepository) {
        this.traceRepository = traceRepository;
    }

    /**
     * Record a player login
     */
    @Transactional
    public PlayerTrace recordLogin(User user) {
        PlayerTrace trace = new PlayerTrace(user, "LOGIN", LocalDateTime.now());

        // Try to capture IP and User-Agent if available
        try {
            VaadinRequest request = VaadinRequest.getCurrent();
            if (request != null) {
                trace.setIpAddress(request.getRemoteAddr());
                trace.setUserAgent(request.getHeader("User-Agent"));
            }
        } catch (Exception e) {
            logger.warn("Could not capture request info: {}", e.getMessage());
        }

        PlayerTrace saved = traceRepository.save(trace);
        logger.info("Recorded LOGIN for user: {}", user.getName());
        return saved;
    }

    /**
     * Record a player logout
     */
    @Transactional
    public PlayerTrace recordLogout(User user) {
        PlayerTrace trace = new PlayerTrace(user, "LOGOUT", LocalDateTime.now());
        PlayerTrace saved = traceRepository.save(trace);
        logger.info("Recorded LOGOUT for user: {}", user.getName());
        return saved;
    }

    /**
     * Record quiz start
     */
    @Transactional
    public PlayerTrace recordQuizStart(User user, Quiz quiz, String quizMode, String sessionCode, String teamName) {
        PlayerTrace trace = new PlayerTrace(user, "START_QUIZ", LocalDateTime.now());
        trace.setQuiz(quiz);
        trace.setQuizMode(quizMode);
        trace.setSessionCode(sessionCode);
        trace.setTeamName(teamName);

        PlayerTrace saved = traceRepository.save(trace);
        logger.info("Recorded START_QUIZ for user: {}, quiz: {}, mode: {}",
                    user.getName(), quiz.getName(), quizMode);
        return saved;
    }

    /**
     * Record quiz completion
     */
    @Transactional
    public PlayerTrace recordQuizComplete(User user, Quiz quiz, String quizMode, Integer score, String sessionCode, String teamName) {
        PlayerTrace trace = new PlayerTrace(user, "COMPLETE_QUIZ", LocalDateTime.now());
        trace.setQuiz(quiz);
        trace.setQuizMode(quizMode);
        trace.setScore(score);
        trace.setSessionCode(sessionCode);
        trace.setTeamName(teamName);

        PlayerTrace saved = traceRepository.save(trace);
        logger.info("Recorded COMPLETE_QUIZ for user: {}, quiz: {}, score: {}",
                    user.getName(), quiz.getName(), score);
        return saved;
    }

    /**
     * Get all traces for a user
     */
    public List<PlayerTrace> getUserTraces(User user) {
        return traceRepository.findByUserOrderByTimestampDesc(user);
    }

    /**
     * Get active users (logged in within the last X hours)
     */
    public List<User> getActiveUsers(int hoursAgo) {
        LocalDateTime since = LocalDateTime.now().minusHours(hoursAgo);
        return traceRepository.findActiveUsers(since);
    }

    /**
     * Count active users
     */
    public Long countActiveUsers(int hoursAgo) {
        LocalDateTime since = LocalDateTime.now().minusHours(hoursAgo);
        return traceRepository.countActiveUsers(since);
    }

    /**
     * Get recent quiz starts
     */
    public List<PlayerTrace> getRecentQuizStarts(int hoursAgo) {
        LocalDateTime since = LocalDateTime.now().minusHours(hoursAgo);
        return traceRepository.findRecentQuizStarts(since);
    }

    /**
     * Get quiz statistics by mode
     */
    public Map<String, Long> getQuizStatsByMode(int hoursAgo) {
        LocalDateTime since = LocalDateTime.now().minusHours(hoursAgo);
        List<Object[]> results = traceRepository.getQuizStatsByMode(since);

        return results.stream()
                .collect(Collectors.toMap(
                    row -> row[0] != null ? (String) row[0] : "UNKNOWN",
                    row -> ((Number) row[1]).longValue()
                ));
    }

    /**
     * Get most played quizzes
     */
    public Map<String, Long> getMostPlayedQuizzes(int hoursAgo, int limit) {
        LocalDateTime since = LocalDateTime.now().minusHours(hoursAgo);
        List<Object[]> results = traceRepository.getMostPlayedQuizzes(since);

        return results.stream()
                .limit(limit)
                .collect(Collectors.toMap(
                    row -> (String) row[0],
                    row -> ((Number) row[1]).longValue(),
                    (v1, v2) -> v1,
                    java.util.LinkedHashMap::new
                ));
    }

    /**
     * Get traces within a time range
     */
    public List<PlayerTrace> getTracesBetween(LocalDateTime start, LocalDateTime end) {
        return traceRepository.findByTimestampBetweenOrderByTimestampDesc(start, end);
    }

    /**
     * Get all traces
     */
    public List<PlayerTrace> getAllTraces() {
        return traceRepository.findAll();
    }
}

