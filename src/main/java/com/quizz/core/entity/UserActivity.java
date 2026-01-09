package com.quizz.core.entity;

import jakarta.persistence.*;
import java.time.LocalDateTime;

/**
 * Entity to track real-time user activity for detecting inactive users
 */
@Entity
@Table(name = "user_activity")
public class UserActivity {

    @Id
    @Column(name = "user_id")
    private Long userId;

    @Column(name = "last_activity", nullable = false)
    private LocalDateTime lastActivity;

    @Column(name = "activity_type", length = 50)
    private String activityType;

    @Column(name = "page_url", length = 500)
    private String pageUrl;

    @Column(name = "session_id", length = 100)
    private String sessionId;

    public UserActivity() {
    }

    public UserActivity(Long userId, LocalDateTime lastActivity) {
        this.userId = userId;
        this.lastActivity = lastActivity;
    }

    public UserActivity(Long userId, LocalDateTime lastActivity, String activityType, String pageUrl) {
        this.userId = userId;
        this.lastActivity = lastActivity;
        this.activityType = activityType;
        this.pageUrl = pageUrl;
    }

    public UserActivity(Long userId, LocalDateTime lastActivity, String activityType, String pageUrl, String sessionId) {
        this.userId = userId;
        this.lastActivity = lastActivity;
        this.activityType = activityType;
        this.pageUrl = pageUrl;
        this.sessionId = sessionId;
    }

    public Long getUserId() {
        return userId;
    }

    public void setUserId(Long userId) {
        this.userId = userId;
    }

    public LocalDateTime getLastActivity() {
        return lastActivity;
    }

    public void setLastActivity(LocalDateTime lastActivity) {
        this.lastActivity = lastActivity;
    }

    public String getActivityType() {
        return activityType;
    }

    public void setActivityType(String activityType) {
        this.activityType = activityType;
    }

    public String getPageUrl() {
        return pageUrl;
    }

    public void setPageUrl(String pageUrl) {
        this.pageUrl = pageUrl;
    }

    public String getSessionId() {
        return sessionId;
    }

    public void setSessionId(String sessionId) {
        this.sessionId = sessionId;
    }

    /**
     * Check if the user is inactive (no activity for more than specified seconds)
     */
    public boolean isInactive(int seconds) {
        return lastActivity.plusSeconds(seconds).isBefore(LocalDateTime.now());
    }

    /**
     * Check if the user is active with a different session
     * @param currentSessionId the session ID of the user trying to connect
     * @param inactivityThresholdSeconds the number of seconds after which a user is considered inactive
     * @return true if the user is active with a different session
     */
    public boolean isActiveWithDifferentSession(String currentSessionId, int inactivityThresholdSeconds) {
        // If same session, allow connection
        if (currentSessionId != null && currentSessionId.equals(this.sessionId)) {
            return false;
        }
        // If activity is older than threshold, user is inactive
        if (isInactive(inactivityThresholdSeconds)) {
            return false;
        }
        // User is active with a different session
        return true;
    }
}

