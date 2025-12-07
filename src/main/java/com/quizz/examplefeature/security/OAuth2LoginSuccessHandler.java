package com.quizz.examplefeature.security;

import com.quizz.examplefeature.User;
import com.vaadin.flow.server.VaadinSession;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.security.core.Authentication;
import org.springframework.security.web.authentication.SavedRequestAwareAuthenticationSuccessHandler;
import org.springframework.stereotype.Component;

import java.io.IOException;

@Component
public class OAuth2LoginSuccessHandler extends SavedRequestAwareAuthenticationSuccessHandler {

    public OAuth2LoginSuccessHandler() {
        setDefaultTargetUrl("/");
        setAlwaysUseDefaultTargetUrl(false);
    }

    @Override
    public void onAuthenticationSuccess(HttpServletRequest request, HttpServletResponse response,
                                        Authentication authentication) throws ServletException, IOException {

        // Extract the user from OAuth2 authentication
        Object principal = authentication.getPrincipal();

        if (principal instanceof CustomOAuth2User customOAuth2User) {
            User user = customOAuth2User.getUser();

            // Store user in Vaadin session if available
            try {
                VaadinSession vaadinSession = VaadinSession.getCurrent();
                if (vaadinSession != null) {
                    vaadinSession.setAttribute(User.class, user);
                }
            } catch (Exception e) {
                // VaadinSession might not be available during OAuth2 flow
                // Store in HTTP session instead
                request.getSession().setAttribute("LOGGED_IN_USER", user);
            }
        }

        super.onAuthenticationSuccess(request, response, authentication);
    }
}

