package com.quizz.examplefeature.security;

import com.quizz.examplefeature.User;
import com.quizz.examplefeature.UserService;
import com.vaadin.flow.server.VaadinSession;
import org.springframework.security.core.Authentication;
import org.springframework.security.oauth2.client.authentication.OAuth2AuthenticationToken;
import org.springframework.security.oauth2.core.user.OAuth2User;
import org.springframework.stereotype.Service;

import java.util.Map;

@Service
public class OAuth2UserService {

    private final UserService userService;

    public OAuth2UserService(UserService userService) {
        this.userService = userService;
    }

    public User processOAuth2User(Authentication authentication) {
        if (!(authentication instanceof OAuth2AuthenticationToken)) {
            return null;
        }

        OAuth2AuthenticationToken oauthToken = (OAuth2AuthenticationToken) authentication;
        OAuth2User oauth2User = oauthToken.getPrincipal();
        String registrationId = oauthToken.getAuthorizedClientRegistrationId();

        // Extract user info based on provider
        String email = extractEmail(oauth2User, registrationId);
        String name = extractName(oauth2User, registrationId);
        String providerId = extractProviderId(oauth2User, registrationId);

        // Create or update user
        User user = userService.createOrUpdateOAuthUser(registrationId, providerId, name, email);

        // Store user in session
        VaadinSession.getCurrent().setAttribute(User.class, user);

        return user;
    }

    private String extractEmail(OAuth2User oauth2User, String provider) {
        Map<String, Object> attributes = oauth2User.getAttributes();

        switch (provider.toLowerCase()) {
            case "google":
                return (String) attributes.get("email");
            case "facebook":
                return (String) attributes.get("email");
            case "linkedin":
                return (String) attributes.get("email");
            default:
                return (String) attributes.get("email");
        }
    }

    private String extractName(OAuth2User oauth2User, String provider) {
        Map<String, Object> attributes = oauth2User.getAttributes();

        switch (provider.toLowerCase()) {
            case "google":
                return (String) attributes.get("name");
            case "facebook":
                return (String) attributes.get("name");
            case "linkedin":
                String firstName = (String) attributes.get("given_name");
                String lastName = (String) attributes.get("family_name");
                return (firstName != null ? firstName : "") + " " + (lastName != null ? lastName : "");
            default:
                return (String) attributes.get("name");
        }
    }

    private String extractProviderId(OAuth2User oauth2User, String provider) {
        Map<String, Object> attributes = oauth2User.getAttributes();

        switch (provider.toLowerCase()) {
            case "google":
                return (String) attributes.get("sub");
            case "facebook":
                return (String) attributes.get("id");
            case "linkedin":
                return (String) attributes.get("sub");
            default:
                return (String) attributes.get("id");
        }
    }
}

