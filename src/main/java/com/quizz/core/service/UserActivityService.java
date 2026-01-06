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

    /**
     * Update user activity timestamp
     */
    @Transactional
    public void updateActivity(User user, String activityType, String pageUrl) {
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
        } else {
            activity = new UserActivity(user.getId(), LocalDateTime.now(), activityType, pageUrl);
        }

        userActivityRepository.save(activity);
        logger.debug("Updated activity for user {} - Type: {}, Page: {}", user.getName(), activityType, pageUrl);
    }

    /**
     * Update user activity with just the user
     */
    @Transactional
    public void updateActivity(User user) {
        updateActivity(user, "INTERACTION", null);
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
}

