package com.quizz.core.service;

import com.quizz.core.repository.UserRepository;
import com.quizz.core.entity.User;
import org.jspecify.annotations.Nullable;
import org.springframework.data.domain.Pageable;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

@Service
public class UserService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;

    UserService(UserRepository userRepository, PasswordEncoder passwordEncoder) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
    }

    @Transactional
    public User createUser(String name, String email, String telephone, String password) {
        // Check if email already exists
        if (userRepository.findByEmail(email).isPresent()) {
            throw new IllegalArgumentException("Email already exists");
        }
        // Encode password before saving
        String encodedPassword = passwordEncoder.encode(password);
        var user = new User(name, email, telephone, encodedPassword);
        return userRepository.saveAndFlush(user);
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

