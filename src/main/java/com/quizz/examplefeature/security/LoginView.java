package com.quizz.examplefeature.security;

import com.quizz.examplefeature.User;
import com.vaadin.flow.component.button.Button;
import com.vaadin.flow.component.button.ButtonVariant;
import com.vaadin.flow.component.html.Div;
import com.vaadin.flow.component.html.H1;
import com.vaadin.flow.component.html.Hr;
import com.vaadin.flow.component.html.Paragraph;
import com.vaadin.flow.component.html.Span;
import com.vaadin.flow.component.icon.Icon;
import com.vaadin.flow.component.icon.VaadinIcon;
import com.vaadin.flow.component.login.LoginForm;
import com.vaadin.flow.component.notification.Notification;
import com.vaadin.flow.component.notification.NotificationVariant;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import com.vaadin.flow.router.BeforeEnterEvent;
import com.vaadin.flow.router.BeforeEnterObserver;
import com.vaadin.flow.router.PageTitle;
import com.vaadin.flow.router.Route;
import com.vaadin.flow.server.auth.AnonymousAllowed;
import jakarta.annotation.security.PermitAll;

@Route("login")
@PageTitle("Login | Quiz Application")
@AnonymousAllowed
@PermitAll
public class LoginView extends VerticalLayout implements BeforeEnterObserver {

    private final LoginForm loginForm = new LoginForm();
    private final AuthenticationService authenticationService;

    public LoginView(AuthenticationService authenticationService) {
        this.authenticationService = authenticationService;

        addClassName("login-view");
        setSizeFull();
        setAlignItems(Alignment.CENTER);
        setJustifyContentMode(JustifyContentMode.CENTER);

        loginForm.setForgotPasswordButtonVisible(true);
        loginForm.addForgotPasswordListener(event ->
            getUI().ifPresent(ui -> ui.navigate(ForgotPasswordView.class))
        );

        loginForm.addLoginListener(event -> handleLogin(event.getUsername(), event.getPassword()));

        H1 title = new H1("Quiz Application");
        Paragraph subtitle = new Paragraph("Sign in to continue");
        subtitle.getStyle()
            .set("color", "var(--lumo-secondary-text-color)")
            .set("margin-top", "0");

        Paragraph registerLink = new Paragraph();
        registerLink.add("Don't have an account? ");
        com.vaadin.flow.router.RouterLink registerRouterLink = new com.vaadin.flow.router.RouterLink("Sign up", RegisterView.class);
        registerLink.add(registerRouterLink);
        registerLink.getStyle()
            .set("text-align", "center")
            .set("margin-top", "var(--lumo-space-s)");

        // OAuth2 section
        Hr divider = new Hr();
        divider.getStyle()
            .set("width", "100%")
            .set("margin", "var(--lumo-space-m) 0");

        Span orText = new Span("Or sign in with");
        orText.getStyle()
            .set("color", "var(--lumo-secondary-text-color)")
            .set("font-size", "var(--lumo-font-size-s)")
            .set("text-align", "center")
            .set("display", "block")
            .set("margin", "var(--lumo-space-m) 0");

        Button googleButton = createOAuthButton("Google", "#4285F4", VaadinIcon.GOOGLE_PLUS);
        googleButton.addClickListener(e ->
            getUI().ifPresent(ui -> ui.getPage().setLocation("/oauth2/authorization/google"))
        );

        Button facebookButton = createOAuthButton("Facebook", "#1877F2", VaadinIcon.FACEBOOK);
        facebookButton.addClickListener(e ->
            getUI().ifPresent(ui -> ui.getPage().setLocation("/oauth2/authorization/facebook"))
        );

        Button linkedinButton = createOAuthButton("LinkedIn", "#0A66C2", VaadinIcon.CONNECT);
        linkedinButton.addClickListener(e ->
            getUI().ifPresent(ui -> ui.getPage().setLocation("/oauth2/authorization/linkedin"))
        );

        VerticalLayout oauthButtons = new VerticalLayout();
        oauthButtons.setSpacing(true);
        oauthButtons.setPadding(false);
        oauthButtons.setWidthFull();
        oauthButtons.add(googleButton, facebookButton, linkedinButton);

        Div loginContainer = new Div();
        loginContainer.getStyle()
            .set("background", "var(--lumo-base-color)")
            .set("padding", "var(--lumo-space-l)")
            .set("border-radius", "var(--lumo-border-radius-l)")
            .set("box-shadow", "var(--lumo-box-shadow-s)")
            .set("max-width", "400px")
            .set("width", "100%");

        VerticalLayout content = new VerticalLayout();
        content.setSpacing(false);
        content.setPadding(false);
        content.setAlignItems(Alignment.CENTER);
        content.add(title, subtitle, loginForm, divider, orText, oauthButtons, registerLink);

        loginContainer.add(content);
        add(loginContainer);

        // Style the page
        getStyle()
            .set("background", "linear-gradient(135deg, #667eea 0%, #764ba2 100%)")
            .set("min-height", "100vh");
    }

    @Override
    public void beforeEnter(BeforeEnterEvent event) {
        if (event.getLocation().getQueryParameters().getParameters().containsKey("error")) {
            loginForm.setError(true);
        }
    }

    private void handleLogin(String email, String password) {
        boolean authenticated = authenticationService.authenticate(email, password);

        if (authenticated) {
            // Get the authenticated user
            User user = authenticationService.getCurrentUser();

            if (user != null) {
                Notification.show("Welcome back, " + user.getName() + "!", 3000, Notification.Position.BOTTOM_END)
                    .addThemeVariants(NotificationVariant.LUMO_SUCCESS);
            }

            // Navigate to main page - use navigate() instead of setLocation() to stay in Vaadin context
            getUI().ifPresent(ui -> {
                // Force a page reload to ensure security context is updated
                ui.getPage().setLocation("/");
            });
        } else {
            loginForm.setError(true);
            Notification.show("Invalid email or password", 3000, Notification.Position.MIDDLE)
                .addThemeVariants(NotificationVariant.LUMO_ERROR);
        }
    }

    private Button createOAuthButton(String providerName, String color, VaadinIcon icon) {
        Button button = new Button(providerName);
        button.setIcon(new Icon(icon));
        button.setWidthFull();
        button.addThemeVariants(ButtonVariant.LUMO_PRIMARY);
        button.getStyle()
            .set("background-color", color)
            .set("border", "none")
            .set("color", "white")
            .set("font-weight", "500")
            .set("text-transform", "none");
        return button;
    }
}

