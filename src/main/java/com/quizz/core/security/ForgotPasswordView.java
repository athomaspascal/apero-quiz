package com.quizz.core.security;

import com.quizz.core.service.TranslationService;
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
import com.vaadin.flow.router.PageTitle;
import com.vaadin.flow.router.Route;
import com.vaadin.flow.router.RouterLink;
import com.vaadin.flow.server.auth.AnonymousAllowed;
import jakarta.annotation.security.PermitAll;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Route("forgot-password")
@PageTitle("Forgot Password | Quiz Application")
@AnonymousAllowed
@PermitAll
public class ForgotPasswordView extends VerticalLayout {

    private static final Logger logger = LoggerFactory.getLogger(ForgotPasswordView.class);

    private final UserService userService;
    private final TranslationService translationService;
    private final EmailField emailField;
    private final Button resetButton;

    public ForgotPasswordView(UserService userService, TranslationService translationService) {
        this.userService = userService;
        this.translationService = translationService;

        addClassName("forgot-password-view");
        setSizeFull();
        setAlignItems(Alignment.CENTER);
        setJustifyContentMode(JustifyContentMode.CENTER);

        H1 title = new H1(translationService.translate("forgot.title"));

        Paragraph instruction = new Paragraph(translationService.translate("forgot.instruction"));
        instruction.getStyle()
            .set("color", "var(--lumo-secondary-text-color)")
            .set("text-align", "center")
            .set("margin", "var(--lumo-space-m) 0");

        emailField = new EmailField(translationService.translate("forgot.email"));
        emailField.setPlaceholder(translationService.translate("forgot.emailPlaceholder"));
        emailField.setWidthFull();
        emailField.setRequired(true);
        emailField.setErrorMessage(translationService.translate("forgot.emailError"));

        resetButton = new Button(translationService.translate("forgot.sendButton"), event -> handlePasswordReset());
        resetButton.addThemeVariants(ButtonVariant.LUMO_PRIMARY);
        resetButton.setWidthFull();

        RouterLink backToLogin = new RouterLink(translationService.translate("forgot.backtologin"), LoginView.class);
        backToLogin.getStyle()
            .set("margin-top", "var(--lumo-space-m)")
            .set("text-align", "center")
            .set("display", "block");

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
        content.add(title, instruction, emailField, resetButton, backToLogin);

        formContainer.add(content);
        add(formContainer);
        add(formContainer);

        // Style the page
        getStyle()
            .set("background", "linear-gradient(135deg, #667eea 0%, #764ba2 100%)")
            .set("min-height", "100vh");
    }

    private void handlePasswordReset() {
        String email = emailField.getValue();

        if (email == null || email.isEmpty()) {
            emailField.setInvalid(true);
            return;
        }

        // Check if user exists
        var user = userService.getByEmail(email);

        // Always show success message for security reasons (don't reveal if email exists)
        if (user != null) {
            // In a real application, you would:
            // 1. Generate a password reset token
            // 2. Save the token with expiration time
            // 3. Send an email with reset link

            Notification.show(
                translationService.translate("forgot.successMessage"),
                5000,
                Notification.Position.MIDDLE
            ).addThemeVariants(NotificationVariant.LUMO_SUCCESS);

            // For demo purposes, show the temporary password in console
            logger.info("Password reset requested for: " + email);
        } else {
            // Still show success message to prevent email enumeration
            Notification.show(
                translationService.translate("forgot.successMessage"),
                5000,
                Notification.Position.MIDDLE
            ).addThemeVariants(NotificationVariant.LUMO_SUCCESS);
        }

        emailField.clear();

        // Redirect to login after a delay
        getUI().ifPresent(ui -> {
            ui.getPage().executeJs("setTimeout(function() { window.location.href = 'login'; }, 3000);");
        });
    }
}

