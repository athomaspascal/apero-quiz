package com.quizz.core.security;

import com.quizz.core.entity.User;
import com.quizz.core.service.TranslationService;
import com.quizz.core.service.UserService;
import com.vaadin.flow.component.button.Button;
import com.vaadin.flow.component.button.ButtonVariant;
import com.vaadin.flow.component.dialog.Dialog;
import com.vaadin.flow.component.html.*;
import com.vaadin.flow.component.icon.Icon;
import com.vaadin.flow.component.icon.VaadinIcon;
import com.vaadin.flow.component.login.LoginForm;
import com.vaadin.flow.component.login.LoginI18n;
import com.vaadin.flow.component.notification.Notification;
import com.vaadin.flow.component.notification.NotificationVariant;
import com.vaadin.flow.component.orderedlayout.FlexLayout;
import com.vaadin.flow.component.orderedlayout.HorizontalLayout;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import com.vaadin.flow.router.BeforeEnterEvent;
import com.vaadin.flow.router.BeforeEnterObserver;
import com.vaadin.flow.router.PageTitle;
import com.vaadin.flow.router.Route;
import com.vaadin.flow.server.StreamResource;
import com.vaadin.flow.server.VaadinSession;
import com.vaadin.flow.server.auth.AnonymousAllowed;
import jakarta.annotation.security.PermitAll;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.data.domain.Pageable;

import java.io.ByteArrayInputStream;
import java.util.List;
import java.util.Locale;

@Route("login")
@PageTitle("Login | Quiz Application")
@AnonymousAllowed
@PermitAll
@SuppressWarnings({"deprecation", "removal"})
public class LoginView extends VerticalLayout implements BeforeEnterObserver {

    private static final Logger logger = LoggerFactory.getLogger(LoginView.class);

    private final LoginForm loginForm = new LoginForm();
    private final AuthenticationService authenticationService;
    private final TranslationService translationService;
    private final UserService userService;
    private final com.quizz.core.service.PlayerTraceService traceService;
    private final com.quizz.core.service.UserActivityService userActivityService;

    // Flag buttons for highlighting
    private Button frenchButton;
    private Button englishButton;
    private Button italianButton;

    public LoginView(AuthenticationService authenticationService, TranslationService translationService,
                    UserService userService, com.quizz.core.service.PlayerTraceService traceService,
                    com.quizz.core.service.UserActivityService userActivityService) {
        this.authenticationService = authenticationService;
        this.translationService = translationService;
        this.userService = userService;
        this.traceService = traceService;
        this.userActivityService = userActivityService;

        addClassName("login-view");
        setSizeFull();
        setAlignItems(Alignment.CENTER);
        setJustifyContentMode(JustifyContentMode.CENTER);

        // Set the UI locale from the translation service
        Locale currentLocale = translationService.getCurrentLocale();
        getUI().ifPresent(ui -> ui.setLocale(currentLocale));

        // Configure login form with translated labels
        configureLoginFormI18n();

        loginForm.setForgotPasswordButtonVisible(true);
        loginForm.addForgotPasswordListener(event ->
            getUI().ifPresent(ui -> ui.navigate(ForgotPasswordView.class))
        );

        loginForm.addLoginListener(event -> handleLogin(event.getUsername(), event.getPassword()));

        H3 title = new H3("🎄 Quiz 🎄");
        title.getStyle()
            .set("color", "#ffffff")
            .set("text-shadow", "2px 2px 4px rgba(0,0,0,0.5)")
            .set("margin-bottom", "0")
            .set("margin-right", "var(--lumo-space-s)")
            .set("z-index", "10")
            .set("position", "relative");

        // Language selector buttons
        HorizontalLayout languageButtons = createLanguageButtons();
        languageButtons.getStyle()
            .set("z-index", "10")
            .set("position", "relative");

        // Title and language buttons in same row
        HorizontalLayout titleRow = new HorizontalLayout(title, languageButtons);
        titleRow.setAlignItems(Alignment.CENTER);
        titleRow.setJustifyContentMode(JustifyContentMode.CENTER);
        titleRow.getStyle()
            .set("margin-bottom", "var(--lumo-space-m)");
        /*
                Paragraph subtitle = new Paragraph("Sign in to continue");
                subtitle.getStyle()
                    .set("color", "rgba(255, 255, 255, 0.9)")
                    .set("margin-top", "0")
                    .set("z-index", "10")
                    .set("position", "relative");
        */
        Paragraph registerLink = new Paragraph();
        registerLink.add(translationService.translate("login.noaccount") + " ");
        com.vaadin.flow.router.RouterLink registerRouterLink = new com.vaadin.flow.router.RouterLink(
                translationService.translate("login.signuplink"), RegisterView.class);
        registerLink.add(registerRouterLink);

        // OAuth2 buttons
        Button googleButton = createOAuthButton("G", "#4285F4", VaadinIcon.GOOGLE_PLUS);
        googleButton.addClickListener(e ->
            getUI().ifPresent(ui -> ui.getPage().setLocation("/oauth2/authorization/google"))
        );

        Button facebookButton = createOAuthButton("F", "#1877F2", VaadinIcon.FACEBOOK);
        facebookButton.addClickListener(e ->
            getUI().ifPresent(ui -> ui.getPage().setLocation("/oauth2/authorization/facebook"))
        );

        Button linkedinButton = createOAuthButton("in", "#0A66C2", VaadinIcon.CONNECT);
        linkedinButton.addClickListener(e ->
            getUI().ifPresent(ui -> ui.getPage().setLocation("/oauth2/authorization/linkedin"))
        );

        HorizontalLayout oauthButtons = new HorizontalLayout();
        oauthButtons.setSpacing(true);
        oauthButtons.setPadding(false);
        oauthButtons.setWidthFull();
        oauthButtons.setJustifyContentMode(JustifyContentMode.CENTER);
        oauthButtons.add(googleButton, facebookButton, linkedinButton);

        // Wrapper for login form with white background
        Div formWrapper = new Div();
        // Update register link style
        registerLink.getStyle()
                .set("text-align", "center")
                .set("margin-top", "var(--lumo-space-s)")
                .set("color", "rgba(0, 0, 0, 0.9)")
                .set("position", "relative")
                .set("z-index", "10");
        formWrapper.getStyle()
            .set("background", "rgba(255, 255, 255, 0.95)")
            .set("padding", "var(--lumo-space-m)")
            .set("border-radius", "var(--lumo-border-radius-m)")
            .set("width", "100%")
            .set("position", "relative")
            .set("z-index", "10");

        // Public avatar button
        Button publicAvatarButton = new Button("👤 " + translationService.translate("login.publicavatar"));
        publicAvatarButton.addThemeVariants(ButtonVariant.LUMO_SMALL, ButtonVariant.LUMO_TERTIARY);
        publicAvatarButton.setWidthFull();
        publicAvatarButton.addClickListener(event -> showPublicAvatarDialog());
        publicAvatarButton.getStyle()
            .set("margin-top", "var(--lumo-space-xs)");

        formWrapper.add(loginForm, publicAvatarButton, registerLink);

        // Wrapper for OAuth section
        Div oauthWrapper = new Div();
        oauthWrapper.getStyle()
            .set("background", "rgba(255, 255, 255, 0.95)")
            .set("padding", "var(--lumo-space-m)")
            .set("border-radius", "var(--lumo-border-radius-m)")
            .set("width", "100%")
            .set("position", "relative")
            .set("z-index", "10");

        Span orText = new Span(translationService.translate("login.orloginwith"));
        orText.getStyle()
            .set("color", "var(--lumo-secondary-text-color)")
            .set("font-size", "var(--lumo-font-size-s)")
            .set("text-align", "center")
            .set("display", "block")
            .set("margin-bottom", "var(--lumo-space-m)");

        oauthWrapper.add(orText, oauthButtons);



        Div loginContainer = new Div();
        loginContainer.getStyle()
            .set("background", "linear-gradient(135deg, #1a472a 0%, #2d5f3f 25%, #c41e3a 50%, #165b33 75%, #0f3823 100%)")
            .set("background-size", "400% 400%")
            .set("animation", "christmasGradient 15s ease infinite")
            .set("padding", "var(--lumo-space-l)")
            .set("border-radius", "var(--lumo-border-radius-l)")
            .set("box-shadow", "0 8px 32px 0 rgba(31, 38, 135, 0.37), 0 0 20px rgba(255, 215, 0, 0.3)")
            .set("border", "2px solid rgba(255, 215, 0, 0.4)")
            .set("max-width", "400px")
            .set("width", "100%")
            .set("max-height", "90vh")
            .set("overflow-y", "auto")
            .set("overflow-x", "hidden")
            .set("position", "relative");

        VerticalLayout content = new VerticalLayout();
        content.setSpacing(true);
        content.setPadding(false);
        content.setAlignItems(Alignment.CENTER);
        content.add(titleRow,
                //subtitle,
                formWrapper, oauthWrapper);

        loginContainer.add(content);
        add(loginContainer);

        // Style the page background
        getStyle()
            .set("background", "var(--lumo-contrast-5pct)")
            .set("min-height", "100vh");

        // Add CSS for animations and snowflakes inside the container
        addAttachListener(event -> {
            getUI().ifPresent(ui -> {
                ui.getPage().executeJs(
                    "const style = document.createElement('style');" +
                    "style.textContent = `" +
                    "@keyframes christmasGradient {" +
                    "  0%, 100% { background-position: 0% 50%; }" +
                    "  50% { background-position: 100% 50%; }" +
                    "}" +
                    "@keyframes snowfall {" +
                    "  0% { transform: translateY(-20px) translateX(0); opacity: 1; }" +
                    "  100% { transform: translateY(600px) translateX(50px); opacity: 0.3; }" +
                    "}" +
                    "@keyframes snowfall2 {" +
                    "  0% { transform: translateY(-20px) translateX(0); opacity: 1; }" +
                    "  100% { transform: translateY(600px) translateX(-50px); opacity: 0.3; }" +
                    "}" +
                    ".container-snowflake {" +
                    "  position: absolute;" +
                    "  top: -20px;" +
                    "  color: white;" +
                    "  font-size: 1.2em;" +
                    "  pointer-events: none;" +
                    "  user-select: none;" +
                    "  z-index: 1;" +
                    "}" +
                    ".container-ornament {" +
                    "  position: absolute;" +
                    "  pointer-events: none;" +
                    "  user-select: none;" +
                    "  z-index: 0;" +
                    "  opacity: 0.2;" +
                    "}" +
                    "`;" +
                    "document.head.appendChild(style);" +

                    // Find the login container
                    "setTimeout(() => {" +
                    "  const containers = document.querySelectorAll('div');" +
                    "  let loginContainer = null;" +
                    "  for(let container of containers) {" +
                    "    const bg = container.style.background;" +
                    "    if(bg && bg.includes('1a472a')) {" +
                    "      loginContainer = container;" +
                    "      break;" +
                    "    }" +
                    "  }" +
                    "  if(!loginContainer) return;" +

                    // Create snowflakes inside container
                    "  for(let i = 0; i < 25; i++) {" +
                    "    const snowflake = document.createElement('div');" +
                    "    snowflake.classList.add('container-snowflake');" +
                    "    snowflake.innerHTML = '❄';" +
                    "    snowflake.style.left = Math.random() * 100 + '%';" +
                    "    snowflake.style.animationDuration = (Math.random() * 8 + 8) + 's';" +
                    "    snowflake.style.animationDelay = Math.random() * 5 + 's';" +
                    "    snowflake.style.opacity = Math.random() * 0.6 + 0.3;" +
                    "    snowflake.style.fontSize = (Math.random() * 0.8 + 0.5) + 'em';" +
                    "    snowflake.style.animation = (i % 2 === 0 ? 'snowfall' : 'snowfall2') + ' ' + snowflake.style.animationDuration + ' linear infinite';" +
                    "    snowflake.style.animationDelay = snowflake.style.animationDelay;" +
                    "    loginContainer.appendChild(snowflake);" +
                    "  }" +

                    // Add Christmas ornaments inside container
                    "  const ornaments = ['⭐', '🔔', '🎄', '🎅', '🎁', '🕯️', '🌟'];" +
                    "  for(let i = 0; i < 12; i++) {" +
                    "    const ornament = document.createElement('div');" +
                    "    ornament.classList.add('container-ornament');" +
                    "    ornament.style.fontSize = (Math.random() * 1.2 + 0.8) + 'em';" +
                    "    ornament.style.left = Math.random() * 100 + '%';" +
                    "    ornament.style.top = Math.random() * 100 + '%';" +
                    "    ornament.innerHTML = ornaments[Math.floor(Math.random() * ornaments.length)];" +
                    "    loginContainer.appendChild(ornament);" +
                    "  }" +
                    "}, 100);"
                );
            });
        });
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
                // Record login trace
                traceService.recordLogin(user);

                // Update user activity
                userActivityService.updateActivity(user, "LOGIN", "login");

                Notification.show(translationService.translate("login.welcomeback", user.getName()), 3000, Notification.Position.BOTTOM_END)
                    .addThemeVariants(NotificationVariant.LUMO_SUCCESS);
            }

            // Check if there's a saved redirect URL
            String redirectUrl = (String) VaadinSession.getCurrent().getAttribute("redirectAfterLogin");
            if (redirectUrl != null) {
                // Clear the saved URL
                VaadinSession.getCurrent().setAttribute("redirectAfterLogin", null);
                // Force full page reload to refresh menu with correct user
                getUI().ifPresent(ui -> ui.getPage().setLocation("/" + redirectUrl));
            } else {
                // Force full page reload to refresh menu with correct user
                getUI().ifPresent(ui -> ui.getPage().setLocation("/"));
            }
        } else {
            loginForm.setError(true);
            Notification.show(translationService.translate("login.error.message"), 3000, Notification.Position.MIDDLE)
                .addThemeVariants(NotificationVariant.LUMO_ERROR);
        }
    }

    private Button createOAuthButton(String providerName, String color, VaadinIcon icon) {
        Button button = new Button();
        button.setIcon(new Icon(icon));
        button.addThemeVariants(ButtonVariant.LUMO_PRIMARY);
        button.getStyle()
            .set("background-color", color)
            .set("border", "none")
            .set("color", "white")
            .set("font-weight", "500")
            .set("min-width", "50px")
            .set("width", "50px")
            .set("height", "50px")
            .set("border-radius", "50%")
            .set("padding", "0");
        button.getElement().setAttribute("title", providerName);
        return button;
    }

    private HorizontalLayout createLanguageButtons() {
        HorizontalLayout layout = new HorizontalLayout();
        layout.setSpacing(true);
        layout.setJustifyContentMode(JustifyContentMode.CENTER);

        // French flag button
        frenchButton = createFlagButton("images/flags/fr.svg", "Français", Locale.FRENCH);

        // English flag button
        englishButton = createFlagButton("images/flags/gb.svg", "English", Locale.ENGLISH);

        // Italian flag button
        italianButton = createFlagButton("images/flags/it.svg", "Italiano", Locale.ITALIAN);

        // Highlight the current locale button
        Locale currentLocale = translationService.getCurrentLocale();
        highlightSelectedButton(frenchButton, currentLocale.getLanguage().equals("fr"));
        highlightSelectedButton(englishButton, currentLocale.getLanguage().equals("en"));
        highlightSelectedButton(italianButton, currentLocale.getLanguage().equals("it"));

        layout.add(frenchButton, englishButton, italianButton);
        return layout;
    }

    private void highlightSelectedButton(Button button, boolean isSelected) {
        if (isSelected) {
            button.getStyle()
                    .set("background-color", "#e3f2fd")
                    .set("box-shadow", "0 0 0 2px #2196F3")
                    .set("transform", "scale(1.05)");
        } else {
            button.getStyle()
                    .remove("background-color")
                    .remove("box-shadow")
                    .remove("transform");
        }
    }

    private Button createFlagButton(String imagePath, String alt, Locale locale) {
        Button button = new Button();
        button.addThemeVariants(ButtonVariant.LUMO_SMALL, ButtonVariant.LUMO_TERTIARY);

        // Create flag image (reduced size by half)
        Image flagImage = new Image(imagePath, alt);
        flagImage.setWidth("16px");
        flagImage.setHeight("12px");
        flagImage.getStyle()
                .set("border", "1px solid #ccc")
                .set("border-radius", "2px")
                .set("display", "block");

        button.getElement().appendChild(flagImage.getElement());

        button.getStyle()
                .set("padding", "2px 4px")
                .set("min-width", "24px")
                .set("cursor", "pointer")
                .set("transition", "all 0.2s ease");

        button.addClickListener(event -> {
            translationService.setLocale(locale);
            // Update highlighting for all buttons
            highlightSelectedButton(frenchButton, locale.getLanguage().equals("fr"));
            highlightSelectedButton(englishButton, locale.getLanguage().equals("en"));
            highlightSelectedButton(italianButton, locale.getLanguage().equals("it"));
            // Update login form labels
            configureLoginFormI18n();
        });

        return button;
    }

    private void configureLoginFormI18n() {
        LoginI18n i18n = LoginI18n.createDefault();

        LoginI18n.Form form = i18n.getForm();
        form.setTitle(translationService.translate("login.title"));
        form.setUsername(translationService.translate("login.email"));
        form.setPassword(translationService.translate("login.password"));
        form.setSubmit(translationService.translate("login.signin"));
        form.setForgotPassword(translationService.translate("login.forgotpassword"));

        LoginI18n.ErrorMessage errorMessage = i18n.getErrorMessage();
        errorMessage.setTitle(translationService.translate("login.error.title"));
        errorMessage.setMessage(translationService.translate("login.error.message"));

        loginForm.setI18n(i18n);
    }

    private void showPublicAvatarDialog() {
        Dialog dialog = new Dialog();
        dialog.setHeaderTitle(translationService.translate("login.selectpublicavatar"));
        dialog.setWidth("800px");
        dialog.setHeight("600px");

        // Load public users
        List<User> publicUsers = userService.listPublicUsers(Pageable.ofSize(100));
        logger.info("Loading public avatars dialog - found {} public users", publicUsers.size());

        // Create a flex layout to display avatars as a grid
        FlexLayout avatarGrid = new FlexLayout();
        avatarGrid.setFlexWrap(FlexLayout.FlexWrap.WRAP);
        avatarGrid.getStyle()
            .set("gap", "10px")
            .set("padding", "10px")
            .set("justify-content", "center");

        for (User user : publicUsers) {
            logger.info("Creating avatar card for user: {} - hasPhoto: {}, hasCountry: {}",
                user.getName(),
                user.getPhotoBytes() != null && user.getPhotoBytes().length > 0,
                user.getCountry() != null);
            VerticalLayout avatarCard = createAvatarCard(user, dialog);
            avatarGrid.add(avatarCard);
        }

        // Make it scrollable
        Div scrollContainer = new Div(avatarGrid);
        scrollContainer.getStyle()
            .set("overflow-y", "auto")
            .set("max-height", "500px");

        Button cancelButton = new Button(translationService.translate("login.cancel"), event -> dialog.close());
        cancelButton.addThemeVariants(ButtonVariant.LUMO_TERTIARY);

        dialog.add(scrollContainer);
        dialog.getFooter().add(cancelButton);
        dialog.open();
    }

    private VerticalLayout createAvatarCard(User user, Dialog dialog) {
        VerticalLayout card = new VerticalLayout();
        card.setWidth("80px");
        card.setAlignItems(Alignment.CENTER);
        card.setSpacing(false);
        card.setPadding(false);
        card.getStyle()
            .set("cursor", "pointer")
            .set("border-radius", "8px")
            .set("padding", "8px")
            .set("transition", "all 0.2s");

        // Avatar image
        Div avatarContainer = new Div();
        avatarContainer.getStyle()
            .set("width", "60px")
            .set("height", "60px")
            .set("border-radius", "50%")
            .set("overflow", "hidden")
            .set("box-shadow", "0 2px 8px rgba(0,0,0,0.15)");

        if (user.getPhotoBytes() != null && user.getPhotoBytes().length > 0) {
            StreamResource imageResource = new StreamResource(
                user.getName() + ".jpg",
                () -> new ByteArrayInputStream(user.getPhotoBytes())
            );
            Image avatarImage = new Image(imageResource, user.getName());
            avatarImage.setWidth("100%");
            avatarImage.setHeight("100%");
            avatarImage.getStyle().set("object-fit", "cover");
            avatarContainer.add(avatarImage);
        } else {
            // Add a placeholder if no photo
            logger.warn("No photo found for user: {}", user.getName());
            Div placeholder = new Div();
            placeholder.setText(user.getName().substring(0, 1));
            placeholder.getStyle()
                .set("width", "100%")
                .set("height", "100%")
                .set("display", "flex")
                .set("align-items", "center")
                .set("justify-content", "center")
                .set("background-color", "#e0e0e0")
                .set("font-size", "24px")
                .set("font-weight", "bold")
                .set("color", "#666");
            avatarContainer.add(placeholder);
        }

        card.add(avatarContainer);

        // Add country flag if available
        if (user.getCountry() != null) {
            String flagSvg = user.getCountry().getCountryFlag();
            if (flagSvg != null && !flagSvg.isEmpty()) {
                Div flagContainer = new Div();
                flagContainer.getStyle()
                    .set("width", "30px")
                    .set("height", "20px")
                    .set("display", "flex")
                    .set("align-items", "center")
                    .set("justify-content", "center")
                    .set("border", "1px solid #e0e0e0")
                    .set("border-radius", "2px")
                    .set("margin-top", "4px")
                    .set("box-shadow", "0 1px 3px rgba(0,0,0,0.1)");

                // Create StreamResource from SVG content
                StreamResource flagResource = new StreamResource("flag.svg",
                    () -> new ByteArrayInputStream(flagSvg.getBytes(java.nio.charset.StandardCharsets.UTF_8)));
                flagResource.setContentType("image/svg+xml");

                Image flagImage = new Image(flagResource, "Country flag");
                flagImage.setWidth("30px");
                flagImage.setHeight("20px");
                flagImage.getStyle()
                    .set("object-fit", "contain");

                flagContainer.add(flagImage);
                card.add(flagContainer);
            }
        }

        // User name
        Span nameLabel = new Span(user.getName());
        nameLabel.getStyle()
            .set("font-size", "10px")
            .set("text-align", "center")
            .set("max-width", "80px")
            .set("overflow", "hidden")
            .set("text-overflow", "ellipsis")
            .set("white-space", "nowrap");

        card.add(nameLabel);

        // Hover effect
        card.addClickListener(event -> {
            // Login with this public user
            boolean authenticated = authenticationService.authenticate(user.getEmail(), "public123");
            if (authenticated) {
                // Record login trace
                traceService.recordLogin(user);

                // Update user activity
                userActivityService.updateActivity(user, "LOGIN", "login");

                Notification.show(translationService.translate("login.welcome", user.getName()), 3000, Notification.Position.BOTTOM_END)
                    .addThemeVariants(NotificationVariant.LUMO_SUCCESS);
                dialog.close();

                // Check if there's a saved redirect URL
                String redirectUrl = (String) VaadinSession.getCurrent().getAttribute("redirectAfterLogin");
                if (redirectUrl != null) {
                    // Clear the saved URL
                    VaadinSession.getCurrent().setAttribute("redirectAfterLogin", null);
                    // Force full page reload to refresh menu with correct user
                    getUI().ifPresent(ui -> ui.getPage().setLocation("/" + redirectUrl));
                } else {
                    // Force full page reload to refresh menu with correct user
                    getUI().ifPresent(ui -> ui.getPage().setLocation("/"));
                }
            } else {
                Notification.show(translationService.translate("login.authenticationfailed"), 3000, Notification.Position.MIDDLE)
                    .addThemeVariants(NotificationVariant.LUMO_ERROR);
            }
        });

        card.getElement().addEventListener("mouseenter", e -> {
            card.getStyle()
                .set("background-color", "#f5f5f5")
                .set("transform", "scale(1.05)");
        });

        card.getElement().addEventListener("mouseleave", e -> {
            card.getStyle()
                .set("background-color", "transparent")
                .set("transform", "scale(1)");
        });

        return card;
    }
}
