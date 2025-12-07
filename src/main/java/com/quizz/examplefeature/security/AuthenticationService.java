package com.quizz.examplefeature.security;

import com.quizz.examplefeature.User;
import com.quizz.examplefeature.UserService;
import com.vaadin.flow.server.VaadinSession;
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

    private final UserService userService;
    private final PasswordEncoder passwordEncoder;

    public AuthenticationService(UserService userService, PasswordEncoder passwordEncoder) {
        this.userService = userService;
        this.passwordEncoder = passwordEncoder;
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

        return true;
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

