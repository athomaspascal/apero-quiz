package com.quizz.core.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

/**
 * Configuration class for inactivity monitoring settings
 */
@Component
public class InactivityConfig {

    @Value("${app.inactivity.threshold-seconds:180}")
    private int thresholdSeconds;

    @Value("${app.inactivity.check-interval-seconds:10}")
    private int checkIntervalSeconds;

    @Value("${app.inactivity.countdown-seconds:10}")
    private int countdownSeconds;

    public int getThresholdSeconds() {
        return thresholdSeconds;
    }

    public int getCheckIntervalSeconds() {
        return checkIntervalSeconds;
    }

    public int getCountdownSeconds() {
        return countdownSeconds;
    }
}

