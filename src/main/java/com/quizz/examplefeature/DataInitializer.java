package com.quizz.examplefeature;

import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class DataInitializer {

    @Bean
    CommandLineRunner initDatabase(UserService userService) {
        return args -> {
            // Create a test user if no users exist
            try {
                userService.createUser(
                    "Test User",
                    "test@example.com",
                    "+33 6 12 34 56 78",
                    "password123"
                );
                System.out.println("Test user created: test@example.com / password123");
            } catch (IllegalArgumentException e) {
                // User already exists, skip
                System.out.println("Test user already exists");
            }
        };
    }
}

