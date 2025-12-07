package com.quizz.core.security;

import com.quizz.core.service.UserService;
import com.vaadin.flow.component.button.Button;
import com.vaadin.flow.component.button.ButtonVariant;
import com.vaadin.flow.component.html.Div;
import com.vaadin.flow.component.html.H1;
import com.vaadin.flow.component.html.Paragraph;
import com.vaadin.flow.component.notification.Notification;
import com.vaadin.flow.component.notification.NotificationVariant;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import com.vaadin.flow.component.textfield.EmailField;
import com.vaadin.flow.component.textfield.PasswordField;
import com.vaadin.flow.component.textfield.TextField;
import com.vaadin.flow.router.PageTitle;
import com.vaadin.flow.router.Route;
import com.vaadin.flow.router.RouterLink;
import com.vaadin.flow.server.auth.AnonymousAllowed;
import jakarta.annotation.security.PermitAll;

@Route("register")
@PageTitle("Register | Quiz Application")
@AnonymousAllowed
@PermitAll
public class RegisterView extends VerticalLayout {

    private final UserService userService;
    private final TextField nameField;
    private final EmailField emailField;
    private final TextField telephoneField;
    private final PasswordField passwordField;
    private final PasswordField confirmPasswordField;
    private final Button registerButton;

    public RegisterView(UserService userService) {
        this.userService = userService;

        addClassName("register-view");
        setSizeFull();
        setAlignItems(Alignment.CENTER);
        setJustifyContentMode(JustifyContentMode.CENTER);

        H1 title = new H1("Create Account");

        Paragraph subtitle = new Paragraph("Sign up to start taking quizzes");
        subtitle.getStyle()
            .set("color", "var(--lumo-secondary-text-color)")
            .set("text-align", "center")
            .set("margin", "0 0 var(--lumo-space-m) 0");

        nameField = new TextField("Full Name");
        nameField.setPlaceholder("John Doe");
        nameField.setWidthFull();
        nameField.setRequired(true);

        emailField = new EmailField("Email");
        emailField.setPlaceholder("your.email@example.com");
        emailField.setWidthFull();
        emailField.setRequired(true);

        telephoneField = new TextField("Telephone");
        telephoneField.setPlaceholder("+33 6 12 34 56 78");
        telephoneField.setWidthFull();
        telephoneField.setRequired(true);

        passwordField = new PasswordField("Password");
        passwordField.setPlaceholder("Enter password");
        passwordField.setWidthFull();
        passwordField.setRequired(true);
        passwordField.setHelperText("Password must be at least 6 characters");

        confirmPasswordField = new PasswordField("Confirm Password");
        confirmPasswordField.setPlaceholder("Confirm password");
        confirmPasswordField.setWidthFull();
        confirmPasswordField.setRequired(true);

        registerButton = new Button("Create Account", event -> handleRegistration());
        registerButton.addThemeVariants(ButtonVariant.LUMO_PRIMARY);
        registerButton.setWidthFull();

        Paragraph loginLink = new Paragraph();
        loginLink.add("Already have an account? ");
        RouterLink loginRouterLink = new RouterLink("Sign in", LoginView.class);
        loginLink.add(loginRouterLink);
        loginLink.getStyle()
            .set("text-align", "center")
            .set("margin-top", "var(--lumo-space-m)");

        Div formContainer = new Div();
        formContainer.getStyle()
            .set("background", "var(--lumo-base-color)")
            .set("padding", "var(--lumo-space-xl)")
            .set("border-radius", "var(--lumo-border-radius-l)")
            .set("box-shadow", "var(--lumo-box-shadow-s)")
            .set("max-width", "400px")
            .set("width", "100%");

        VerticalLayout content = new VerticalLayout();
        content.setSpacing(true);
        content.setPadding(false);
        content.setAlignItems(Alignment.STRETCH);
        content.add(
            title,
            subtitle,
            nameField,
            emailField,
            telephoneField,
            passwordField,
            confirmPasswordField,
            registerButton,
            loginLink
        );

        formContainer.add(content);
        add(formContainer);

        // Style the page
        getStyle()
            .set("background", "linear-gradient(135deg, #667eea 0%, #764ba2 100%)")
            .set("min-height", "100vh");
    }

    private void handleRegistration() {
        // Validate fields
        if (nameField.isEmpty() || emailField.isEmpty() ||
            telephoneField.isEmpty() || passwordField.isEmpty() ||
            confirmPasswordField.isEmpty()) {
            Notification.show("Please fill in all fields", 3000, Notification.Position.MIDDLE)
                .addThemeVariants(NotificationVariant.LUMO_ERROR);
            return;
        }

        // Validate email format
        if (emailField.isInvalid()) {
            Notification.show("Please enter a valid email address", 3000, Notification.Position.MIDDLE)
                .addThemeVariants(NotificationVariant.LUMO_ERROR);
            return;
        }

        // Validate password length
        if (passwordField.getValue().length() < 6) {
            Notification.show("Password must be at least 6 characters", 3000, Notification.Position.MIDDLE)
                .addThemeVariants(NotificationVariant.LUMO_ERROR);
            return;
        }

        // Validate password match
        if (!passwordField.getValue().equals(confirmPasswordField.getValue())) {
            Notification.show("Passwords do not match", 3000, Notification.Position.MIDDLE)
                .addThemeVariants(NotificationVariant.LUMO_ERROR);
            return;
        }

        try {
            userService.createUser(
                nameField.getValue(),
                emailField.getValue(),
                telephoneField.getValue(),
                passwordField.getValue()
            );

            Notification.show("Account created successfully! Please login.", 3000, Notification.Position.MIDDLE)
                .addThemeVariants(NotificationVariant.LUMO_SUCCESS);

            // Redirect to login
            getUI().ifPresent(ui -> ui.navigate(LoginView.class));
        } catch (IllegalArgumentException e) {
            Notification.show(e.getMessage(), 3000, Notification.Position.MIDDLE)
                .addThemeVariants(NotificationVariant.LUMO_ERROR);
        }
    }
}

