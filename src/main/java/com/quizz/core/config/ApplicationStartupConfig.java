package com.quizz.core.config;

import com.quizz.core.service.UserActivityService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.context.event.ApplicationReadyEvent;
import org.springframework.context.event.EventListener;
import org.springframework.stereotype.Component;

/**
 * Configuration class that runs initialization tasks at application startup
 */
@Component
public class ApplicationStartupConfig {

    private static final Logger logger = LoggerFactory.getLogger(ApplicationStartupConfig.class);

    private final UserActivityService userActivityService;

    public ApplicationStartupConfig(UserActivityService userActivityService) {
        this.userActivityService = userActivityService;
    }

    /**
     * Reset all user activities when the application starts
     * This ensures a clean state and prevents stale session data from blocking logins
     */
    @EventListener(ApplicationReadyEvent.class)
    public void onApplicationReady() {
        logger.info("Application started - resetting all user activities");
        userActivityService.resetAllUserActivities();
        logger.info("User activities reset completed");
    }
}

