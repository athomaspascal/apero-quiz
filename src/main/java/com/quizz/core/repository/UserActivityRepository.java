package com.quizz.core.repository;

import com.quizz.core.entity.UserActivity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Repository
public interface UserActivityRepository extends JpaRepository<UserActivity, Long> {

    /**
     * Find user activity by user ID
     */
    Optional<UserActivity> findByUserId(Long userId);

    /**
     * Find all inactive users (no activity after cutoff time)
     */
    @Query("SELECT ua FROM UserActivity ua WHERE ua.lastActivity < :cutoffTime")
    List<UserActivity> findInactiveUsers(@Param("cutoffTime") LocalDateTime cutoffTime);

    /**
     * Find all active users (activity after cutoff time)
     */
    @Query("SELECT ua FROM UserActivity ua WHERE ua.lastActivity >= :cutoffTime")
    List<UserActivity> findActiveUsers(@Param("cutoffTime") LocalDateTime cutoffTime);

    /**
     * Delete old activity records (cleanup)
     */
    void deleteByLastActivityBefore(LocalDateTime cutoffTime);
}

