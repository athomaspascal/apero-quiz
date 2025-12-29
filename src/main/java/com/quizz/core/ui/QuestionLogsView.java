package com.quizz.core.ui;

import com.quizz.base.ui.component.ViewToolbar;
import com.quizz.core.entity.QuizQuestionLog;
import com.quizz.core.entity.User;
import com.quizz.core.service.QuizQuestionLogService;
import com.quizz.core.service.TranslationService;
import com.vaadin.flow.component.grid.Grid;
import com.vaadin.flow.component.html.Main;
import com.vaadin.flow.component.notification.Notification;
import com.vaadin.flow.component.notification.NotificationVariant;
import com.vaadin.flow.router.*;
import com.vaadin.flow.server.VaadinSession;
import com.vaadin.flow.theme.lumo.LumoUtility;

import java.time.format.DateTimeFormatter;

import static com.vaadin.flow.spring.data.VaadinSpringDataHelpers.toSpringPageRequest;

@Route("question-logs")
@PageTitle("Question Logs")
@Menu(order = 3, icon = "vaadin:records", title = "Question Logs")
class QuestionLogsView extends Main implements BeforeEnterObserver {

    private final QuizQuestionLogService logService;
    private final TranslationService translationService;
    private final Grid<QuizQuestionLog> logGrid;
    private static final DateTimeFormatter DATE_FORMATTER = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

    QuestionLogsView(QuizQuestionLogService logService, TranslationService translationService) {
        this.logService = logService;
        this.translationService = translationService;

        logGrid = new Grid<>();

        // Fix: Use lazy data provider with proper pagination
        logGrid.setItems(query -> {
            User currentUser = VaadinSession.getCurrent().getAttribute(User.class);
            if (currentUser == null) {
                return java.util.stream.Stream.empty();
            }

            // Get all logs and convert to stream with proper limit
            java.util.List<QuizQuestionLog> allLogs = logService.getUserLogs(currentUser);
            return allLogs.stream()
                .skip(query.getOffset())
                .limit(query.getLimit());
        });

        logGrid.addColumn(log -> log.getAskedAt().format(DATE_FORMATTER))
            .setHeader(translationService.translate("questionLogs.grid.dateTime"))
            .setSortable(true)
            .setAutoWidth(true);

        logGrid.addColumn(log -> log.getQuiz().getName())
            .setHeader(translationService.translate("questionLogs.grid.quiz"))
            .setSortable(true)
            .setAutoWidth(true);

        logGrid.addColumn(QuizQuestionLog::getQuestionText)
            .setHeader(translationService.translate("questionLogs.grid.question"))
            .setAutoWidth(true)
            .setFlexGrow(2);

        logGrid.addColumn(log -> {
            StringBuilder options = new StringBuilder();
            if (log.getOption1() != null) options.append("1:").append(log.getOption1()).append(" | ");
            if (log.getOption2() != null) options.append("2:").append(log.getOption2()).append(" | ");
            if (log.getOption3() != null) options.append("3:").append(log.getOption3()).append(" | ");
            if (log.getOption4() != null) options.append("4:").append(log.getOption4());
            return options.toString();
        })
            .setHeader(translationService.translate("questionLogs.grid.optionsProposed"))
            .setAutoWidth(true)
            .setFlexGrow(3);

        logGrid.addColumn(QuizQuestionLog::getCorrectAnswer)
            .setHeader(translationService.translate("questionLogs.grid.correctAnswer"))
            .setAutoWidth(true);

        logGrid.addColumn(QuizQuestionLog::getUserAnswer)
            .setHeader(translationService.translate("questionLogs.grid.yourAnswer"))
            .setAutoWidth(true);

        logGrid.addColumn(log -> log.isCorrect() ? "✓" : "✗")
            .setHeader(translationService.translate("questionLogs.grid.result"))
            .setAutoWidth(true);

        logGrid.addColumn(log -> log.getTimeTakenSeconds() + "s")
            .setHeader(translationService.translate("questionLogs.grid.time"))
            .setAutoWidth(true);

        logGrid.setSizeFull();

        setSizeFull();
        addClassNames(LumoUtility.BoxSizing.BORDER, LumoUtility.Display.FLEX, LumoUtility.FlexDirection.COLUMN,
                LumoUtility.Padding.MEDIUM, LumoUtility.Gap.SMALL);

        add(new ViewToolbar(translationService.translate("questionLogs.toolbarTitle")));
        add(logGrid);
    }

    @Override
    public void beforeEnter(BeforeEnterEvent event) {
        // Check if current user is admin
        User currentUser = VaadinSession.getCurrent().getAttribute(User.class);

        if (currentUser == null || !currentUser.isAdmin()) {
            // Redirect to quiz list if not admin
            event.rerouteTo("");
            Notification.show(translationService.translate("questionLogs.accessDenied"), 3000, Notification.Position.MIDDLE)
                .addThemeVariants(NotificationVariant.LUMO_ERROR);
        }
    }
}

