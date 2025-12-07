package com.quizz.examplefeature.security;

import com.quizz.examplefeature.User;
import com.quizz.examplefeature.UserRepository;
import org.springframework.security.oauth2.client.userinfo.DefaultOAuth2UserService;
import org.springframework.security.oauth2.client.userinfo.OAuth2UserRequest;
import org.springframework.security.oauth2.core.OAuth2AuthenticationException;
import org.springframework.security.oauth2.core.user.OAuth2User;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.Map;
import java.util.Optional;

@Service
public class CustomOAuth2UserService extends DefaultOAuth2UserService {

    private final UserRepository userRepository;

    public CustomOAuth2UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    @Override
    @Transactional
    public OAuth2User loadUser(OAuth2UserRequest userRequest) throws OAuth2AuthenticationException {
        OAuth2User oauth2User = super.loadUser(userRequest);

        String registrationId = userRequest.getClientRegistration().getRegistrationId();
        Map<String, Object> attributes = oauth2User.getAttributes();

        // Extract user information based on provider
        String providerId = extractProviderId(registrationId, attributes);
        String email = extractEmail(attributes);
        String name = extractName(registrationId, attributes);

        // Find or create user
        User user = findOrCreateUser(registrationId, providerId, email, name);

        // Return custom OAuth2User with our User entity
        return new CustomOAuth2User(oauth2User, user);
    }

    private String extractProviderId(String provider, Map<String, Object> attributes) {
        return switch (provider) {
            case "google" -> (String) attributes.get("sub");
            case "facebook" -> (String) attributes.get("id");
            case "linkedin" -> (String) attributes.get("sub");
            default -> throw new IllegalArgumentException("Unknown provider: " + provider);
        };
    }

    private String extractEmail(Map<String, Object> attributes) {
        String email = (String) attributes.get("email");
        if (email == null || email.isEmpty()) {
            throw new OAuth2AuthenticationException("Email not available from OAuth2 provider");
        }
        return email;
    }

    private String extractName(String provider, Map<String, Object> attributes) {
        return switch (provider) {
            case "google" -> (String) attributes.get("name");
            case "facebook" -> (String) attributes.get("name");
            case "linkedin" -> {
                // LinkedIn provides name differently
                String name = (String) attributes.get("name");
                if (name == null) {
                    String givenName = (String) attributes.get("given_name");
                    String familyName = (String) attributes.get("family_name");
                    name = (givenName != null ? givenName : "") + " " + (familyName != null ? familyName : "");
                }
                yield name.trim();
            }
            default -> "Unknown User";
        };
    }

    private User findOrCreateUser(String provider, String providerId, String email, String name) {
        // First, try to find by OAuth provider and provider ID
        Optional<User> existingUser = userRepository.findByOauthProviderAndOauthProviderId(provider, providerId);

        if (existingUser.isPresent()) {
            return existingUser.get();
        }

        // If not found, try to find by email and link the OAuth account
        Optional<User> userByEmail = userRepository.findByEmail(email);
        if (userByEmail.isPresent()) {
            User user = userByEmail.get();
            user.setOauthProvider(provider);
            user.setOauthProviderId(providerId);
            return userRepository.save(user);
        }

        // Create new user
        User newUser = new User(name, email, "", ""); // No password for OAuth users
        newUser.setOauthProvider(provider);
        newUser.setOauthProviderId(providerId);
        return userRepository.save(newUser);
    }
}

