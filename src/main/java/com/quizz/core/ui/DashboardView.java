package com.quizz.core.ui;

import com.quizz.base.ui.component.ViewToolbar;
import com.quizz.core.entity.PlayerTrace;
import com.quizz.core.entity.User;
import com.quizz.core.service.PlayerTraceService;
import com.quizz.core.service.TranslationService;
import com.vaadin.flow.component.Component;
import com.vaadin.flow.component.button.Button;
import com.vaadin.flow.component.button.ButtonVariant;
import com.vaadin.flow.component.grid.Grid;
import com.vaadin.flow.component.html.Div;
import com.vaadin.flow.component.html.H3;
import com.vaadin.flow.component.html.Paragraph;
import com.vaadin.flow.component.html.Span;
import com.vaadin.flow.component.icon.VaadinIcon;
import com.vaadin.flow.component.notification.Notification;
import com.vaadin.flow.component.notification.NotificationVariant;
import com.vaadin.flow.component.orderedlayout.HorizontalLayout;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import com.vaadin.flow.component.select.Select;
import com.vaadin.flow.data.renderer.ComponentRenderer;
import com.vaadin.flow.router.BeforeEnterEvent;
import com.vaadin.flow.router.BeforeEnterObserver;
import com.vaadin.flow.router.Menu;
import com.vaadin.flow.router.PageTitle;
import com.vaadin.flow.router.Route;
import com.vaadin.flow.server.VaadinSession;
import com.vaadin.flow.theme.lumo.LumoUtility;
import jakarta.annotation.security.RolesAllowed;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.time.format.DateTimeFormatter;
import java.util.List;
import java.util.Map;

@Route("dashboard")
@PageTitle("Dashboard")
@Menu(order = 5, icon = "vaadin:dashboard", title = "menu.dashboard")
@RolesAllowed("ADMIN")
public class DashboardView extends VerticalLayout implements BeforeEnterObserver {

    private static final Logger logger = LoggerFactory.getLogger(DashboardView.class);
    private static final DateTimeFormatter DATE_TIME_FORMATTER = DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm:ss");

    private final PlayerTraceService traceService;
    private final TranslationService translationService;

    private Select<Integer> timeRangeSelect;
    private Div statsContainer;
    private Grid<PlayerTrace> recentActivityGrid;

    public DashboardView(PlayerTraceService traceService, TranslationService translationService) {
        this.traceService = traceService;
        this.translationService = translationService;

        setPadding(true);
        setSpacing(true);
        addClassNames(LumoUtility.MaxWidth.SCREEN_LARGE, LumoUtility.Margin.Horizontal.AUTO);

        add(new ViewToolbar(translationService.translate("dashboard.title")));

        // Time range selector
        HorizontalLayout controlsLayout = createControlsLayout();
        add(controlsLayout);

        // Statistics cards
        statsContainer = new Div();
        statsContainer.addClassNames(
            LumoUtility.Display.FLEX,
            LumoUtility.Gap.MEDIUM,
            LumoUtility.FlexWrap.WRAP,
            LumoUtility.Margin.Bottom.LARGE
        );
        add(statsContainer);

        // Recent activity grid
        H3 recentActivityTitle = new H3(translationService.translate("dashboard.recentActivity"));
        add(recentActivityTitle);

        recentActivityGrid = createRecentActivityGrid();
        add(recentActivityGrid);

        // Load initial data
        refreshDashboard();
    }

    private HorizontalLayout createControlsLayout() {
        HorizontalLayout layout = new HorizontalLayout();
        layout.setAlignItems(HorizontalLayout.Alignment.CENTER);
        layout.addClassNames(LumoUtility.Margin.Bottom.MEDIUM);

        Span label = new Span(translationService.translate("dashboard.timeRange") + ":");
        label.getStyle().set("margin-right", "var(--lumo-space-s)");

        timeRangeSelect = new Select<>();
        timeRangeSelect.setItems(1, 6, 12, 24, 48, 168); // 1h, 6h, 12h, 24h, 48h, 1 week
        timeRangeSelect.setValue(24); // Default to 24 hours
        timeRangeSelect.setItemLabelGenerator(hours -> {
            if (hours < 24) {
                return hours + " " + translationService.translate("dashboard.hours");
            } else {
                int days = hours / 24;
                return days + " " + (days == 1 ? translationService.translate("dashboard.day") : translationService.translate("dashboard.days"));
            }
        });
        timeRangeSelect.addValueChangeListener(event -> refreshDashboard());

        Button refreshButton = new Button(translationService.translate("common.refresh"), VaadinIcon.REFRESH.create());
        refreshButton.addThemeVariants(ButtonVariant.LUMO_TERTIARY);
        refreshButton.addClickListener(event -> refreshDashboard());

        layout.add(label, timeRangeSelect, refreshButton);
        return layout;
    }

    private void refreshDashboard() {
        int hours = timeRangeSelect.getValue();
        logger.info("Refreshing dashboard for last {} hours", hours);

        statsContainer.removeAll();

        // Active users card
        Long activeUsersCount = traceService.countActiveUsers(hours);
        statsContainer.add(createStatCard(
            translationService.translate("dashboard.activeUsers"),
            String.valueOf(activeUsersCount),
            VaadinIcon.USERS,
            "var(--lumo-success-color)"
        ));

        // Quiz stats by mode
        Map<String, Long> modeStats = traceService.getQuizStatsByMode(hours);
        Long normalMode = modeStats.getOrDefault("NORMAL", 0L);
        Long teamMode = modeStats.getOrDefault("TEAM", 0L);
        Long totalQuizzes = normalMode + teamMode;

        statsContainer.add(createStatCard(
            translationService.translate("dashboard.totalQuizzes"),
            String.valueOf(totalQuizzes),
            VaadinIcon.PLAY,
            "var(--lumo-primary-color)"
        ));

        statsContainer.add(createStatCard(
            translationService.translate("dashboard.normalMode"),
            String.valueOf(normalMode),
            VaadinIcon.USER,
            "var(--lumo-contrast-60pct)"
        ));

        statsContainer.add(createStatCard(
            translationService.translate("dashboard.teamMode"),
            String.valueOf(teamMode),
            VaadinIcon.GROUP,
            "var(--lumo-error-color)"
        ));

        // Most played quizzes
        Map<String, Long> mostPlayed = traceService.getMostPlayedQuizzes(hours, 5);
        if (!mostPlayed.isEmpty()) {
            statsContainer.add(createMostPlayedCard(mostPlayed));
        }

        // Refresh recent activity grid
        List<PlayerTrace> recentTraces = traceService.getRecentQuizStarts(hours);
        recentActivityGrid.setItems(recentTraces);
    }

    private Component createStatCard(String title, String value, VaadinIcon icon, String color) {
        Div card = new Div();
        card.addClassNames(
            LumoUtility.Background.CONTRAST_5,
            LumoUtility.BorderRadius.MEDIUM,
            LumoUtility.Padding.MEDIUM
        );
        card.setWidth("200px");

        HorizontalLayout header = new HorizontalLayout();
        header.setWidthFull();
        header.setAlignItems(HorizontalLayout.Alignment.CENTER);
        header.setJustifyContentMode(HorizontalLayout.JustifyContentMode.BETWEEN);

        Span titleSpan = new Span(title);
        titleSpan.addClassNames(LumoUtility.FontSize.SMALL, LumoUtility.TextColor.SECONDARY);

        Span iconSpan = new Span(icon.create());
        iconSpan.getStyle().set("color", color);

        header.add(titleSpan, iconSpan);

        Paragraph valueP = new Paragraph(value);
        valueP.addClassNames(LumoUtility.FontSize.XXXLARGE, LumoUtility.FontWeight.BOLD);
        valueP.getStyle().set("margin", "var(--lumo-space-xs) 0 0 0");

        card.add(header, valueP);
        return card;
    }

    private Component createMostPlayedCard(Map<String, Long> mostPlayed) {
        Div card = new Div();
        card.addClassNames(
            LumoUtility.Background.CONTRAST_5,
            LumoUtility.BorderRadius.MEDIUM,
            LumoUtility.Padding.MEDIUM
        );
        card.setWidth("300px");

        H3 title = new H3(translationService.translate("dashboard.mostPlayed"));
        title.addClassNames(LumoUtility.FontSize.MEDIUM, LumoUtility.Margin.NONE);

        VerticalLayout list = new VerticalLayout();
        list.setPadding(false);
        list.setSpacing(false);
        list.getStyle().set("gap", "var(--lumo-space-xs)");

        mostPlayed.forEach((quizName, count) -> {
            HorizontalLayout item = new HorizontalLayout();
            item.setWidthFull();
            item.setJustifyContentMode(HorizontalLayout.JustifyContentMode.BETWEEN);

            Span name = new Span(quizName);
            name.addClassNames(LumoUtility.FontSize.SMALL);
            name.getStyle().set("overflow", "hidden")
                          .set("text-overflow", "ellipsis")
                          .set("white-space", "nowrap")
                          .set("flex", "1");

            Span countSpan = new Span(String.valueOf(count));
            countSpan.addClassNames(LumoUtility.FontSize.SMALL, LumoUtility.FontWeight.BOLD);
            countSpan.getStyle().set("color", "var(--lumo-primary-color)");

            item.add(name, countSpan);
            list.add(item);
        });

        card.add(title, list);
        return card;
    }

    private Grid<PlayerTrace> createRecentActivityGrid() {
        Grid<PlayerTrace> grid = new Grid<>(PlayerTrace.class, false);
        grid.addClassNames(LumoUtility.Border.ALL, LumoUtility.BorderRadius.MEDIUM);

        grid.addColumn(new ComponentRenderer<>(trace -> {
            Span timestamp = new Span(trace.getTimestamp().format(DATE_TIME_FORMATTER));
            timestamp.addClassNames(LumoUtility.FontSize.SMALL);
            return timestamp;
        })).setHeader(translationService.translate("dashboard.timestamp"))
           .setAutoWidth(true)
           .setFlexGrow(0);

        grid.addColumn(trace -> trace.getUser() != null ? trace.getUser().getName() : "")
            .setHeader(translationService.translate("dashboard.player"))
            .setAutoWidth(true);

        grid.addColumn(trace -> trace.getQuiz() != null ? trace.getQuiz().getName() : "")
            .setHeader(translationService.translate("dashboard.quiz"))
            .setAutoWidth(true)
            .setFlexGrow(1);

        grid.addColumn(new ComponentRenderer<>(trace -> {
            String mode = trace.getQuizMode();
            Span badge = new Span(mode != null ? mode : "NORMAL");
            badge.addClassNames(LumoUtility.FontSize.XSMALL, LumoUtility.Padding.Horizontal.SMALL);
            badge.getStyle()
                .set("border-radius", "var(--lumo-border-radius-m)")
                .set("background-color", "TEAM".equals(mode) ? "var(--lumo-error-color-10pct)" : "var(--lumo-contrast-10pct)")
                .set("color", "TEAM".equals(mode) ? "var(--lumo-error-color)" : "var(--lumo-contrast-60pct)");
            return badge;
        })).setHeader(translationService.translate("dashboard.mode"))
           .setAutoWidth(true)
           .setFlexGrow(0);

        grid.addColumn(trace -> trace.getTeamName() != null ? trace.getTeamName() : "-")
            .setHeader(translationService.translate("dashboard.team"))
            .setAutoWidth(true);

        grid.addColumn(trace -> trace.getSessionCode() != null ? trace.getSessionCode() : "-")
            .setHeader(translationService.translate("dashboard.sessionCode"))
            .setAutoWidth(true);

        return grid;
    }

    @Override
    public void beforeEnter(BeforeEnterEvent event) {
        // Check if current user is admin
        User currentUser = VaadinSession.getCurrent().getAttribute(User.class);

        if (currentUser == null || !currentUser.isAdmin()) {
            // Redirect to quiz list if not admin
            event.rerouteTo("");
            Notification.show(translationService.translate("common.accessDenied"), 3000, Notification.Position.MIDDLE)
                .addThemeVariants(NotificationVariant.LUMO_ERROR);
            logger.warn("Non-admin user attempted to access dashboard: {}",
                       currentUser != null ? currentUser.getName() : "unknown");
        }
    }
}

