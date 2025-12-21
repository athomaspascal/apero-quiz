package com.quizz.core;

import com.quizz.core.entity.Gender;
import com.quizz.core.entity.User;
import com.quizz.core.service.UserService;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import javax.imageio.ImageIO;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.ByteArrayOutputStream;
import java.io.IOException;

@Configuration
public class DataInitializer {

    @Bean
    CommandLineRunner initDatabase(UserService userService) {
        return args -> {
            createAdminUser(userService);
            createPublicUsers(userService);
        };
    }

    private void createAdminUser(UserService userService) {
        String adminEmail = "administrateur@quiz.admin";

        // Check if admin user already exists
        if (userService.findByEmail(adminEmail).isPresent()) {
            System.out.println("Admin user already exists, skipping creation.");
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

            // Mark as admin
            userService.updateAdminFlag(admin.getId(), true);
            System.out.println("✅ Default admin user created: " + adminEmail + " / quizz2025!!");
        } catch (Exception e) {
            System.err.println("❌ Error creating admin user: " + e.getMessage());
        }
    }

    private void createPublicUsers(UserService userService) {
        String[][] famousPeople = {
            // Format: {Name, Initials, Gender}
            {"Barack Obama", "BO", "MALE"},
            {"Nelson Mandela", "NM", "MALE"},
            {"Marie Curie", "MC", "FEMALE"},
            {"Albert Einstein", "AE", "MALE"},
            {"Leonardo da Vinci", "LV", "MALE"},
            {"Cleopatra", "CL", "FEMALE"},
            {"Martin Luther King Jr", "MK", "MALE"},
            {"Mother Teresa", "MT", "FEMALE"},
            {"Mahatma Gandhi", "MG", "MALE"},
            {"Winston Churchill", "WC", "MALE"},
            {"Abraham Lincoln", "AL", "MALE"},
            {"Charles Darwin", "CD", "MALE"},
            {"Isaac Newton", "IN", "MALE"},
            {"William Shakespeare", "WS", "MALE"},
            {"Ludwig van Beethoven", "LB", "MALE"},
            {"Wolfgang Mozart", "WM", "MALE"},
            {"Pablo Picasso", "PP", "MALE"},
            {"Vincent van Gogh", "VG", "MALE"},
            {"Frida Kahlo", "FK", "FEMALE"},
            {"Coco Chanel", "CC", "FEMALE"},
            {"Steve Jobs", "SJ", "MALE"},
            {"Bill Gates", "BG", "MALE"},
            {"Elon Musk", "EM", "MALE"},
            {"Mark Zuckerberg", "MZ", "MALE"},
            {"Oprah Winfrey", "OW", "FEMALE"},
            {"Walt Disney", "WD", "MALE"},
            {"Michael Jackson", "MJ", "MALE"},
            {"Elvis Presley", "EP", "MALE"},
            {"The Beatles", "TB", "MALE"},
            {"Madonna", "MA", "FEMALE"},
            {"Beyoncé", "BE", "FEMALE"},
            {"Muhammad Ali", "MA", "MALE"},
            {"Pelé", "PE", "MALE"},
            {"Cristiano Ronaldo", "CR", "MALE"},
            {"Lionel Messi", "LM", "MALE"},
            {"Serena Williams", "SW", "FEMALE"},
            {"Michael Jordan", "MJ", "MALE"},
            {"Tiger Woods", "TW", "MALE"},
            {"Roger Federer", "RF", "MALE"},
            {"Usain Bolt", "UB", "MALE"},
            {"Neil Armstrong", "NA", "MALE"},
            {"Yuri Gagarin", "YG", "MALE"},
            {"Stephen Hawking", "SH", "MALE"},
            {"Carl Sagan", "CS", "MALE"},
            {"Jane Goodall", "JG", "FEMALE"},
            {"Rosa Parks", "RP", "FEMALE"},
            {"Malala Yousafzai", "MY", "FEMALE"},
            {"Anne Frank", "AF", "FEMALE"},
            {"Helen Keller", "HK", "FEMALE"},
            {"Florence Nightingale", "FN", "FEMALE"},
            {"Sigmund Freud", "SF", "MALE"},
            {"Karl Marx", "KM", "MALE"},
            {"Friedrich Nietzsche", "FN", "MALE"},
            {"Socrates", "SO", "MALE"},
            {"Plato", "PL", "MALE"},
            {"Aristotle", "AR", "MALE"},
            {"Confucius", "CO", "MALE"},
            {"Buddha", "BU", "MALE"},
            {"Jesus Christ", "JC", "MALE"},
            {"Prophet Muhammad", "PM", "MALE"},
            {"Pope Francis", "PF", "MALE"},
            {"Dalai Lama", "DL", "MALE"},
            {"Elizabeth II", "E2", "FEMALE"},
            {"Napoleon Bonaparte", "NB", "MALE"},
            {"Julius Caesar", "JC", "MALE"},
            {"Alexander the Great", "AG", "MALE"},
            {"Genghis Khan", "GK", "MALE"},
            {"Joan of Arc", "JA", "FEMALE"},
            {"George Washington", "GW", "MALE"},
            {"Thomas Jefferson", "TJ", "MALE"},
            {"Franklin D Roosevelt", "FR", "MALE"},
            {"John F Kennedy", "JK", "MALE"},
            {"Margaret Thatcher", "MT", "FEMALE"},
            {"Angela Merkel", "AM", "FEMALE"},
            {"Indira Gandhi", "IG", "FEMALE"},
            {"Eva Perón", "EP", "FEMALE"},
            {"Che Guevara", "CG", "MALE"},
            {"Vladimir Lenin", "VL", "MALE"},
            {"Joseph Stalin", "JS", "MALE"},
            {"Mao Zedong", "MZ", "MALE"},
            {"Charles de Gaulle", "CG", "MALE"},
            {"Simone de Beauvoir", "SB", "FEMALE"},
            {"Virginia Woolf", "VW", "FEMALE"},
            {"Jane Austen", "JA", "FEMALE"},
            {"Mark Twain", "MT", "MALE"},
            {"Ernest Hemingway", "EH", "MALE"},
            {"Victor Hugo", "VH", "MALE"},
            {"Voltaire", "VO", "MALE"},
            {"Molière", "MO", "MALE"},
            {"Dante Alighieri", "DA", "MALE"},
            {"Miguel de Cervantes", "MC", "MALE"},
            {"Leo Tolstoy", "LT", "MALE"},
            {"Fyodor Dostoevsky", "FD", "MALE"},
            {"Gabriel García Márquez", "GM", "MALE"},
            {"Toni Morrison", "TM", "FEMALE"},
            {"Maya Angelou", "MA", "FEMALE"},
            {"J.K. Rowling", "JR", "FEMALE"},
            {"George Orwell", "GO", "MALE"},
            {"Agatha Christie", "AC", "FEMALE"}
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
                // Mark as public user and save again
                userService.updatePublicFlag(user.getId(), true);
                successCount++;

                if ((i + 1) % 20 == 0) {
                    System.out.println("Created " + (i + 1) + " public users...");
                }
            } catch (IllegalArgumentException e) {
                skipCount++;
            }
        }

        System.out.println("Public users initialization complete: " + successCount + " created, " + skipCount + " skipped (already exist)");
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
            System.err.println("Error generating avatar image: " + e.getMessage());
            return null;
        }
    }
}
