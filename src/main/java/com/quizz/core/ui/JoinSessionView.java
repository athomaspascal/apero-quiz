package com.quizz.core.ui;

import com.quizz.core.entity.QuizSession;
import com.quizz.core.service.QuizSessionService;
import com.quizz.core.entity.User;
import com.quizz.core.service.TranslationService;
import com.vaadin.flow.component.AttachEvent;
import com.vaadin.flow.component.button.Button;
import com.vaadin.flow.component.button.ButtonVariant;
import com.vaadin.flow.component.html.Div;
import com.vaadin.flow.component.html.H2;
import com.vaadin.flow.component.html.Paragraph;
import com.vaadin.flow.component.icon.VaadinIcon;
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
@Menu(order = 3, icon = "vaadin:group", title = "menu.joinSession")
public class JoinSessionView extends VerticalLayout {

    private final QuizSessionService sessionService;
    private final TranslationService translationService;
    private final TextField sessionCodeField;

    public JoinSessionView(QuizSessionService sessionService, TranslationService translationService) {
        this.sessionService = sessionService;
        this.translationService = translationService;

        setSizeFull();
        setAlignItems(Alignment.CENTER);
        setJustifyContentMode(JustifyContentMode.CENTER);

        // Bouton de retour en haut à gauche (visible uniquement quand le menu latéral n'est pas affiché)
        Button backButton = new Button(translationService.translate("quiz.backToList"), VaadinIcon.ARROW_LEFT.create());
        backButton.addThemeVariants(ButtonVariant.LUMO_TERTIARY);
        backButton.addClickListener(event -> getUI().ifPresent(ui -> ui.navigate("")));
        backButton.getStyle()
            .set("position", "absolute")
            .set("top", "10px")
            .set("left", "10px");

        // Hide back button when side menu is visible
        backButton.addAttachListener(attachEvent -> {
            getUI().ifPresent(ui -> {
                ui.getPage().executeJs(
                    "const checkMenu = () => {" +
                    "  const drawer = document.querySelector('vaadin-app-layout vaadin-drawer-toggle');" +
                    "  const sideNav = document.querySelector('vaadin-side-nav');" +
                    "  if (drawer && window.getComputedStyle(drawer).display !== 'none') {" +
                    "    $0.style.display = 'none';" +
                    "  } else if (sideNav && window.getComputedStyle(sideNav).display !== 'none') {" +
                    "    $0.style.display = 'none';" +
                    "  } else {" +
                    "    $0.style.display = '';" +
                    "  }" +
                    "};" +
                    "checkMenu();" +
                    "window.addEventListener('resize', checkMenu);" +
                    "setTimeout(checkMenu, 100);" +
                    "setTimeout(checkMenu, 500);",
                    backButton.getElement()
                );
            });
        });

        Div container = new Div();
        container.addClassNames(
            LumoUtility.Background.BASE,
            LumoUtility.Padding.XLARGE,
            LumoUtility.BorderRadius.LARGE,
            LumoUtility.BoxShadow.SMALL
        );
        container.getStyle().set("max-width", "500px");
        container.getStyle().set("width", "100%");

        H2 title = new H2(translationService.translate("joinSession.title"));
        title.addClassNames(LumoUtility.Margin.Bottom.MEDIUM);

        Paragraph instruction = new Paragraph(
            translationService.translate("joinSession.instruction")
        );
        instruction.addClassNames(
            LumoUtility.TextColor.SECONDARY,
            LumoUtility.Margin.Bottom.LARGE
        );

        sessionCodeField = new TextField(translationService.translate("joinSession.codeLabel"));
        sessionCodeField.setPlaceholder(translationService.translate("joinSession.codePlaceholder"));
        sessionCodeField.setMaxLength(8);
        sessionCodeField.setWidthFull();
        sessionCodeField.getStyle().set("text-transform", "uppercase");
        sessionCodeField.addValueChangeListener(event -> {
            if (event.getValue() != null) {
                sessionCodeField.setValue(event.getValue().toUpperCase());
            }
        });

        Button joinButton = new Button(translationService.translate("joinSession.joinButton"), event -> joinSession());
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
        add(backButton, container);

        // Set initial dynamic page title
        getUI().ifPresent(ui -> ui.getPage().setTitle(translationService.translate("joinSession.title")));
    }

    @Override
    protected void onAttach(AttachEvent attachEvent) {
        super.onAttach(attachEvent);
        // Update page title on attach to reflect current locale
        getUI().ifPresent(ui -> ui.getPage().setTitle(translationService.translate("joinSession.title")));
    }

    private void joinSession() {
        String code = sessionCodeField.getValue();

        if (code == null || code.trim().isEmpty()) {
            Notification.show(translationService.translate("joinSession.error.emptyCode"), 3000, Notification.Position.MIDDLE)
                .addThemeVariants(NotificationVariant.LUMO_ERROR);
            return;
        }

        User currentUser = VaadinSession.getCurrent().getAttribute(User.class);
        if (currentUser == null) {
            Notification.show(translationService.translate("joinSession.error.loginRequired"), 3000, Notification.Position.MIDDLE)
                .addThemeVariants(NotificationVariant.LUMO_ERROR);
            getUI().ifPresent(ui -> ui.navigate("login"));
            return;
        }

        QuizSession session = sessionService.getSessionByCode(code.trim());

        if (session == null) {
            Notification.show(translationService.translate("joinSession.error.notFound"),
                3000, Notification.Position.MIDDLE)
                .addThemeVariants(NotificationVariant.LUMO_ERROR);
            return;
        }

        // Navigate to session view
        getUI().ifPresent(ui -> ui.navigate("quiz-session/" + code.trim()));
    }
}

