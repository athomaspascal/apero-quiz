package com.quizz.base.ui;

import com.quizz.core.entity.User;
import com.quizz.core.service.TranslationService;
import com.vaadin.flow.component.AttachEvent;
import com.vaadin.flow.component.applayout.AppLayout;
import com.vaadin.flow.component.button.Button;
import com.vaadin.flow.component.button.ButtonVariant;
import com.vaadin.flow.component.html.Div;
import com.vaadin.flow.component.html.Span;
import com.vaadin.flow.component.icon.Icon;
import com.vaadin.flow.component.icon.VaadinIcon;
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

import static com.vaadin.flow.theme.lumo.LumoUtility.*;
import static org.atmosphere.annotation.AnnotationUtil.logger;

@Layout
public final class MainLayout extends AppLayout {

    private final TranslationService translationService;

    // Keep references to refresh labels on locale change
    private SideNav sideNav;
    private List<MenuEntry> menuEntries = new ArrayList<>();
    private Scroller sideNavScroller;
    private Div footerDiv;

    MainLayout(@Autowired TranslationService translationService) {
        this.translationService = translationService;
        setPrimarySection(Section.DRAWER);
        // Don't create menu here - it will be created in onAttach() with correct user
        logger.info("MainLayout constructor called");
    }

    @Override
    protected void onAttach(AttachEvent attachEvent) {
        super.onAttach(attachEvent);
        logger.info("MainLayout onAttach() called - creating/refreshing menu");
        // Create or refresh the menu when the layout is attached to ensure current user state
        if (sideNavScroller == null) {
            // First time - create everything
            logger.info("First attach - creating menu from scratch");
            footerDiv = createFooter();
            sideNavScroller = new Scroller(createSideNav());
            addToDrawer(createHeader(), sideNavScroller, footerDiv);
        } else {
            // Subsequent attach - refresh menu
            logger.info("Subsequent attach - refreshing menu");
            refreshMenu();
        }
    }

    public void refreshMenu() {
        logger.info("refreshMenu() called - rebuilding side navigation");
        // Remove old sidenav and footer
        remove(sideNavScroller);
        remove(footerDiv);

        // Recreate them with current user state
        sideNavScroller = new Scroller(createSideNav());
        footerDiv = createFooter();

        // Add them back
        addToDrawer(sideNavScroller, footerDiv);
        logger.info("refreshMenu() completed");
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
        menuEntries.forEach(entry -> logger.info("Menu Entry: title=" + entry.title() + ", path=" + entry.path()));
        sideNav.removeAll();

        // Get current user from session
        User currentUser = VaadinSession.getCurrent().getAttribute(User.class);
        boolean isAdmin = currentUser != null && currentUser.isAdmin();

        logger.info("=== createSideNav called ===");
        logger.info("Current user: " + (currentUser != null ? currentUser.getName() : "null") + ", isAdmin: " + isAdmin);
        logger.info("Current user isPublic: " + (currentUser != null ? currentUser.isPublic() : "n/a"));

        // Filter menu entries based on user role
        menuEntries.forEach(entry -> {
            String path = entry.path();
            String title = entry.title();

            // Admin-only menus - check both path and title
            boolean isAdminMenu = "users".equals(path)
                || "question-logs".equals(path)
                || "admin/quiz-editor".equals(path)
                || "dashboard".equals(path)
                || "menu.users".equals(title)
                || "menu.questionlogs".equals(title)
                || "menu.editquizzes".equals(title)
                || "menu.dashboard".equals(title);

            boolean willBeAdded = !isAdminMenu || isAdmin;
            logger.info("Menu: path='" + path + "', title='" + title + "', isAdminMenu=" + isAdminMenu + ", isAdmin=" + isAdmin + ", willBeAdded=" + willBeAdded);

            // Add menu item only if user is admin or menu is not admin-only
            if (willBeAdded) {
                logger.info("  -> ADDING menu: " + title);
                sideNav.addItem(createSideNavItem(entry));
            } else {
                logger.info("  -> SKIPPING menu: " + title);
            }
        });

        logger.info("=== createSideNav finished ===");
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


    private Div createFooter() {
        Div footer = new Div();
        footer.addClassNames(Padding.MEDIUM, Display.FLEX, FlexDirection.COLUMN, Gap.SMALL);

        // Get current user from session
        User currentUser = VaadinSession.getCurrent().getAttribute(User.class);

        if (currentUser != null) {
            // User info
            Span userInfo = new Span(translationService.translate("app.loggedinas"));
            userInfo.addClassNames(FontSize.SMALL, TextColor.SECONDARY);

            // User name with flag
            com.vaadin.flow.component.orderedlayout.HorizontalLayout userNameLayout = new com.vaadin.flow.component.orderedlayout.HorizontalLayout();
            userNameLayout.setSpacing(true);
            userNameLayout.setAlignItems(com.vaadin.flow.component.orderedlayout.FlexComponent.Alignment.CENTER);
            userNameLayout.getStyle().set("gap", "8px");

            // Display country flag if available
            if (currentUser.getCountry() != null && currentUser.getCountry().getCountryFlag() != null && !currentUser.getCountry().getCountryFlag().isEmpty()) {
                Div flagContainer = new Div();
                flagContainer.getStyle()
                    .set("width", "20px")
                    .set("height", "14px")
                    .set("display", "inline-flex")
                    .set("align-items", "center")
                    .set("justify-content", "center")
                    .set("border", "1px solid #e0e0e0")
                    .set("border-radius", "2px")
                    .set("flex-shrink", "0");

                // Embed SVG directly as HTML
                flagContainer.getElement().setProperty("innerHTML", currentUser.getCountry().getCountryFlag());

                userNameLayout.add(flagContainer);
            }

            Span userName = new Span(currentUser.getName());
            userName.addClassNames(FontSize.SMALL, FontWeight.SEMIBOLD);
            userNameLayout.add(userName);

            // Logout button
            Button logoutButton = new Button(translationService.translate("app.logout"), VaadinIcon.SIGN_OUT.create());
            logoutButton.addThemeVariants(ButtonVariant.LUMO_TERTIARY, ButtonVariant.LUMO_ERROR);
            logoutButton.addClassNames(Width.FULL);
            logoutButton.addClickListener(event -> {
                VaadinSession.getCurrent().getSession().invalidate();
                VaadinSession.getCurrent().close();
                getUI().ifPresent(ui -> ui.getPage().setLocation("login"));
            });

            footer.add(userInfo, userNameLayout, logoutButton);
        }

        return footer;
    }


}
