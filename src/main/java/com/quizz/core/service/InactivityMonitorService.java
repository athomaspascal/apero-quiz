package com.quizz.core.service;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

/**
 * Scheduled service to monitor user activity and cancel inactive duels
 */
@Service
public class InactivityMonitorService {

    private static final Logger logger = LoggerFactory.getLogger(InactivityMonitorService.class);
    private static final int INACTIVITY_THRESHOLD_SECONDS = 60; // 60 seconds of inactivity

    private final DuelService duelService;
    private final UserActivityService userActivityService;

    public InactivityMonitorService(DuelService duelService, UserActivityService userActivityService) {
        this.duelService = duelService;
        this.userActivityService = userActivityService;
    }

    /**
     * Check for inactive users and cancel their duels every 30 seconds
     */
    @Scheduled(fixedDelay = 30000, initialDelay = 30000) // Every 30 seconds
    public void monitorInactiveUsers() {
        logger.debug("Monitoring user activity for inactive duel participants");

        try {
            // Cancel duels for users who have been inactive for more than 60 seconds
            int cancelledDuels = duelService.cancelDuelsForInactiveUsers(INACTIVITY_THRESHOLD_SECONDS);

            if (cancelledDuels > 0) {
                logger.info("Inactivity monitor: Cancelled {} duel(s) due to user inactivity", cancelledDuels);
            }
        } catch (Exception e) {
            logger.error("Error while monitoring inactive users", e);
        }
    }

    /**
     * Cleanup old activity records every hour
     */
    @Scheduled(fixedDelay = 3600000, initialDelay = 3600000) // Every hour
    public void cleanupOldActivities() {
        logger.debug("Cleaning up old activity records");

        try {
            // Remove activity records older than 24 hours
            userActivityService.cleanupOldActivities(24);
            logger.info("Cleanup completed for activity records older than 24 hours");
        } catch (Exception e) {
            logger.error("Error while cleaning up old activities", e);
        }
    }
}

