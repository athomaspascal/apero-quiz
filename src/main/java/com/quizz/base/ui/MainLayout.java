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
        footerDiv = createFooter();
        sideNavScroller = new Scroller(createSideNav());
        addToDrawer(createHeader(), sideNavScroller, footerDiv);
    }

    @Override
    protected void onAttach(AttachEvent attachEvent) {
        super.onAttach(attachEvent);
        // Refresh the menu when the layout is attached to ensure current user state
        refreshMenu();
    }

    private void refreshMenu() {
        // Remove old sidenav and footer
        remove(sideNavScroller);
        remove(footerDiv);

        // Recreate them with current user state
        sideNavScroller = new Scroller(createSideNav());
        footerDiv = createFooter();

        // Add them back
        addToDrawer(sideNavScroller, footerDiv);
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

        logger.info("Current user: " + (currentUser != null ? currentUser.getName() : "null") + ", isAdmin: " + isAdmin);

        // Filter menu entries based on user role
        menuEntries.forEach(entry -> {
            String path = entry.path();

            // Admin-only menus
            boolean isAdminMenu = "users".equals(path)
                || "question-logs".equals(path)
                || "admin/quiz-editor".equals(path);

            logger.info("Menu path=" + path + ", isAdminMenu=" + isAdminMenu + ", willBeAdded=" + (!isAdminMenu || isAdmin));

            // Add menu item only if user is admin or menu is not admin-only
            if (!isAdminMenu || isAdmin) {
                sideNav.addItem(createSideNavItem(entry));
            }
        });

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

            footer.add(userInfo, userName, logoutButton);
        }

        return footer;
    }


}
