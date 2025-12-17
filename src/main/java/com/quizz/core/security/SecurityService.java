package com.quizz.core.security;

import com.quizz.core.entity.User;
import com.vaadin.flow.router.BeforeEnterEvent;
import com.vaadin.flow.server.ServiceInitEvent;
import com.vaadin.flow.server.VaadinServiceInitListener;
import com.vaadin.flow.server.VaadinSession;
import org.springframework.stereotype.Component;

import java.util.Locale;

@Component
public class SecurityService implements VaadinServiceInitListener {

    private static final String SESSION_LOCALE_KEY = "user.locale";

    @Override
    public void serviceInit(ServiceInitEvent event) {
        event.getSource().addUIInitListener(uiEvent -> {
            // Restore locale from session
            Locale savedLocale = (Locale) VaadinSession.getCurrent().getAttribute(SESSION_LOCALE_KEY);
            if (savedLocale != null) {
                uiEvent.getUI().setLocale(savedLocale);
            }

            uiEvent.getUI().addBeforeEnterListener(this::authenticateNavigation);
        });
    }

    private void authenticateNavigation(BeforeEnterEvent event) {
        Class<?> target = event.getNavigationTarget();

        // Check if the target view allows anonymous access
        boolean isAnonymousAllowed = target.isAnnotationPresent(
            com.vaadin.flow.server.auth.AnonymousAllowed.class
        );

        if (!isAnonymousAllowed) {
            // Check if user is logged in
            User currentUser = VaadinSession.getCurrent().getAttribute(User.class);

            if (currentUser == null) {
                // Redirect to login
                event.rerouteTo(LoginView.class);
            }
        }
    }
}

