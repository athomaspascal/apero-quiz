package com.quizz.examplefeature.security;

import com.quizz.examplefeature.User;
import com.quizz.examplefeature.UserService;
import com.vaadin.flow.component.html.Div;
import com.vaadin.flow.component.html.H1;
import com.vaadin.flow.component.html.Paragraph;
import com.vaadin.flow.component.login.LoginForm;
import com.vaadin.flow.component.notification.Notification;
import com.vaadin.flow.component.notification.NotificationVariant;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import com.vaadin.flow.router.BeforeEnterEvent;
import com.vaadin.flow.router.BeforeEnterObserver;
import com.vaadin.flow.router.PageTitle;
import com.vaadin.flow.router.Route;
import com.vaadin.flow.server.VaadinSession;
import com.vaadin.flow.server.auth.AnonymousAllowed;
import org.springframework.security.crypto.password.PasswordEncoder;

@Route("login")
@PageTitle("Login | Quiz Application")
@AnonymousAllowed
public class LoginView extends VerticalLayout implements BeforeEnterObserver {

    private final LoginForm loginForm = new LoginForm();
    private final UserService userService;
    private final PasswordEncoder passwordEncoder;

    public LoginView(UserService userService, PasswordEncoder passwordEncoder) {
        this.userService = userService;
        this.passwordEncoder = passwordEncoder;

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
        content.add(title, subtitle, loginForm, registerLink);

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
        User user = userService.getByEmail(email);

        if (user != null && passwordEncoder.matches(password, user.getPassword())) {
            // Store user in session
            VaadinSession.getCurrent().setAttribute(User.class, user);

            // Redirect to main page
            getUI().ifPresent(ui -> ui.navigate(""));

            Notification.show("Welcome back, " + user.getName() + "!", 3000, Notification.Position.BOTTOM_END)
                .addThemeVariants(NotificationVariant.LUMO_SUCCESS);
        } else {
            loginForm.setError(true);
            Notification.show("Invalid email or password", 3000, Notification.Position.MIDDLE)
                .addThemeVariants(NotificationVariant.LUMO_ERROR);
        }
    }
}

