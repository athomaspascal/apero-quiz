package com.quizz.core.security;

import com.quizz.core.entity.User;
import com.quizz.core.service.UserActivityService;
import com.quizz.core.service.UserService;
import com.vaadin.flow.server.VaadinSession;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.context.SecurityContext;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.Collections;

@Service
public class AuthenticationService {

    private static final Logger logger = LoggerFactory.getLogger(AuthenticationService.class);

    private final UserService userService;
    private final PasswordEncoder passwordEncoder;
    private final UserActivityService userActivityService;

    public AuthenticationService(UserService userService, PasswordEncoder passwordEncoder,
                                  UserActivityService userActivityService) {
        this.userService = userService;
        this.passwordEncoder = passwordEncoder;
        this.userActivityService = userActivityService;
    }

    /**
     * Authenticate a user with email and password
     * @param email User email
     * @param password User password (plain text)
     * @return true if authentication successful, false otherwise
     */
    public boolean authenticate(String email, String password) {
        User user = userService.getByEmail(email);

        if (user == null) {
            return false;
        }

        // Check password
        if (!passwordEncoder.matches(password, user.getPassword())) {
            return false;
        }

        // Get current session ID
        String currentSessionId = getCurrentSessionId();

        // Check if user is already active with a different session
        if (userActivityService.isUserActiveWithDifferentSession(user.getId(), currentSessionId)) {
            logger.warn("User {} is already active with a different session. Connection denied.", user.getEmail());
            return false;
        }

        // Create Spring Security authentication with authenticated = true
        UsernamePasswordAuthenticationToken authToken = new UsernamePasswordAuthenticationToken(
            user.getEmail(),
            null, // Don't store password in authentication
            Collections.singletonList(new SimpleGrantedAuthority("ROLE_USER"))
        );
        authToken.setDetails(user);

        // Set authentication in security context
        SecurityContext context = SecurityContextHolder.getContext();
        context.setAuthentication(authToken);

        // Store the security context in the session to persist across requests
        VaadinSession vaadinSession = VaadinSession.getCurrent();
        if (vaadinSession != null) {
            vaadinSession.getSession().setAttribute("SPRING_SECURITY_CONTEXT", context);
            // Also store user in Vaadin session for easy access
            vaadinSession.setAttribute(User.class, user);
        }

        // Update user activity with the new session ID
        userActivityService.updateActivity(user, "LOGIN", "login", currentSessionId);
        logger.info("User {} authenticated successfully with session {}", user.getEmail(), currentSessionId);

        return true;
    }

    /**
     * Authentication result enum
     */
    public enum AuthenticationResult {
        SUCCESS,
        INVALID_CREDENTIALS,
        USER_ALREADY_ACTIVE
    }

    /**
     * Authenticate a user with email and password, returning detailed result
     * @param email User email
     * @param password User password (plain text)
     * @return AuthenticationResult indicating success or type of failure
     */
    public AuthenticationResult authenticateWithResult(String email, String password) {
        User user = userService.getByEmail(email);

        if (user == null) {
            return AuthenticationResult.INVALID_CREDENTIALS;
        }

        // Check password
        if (!passwordEncoder.matches(password, user.getPassword())) {
            return AuthenticationResult.INVALID_CREDENTIALS;
        }

        // Get current session ID
        String currentSessionId = getCurrentSessionId();

        // Check if user is already active with a different session
        if (userActivityService.isUserActiveWithDifferentSession(user.getId(), currentSessionId)) {
            logger.warn("User {} is already active with a different session. Connection denied.", user.getEmail());
            return AuthenticationResult.USER_ALREADY_ACTIVE;
        }

        // Create Spring Security authentication with authenticated = true
        UsernamePasswordAuthenticationToken authToken = new UsernamePasswordAuthenticationToken(
            user.getEmail(),
            null, // Don't store password in authentication
            Collections.singletonList(new SimpleGrantedAuthority("ROLE_USER"))
        );
        authToken.setDetails(user);

        // Set authentication in security context
        SecurityContext context = SecurityContextHolder.getContext();
        context.setAuthentication(authToken);

        // Store the security context in the session to persist across requests
        VaadinSession vaadinSession = VaadinSession.getCurrent();
        if (vaadinSession != null) {
            vaadinSession.getSession().setAttribute("SPRING_SECURITY_CONTEXT", context);
            // Also store user in Vaadin session for easy access
            vaadinSession.setAttribute(User.class, user);
        }

        // Update user activity with the new session ID
        userActivityService.updateActivity(user, "LOGIN", "login", currentSessionId);
        logger.info("User {} authenticated successfully with session {}", user.getEmail(), currentSessionId);

        return AuthenticationResult.SUCCESS;
    }

    /**
     * Get the current session ID
     */
    private String getCurrentSessionId() {
        VaadinSession vaadinSession = VaadinSession.getCurrent();
        if (vaadinSession != null && vaadinSession.getSession() != null) {
            return vaadinSession.getSession().getId();
        }
        return null;
    }

    /**
     * Get the currently authenticated user
     * @return User or null if not authenticated
     */
    public User getCurrentUser() {
        // Try to get from Vaadin session first
        VaadinSession session = VaadinSession.getCurrent();
        if (session != null) {
            User user = session.getAttribute(User.class);
            if (user != null) {
                return user;
            }
        }

        // Fallback to Spring Security context
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        if (authentication != null && authentication.isAuthenticated()) {
            String email = authentication.getName();
            return userService.getByEmail(email);
        }

        return null;
    }

    /**
     * Logout the current user
     */
    public void logout() {
        SecurityContextHolder.clearContext();
        VaadinSession session = VaadinSession.getCurrent();
        if (session != null) {
            session.close();
        }
    }
}

