package com.quizz.core.ui;

import com.quizz.core.service.TranslationService;
import com.vaadin.flow.component.button.Button;
import com.vaadin.flow.component.button.ButtonVariant;
import com.vaadin.flow.component.html.*;
import com.vaadin.flow.component.orderedlayout.FlexComponent;
import com.vaadin.flow.component.orderedlayout.HorizontalLayout;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import com.vaadin.flow.router.PageTitle;
import com.vaadin.flow.router.Route;
import com.vaadin.flow.server.auth.AnonymousAllowed;

import java.util.Locale;

/**
 * Public welcome page that visitors can see without logging in.
 * Displays a fun quiz-themed welcome screen with a call-to-action to login.
 */
@Route("welcome")
@PageTitle("Welcome to Quiz!")
@AnonymousAllowed
public class WelcomeView extends VerticalLayout {

    private final TranslationService translationService;

    // Language flag buttons
    private Button frenchButton;
    private Button englishButton;
    private Button italianButton;

    // Components that need translation update
    private H2 subtitle;
    private Paragraph description;
    private Div featuresDiv;
    private Button loginButton;
    private Button registerButton;
    private Paragraph footerMessage;
    private Span languageLabel;

    public WelcomeView(TranslationService translationService) {
        this.translationService = translationService;

        setSizeFull();
        setAlignItems(FlexComponent.Alignment.CENTER);
        setJustifyContentMode(FlexComponent.JustifyContentMode.CENTER);
        setPadding(true);
        setSpacing(true);

        // Apply gradient background
        getStyle()
            .set("background", "linear-gradient(135deg, #667eea 0%, #764ba2 100%)")
            .set("min-height", "100vh");

        // Main content container
        Div contentContainer = new Div();
        contentContainer.getStyle()
            .set("background", "rgba(255, 255, 255, 0.95)")
            .set("padding", "40px")
            .set("border-radius", "20px")
            .set("box-shadow", "0 10px 40px rgba(0,0,0,0.3)")
            .set("text-align", "center")
            .set("max-width", "600px")
            .set("width", "90%");

        // Fun title with emoji
        H1 title = new H1("🎯 Quizz Time! 🧠");
        title.getStyle()
            .set("font-size", "3rem")
            .set("margin-bottom", "10px")
            .set("background", "linear-gradient(135deg, #667eea, #764ba2)")
            .set("-webkit-background-clip", "text")
            .set("-webkit-text-fill-color", "transparent")
            .set("background-clip", "text");

        // Subtitle
        subtitle = new H2(translationService.translate("welcome.subtitle"));
        subtitle.getStyle()
            .set("color", "#666")
            .set("font-weight", "normal")
            .set("font-size", "1.3rem")
            .set("margin-top", "0");

        // Quiz image
        Image quizImage = new Image("images/quiz-welcome.svg", "Quiz illustration");
        quizImage.setWidth("300px");
        quizImage.setHeight("225px");
        quizImage.getStyle()
            .set("margin", "20px auto")
            .set("display", "block");

        // Description with fun text
        description = new Paragraph(translationService.translate("welcome.description"));
        description.getStyle()
            .set("color", "#555")
            .set("font-size", "1.1rem")
            .set("line-height", "1.6")
            .set("margin-bottom", "25px");

        // Features list
        featuresDiv = new Div();
        featuresDiv.getStyle()
            .set("display", "flex")
            .set("justify-content", "center")
            .set("flex-wrap", "wrap")
            .set("gap", "15px")
            .set("margin-bottom", "30px");

        updateFeatures();

        // Buttons
        HorizontalLayout buttonLayout = new HorizontalLayout();
        buttonLayout.setSpacing(true);
        buttonLayout.setJustifyContentMode(FlexComponent.JustifyContentMode.CENTER);
        buttonLayout.setWidthFull();

        loginButton = new Button(translationService.translate("welcome.login"));
        loginButton.addThemeVariants(ButtonVariant.LUMO_PRIMARY);
        loginButton.getStyle()
            .set("background", "linear-gradient(135deg, #667eea 0%, #764ba2 100%)")
            .set("color", "white")
            .set("font-size", "0.9rem")
            .set("padding", "10px 20px")
            .set("border-radius", "20px")
            .set("cursor", "pointer");
        loginButton.addClickListener(e -> getUI().ifPresent(ui -> ui.navigate("login")));

        registerButton = new Button(translationService.translate("welcome.register"));
        registerButton.getStyle()
            .set("background", "white")
            .set("color", "#667eea")
            .set("border", "2px solid #667eea")
            .set("font-size", "0.9rem")
            .set("padding", "10px 20px")
            .set("border-radius", "20px")
            .set("cursor", "pointer");
        registerButton.addClickListener(e -> getUI().ifPresent(ui -> ui.navigate("register")));

        buttonLayout.add(loginButton, registerButton);

        // Language flags below buttons
        HorizontalLayout flagsLayout = createLanguageFlags();

        // Label for language selection
        languageLabel = new Span(translationService.translate("welcome.selectlanguage"));
        languageLabel.getStyle()
            .set("color", "#888")
            .set("font-size", "0.85rem")
            .set("margin-top", "20px")
            .set("display", "block");

        // Fun footer message
        footerMessage = new Paragraph("🎉 " + translationService.translate("welcome.footer") + " 🎉");
        footerMessage.getStyle()
            .set("color", "#888")
            .set("font-size", "0.9rem")
            .set("margin-top", "25px")
            .set("font-style", "italic");

        // Add all to container
        contentContainer.add(title, subtitle, quizImage, description, featuresDiv, buttonLayout, languageLabel, flagsLayout, footerMessage);

        add(contentContainer);
    }

    private void updateFeatures() {
        featuresDiv.removeAll();

        String[] features = {
            "🏆 " + translationService.translate("welcome.feature.compete"),
            "👥 " + translationService.translate("welcome.feature.friends"),
            "🎮 " + translationService.translate("welcome.feature.duel"),
            "📚 " + translationService.translate("welcome.feature.topics")
        };

        for (String feature : features) {
            Span featureSpan = new Span(feature);
            featureSpan.getStyle()
                .set("background", "#f0f4ff")
                .set("padding", "8px 15px")
                .set("border-radius", "20px")
                .set("font-size", "0.95rem")
                .set("color", "#444");
            featuresDiv.add(featureSpan);
        }
    }

    private HorizontalLayout createLanguageFlags() {
        HorizontalLayout layout = new HorizontalLayout();
        layout.setSpacing(true);
        layout.setJustifyContentMode(FlexComponent.JustifyContentMode.CENTER);
        layout.getStyle()
            .set("margin-top", "10px");

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

    private Button createFlagButton(String imagePath, String alt, Locale locale) {
        Button button = new Button();
        button.addThemeVariants(ButtonVariant.LUMO_SMALL, ButtonVariant.LUMO_TERTIARY);

        // Create flag image
        Image flagImage = new Image(imagePath, alt);
        flagImage.setWidth("32px");
        flagImage.setHeight("24px");
        flagImage.getStyle()
            .set("border", "1px solid #ccc")
            .set("border-radius", "4px")
            .set("display", "block");

        button.getElement().appendChild(flagImage.getElement());

        button.getStyle()
            .set("padding", "4px 8px")
            .set("min-width", "40px")
            .set("cursor", "pointer")
            .set("transition", "all 0.2s ease");

        button.addClickListener(event -> {
            translationService.setLocale(locale);
            // Update highlighting for all buttons
            highlightSelectedButton(frenchButton, locale.getLanguage().equals("fr"));
            highlightSelectedButton(englishButton, locale.getLanguage().equals("en"));
            highlightSelectedButton(italianButton, locale.getLanguage().equals("it"));
            // Update all translated content
            updateTranslations();
        });

        return button;
    }

    private void highlightSelectedButton(Button button, boolean isSelected) {
        if (isSelected) {
            button.getStyle()
                .set("background-color", "#e3f2fd")
                .set("box-shadow", "0 0 0 2px #2196F3")
                .set("transform", "scale(1.1)");
        } else {
            button.getStyle()
                .remove("background-color")
                .remove("box-shadow")
                .remove("transform");
        }
    }

    private void updateTranslations() {
        subtitle.setText(translationService.translate("welcome.subtitle"));
        description.setText(translationService.translate("welcome.description"));
        loginButton.setText(translationService.translate("welcome.login"));
        registerButton.setText(translationService.translate("welcome.register"));
        footerMessage.setText("🎉 " + translationService.translate("welcome.footer") + " 🎉");
        languageLabel.setText(translationService.translate("welcome.selectlanguage"));
        updateFeatures();
    }
}

