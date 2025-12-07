package com.quizz.core.ui;

import com.quizz.base.ui.component.ViewToolbar;
import com.quizz.core.entity.Quiz;
import com.quizz.core.entity.QuizSession;
import com.quizz.core.entity.User;
import com.quizz.core.service.QuizService;
import com.quizz.core.service.QuizSessionService;
import com.quizz.core.util.QRCodeGenerator;
import com.vaadin.flow.component.button.Button;
import com.vaadin.flow.component.button.ButtonVariant;
import com.vaadin.flow.component.dialog.Dialog;
import com.vaadin.flow.component.grid.Grid;
import com.vaadin.flow.component.html.*;
import com.vaadin.flow.component.notification.Notification;
import com.vaadin.flow.component.notification.NotificationVariant;
import com.vaadin.flow.component.orderedlayout.HorizontalLayout;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import com.vaadin.flow.component.textfield.TextField;
import com.vaadin.flow.router.Menu;
import com.vaadin.flow.router.PageTitle;
import com.vaadin.flow.router.Route;
import com.vaadin.flow.server.VaadinSession;
import com.vaadin.flow.theme.lumo.LumoUtility;

import java.io.InputStream;
import java.util.Properties;

import static com.vaadin.flow.spring.data.VaadinSpringDataHelpers.toSpringPageRequest;

@Route("")
@PageTitle("New Quiz")
@Menu(order = 1, icon = "vaadin:question-circle", title = "New Quiz")
class QuizListView extends Main {

    private final QuizService quizService;
    private final QuizSessionService sessionService;

    final TextField name;
    final Button createBtn;
    final Grid<Quiz> quizGrid;

    QuizListView(QuizService quizService, QuizSessionService sessionService) {
        this.quizService = quizService;
        this.sessionService = sessionService;

        name = new TextField();
        name.setPlaceholder("Quiz name");
        name.setAriaLabel("Quiz name");
        name.setMaxLength(Quiz.NAME_MAX_LENGTH);
        name.setMinWidth("20em");

        createBtn = new Button("Create", event -> createQuiz());
        createBtn.addThemeVariants(ButtonVariant.LUMO_PRIMARY);

        quizGrid = new Grid<>();
        quizGrid.setItems(query -> quizService.list(toSpringPageRequest(query)).stream());
        quizGrid.addColumn(Quiz::getName).setHeader("Name");
        quizGrid.addComponentColumn(quiz -> {
            Button playButton = new Button("Play", event ->
                getUI().ifPresent(ui -> ui.navigate("quiz-questions/" + quiz.getId()))
            );
            playButton.addThemeVariants(ButtonVariant.LUMO_SUCCESS, ButtonVariant.LUMO_SMALL);

            Button shareButton = new Button("Share", event -> showShareDialog(quiz));
            shareButton.addThemeVariants(ButtonVariant.LUMO_PRIMARY, ButtonVariant.LUMO_SMALL);

            HorizontalLayout actions = new HorizontalLayout(playButton, shareButton);
            actions.setSpacing(true);
            return actions;
        }).setHeader("Action").setAutoWidth(true);
        quizGrid.setSizeFull();

        setSizeFull();
        addClassNames(LumoUtility.BoxSizing.BORDER, LumoUtility.Display.FLEX, LumoUtility.FlexDirection.COLUMN,
                LumoUtility.Padding.MEDIUM, LumoUtility.Gap.SMALL);

        add(new ViewToolbar("Quiz List", ViewToolbar.group(name, createBtn)));
        add(quizGrid);
    }

    private void createQuiz() {
        quizService.createQuiz(name.getValue());
        quizGrid.getDataProvider().refreshAll();
        name.clear();
        Notification.show("Quiz added", 3000, Notification.Position.BOTTOM_END)
                .addThemeVariants(NotificationVariant.LUMO_SUCCESS);
    }

    private void showShareDialog(Quiz quiz) {
        User currentUser = VaadinSession.getCurrent().getAttribute(User.class);
        if (currentUser == null || currentUser.getId() == null) {
            Notification.show("Please login to share a quiz", 3000, Notification.Position.MIDDLE)
                .addThemeVariants(NotificationVariant.LUMO_ERROR);
            return;
        }

        // Create a new session
        QuizSession session = sessionService.createSession(quiz, currentUser.getId());

        Dialog dialog = new Dialog();
        dialog.setHeaderTitle("Share Quiz: " + quiz.getName());
        dialog.setWidth("500px");

        VerticalLayout content = new VerticalLayout();
        content.setSpacing(true);
        content.setPadding(false);
        content.setAlignItems(VerticalLayout.Alignment.CENTER);

        H3 instructionTitle = new H3("Scan QR Code to Join");
        instructionTitle.getStyle().set("margin-top", "0");

        // Generate QR code with session URL
        Properties appProperties = new Properties();
        InputStream resourceAsStream = Thread.currentThread().getContextClassLoader().getResourceAsStream("application.properties");
        try {
            appProperties.load(resourceAsStream);
        } catch (Exception e) {
            throw new RuntimeException("Unable to load application properties", e);
        }

        String addressServer= appProperties.getProperty("server.address");
        String portServer= appProperties.getProperty("server.port");
        String sessionUrl = "http://" + addressServer + ":" + portServer +"/quiz-session/" + session.getSessionCode();

        Image qrCode = new Image(QRCodeGenerator.generateQRCode(sessionUrl, 300, 300), "QR Code");
        qrCode.setWidth("300px");
        qrCode.setHeight("300px");

        Div codeContainer = new Div();
        codeContainer.getStyle()
            .set("background", "var(--lumo-contrast-5pct)")
            .set("padding", "var(--lumo-space-m)")
            .set("border-radius", "var(--lumo-border-radius-m)")
            .set("text-align", "center");

        H2 sessionCodeDisplay = new H2("Code: " + session.getSessionCode());
        sessionCodeDisplay.getStyle()
            .set("margin", "0")
            .set("color", "var(--lumo-primary-color)")
            .set("font-family", "monospace");

        codeContainer.add(sessionCodeDisplay);

        Paragraph instructions = new Paragraph(
            "Share this QR code or session code with other participants. " +
            "They can scan it or enter the code to join the quiz session."
        );
        instructions.getStyle()
            .set("text-align", "center")
            .set("color", "var(--lumo-secondary-text-color)");

        Button goToSessionButton = new Button("Go to Session Room", event -> {
            dialog.close();
            getUI().ifPresent(ui -> ui.navigate("quiz-session/" + session.getSessionCode()));
        });
        goToSessionButton.addThemeVariants(ButtonVariant.LUMO_PRIMARY);

        Button copyLinkButton = new Button("Copy Link", event -> {
            getUI().ifPresent(ui -> ui.getPage().executeJs(
                "navigator.clipboard.writeText($0).then(() => {}, () => {})",
                sessionUrl
            ));
            Notification.show("Link copied to clipboard!", 2000, Notification.Position.BOTTOM_CENTER)
                .addThemeVariants(NotificationVariant.LUMO_SUCCESS);
        });
        copyLinkButton.addThemeVariants(ButtonVariant.LUMO_TERTIARY);

        Button closeButton = new Button("Close", event -> dialog.close());

        HorizontalLayout buttonLayout = new HorizontalLayout(goToSessionButton, copyLinkButton, closeButton);
        buttonLayout.setSpacing(true);

        content.add(instructionTitle, qrCode, codeContainer, instructions, buttonLayout);
        dialog.add(content);
        dialog.open();
    }

}
