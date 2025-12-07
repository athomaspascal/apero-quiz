package com.quizz.examplefeature.security;

import com.quizz.examplefeature.User;
import com.vaadin.flow.router.BeforeEnterEvent;
import com.vaadin.flow.server.ServiceInitEvent;
import com.vaadin.flow.server.VaadinServiceInitListener;
import com.vaadin.flow.server.VaadinSession;
import org.springframework.stereotype.Component;

@Component
public class SecurityService implements VaadinServiceInitListener {

    @Override
    public void serviceInit(ServiceInitEvent event) {
        event.getSource().addUIInitListener(uiEvent -> {
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

