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

    /**
     * Check if the user is inactive (no activity for more than specified seconds)
     */
    public boolean isInactive(int seconds) {
        return lastActivity.plusSeconds(seconds).isBefore(LocalDateTime.now());
    }
}

