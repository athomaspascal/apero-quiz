package com.quizz.core.ui;

import com.quizz.core.entity.QuizSession;
import com.quizz.core.service.QuizSessionService;
import com.quizz.core.entity.User;
import com.vaadin.flow.component.button.Button;
import com.vaadin.flow.component.button.ButtonVariant;
import com.vaadin.flow.component.html.Div;
import com.vaadin.flow.component.html.H2;
import com.vaadin.flow.component.html.Paragraph;
import com.vaadin.flow.component.notification.Notification;
import com.vaadin.flow.component.notification.NotificationVariant;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import com.vaadin.flow.component.textfield.TextField;
import com.vaadin.flow.router.Menu;
import com.vaadin.flow.router.PageTitle;
import com.vaadin.flow.router.Route;
import com.vaadin.flow.server.VaadinSession;
import com.vaadin.flow.theme.lumo.LumoUtility;

@Route("join-session")
@PageTitle("Join Quiz Session")
@Menu(order = 3, icon = "vaadin:group", title = "Join Session")
public class JoinSessionView extends VerticalLayout {

    private final QuizSessionService sessionService;
    private final TextField sessionCodeField;

    public JoinSessionView(QuizSessionService sessionService) {
        this.sessionService = sessionService;

        setSizeFull();
        setAlignItems(Alignment.CENTER);
        setJustifyContentMode(JustifyContentMode.CENTER);

        Div container = new Div();
        container.addClassNames(
            LumoUtility.Background.BASE,
            LumoUtility.Padding.XLARGE,
            LumoUtility.BorderRadius.LARGE,
            LumoUtility.BoxShadow.SMALL
        );
        container.getStyle().set("max-width", "500px");
        container.getStyle().set("width", "100%");

        H2 title = new H2("Join Quiz Session");
        title.addClassNames(LumoUtility.Margin.Bottom.MEDIUM);

        Paragraph instruction = new Paragraph(
            "Enter the session code provided by the quiz host to join the session."
        );
        instruction.addClassNames(
            LumoUtility.TextColor.SECONDARY,
            LumoUtility.Margin.Bottom.LARGE
        );

        sessionCodeField = new TextField("Session Code");
        sessionCodeField.setPlaceholder("e.g., ABC12345");
        sessionCodeField.setMaxLength(8);
        sessionCodeField.setWidthFull();
        sessionCodeField.getStyle().set("text-transform", "uppercase");
        sessionCodeField.addValueChangeListener(event -> {
            if (event.getValue() != null) {
                sessionCodeField.setValue(event.getValue().toUpperCase());
            }
        });

        Button joinButton = new Button("Join Session", event -> joinSession());
        joinButton.addThemeVariants(ButtonVariant.LUMO_PRIMARY, ButtonVariant.LUMO_LARGE);
        joinButton.setWidthFull();

        VerticalLayout content = new VerticalLayout(
            title,
            instruction,
            sessionCodeField,
            joinButton
        );
        content.setSpacing(true);
        content.setPadding(false);
        content.setAlignItems(Alignment.STRETCH);

        container.add(content);
        add(container);
    }

    private void joinSession() {
        String code = sessionCodeField.getValue();

        if (code == null || code.trim().isEmpty()) {
            Notification.show("Please enter a session code", 3000, Notification.Position.MIDDLE)
                .addThemeVariants(NotificationVariant.LUMO_ERROR);
            return;
        }

        User currentUser = VaadinSession.getCurrent().getAttribute(User.class);
        if (currentUser == null) {
            Notification.show("Please login to join a session", 3000, Notification.Position.MIDDLE)
                .addThemeVariants(NotificationVariant.LUMO_ERROR);
            getUI().ifPresent(ui -> ui.navigate("login"));
            return;
        }

        QuizSession session = sessionService.getSessionByCode(code.trim());

        if (session == null) {
            Notification.show("Session not found. Please check the code and try again.",
                3000, Notification.Position.MIDDLE)
                .addThemeVariants(NotificationVariant.LUMO_ERROR);
            return;
        }

        // Navigate to session view
        getUI().ifPresent(ui -> ui.navigate("quiz-session/" + code.trim()));
    }
}

