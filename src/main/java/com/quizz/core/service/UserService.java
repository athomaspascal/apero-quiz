package com.quizz.core.service;

import com.quizz.core.repository.UserRepository;
import com.quizz.core.entity.Gender;
import com.quizz.core.entity.User;
import org.jspecify.annotations.Nullable;
import org.springframework.data.domain.Pageable;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.imageio.ImageIO;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.util.List;
import java.util.Optional;

@Service
public class UserService {

    private static final Logger logger = LoggerFactory.getLogger(UserService.class);

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private static final int AVATAR_SIZE = 200; // Standard avatar size

    UserService(UserRepository userRepository, PasswordEncoder passwordEncoder) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
    }

    /**
     * Resize an image to the standard avatar size (200x200)
     * @param imageBytes Original image bytes
     * @return Resized image bytes or null if error
     */
    private byte[] resizeImage(byte[] imageBytes) {
        if (imageBytes == null || imageBytes.length == 0) {
            return null;
        }

        try {
            ByteArrayInputStream bais = new ByteArrayInputStream(imageBytes);
            BufferedImage originalImage = ImageIO.read(bais);

            if (originalImage == null) {
                return imageBytes; // Return original if can't read
            }

            // Create resized image
            BufferedImage resizedImage = new BufferedImage(AVATAR_SIZE, AVATAR_SIZE, BufferedImage.TYPE_INT_RGB);
            Graphics2D g2d = resizedImage.createGraphics();

            // Enable high-quality rendering
            g2d.setRenderingHint(RenderingHints.KEY_INTERPOLATION, RenderingHints.VALUE_INTERPOLATION_BICUBIC);
            g2d.setRenderingHint(RenderingHints.KEY_RENDERING, RenderingHints.VALUE_RENDER_QUALITY);
            g2d.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);

            // Draw resized image
            g2d.drawImage(originalImage, 0, 0, AVATAR_SIZE, AVATAR_SIZE, null);
            g2d.dispose();

            // Convert to byte array
            ByteArrayOutputStream baos = new ByteArrayOutputStream();
            ImageIO.write(resizedImage, "jpg", baos);
            return baos.toByteArray();
        } catch (IOException e) {
            logger.error("Error resizing image: " + e.getMessage());
            return imageBytes; // Return original if resize fails
        }
    }

    @Transactional
    public User createUser(String name, String email, String telephone, String password, Gender gender, byte[] photoBytes) {
        return createUser(name, email, telephone, password, gender, photoBytes, null);
    }

    @Transactional
    public User createUser(String name, String email, String telephone, String password, Gender gender, byte[] photoBytes, com.quizz.core.entity.Country country) {
        // Check if email already exists
        if (userRepository.findByEmail(email).isPresent()) {
            throw new IllegalArgumentException("Email already exists");
        }
        // Encode password before saving
        String encodedPassword = passwordEncoder.encode(password);
        var user = new User(name, email, telephone, encodedPassword, gender);

        // Set country if provided
        if (country != null) {
            user.setCountry(country);
        }

        // Resize photo if provided
        if (photoBytes != null && photoBytes.length > 0) {
            byte[] resizedPhoto = resizeImage(photoBytes);
            user.setPhotoBytes(resizedPhoto);
        } else {
            user.setPhotoBytes(null);
        }

        return userRepository.saveAndFlush(user);
    }

    @Transactional
    public User createUser(String name, String email, String telephone, String password, Gender gender) {
        return createUser(name, email, telephone, password, gender, null);
    }

    @Transactional
    public User updateUser(Long id, String name, String email, String telephone, String password) {
        User user = userRepository.findById(id)
            .orElseThrow(() -> new IllegalArgumentException("User not found"));

        // Check if email is being changed to an existing email
        if (!user.getEmail().equals(email)) {
            Optional<User> existingUser = userRepository.findByEmail(email);
            if (existingUser.isPresent()) {
                Long existingId = existingUser.get().getId();
                if (existingId != null && !existingId.equals(id)) {
                    throw new IllegalArgumentException("Email already exists");
                }
            }
        }

        user.setName(name);
        user.setEmail(email);
        user.setTelephone(telephone);
        // Encode password before saving
        String encodedPassword = passwordEncoder.encode(password);
        user.setPassword(encodedPassword);
        return userRepository.saveAndFlush(user);
    }

    @Transactional(readOnly = true)
    public List<User> list(Pageable pageable) {
        return userRepository.findAllBy(pageable).toList();
    }

    @Transactional(readOnly = true)
    public List<User> listPublicUsers(Pageable pageable) {
        return userRepository.findByIsPublicTrue(pageable).toList();
    }

    @Transactional(readOnly = true)
    public long countPublicUsers() {
        return userRepository.countByIsPublicTrue();
    }

    @Transactional(readOnly = true)
    public @Nullable User getById(Long id) {
        return userRepository.findById(id).orElse(null);
    }

    @Transactional(readOnly = true)
    public @Nullable User getByEmail(String email) {
        return userRepository.findByEmail(email).orElse(null);
    }

    @Transactional
    public void deleteUser(Long id) {
        userRepository.deleteById(id);
    }

    @Transactional
    public void updatePublicFlag(Long id, boolean isPublic) {
        User user = userRepository.findById(id)
            .orElseThrow(() -> new IllegalArgumentException("User not found"));
        user.setPublic(isPublic);
        userRepository.saveAndFlush(user);
    }

    @Transactional
    public void updateAdminFlag(Long id, boolean isAdmin) {
        User user = userRepository.findById(id)
            .orElseThrow(() -> new IllegalArgumentException("User not found"));
        user.setAdmin(isAdmin);
        userRepository.saveAndFlush(user);
    }

    /**
     * Save or update a user
     * @param user The user to save
     * @return The saved user
     */
    @Transactional
    public User save(User user) {
        return userRepository.saveAndFlush(user);
    }

    @Transactional(readOnly = true)
    public Optional<User> findByEmail(String email) {
        return userRepository.findByEmail(email);
    }

    @Transactional
    public User createOrUpdateOAuthUser(String provider, String providerId, String name, String email) {
        // Check if user already exists with this OAuth provider
        Optional<User> existingUser = userRepository.findByOauthProviderAndOauthProviderId(provider, providerId);

        if (existingUser.isPresent()) {
            // Update existing user
            User user = existingUser.get();
            user.setName(name);
            user.setEmail(email);
            return userRepository.saveAndFlush(user);
        }

        // Check if user exists with this email
        Optional<User> userByEmail = userRepository.findByEmail(email);
        if (userByEmail.isPresent()) {
            // Link OAuth to existing account
            User user = userByEmail.get();
            user.setOauthProvider(provider);
            user.setOauthProviderId(providerId);
            return userRepository.saveAndFlush(user);
        }

        // Create new user
        User newUser = new User();
        newUser.setName(name);
        newUser.setEmail(email);
        newUser.setTelephone("");
        newUser.setPassword(""); // OAuth users don't need password
        newUser.setOauthProvider(provider);
        newUser.setOauthProviderId(providerId);
        return userRepository.saveAndFlush(newUser);
    }
}
