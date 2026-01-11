package com.quizz.core.security;

import com.quizz.core.entity.Country;
import com.quizz.core.entity.Gender;
import com.quizz.core.service.CountryService;
import com.quizz.core.service.TranslationService;
import com.quizz.core.service.UserService;
import com.vaadin.flow.component.button.Button;
import com.vaadin.flow.component.button.ButtonVariant;
import com.vaadin.flow.component.combobox.ComboBox;
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
    private final CountryService countryService;
    private final TranslationService translationService;
    private final TextField nameField;
    private final EmailField emailField;
    private final TextField telephoneField;
    private final RadioButtonGroup<Gender> genderField;
    private final ComboBox<Country> countryComboBox;
    private final PasswordField passwordField;
    private final PasswordField confirmPasswordField;
    private byte[] uploadedPhotoBytes;

    public RegisterView(UserService userService, CountryService countryService, TranslationService translationService) {
        this.userService = userService;
        this.countryService = countryService;
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

        // Use item label generator to display symbol + first letter
        genderField.setItemLabelGenerator(gender -> {
            if (gender == Gender.MALE) {
                // Get full translation and extract first letter after symbol
                String fullLabel = translationService.translate("register.gender.male");
                // fullLabel is like "♂ Male" or "♂ Homme"
                // Extract the first letter after the space
                String[] parts = fullLabel.trim().split("\\s+");
                if (parts.length > 1 && !parts[1].isEmpty()) {
                    return "♂ " + parts[1].charAt(0); // "♂ M" or "♂ H"
                }
                return "♂ M"; // Fallback
            } else {
                // Get full translation and extract first letter after symbol
                String fullLabel = translationService.translate("register.gender.female");
                // fullLabel is like "♀ Female" or "♀ Femme"
                // Extract the first letter after the space
                String[] parts = fullLabel.trim().split("\\s+");
                if (parts.length > 1 && !parts[1].isEmpty()) {
                    return "♀ " + parts[1].charAt(0); // "♀ F"
                }
                return "♀ F"; // Fallback
            }
        });

        genderField.setRequired(true);

        // Force gender radio buttons to display horizontally (inline)
        genderField.getElement().getStyle()
            .set("flex-direction", "row")
            .set("display", "flex");

        // Force the internal radio button group to be horizontal
        genderField.getElement().executeJs(
            "const radioGroup = this.shadowRoot.querySelector('[part=\"group-field\"]');" +
            "if (radioGroup) { radioGroup.style.flexDirection = 'row'; radioGroup.style.display = 'flex'; }"
        );

        // Name and gender on the same row
        HorizontalLayout nameGenderRow = new HorizontalLayout(nameField, genderField);
        nameGenderRow.setWidthFull();
        nameGenderRow.setAlignItems(Alignment.BASELINE);
        nameGenderRow.setSpacing(true);
        nameField.setWidth("55%"); // 55% space for complete name
        genderField.setWidth("45%"); // 45% for compact gender symbols

        emailField = new EmailField(translationService.translate("register.email"));
        emailField.setPlaceholder(translationService.translate("register.emailPlaceholder"));
        emailField.setWidthFull();
        emailField.setRequired(true);

        telephoneField = new TextField(translationService.translate("register.telephone"));
        telephoneField.setPlaceholder(translationService.translate("register.telephonePlaceholder"));
        telephoneField.setRequired(true);

        // Add country selection ComboBox with flag display
        countryComboBox = new ComboBox<>(translationService.translate("users.country"));
        countryComboBox.setItems(countryService.findAll());
        countryComboBox.setItemLabelGenerator(Country::getCountryName);

        // Container to display the selected country flag
        Div selectedFlagContainer = new Div();
        selectedFlagContainer.getStyle()
            .set("width", "30px")
            .set("height", "20px")
            .set("display", "flex")
            .set("align-items", "center")
            .set("justify-content", "center")
            .set("border", "1px solid #e0e0e0")
            .set("border-radius", "2px")
            .set("margin-top", "8px");

        // Custom renderer to display flag and country name in dropdown
        countryComboBox.setRenderer(new com.vaadin.flow.data.renderer.ComponentRenderer<>(country -> {
            HorizontalLayout layout = new HorizontalLayout();
            layout.setAlignItems(Alignment.CENTER);
            layout.setSpacing(true);
            layout.getStyle().set("line-height", "var(--lumo-line-height-xs)");

            // Create flag container for dropdown
            if (country.getCountryFlag() != null && !country.getCountryFlag().isEmpty()) {
                Div flagContainer = new Div();
                flagContainer.getStyle()
                    .set("width", "24px")
                    .set("height", "16px")
                    .set("display", "flex")
                    .set("align-items", "center")
                    .set("justify-content", "center")
                    .set("border", "1px solid #e0e0e0")
                    .set("border-radius", "2px")
                    .set("flex-shrink", "0");

                // Embed SVG directly as HTML
                flagContainer.getElement().setProperty("innerHTML", country.getCountryFlag());
                flagContainer.getElement().getStyle()
                    .set("width", "24px")
                    .set("height", "16px");

                layout.add(flagContainer);
            }

            // Add country name
            com.vaadin.flow.component.html.Span nameSpan = new com.vaadin.flow.component.html.Span(country.getCountryName());
            layout.add(nameSpan);

            return layout;
        }));

        // Add value change listener to update the selected flag display
        countryComboBox.addValueChangeListener(event -> {
            selectedFlagContainer.removeAll();
            Country selectedCountry = event.getValue();
            if (selectedCountry != null && selectedCountry.getCountryFlag() != null && !selectedCountry.getCountryFlag().isEmpty()) {
                // Embed SVG directly as HTML for the selected flag
                selectedFlagContainer.getElement().setProperty("innerHTML", selectedCountry.getCountryFlag());
            }
        });

        countryComboBox.setRequired(true);
        countryComboBox.setRequiredIndicatorVisible(true);
        countryComboBox.setPlaceholder(translationService.translate("users.selectCountry"));

        // Set France as default value
        countryService.findBySigle("FRA").ifPresent(france -> {
            countryComboBox.setValue(france);
            // Display the flag for France
            if (france.getCountryFlag() != null && !france.getCountryFlag().isEmpty()) {
                selectedFlagContainer.getElement().setProperty("innerHTML", france.getCountryFlag());
            }
        });

        // Create a horizontal layout to hold the combobox and the selected flag on the same line
        HorizontalLayout countryLayout = new HorizontalLayout();
        countryLayout.setSpacing(true);
        countryLayout.setPadding(false);
        countryLayout.setAlignItems(Alignment.END); // Align to bottom
        countryLayout.setWidthFull();
        selectedFlagContainer.getStyle()
            .set("margin-top", "0")
            .set("margin-bottom", "4px") // Align with the bottom of the input field
            .set("flex-shrink", "0"); // Prevent flag from shrinking
        countryLayout.add(countryComboBox, selectedFlagContainer);
        countryLayout.setFlexGrow(1, countryComboBox); // ComboBox takes available space
        countryLayout.setFlexGrow(0, selectedFlagContainer); // Flag container has fixed size

        // Set max width for country combobox to leave room for flag
        countryComboBox.setMaxWidth("calc(100% - 45px)"); // Reserve 45px for flag + spacing
        countryComboBox.setWidth("100%");

        // Telephone and country on the same row
        HorizontalLayout telephoneCountryRow = new HorizontalLayout(telephoneField, countryLayout);
        telephoneCountryRow.setWidthFull();
        telephoneCountryRow.setAlignItems(Alignment.BASELINE);
        telephoneCountryRow.setSpacing(true);
        telephoneField.setWidth("40%"); // Narrower telephone field
        countryLayout.setWidth("60%"); // Wider country layout to fit flag

        passwordField = new PasswordField(translationService.translate("register.password"));
        passwordField.setPlaceholder(translationService.translate("register.passwordPlaceholder"));
        passwordField.setWidthFull();
        passwordField.setRequired(true);
        passwordField.setHelperText(translationService.translate("register.passwordHelper"));

        confirmPasswordField = new PasswordField(translationService.translate("register.confirmPassword"));
        confirmPasswordField.setPlaceholder(translationService.translate("register.confirmPasswordPlaceholder"));
        confirmPasswordField.setWidthFull();
        confirmPasswordField.setRequired(true);

        // Photo upload button that opens a dialog
        Button photoUploadButton = new Button(translationService.translate("register.photoUpload"), event -> openPhotoUploadDialog());
        photoUploadButton.addThemeVariants(ButtonVariant.LUMO_TERTIARY);
        photoUploadButton.setWidthFull();

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

        // Add title and subtitle with default gap
        content.add(title, subtitle);

        // Add form fields with reduced gap between name and email
        VerticalLayout formFields = new VerticalLayout();
        formFields.setSpacing(false);
        formFields.setPadding(false);
        formFields.setAlignItems(Alignment.STRETCH);
        formFields.getStyle().set("gap", "2px"); // Reduced gap for form fields
        formFields.add(
            nameGenderRow,
            emailField,
            telephoneCountryRow,
            passwordField,
            confirmPasswordField
        );

        content.add(
            formFields,
            photoUploadButton,
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

    private void openPhotoUploadDialog() {
        com.vaadin.flow.component.dialog.Dialog dialog = new com.vaadin.flow.component.dialog.Dialog();
        dialog.setHeaderTitle(translationService.translate("register.photoUpload"));
        dialog.setWidth("400px");

        VerticalLayout dialogLayout = new VerticalLayout();
        dialogLayout.setSpacing(true);
        dialogLayout.setPadding(true);

        // Photo upload with MemoryBuffer
        MemoryBuffer buffer = new MemoryBuffer();
        Upload photoUpload = new Upload(buffer);
        photoUpload.setAcceptedFileTypes("image/jpeg", "image/png", "image/gif");
        photoUpload.setMaxFiles(1);
        photoUpload.setMaxFileSize(10 * 1024 * 1024); // 10 MB
        photoUpload.setWidthFull();

        Paragraph helpText = new Paragraph(translationService.translate("register.photoUploadHelper"));
        helpText.getStyle().set("color", "var(--lumo-secondary-text-color)").set("font-size", "var(--lumo-font-size-s)");

        photoUpload.addSucceededListener(event -> {
            try {
                InputStream inputStream = buffer.getInputStream();
                uploadedPhotoBytes = inputStream.readAllBytes();
                Notification.show(
                    translationService.translate("register.photoUploadSuccess"),
                    3000,
                    Notification.Position.MIDDLE
                ).addThemeVariants(NotificationVariant.LUMO_SUCCESS);
                dialog.close();
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

        dialogLayout.add(helpText, photoUpload);

        Button cancelButton = new Button(translationService.translate("session.close"), e -> dialog.close());
        cancelButton.addThemeVariants(ButtonVariant.LUMO_TERTIARY);

        dialog.add(dialogLayout);
        dialog.getFooter().add(cancelButton);

        dialog.open();
    }

    private void handleRegistration() {
        // Validate fields
        if (nameField.isEmpty() || emailField.isEmpty() ||
            telephoneField.isEmpty() || passwordField.isEmpty() ||
            confirmPasswordField.isEmpty() || genderField.isEmpty() ||
            countryComboBox.isEmpty()) {
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
                uploadedPhotoBytes,
                countryComboBox.getValue()
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
