package com.quizz.base.ui;

import com.quizz.core.entity.User;
import com.quizz.core.service.TranslationService;
import com.vaadin.flow.component.UI;
import com.vaadin.flow.component.applayout.AppLayout;
import com.vaadin.flow.component.button.Button;
import com.vaadin.flow.component.button.ButtonVariant;
import com.vaadin.flow.component.html.Div;
import com.vaadin.flow.component.html.Span;
import com.vaadin.flow.component.icon.Icon;
import com.vaadin.flow.component.icon.VaadinIcon;
import com.vaadin.flow.component.orderedlayout.HorizontalLayout;
import com.vaadin.flow.component.orderedlayout.Scroller;
import com.vaadin.flow.component.sidenav.SideNav;
import com.vaadin.flow.component.sidenav.SideNavItem;
import com.vaadin.flow.router.Layout;
import com.vaadin.flow.server.VaadinSession;
import com.vaadin.flow.server.menu.MenuConfiguration;
import com.vaadin.flow.server.menu.MenuEntry;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

import static com.vaadin.flow.theme.lumo.LumoUtility.*;
import static org.atmosphere.annotation.AnnotationUtil.logger;

@Layout
public final class MainLayout extends AppLayout {

    private final TranslationService translationService;

    // Keep references to refresh labels on locale change
    private SideNav sideNav;
    private List<MenuEntry> menuEntries = new ArrayList<>();

    MainLayout(@Autowired TranslationService translationService) {
        this.translationService = translationService;
        setPrimarySection(Section.DRAWER);
        addToDrawer(createHeader(), new Scroller(createSideNav()), createFooter());
    }

    private Div createHeader() {
        // TODO Replace with real application logo and name
        var appLogo = VaadinIcon.CUBES.create();
        appLogo.addClassNames(TextColor.PRIMARY, IconSize.LARGE);

        Span appNameSpan = new Span("Quizz1");
        appNameSpan.addClassNames(FontWeight.SEMIBOLD, FontSize.LARGE);

        var header = new Div(appLogo, appNameSpan);
        header.addClassNames(Display.FLEX, Padding.MEDIUM, Gap.MEDIUM, AlignItems.CENTER);
        return header;
    }

    private SideNav createSideNav() {
        sideNav = new SideNav();
        sideNav.addClassNames(Margin.Horizontal.MEDIUM);
        menuEntries = MenuConfiguration.getMenuEntries();
        menuEntries.forEach(entry -> logger.info("Menu Entry:" + entry.title()));
        sideNav.removeAll();
        menuEntries.forEach(entry -> sideNav.addItem(createSideNavItem(entry)));
        return sideNav;
    }

    private SideNavItem createSideNavItem(MenuEntry menuEntry) {
        // Translate menu title
        String translatedTitle = translationService.translate(menuEntry.title());

        if (menuEntry.icon() != null) {
            return new SideNavItem(translatedTitle, menuEntry.path(), new Icon(menuEntry.icon()));
        } else {
            return new SideNavItem(translatedTitle, menuEntry.path());
        }
    }

    private void refreshTranslations() {
        // Rebuild side nav items with translated titles
        if (sideNav != null) {
            sideNav.removeAll();
            menuEntries.forEach(entry -> sideNav.addItem(createSideNavItem(entry)));
        }

        // Trigger a light refresh
        getUI().ifPresent(UI::push);
    }

    private Div createFooter() {
        Div footer = new Div();
        footer.addClassNames(Padding.MEDIUM, Display.FLEX, FlexDirection.COLUMN, Gap.SMALL);

        // Get current user from session
        User currentUser = VaadinSession.getCurrent().getAttribute(User.class);

        if (currentUser != null) {
            // Language flags
            HorizontalLayout languageButtons = createLanguageButtons();
            languageButtons.addClassNames(JustifyContent.CENTER, Margin.Bottom.SMALL);

            // User info
            Span userInfo = new Span(translationService.translate("app.loggedinas"));
            userInfo.addClassNames(FontSize.SMALL, TextColor.SECONDARY);

            Span userName = new Span(currentUser.getName());
            userName.addClassNames(FontSize.SMALL, FontWeight.SEMIBOLD);

            // Logout button
            Button logoutButton = new Button(translationService.translate("app.logout"), VaadinIcon.SIGN_OUT.create());
            logoutButton.addThemeVariants(ButtonVariant.LUMO_TERTIARY, ButtonVariant.LUMO_ERROR);
            logoutButton.addClassNames(Width.FULL);
            logoutButton.addClickListener(event -> {
                VaadinSession.getCurrent().getSession().invalidate();
                VaadinSession.getCurrent().close();
                getUI().ifPresent(ui -> ui.getPage().setLocation("login"));
            });

            footer.add(languageButtons, userInfo, userName, logoutButton);
        }

        return footer;
    }

    private HorizontalLayout createLanguageButtons() {
        HorizontalLayout layout = new HorizontalLayout();
        layout.setSpacing(true);
        layout.addClassNames(Gap.SMALL);

        // French flag button
        Button frenchButton = createFlagButton("images/flags/fr.svg", "Français", Locale.FRENCH);

        // English flag button (avoid deprecated constructor)
        Button englishButton = createFlagButton("images/flags/gb.svg", "English", Locale.ENGLISH);

        // Italian flag button
        Button italianButton = createFlagButton("images/flags/it.svg", "Italiano", Locale.ITALIAN);

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

        // Create flag image
        com.vaadin.flow.component.html.Image flagImage = new com.vaadin.flow.component.html.Image(imagePath, alt);
        flagImage.setWidth("32px");
        flagImage.setHeight("24px");
        flagImage.getStyle()
                .set("border", "1px solid #ccc")
                .set("border-radius", "2px")
                .set("display", "block");

        button.getElement().appendChild(flagImage.getElement());

        button.getStyle()
                .set("padding", "4px 8px")
                .set("min-width", "40px")
                .set("cursor", "pointer")
                .set("transition", "all 0.2s ease");

        button.addClickListener(event -> {
            translationService.setLocale(locale);
            // Refresh side nav and any translated labels in layout
            highlightSelectedButton(button, true);
            refreshTranslations();
        });

        return button;
    }

}
