package com.quizz.core.security;

import com.quizz.core.entity.User;
import org.springframework.security.core.Authentication;
import org.springframework.security.oauth2.client.authentication.OAuth2AuthenticationToken;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class OAuth2LoginSuccessController {

    private final OAuth2UserService oAuth2UserService;

    public OAuth2LoginSuccessController(OAuth2UserService oAuth2UserService) {
        this.oAuth2UserService = oAuth2UserService;
    }

    @GetMapping("/login/oauth2/success")
    public String onLoginSuccess(Authentication authentication) {
        if (authentication instanceof OAuth2AuthenticationToken) {
            User user = oAuth2UserService.processOAuth2User(authentication);
            if (user != null) {
                return "redirect:/";
            }
        }
        return "redirect:/login?error";
    }
}

