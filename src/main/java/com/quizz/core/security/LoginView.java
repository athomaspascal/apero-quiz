package com.quizz.core.security;

import com.quizz.core.entity.User;
import com.vaadin.flow.component.button.Button;
import com.vaadin.flow.component.button.ButtonVariant;
import com.vaadin.flow.component.html.*;
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

        H3 title = new H3("🎄 Quiz Application 🎄");
        title.getStyle()
            .set("color", "#ffffff")
            .set("text-shadow", "2px 2px 4px rgba(0,0,0,0.5)")
            .set("margin-bottom", "0")
            .set("z-index", "10")
            .set("position", "relative");
/*
        Paragraph subtitle = new Paragraph("Sign in to continue");
        subtitle.getStyle()
            .set("color", "rgba(255, 255, 255, 0.9)")
            .set("margin-top", "0")
            .set("z-index", "10")
            .set("position", "relative");
*/
        Paragraph registerLink = new Paragraph();
        registerLink.add("Don't have an account? ");
        com.vaadin.flow.router.RouterLink registerRouterLink = new com.vaadin.flow.router.RouterLink("Sign up", RegisterView.class);
        registerLink.add(registerRouterLink);

        // OAuth2 buttons
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
        formWrapper.add(loginForm,registerLink);

        // Wrapper for OAuth section
        Div oauthWrapper = new Div();
        oauthWrapper.getStyle()
            .set("background", "rgba(255, 255, 255, 0.95)")
            .set("padding", "var(--lumo-space-m)")
            .set("border-radius", "var(--lumo-border-radius-m)")
            .set("width", "100%")
            .set("position", "relative")
            .set("z-index", "10");

        Span orText = new Span("Or sign in with");
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
        content.add(title,
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

