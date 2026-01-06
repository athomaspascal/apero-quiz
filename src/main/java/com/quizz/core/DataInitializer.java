package com.quizz.core;

import com.quizz.core.entity.Gender;
import com.quizz.core.entity.User;
import com.quizz.core.service.CountryService;
import com.quizz.core.service.UserService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.DependsOn;
import org.springframework.core.annotation.Order;

import javax.imageio.ImageIO;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.ByteArrayOutputStream;
import java.io.IOException;

@Configuration
public class DataInitializer {

    private static final Logger logger = LoggerFactory.getLogger(DataInitializer.class);

    // OPTIMIZATION: Users (admin and public avatars) are now persisted in the database
    // No need to re-initialize on every startup
    /*
    @Bean
    @Order(2) // Execute after CountryService
    @DependsOn("countryService") // Wait for CountryService to be initialized
    CommandLineRunner initDatabase(UserService userService, CountryService countryService) {
        return args -> {
            logger.info("=== DataInitializer: Starting user and country initialization ===");
            createAdminUser(userService, countryService);
            createPublicUsers(userService, countryService);
            logger.info("=== DataInitializer: Completed ===");
        };
    }
    */

    private void createAdminUser(UserService userService, CountryService countryService) {
        String adminEmail = "administrateur@quiz.admin";

        // Check if admin user already exists
        if (userService.findByEmail(adminEmail).isPresent()) {
            logger.info("Admin user already exists, checking country association...");
            User existingAdmin = userService.findByEmail(adminEmail).get();

            // If admin doesn't have a country, link to France
            if (existingAdmin.getCountry() == null) {
                countryService.findBySigle("FRA").ifPresent(country -> {
                    existingAdmin.setCountry(country);
                    userService.save(existingAdmin);
                    logger.info("Existing admin user linked to France");
                });
            } else {
                logger.info("Admin user already linked to country: {}", existingAdmin.getCountry().getCountryName());
            }
            return;
        }

        try {
            // Create admin user with a male avatar
            Color adminColor = new Color(220, 38, 38); // Red color for admin
            User admin = userService.createUser(
                "Administrateur",
                adminEmail,
                "+33 0 00 00 00 00",
                "quizz2025!!", // Admin password
                Gender.MALE,
                generateAvatarImage("AD", adminColor)
            );

            // Mark as admin FIRST
            userService.updateAdminFlag(admin.getId(), true);

            // Reload admin to get updated isAdmin flag
            User updatedAdmin = userService.getById(admin.getId());

            // Then link admin to France (after admin flag is set)
            if (updatedAdmin != null) {
                countryService.findBySigle("FRA").ifPresent(country -> {
                    updatedAdmin.setCountry(country);
                    userService.save(updatedAdmin); // Save the admin user with the country association
                    logger.info("Admin user linked to France");
                });
            }

            logger.info("Default admin user created: {} / quizz2025!! (linked to France)", adminEmail);
        } catch (Exception e) {
            logger.error("Error creating admin user: {}", e.getMessage(), e);
        }
    }

    private void createPublicUsers(UserService userService, CountryService countryService) {
        String[][] famousPeople = {
            // Format: {Name, Initials, Gender, CountryCode}
            {"Barack Obama", "BO", "MALE", "USA"},
            {"Nelson Mandela", "NM", "MALE", "ZAF"},
            {"Marie Curie", "MC", "FEMALE", "POL"},
            {"Albert Einstein", "AE", "MALE", "DEU"},
            {"Leonardo da Vinci", "LV", "MALE", "ITA"},
            {"Cleopatra", "CL", "FEMALE", "EGY"},
            {"Martin Luther King Jr", "MK", "MALE", "USA"},
            {"Mother Teresa", "MT", "FEMALE", "IND"},
            {"Mahatma Gandhi", "MG", "MALE", "IND"},
            {"Winston Churchill", "WC", "MALE", "GBR"},
            {"Abraham Lincoln", "AL", "MALE", "USA"},
            {"Charles Darwin", "CD", "MALE", "GBR"},
            {"Isaac Newton", "IN", "MALE", "GBR"},
            {"William Shakespeare", "WS", "MALE", "GBR"},
            {"Ludwig van Beethoven", "LB", "MALE", "DEU"},
            {"Wolfgang Mozart", "WM", "MALE", "AUT"},
            {"Pablo Picasso", "PP", "MALE", "ESP"},
            {"Vincent van Gogh", "VG", "MALE", "NLD"},
            {"Frida Kahlo", "FK", "FEMALE", "MEX"},
            {"Coco Chanel", "CC", "FEMALE", "FRA"},
            {"Steve Jobs", "SJ", "MALE", "USA"},
            {"Bill Gates", "BG", "MALE", "USA"},
            {"Elon Musk", "EM", "MALE", "ZAF"},
            {"Mark Zuckerberg", "MZ", "MALE", "USA"},
            {"Oprah Winfrey", "OW", "FEMALE", "USA"},
            {"Walt Disney", "WD", "MALE", "USA"},
            {"Michael Jackson", "MJ", "MALE", "USA"},
            {"Elvis Presley", "EP", "MALE", "USA"},
            {"The Beatles", "TB", "MALE", "GBR"},
            {"Madonna", "MA", "FEMALE", "USA"},
            {"Beyoncé", "BE", "FEMALE", "USA"},
            {"Muhammad Ali", "MA", "MALE", "USA"},
            {"Pelé", "PE", "MALE", "BRA"},
            {"Cristiano Ronaldo", "CR", "MALE", "PRT"},
            {"Lionel Messi", "LM", "MALE", "ARG"},
            {"Serena Williams", "SW", "FEMALE", "USA"},
            {"Michael Jordan", "MJ", "MALE", "USA"},
            {"Tiger Woods", "TW", "MALE", "USA"},
            {"Roger Federer", "RF", "MALE", "CHE"},
            {"Usain Bolt", "UB", "MALE", "JAM"},
            {"Neil Armstrong", "NA", "MALE", "USA"},
            {"Yuri Gagarin", "YG", "MALE", "RUS"},
            {"Stephen Hawking", "SH", "MALE", "GBR"},
            {"Carl Sagan", "CS", "MALE", "USA"},
            {"Jane Goodall", "JG", "FEMALE", "GBR"},
            {"Rosa Parks", "RP", "FEMALE", "USA"},
            {"Malala Yousafzai", "MY", "FEMALE", "PAK"},
            {"Anne Frank", "AF", "FEMALE", "DEU"},
            {"Helen Keller", "HK", "FEMALE", "USA"},
            {"Florence Nightingale", "FN", "FEMALE", "GBR"},
            {"Sigmund Freud", "SF", "MALE", "AUT"},
            {"Karl Marx", "KM", "MALE", "DEU"},
            {"Friedrich Nietzsche", "FN", "MALE", "DEU"},
            {"Socrates", "SO", "MALE", "GRC"},
            {"Plato", "PL", "MALE", "GRC"},
            {"Aristotle", "AR", "MALE", "GRC"},
            {"Confucius", "CO", "MALE", "CHN"},
            {"Buddha", "BU", "MALE", "IND"},
            {"Jesus Christ", "JC", "MALE", "ISR"},
            {"Prophet Muhammad", "PM", "MALE", "SAU"},
            {"Pope Francis", "PF", "MALE", "ARG"},
            {"Dalai Lama", "DL", "MALE", "IND"},
            {"Elizabeth II", "E2", "FEMALE", "GBR"},
            {"Napoleon Bonaparte", "NB", "MALE", "FRA"},
            {"Julius Caesar", "JC", "MALE", "ITA"},
            {"Alexander the Great", "AG", "MALE", "GRC"},
            {"Genghis Khan", "GK", "MALE", "MNG"},
            {"Joan of Arc", "JA", "FEMALE", "FRA"},
            {"George Washington", "GW", "MALE", "USA"},
            {"Thomas Jefferson", "TJ", "MALE", "USA"},
            {"Franklin D Roosevelt", "FR", "MALE", "USA"},
            {"John F Kennedy", "JK", "MALE", "USA"},
            {"Margaret Thatcher", "MT", "FEMALE", "GBR"},
            {"Angela Merkel", "AM", "FEMALE", "DEU"},
            {"Indira Gandhi", "IG", "FEMALE", "IND"},
            {"Eva Perón", "EP", "FEMALE", "ARG"},
            {"Che Guevara", "CG", "MALE", "ARG"},
            {"Vladimir Lenin", "VL", "MALE", "RUS"},
            {"Joseph Stalin", "JS", "MALE", "RUS"},
            {"Mao Zedong", "MZ", "MALE", "CHN"},
            {"Charles de Gaulle", "CG", "MALE", "FRA"},
            {"Simone de Beauvoir", "SB", "FEMALE", "FRA"},
            {"Virginia Woolf", "VW", "FEMALE", "GBR"},
            {"Jane Austen", "JA", "FEMALE", "GBR"},
            {"Mark Twain", "MT", "MALE", "USA"},
            {"Ernest Hemingway", "EH", "MALE", "USA"},
            {"Victor Hugo", "VH", "MALE", "FRA"},
            {"Voltaire", "VO", "MALE", "FRA"},
            {"Molière", "MO", "MALE", "FRA"},
            {"Dante Alighieri", "DA", "MALE", "ITA"},
            {"Miguel de Cervantes", "MC", "MALE", "ESP"},
            {"Leo Tolstoy", "LT", "MALE", "RUS"},
            {"Fyodor Dostoevsky", "FD", "MALE", "RUS"},
            {"Gabriel García Márquez", "GM", "MALE", "COL"},
            {"Toni Morrison", "TM", "FEMALE", "USA"},
            {"Maya Angelou", "MA", "FEMALE", "USA"},
            {"J.K. Rowling", "JR", "FEMALE", "GBR"},
            {"George Orwell", "GO", "MALE", "GBR"},
            {"Agatha Christie", "AC", "FEMALE", "GBR"}
        };

        Color[] avatarColors = {
            new Color(102, 126, 234), new Color(234, 102, 150), new Color(52, 168, 83),
            new Color(251, 191, 36), new Color(245, 158, 11), new Color(239, 68, 68),
            new Color(139, 92, 246), new Color(236, 72, 153), new Color(14, 165, 233),
            new Color(34, 197, 94), new Color(168, 85, 247), new Color(249, 115, 22),
            new Color(59, 130, 246), new Color(236, 114, 114), new Color(74, 222, 128),
            new Color(251, 146, 60), new Color(190, 24, 93), new Color(79, 70, 229),
            new Color(21, 128, 61), new Color(124, 58, 237)
        };

        int successCount = 0;
        int skipCount = 0;

        for (int i = 0; i < famousPeople.length; i++) {
            String[] person = famousPeople[i];
            String name = person[0];
            String initials = person[1];
            Gender gender = person[2].equals("MALE") ? Gender.MALE : Gender.FEMALE;
            String countryCode = person[3];

            // Create email from name
            String email = name.toLowerCase().replace(" ", ".").replaceAll("[^a-z.]", "") + "@public.quiz";

            // Select color
            Color color = avatarColors[i % avatarColors.length];

            try {
                User user = userService.createUser(
                    name,
                    email,
                    "+1 000 000 0000",
                    "public123", // Default password for public users
                    gender,
                    generateAvatarImage(initials, color)
                );

                // Mark as public user FIRST
                userService.updatePublicFlag(user.getId(), true);
                logger.info("Set isPublic=true for user: {}", name);

                // Then link user to their country (after public flag is set)
                boolean countryLinked = false;
                var countryOpt = countryService.findBySigle(countryCode);
                if (countryOpt.isPresent()) {
                    // Reload user to ensure we have the latest state with isPublic=true
                    User updatedUser = userService.getById(user.getId());
                    if (updatedUser != null) {
                        updatedUser.setCountry(countryOpt.get());
                        userService.save(updatedUser); // Save the user with the country association
                        logger.info("Linked {} to {} ({}), isPublic={}", name, countryOpt.get().getCountryName(), countryCode, updatedUser.isPublic());
                        countryLinked = true;
                    }
                } else {
                    logger.warn("Country with code {} not found for user {}", countryCode, name);
                }

                successCount++;

                if ((i + 1) % 20 == 0) {
                    logger.info("Created {} public users...", (i + 1));
                }
            } catch (IllegalArgumentException e) {
                skipCount++;
            }
        }

        logger.info("Public users initialization complete: {} created, {} skipped (already exist)", successCount, skipCount);

        // Verify how many public users are in the database
        long publicUserCount = userService.countPublicUsers();
        logger.info("Total public users in database after initialization: {}", publicUserCount);
    }

    /**
     * Generate a simple avatar image with initials
     * @param initials The initials to display
     * @param bgColor The background color
     * @return byte array of the PNG image
     */
    private byte[] generateAvatarImage(String initials, Color bgColor) {
        try {
            int size = 200;
            BufferedImage image = new BufferedImage(size, size, BufferedImage.TYPE_INT_RGB);
            Graphics2D g2d = image.createGraphics();

            // Enable anti-aliasing
            g2d.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
            g2d.setRenderingHint(RenderingHints.KEY_TEXT_ANTIALIASING, RenderingHints.VALUE_TEXT_ANTIALIAS_ON);

            // Draw background
            g2d.setColor(bgColor);
            g2d.fillRect(0, 0, size, size);

            // Draw initials
            g2d.setColor(Color.WHITE);
            g2d.setFont(new Font("Arial", Font.BOLD, 80));
            FontMetrics fm = g2d.getFontMetrics();
            int x = (size - fm.stringWidth(initials)) / 2;
            int y = ((size - fm.getHeight()) / 2) + fm.getAscent();
            g2d.drawString(initials, x, y);

            g2d.dispose();

            // Convert to byte array
            ByteArrayOutputStream baos = new ByteArrayOutputStream();
            ImageIO.write(image, "png", baos);
            return baos.toByteArray();
        } catch (IOException e) {
            logger.error("Error generating avatar image: {}", e.getMessage(), e);
            return null;
        }
    }
}
