package com.quizz.core.migration;

import com.quizz.core.entity.User;
import com.quizz.core.repository.UserRepository;
import com.quizz.core.service.CountryService;
import com.quizz.core.service.UserService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.CommandLineRunner;
import org.springframework.core.annotation.Order;
import org.springframework.stereotype.Component;

import java.util.List;

/**
 * Migration to link existing users to their countries
 * OPTIMIZATION: This migration is now disabled as all users are persisted with their countries in the database
 */
@Component
@Order(100) // Run after other initializers
public class UserCountryMigration implements CommandLineRunner {

    private static final Logger logger = LoggerFactory.getLogger(UserCountryMigration.class);

    private final UserService userService;
    private final UserRepository userRepository;
    private final CountryService countryService;

    public UserCountryMigration(UserService userService, UserRepository userRepository, CountryService countryService) {
        this.userService = userService;
        this.userRepository = userRepository;
        this.countryService = countryService;
    }

    @Override
    public void run(String... args) throws Exception {
        logger.info("=== UserCountryMigration: SKIPPED (optimization - data persisted in database) ===");
        // Migration disabled - all users are already linked to their countries in the database
        /*
        logger.info("=== UserCountryMigration: Starting ===");

        // Get all users
        List<User> users = userRepository.findAll();
        logger.info("Found {} users to check", users.size());

        int updatedCount = 0;

        for (User user : users) {
            if (user.getCountry() == null) {
                logger.info("User '{}' has no country, attempting to link...", user.getName());

                // Link admin to France
                if (user.getEmail().equals("administrateur@quiz.admin")) {
                    countryService.findBySigle("FRA").ifPresent(country -> {
                        user.setCountry(country);
                        userService.save(user);
                        logger.info("Linked admin user to France");
                    });
                    updatedCount++;
                }
                // Link famous users based on their known nationality
                else if (user.getName().equals("Albert Einstein")) {
                    countryService.findBySigle("DEU").ifPresent(country -> {
                        user.setCountry(country);
                        userService.save(user);
                        logger.info("Linked {} to Germany", user.getName());
                    });
                    updatedCount++;
                }
                else if (user.getName().equals("Marie Curie")) {
                    countryService.findBySigle("POL").ifPresent(country -> {
                        user.setCountry(country);
                        userService.save(user);
                        logger.info("Linked {} to Poland", user.getName());
                    });
                    updatedCount++;
                }
                else if (user.getName().equals("Leonardo da Vinci")) {
                    countryService.findBySigle("ITA").ifPresent(country -> {
                        user.setCountry(country);
                        userService.save(user);
                        logger.info("Linked {} to Italy", user.getName());
                    });
                    updatedCount++;
                }
                else if (user.getName().equals("William Shakespeare")) {
                    countryService.findBySigle("GBR").ifPresent(country -> {
                        user.setCountry(country);
                        userService.save(user);
                        logger.info("Linked {} to United Kingdom", user.getName());
                    });
                    updatedCount++;
                }
                else if (user.getName().equals("Pablo Picasso")) {
                    countryService.findBySigle("ESP").ifPresent(country -> {
                        user.setCountry(country);
                        userService.save(user);
                        logger.info("Linked {} to Spain", user.getName());
                    });
                    updatedCount++;
                }
                else if (user.getName().equals("Mahatma Gandhi")) {
                    countryService.findBySigle("IND").ifPresent(country -> {
                        user.setCountry(country);
                        userService.save(user);
                        logger.info("Linked {} to India", user.getName());
                    });
                    updatedCount++;
                }
                else if (user.getName().equals("Nelson Mandela")) {
                    countryService.findBySigle("ZAF").ifPresent(country -> {
                        user.setCountry(country);
                        userService.save(user);
                        logger.info("Linked {} to South Africa", user.getName());
                    });
                    updatedCount++;
                }
                else if (user.getName().equals("Barack Obama")) {
                    countryService.findBySigle("USA").ifPresent(country -> {
                        user.setCountry(country);
                        userService.save(user);
                        logger.info("Linked {} to United States", user.getName());
                    });
                    updatedCount++;
                }
                else if (user.getName().equals("Napoleon Bonaparte")) {
                    countryService.findBySigle("FRA").ifPresent(country -> {
                        user.setCountry(country);
                        userService.save(user);
                        logger.info("Linked {} to France", user.getName());
                    });
                    updatedCount++;
                }
                else if (user.getName().equals("Wolfgang Amadeus Mozart")) {
                    countryService.findBySigle("AUT").ifPresent(country -> {
                        user.setCountry(country);
                        userService.save(user);
                        logger.info("Linked {} to Austria", user.getName());
                    });
                    updatedCount++;
                }
                else if (user.getName().equals("Cleopatra")) {
                    countryService.findBySigle("EGY").ifPresent(country -> {
                        user.setCountry(country);
                        userService.save(user);
                        logger.info("Linked {} to Egypt", user.getName());
                    });
                    updatedCount++;
                }
                else if (user.getName().equals("Confucius")) {
                    countryService.findBySigle("CHN").ifPresent(country -> {
                        user.setCountry(country);
                        userService.save(user);
                        logger.info("Linked {} to China", user.getName());
                    });
                    updatedCount++;
                }
                else if (user.getName().equals("Julius Caesar")) {
                    countryService.findBySigle("ITA").ifPresent(country -> {
                        user.setCountry(country);
                        userService.save(user);
                        logger.info("Linked {} to Italy", user.getName());
                    });
                    updatedCount++;
                }
                else if (user.getName().equals("Queen Elizabeth I")) {
                    countryService.findBySigle("GBR").ifPresent(country -> {
                        user.setCountry(country);
                        userService.save(user);
                        logger.info("Linked {} to United Kingdom", user.getName());
                    });
                    updatedCount++;
                }
                else if (user.getName().equals("Frida Kahlo")) {
                    countryService.findBySigle("MEX").ifPresent(country -> {
                        user.setCountry(country);
                        userService.save(user);
                        logger.info("Linked {} to Mexico", user.getName());
                    });
                    updatedCount++;
                }
                else {
                    logger.warn("No country mapping found for user: {}", user.getName());
                }
            } else {
                logger.debug("User '{}' already linked to {}", user.getName(), user.getCountry().getCountryName());
            }
        }

        logger.info("=== UserCountryMigration: Completed. Updated {} users ===", updatedCount);
        */
    }
}

