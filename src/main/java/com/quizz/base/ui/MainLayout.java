package com.quizz.base.ui;

import com.quizz.examplefeature.User;
import com.vaadin.flow.component.applayout.AppLayout;
import com.vaadin.flow.component.button.Button;
import com.vaadin.flow.component.button.ButtonVariant;
import com.vaadin.flow.component.html.Div;
import com.vaadin.flow.component.html.Span;
import com.vaadin.flow.component.icon.Icon;
import com.vaadin.flow.component.icon.VaadinIcon;
import com.vaadin.flow.component.orderedlayout.FlexComponent;
import com.vaadin.flow.component.orderedlayout.HorizontalLayout;
import com.vaadin.flow.component.orderedlayout.Scroller;
import com.vaadin.flow.component.sidenav.SideNav;
import com.vaadin.flow.component.sidenav.SideNavItem;
import com.vaadin.flow.router.Layout;
import com.vaadin.flow.server.VaadinSession;
import com.vaadin.flow.server.menu.MenuConfiguration;
import com.vaadin.flow.server.menu.MenuEntry;

import java.util.List;

import static com.vaadin.flow.theme.lumo.LumoUtility.*;
import static org.atmosphere.annotation.AnnotationUtil.logger;

@Layout
public final class MainLayout extends AppLayout {

    MainLayout() {
        setPrimarySection(Section.DRAWER);
        addToDrawer(createHeader(), new Scroller(createSideNav()), createFooter());
    }

    private Div createHeader() {
        // TODO Replace with real application logo and name
        var appLogo = VaadinIcon.CUBES.create();
        appLogo.addClassNames(TextColor.PRIMARY, IconSize.LARGE);

        var appName = new Span("Quizz1");
        appName.addClassNames(FontWeight.SEMIBOLD, FontSize.LARGE);

        var header = new Div(appLogo, appName);
        header.addClassNames(Display.FLEX, Padding.MEDIUM, Gap.MEDIUM, AlignItems.CENTER);
        return header;
    }

    private SideNav createSideNav() {
        var nav = new SideNav();
        nav.addClassNames(Margin.Horizontal.MEDIUM);
        List<MenuEntry> menuEntries = MenuConfiguration.getMenuEntries();
        menuEntries.forEach(entry -> {
            logger.info("Menu Entry:" + entry.title() );
        });
        ;
        menuEntries.forEach(entry -> nav.addItem(createSideNavItem(entry)));
        return nav;
    }

    private SideNavItem createSideNavItem(MenuEntry menuEntry) {
        if (menuEntry.icon() != null) {
            return new SideNavItem(menuEntry.title(), menuEntry.path(), new Icon(menuEntry.icon()));
        } else {
            return new SideNavItem(menuEntry.title(), menuEntry.path());
        }
    }

    private Div createFooter() {
        Div footer = new Div();
        footer.addClassNames(Padding.MEDIUM, Display.FLEX, FlexDirection.COLUMN, Gap.SMALL);

        // Get current user from session
        User currentUser = VaadinSession.getCurrent().getAttribute(User.class);

        if (currentUser != null) {
            // User info
            Span userInfo = new Span("Logged in as:");
            userInfo.addClassNames(FontSize.SMALL, TextColor.SECONDARY);

            Span userName = new Span(currentUser.getName());
            userName.addClassNames(FontSize.SMALL, FontWeight.SEMIBOLD);

            // Logout button
            Button logoutButton = new Button("Logout", VaadinIcon.SIGN_OUT.create());
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
