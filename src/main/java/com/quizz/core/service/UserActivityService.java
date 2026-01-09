package com.quizz.core.service;

import com.quizz.core.entity.UserActivity;
import com.quizz.core.entity.User;
import com.quizz.core.repository.UserActivityRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

/**
 * Service to track real-time user activity and detect inactive users
 */
@Service
public class UserActivityService {

    private static final Logger logger = LoggerFactory.getLogger(UserActivityService.class);
    private final UserActivityRepository userActivityRepository;

    public UserActivityService(UserActivityRepository userActivityRepository) {
        this.userActivityRepository = userActivityRepository;
    }

    private static final int INACTIVITY_THRESHOLD_SECONDS = 180;

    /**
     * Update user activity timestamp with session ID
     */
    @Transactional
    public void updateActivity(User user, String activityType, String pageUrl, String sessionId) {
        if (user == null || user.getId() == null) {
            return;
        }

        Optional<UserActivity> existingActivity = userActivityRepository.findByUserId(user.getId());
        UserActivity activity;

        if (existingActivity.isPresent()) {
            activity = existingActivity.get();
            activity.setLastActivity(LocalDateTime.now());
            activity.setActivityType(activityType);
            activity.setPageUrl(pageUrl);
            if (sessionId != null) {
                activity.setSessionId(sessionId);
            }
        } else {
            activity = new UserActivity(user.getId(), LocalDateTime.now(), activityType, pageUrl, sessionId);
        }

        userActivityRepository.save(activity);
        logger.debug("Updated activity for user {} - Type: {}, Page: {}, Session: {}",
            user.getName(), activityType, pageUrl, sessionId);
    }

    /**
     * Update user activity timestamp (without session ID)
     */
    @Transactional
    public void updateActivity(User user, String activityType, String pageUrl) {
        updateActivity(user, activityType, pageUrl, null);
    }

    /**
     * Update user activity with just the user
     */
    @Transactional
    public void updateActivity(User user) {
        updateActivity(user, "INTERACTION", null, null);
    }

    /**
     * Check if user is already active with a different session
     * @param userId the user ID to check
     * @param currentSessionId the session ID of the user trying to connect
     * @return true if the user is active with a different session (connection should be denied)
     */
    public boolean isUserActiveWithDifferentSession(Long userId, String currentSessionId) {
        if (userId == null) {
            return false;
        }

        Optional<UserActivity> activity = userActivityRepository.findByUserId(userId);
        if (activity.isEmpty()) {
            // No activity record = user can connect
            return false;
        }

        boolean isActiveWithDifferent = activity.get().isActiveWithDifferentSession(currentSessionId, INACTIVITY_THRESHOLD_SECONDS);
        if (isActiveWithDifferent) {
            logger.warn("User {} is already active with a different session. Last activity: {}, Session: {}",
                userId, activity.get().getLastActivity(), activity.get().getSessionId());
        }
        return isActiveWithDifferent;
    }

    /**
     * Get user activity
     */
    public Optional<UserActivity> getUserActivity(Long userId) {
        return userActivityRepository.findByUserId(userId);
    }

    /**
     * Check if user is inactive (no activity for more than specified seconds)
     */
    public boolean isUserInactive(Long userId, int inactiveSeconds) {
        Optional<UserActivity> activity = userActivityRepository.findByUserId(userId);
        if (activity.isEmpty()) {
            // No activity record = inactive
            return true;
        }
        return activity.get().isInactive(inactiveSeconds);
    }

    /**
     * Get all inactive users (no activity for more than specified seconds)
     */
    public List<Long> getInactiveUserIds(int inactiveSeconds) {
        LocalDateTime cutoffTime = LocalDateTime.now().minusSeconds(inactiveSeconds);
        return userActivityRepository.findInactiveUsers(cutoffTime)
            .stream()
            .map(UserActivity::getUserId)
            .collect(Collectors.toList());
    }

    /**
     * Get all active users (activity within specified seconds)
     */
    public List<Long> getActiveUserIds(int activeSeconds) {
        LocalDateTime cutoffTime = LocalDateTime.now().minusSeconds(activeSeconds);
        return userActivityRepository.findActiveUsers(cutoffTime)
            .stream()
            .map(UserActivity::getUserId)
            .collect(Collectors.toList());
    }

    /**
     * Remove user activity (e.g., on logout)
     */
    @Transactional
    public void removeUserActivity(Long userId) {
        userActivityRepository.deleteById(userId);
        logger.info("Removed activity tracking for user {}", userId);
    }

    /**
     * Cleanup old activity records (older than specified hours)
     */
    @Transactional
    public void cleanupOldActivities(int hoursOld) {
        LocalDateTime cutoffTime = LocalDateTime.now().minusHours(hoursOld);
        userActivityRepository.deleteByLastActivityBefore(cutoffTime);
        logger.info("Cleaned up activity records older than {} hours", hoursOld);
    }

    /**
     * Reset all user activities at application startup
     * This clears all session IDs and activity records to ensure clean state
     */
    @Transactional
    public void resetAllUserActivities() {
        userActivityRepository.deleteAll();
        logger.info("Reset all user activities at application startup");
    }
}

