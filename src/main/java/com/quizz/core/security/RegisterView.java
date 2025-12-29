package com.quizz.core.security;

import com.quizz.core.entity.Gender;
import com.quizz.core.service.TranslationService;
import com.quizz.core.service.UserService;
import com.vaadin.flow.component.button.Button;
import com.vaadin.flow.component.button.ButtonVariant;
import com.vaadin.flow.component.html.Div;
import com.vaadin.flow.component.html.H1;
import com.vaadin.flow.component.html.Paragraph;
import com.vaadin.flow.component.notification.Notification;
import com.vaadin.flow.component.notification.NotificationVariant;
import com.vaadin.flow.component.orderedlayout.HorizontalLayout;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import com.vaadin.flow.component.radiobutton.RadioButtonGroup;
import com.vaadin.flow.component.textfield.EmailField;
import com.vaadin.flow.component.textfield.PasswordField;
import com.vaadin.flow.component.textfield.TextField;
import com.vaadin.flow.component.upload.Upload;
import com.vaadin.flow.component.upload.receivers.MemoryBuffer;
import com.vaadin.flow.router.PageTitle;
import com.vaadin.flow.router.Route;
import com.vaadin.flow.router.RouterLink;
import com.vaadin.flow.server.auth.AnonymousAllowed;
import jakarta.annotation.security.PermitAll;

import java.io.InputStream;

@Route("register")
@PageTitle("Register | Quiz Application")
@AnonymousAllowed
@PermitAll
@SuppressWarnings({"deprecation", "removal"})
public class RegisterView extends VerticalLayout {

    private final UserService userService;
    private final TranslationService translationService;
    private final TextField nameField;
    private final EmailField emailField;
    private final TextField telephoneField;
    private final RadioButtonGroup<Gender> genderField;
    private final PasswordField passwordField;
    private final PasswordField confirmPasswordField;
    private byte[] uploadedPhotoBytes;

    public RegisterView(UserService userService, TranslationService translationService) {
        this.userService = userService;
        this.translationService = translationService;

        addClassName("register-view");
        setSizeFull();
        setAlignItems(Alignment.CENTER);
        setJustifyContentMode(JustifyContentMode.CENTER);

        H1 title = new H1(translationService.translate("register.title"));

        Paragraph subtitle = new Paragraph(translationService.translate("register.subtitle"));
        subtitle.getStyle()
            .set("color", "var(--lumo-secondary-text-color)")
            .set("text-align", "center")
            .set("margin", "0 0 var(--lumo-space-m) 0");

        nameField = new TextField(translationService.translate("register.name"));
        nameField.setPlaceholder(translationService.translate("register.namePlaceholder"));
        nameField.setRequired(true);

        // Gender radio button group
        genderField = new RadioButtonGroup<>(translationService.translate("register.gender"));
        genderField.setItems(Gender.MALE, Gender.FEMALE);
        genderField.setItemLabelGenerator(gender -> {
            if (gender == Gender.MALE) {
                return translationService.translate("register.gender.male");
            } else {
                return translationService.translate("register.gender.female");
            }
        });
        genderField.setRequired(true);

        // Name and gender on the same row
        HorizontalLayout nameGenderRow = new HorizontalLayout(nameField, genderField);
        nameGenderRow.setWidthFull();
        nameGenderRow.setAlignItems(Alignment.BASELINE);
        nameGenderRow.setSpacing(true);
        nameField.setWidth("60%");
        genderField.setWidth("40%");

        emailField = new EmailField(translationService.translate("register.email"));
        emailField.setPlaceholder(translationService.translate("register.emailPlaceholder"));
        emailField.setWidthFull();
        emailField.setRequired(true);

        telephoneField = new TextField(translationService.translate("register.telephone"));
        telephoneField.setPlaceholder(translationService.translate("register.telephonePlaceholder"));
        telephoneField.setWidthFull();
        telephoneField.setRequired(true);

        passwordField = new PasswordField(translationService.translate("register.password"));
        passwordField.setPlaceholder(translationService.translate("register.passwordPlaceholder"));
        passwordField.setWidthFull();
        passwordField.setRequired(true);
        passwordField.setHelperText(translationService.translate("register.passwordHelper"));

        confirmPasswordField = new PasswordField(translationService.translate("register.confirmPassword"));
        confirmPasswordField.setPlaceholder(translationService.translate("register.confirmPasswordPlaceholder"));
        confirmPasswordField.setWidthFull();
        confirmPasswordField.setRequired(true);

        // Photo upload with MemoryBuffer (deprecated but functional)
        MemoryBuffer buffer = new MemoryBuffer();
        Upload photoUpload = new Upload(buffer);
        photoUpload.setAcceptedFileTypes("image/jpeg", "image/png", "image/gif");
        photoUpload.setMaxFiles(1);
        photoUpload.setMaxFileSize(10 * 1024 * 1024); // 10 MB

        Div uploadLabel = new Div();
        uploadLabel.setText(translationService.translate("register.photoUpload"));
        uploadLabel.getStyle().set("font-weight", "500").set("margin-bottom", "4px");

        photoUpload.addSucceededListener(event -> {
            try {
                InputStream inputStream = buffer.getInputStream();
                uploadedPhotoBytes = inputStream.readAllBytes();
                Notification.show(
                    translationService.translate("register.photoUploadSuccess"),
                    3000,
                    Notification.Position.MIDDLE
                ).addThemeVariants(NotificationVariant.LUMO_SUCCESS);
            } catch (Exception e) {
                Notification.show(
                    translationService.translate("register.photoUploadError"),
                    3000,
                    Notification.Position.MIDDLE
                ).addThemeVariants(NotificationVariant.LUMO_ERROR);
            }
        });

        photoUpload.addFileRejectedListener(event -> {
            Notification.show(
                translationService.translate("register.photoUploadError") + " (" + event.getErrorMessage() + ")",
                4000,
                Notification.Position.MIDDLE
            ).addThemeVariants(NotificationVariant.LUMO_ERROR);
        });

        photoUpload.addFailedListener(event -> {
            Notification.show(
                translationService.translate("register.photoUploadError"),
                3000,
                Notification.Position.MIDDLE
            ).addThemeVariants(NotificationVariant.LUMO_ERROR);
        });

        Button registerButton = new Button(translationService.translate("register.signup"), event -> handleRegistration());
        registerButton.addThemeVariants(ButtonVariant.LUMO_PRIMARY);
        registerButton.setWidthFull();

        Paragraph loginLink = new Paragraph();
        loginLink.add(translationService.translate("register.alreadyAccount") + " ");
        RouterLink loginRouterLink = new RouterLink(translationService.translate("register.signinlink"), LoginView.class);
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
        content.setSpacing(false);
        content.setPadding(false);
        content.setAlignItems(Alignment.STRETCH);
        content.getStyle().set("gap", "8px");
        content.add(
            title,
            subtitle,
            nameGenderRow,
            emailField,
            telephoneField,
            passwordField,
            confirmPasswordField,
            uploadLabel,
            photoUpload,
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
            confirmPasswordField.isEmpty() || genderField.isEmpty()) {
            Notification.show(translationService.translate("register.error.fillAll"), 3000, Notification.Position.MIDDLE)
                .addThemeVariants(NotificationVariant.LUMO_ERROR);
            return;
        }

        // Validate email format
        if (emailField.isInvalid()) {
            Notification.show(translationService.translate("register.error.invalidEmail"), 3000, Notification.Position.MIDDLE)
                .addThemeVariants(NotificationVariant.LUMO_ERROR);
            return;
        }

        // Validate password length
        if (passwordField.getValue().length() < 6) {
            Notification.show(translationService.translate("register.error.passwordLength"), 3000, Notification.Position.MIDDLE)
                .addThemeVariants(NotificationVariant.LUMO_ERROR);
            return;
        }

        // Validate password match
        if (!passwordField.getValue().equals(confirmPasswordField.getValue())) {
            Notification.show(translationService.translate("register.error.passwordMismatch"), 3000, Notification.Position.MIDDLE)
                .addThemeVariants(NotificationVariant.LUMO_ERROR);
            return;
        }

        try {
            userService.createUser(
                nameField.getValue(),
                emailField.getValue(),
                telephoneField.getValue(),
                passwordField.getValue(),
                genderField.getValue(),
                uploadedPhotoBytes
            );

            Notification.show(translationService.translate("register.success"), 3000, Notification.Position.MIDDLE)
                .addThemeVariants(NotificationVariant.LUMO_SUCCESS);

            // Redirect to login
            getUI().ifPresent(ui -> ui.navigate(LoginView.class));
        } catch (IllegalArgumentException e) {
            Notification.show(e.getMessage(), 3000, Notification.Position.MIDDLE)
                .addThemeVariants(NotificationVariant.LUMO_ERROR);
        }
    }
}
