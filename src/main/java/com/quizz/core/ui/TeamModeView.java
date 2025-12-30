package com.quizz.core.ui;

import com.quizz.base.ui.component.ViewToolbar;
import com.quizz.core.entity.Quiz;
import com.quizz.core.entity.QuizSession;
import com.quizz.core.entity.User;
import com.quizz.core.service.QuizService;
import com.quizz.core.service.QuizSessionService;
import com.quizz.core.service.TranslationService;
import com.quizz.core.util.QRCodeGenerator;
import com.vaadin.flow.component.button.Button;
import com.vaadin.flow.component.button.ButtonVariant;
import com.vaadin.flow.component.checkbox.Checkbox;
import com.vaadin.flow.component.dialog.Dialog;
import com.vaadin.flow.component.html.*;
import com.vaadin.flow.component.notification.Notification;
import com.vaadin.flow.component.notification.NotificationVariant;
import com.vaadin.flow.component.orderedlayout.HorizontalLayout;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import com.vaadin.flow.router.Menu;
import com.vaadin.flow.router.PageTitle;
import com.vaadin.flow.router.Route;
import com.vaadin.flow.server.VaadinSession;
import com.vaadin.flow.theme.lumo.LumoUtility;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.ByteArrayInputStream;
import java.io.InputStream;
import java.util.*;

@Route("team-mode")
@PageTitle("Team Mode")
@Menu(order = 2, icon = "vaadin:users", title = "menu.teammode")
public class TeamModeView extends Main {

    private static final Logger logger = LoggerFactory.getLogger(TeamModeView.class);

    private final QuizService quizService;
    private final QuizSessionService sessionService;
    private final TranslationService translationService;

    private final Button shareBtn;
    private HorizontalLayout quizCardsContainer;
    private VerticalLayout teamSelectionContainer;
    private Quiz selectedQuiz = null;
    private final Map<String, Checkbox> teamCheckboxes = new HashMap<>();
    private final Set<String> selectedTeams = new HashSet<>();

    public TeamModeView(QuizService quizService, QuizSessionService sessionService, TranslationService translationService) {
        logger.info("=== TeamModeView Constructor: Starting ===");

        this.quizService = quizService;
        this.sessionService = sessionService;
        this.translationService = translationService;

        logger.info("Services injected successfully");

        // Share button to start quiz in team mode
        shareBtn = new Button(translationService.translate("teammode.startShared"), event -> {
            if (selectedQuiz != null) {
                if (selectedTeams.size() < 2) {
                    String warningMessage;
                    if (selectedTeams.isEmpty()) {
                        warningMessage = translationService.translate("teammode.selectTeams.warning");
                    } else {
                        warningMessage = translationService.translate("teammode.selectTeams.minimum")
                            .replace("{0}", String.valueOf(selectedTeams.size()));
                    }
                    Notification notification = Notification.show(
                        warningMessage,
                        5000,
                        Notification.Position.MIDDLE
                    );
                    notification.addThemeVariants(NotificationVariant.LUMO_ERROR);
                    return;
                }
                showShareDialog(selectedQuiz);
            }
        });
        shareBtn.addThemeVariants(ButtonVariant.LUMO_PRIMARY);
        shareBtn.setEnabled(false);

        // Team selection container
        teamSelectionContainer = createTeamSelectionSection();

        // Quiz cards container
        quizCardsContainer = new HorizontalLayout();
        quizCardsContainer.setSpacing(true);
        quizCardsContainer.getStyle()
            .set("flex-wrap", "wrap")
            .set("gap", "10px")
            .set("padding", "10px");

        setSizeFull();
        addClassNames(LumoUtility.BoxSizing.BORDER, LumoUtility.Display.FLEX, LumoUtility.FlexDirection.COLUMN,
                LumoUtility.Padding.MEDIUM, LumoUtility.Gap.SMALL);

        // Create user profile section
        VerticalLayout userProfileSection = createUserProfileSection();

        add(userProfileSection);
        add(new ViewToolbar(translationService.translate("teammode.title"), ViewToolbar.group(shareBtn)));
        add(teamSelectionContainer);
        add(new H3(translationService.translate("teammode.selectQuiz")));
        add(quizCardsContainer);

        logger.info("UI components created, about to load quiz cards...");

        loadQuizCards();

        logger.info("Quiz cards loaded");

        // Hide Users menu if not admin
        hideUsersMenuIfNotAdmin();

        logger.info("=== TeamModeView Constructor: Completed ===");
    }

    private void hideUsersMenuIfNotAdmin() {
        User currentUser = VaadinSession.getCurrent().getAttribute(User.class);
        boolean isAdmin = currentUser != null && currentUser.isAdmin();

        if (!isAdmin) {
            // Use JavaScript to hide the admin-only menu items (Users, Question Logs, Quiz Editor)
            getElement().executeJs(
                "setTimeout(() => {" +
                "  const sideNav = document.querySelector('vaadin-side-nav');" +
                "  if (sideNav) {" +
                "    const items = sideNav.querySelectorAll('vaadin-side-nav-item');" +
                "    items.forEach(item => {" +
                "      const path = item.getAttribute('path');" +
                "      if (path === 'users' || path === 'question-logs' || path === 'admin/quiz-editor') {" +
                "        item.style.display = 'none';" +
                "      }" +
                "    });" +
                "  }" +
                "}, 100);"
            );
        }
    }

    private VerticalLayout createUserProfileSection() {
        VerticalLayout profileSection = new VerticalLayout();
        profileSection.setAlignItems(VerticalLayout.Alignment.CENTER);
        profileSection.setPadding(false);
        profileSection.setSpacing(false);
        profileSection.getStyle()
            .set("margin-bottom", "20px");

        User currentUser = VaadinSession.getCurrent().getAttribute(User.class);

        Div avatarContainer = new Div();
        avatarContainer.getStyle()
            .set("width", "80px")
            .set("height", "80px")
            .set("border-radius", "50%")
            .set("overflow", "hidden")
            .set("display", "flex")
            .set("align-items", "center")
            .set("justify-content", "center")
            .set("box-shadow", "0 4px 12px rgba(0,0,0,0.15)")
            .set("cursor", "pointer");

        if (currentUser != null && currentUser.getPhotoBytes() != null && currentUser.getPhotoBytes().length > 0) {
            Image userPhoto = new Image();
            userPhoto.setSrc("data:image/jpeg;base64," +
                java.util.Base64.getEncoder().encodeToString(currentUser.getPhotoBytes()));
            userPhoto.setAlt("User photo");
            userPhoto.setWidth("100%");
            userPhoto.setHeight("100%");
            userPhoto.getStyle().set("object-fit", "cover");
            avatarContainer.add(userPhoto);
        } else if (currentUser != null && currentUser.getName() != null && !currentUser.getName().isEmpty()) {
            avatarContainer.getStyle()
                .set("background", "linear-gradient(135deg, #667eea 0%, #764ba2 100%)")
                .set("color", "white")
                .set("font-size", "32px")
                .set("font-weight", "bold");
            String initials = getInitials(currentUser.getName());
            Span initialsSpan = new Span(initials);
            avatarContainer.add(initialsSpan);
        } else {
            avatarContainer.getStyle()
                .set("background", "linear-gradient(135deg, #667eea 0%, #764ba2 100%)")
                .set("color", "white")
                .set("font-size", "32px");
            Span defaultIcon = new Span("👤");
            avatarContainer.add(defaultIcon);
        }

        if (currentUser != null && currentUser.getName() != null) {
            Paragraph userName = new Paragraph(currentUser.getName());
            userName.getStyle()
                .set("margin-top", "8px")
                .set("margin-bottom", "0")
                .set("font-size", "14px")
                .set("font-weight", "500")
                .set("color", "#333");
            profileSection.add(avatarContainer, userName);
        } else {
            profileSection.add(avatarContainer);
        }

        return profileSection;
    }

    private String getInitials(String name) {
        if (name == null || name.isEmpty()) {
            return "?";
        }

        String[] parts = name.trim().split("\\s+");
        if (parts.length == 1) {
            return parts[0].substring(0, Math.min(2, parts[0].length())).toUpperCase();
        } else {
            return (parts[0].substring(0, 1) + parts[parts.length - 1].substring(0, 1)).toUpperCase();
        }
    }

    private VerticalLayout createTeamSelectionSection() {
        VerticalLayout teamSection = new VerticalLayout();
        teamSection.setPadding(true);
        teamSection.setSpacing(true);
        teamSection.getStyle()
            .set("background", "var(--lumo-contrast-5pct)")
            .set("border-radius", "var(--lumo-border-radius-m)")
            .set("margin-bottom", "20px");

        H3 teamTitle = new H3(translationService.translate("teammode.selectTeams"));
        teamTitle.getStyle().set("margin", "0 0 var(--lumo-space-m) 0");

        String[] availableTeams = {"stark", "lannister", "targaryen", "baratheon", "tyrell", "martell", "arryn", "tully", "greyjoy"};

        HorizontalLayout teamsCheckboxLayout = new HorizontalLayout();
        teamsCheckboxLayout.setSpacing(true);
        teamsCheckboxLayout.getStyle().set("flex-wrap", "wrap");

        for (String team : availableTeams) {
            Checkbox teamCheckbox = new Checkbox(
                translationService.translate("quizSession.teamMode.team." + team)
            );
            teamCheckbox.addValueChangeListener(event -> {
                if (event.getValue()) {
                    selectedTeams.add(team);
                } else {
                    selectedTeams.remove(team);
                }
                updateShareButtonState();
            });
            teamCheckboxes.put(team, teamCheckbox);
            teamsCheckboxLayout.add(teamCheckbox);
        }

        teamSection.add(teamTitle, teamsCheckboxLayout);
        return teamSection;
    }

    private void loadQuizCards() {
        quizCardsContainer.removeAll();

        List<Quiz> quizzes = quizService.list(org.springframework.data.domain.Pageable.unpaged());

        logger.info("=== TeamModeView: Loading Quiz Cards ===");
        logger.info("Number of quizzes retrieved: " + quizzes.size());

        if (quizzes.isEmpty()) {
            logger.info("WARNING: No quizzes found in database!");
            Paragraph noQuizMessage = new Paragraph(translationService.translate("teammode.noQuizzes"));
            noQuizMessage.getStyle().set("color", "red").set("font-weight", "bold");
            quizCardsContainer.add(noQuizMessage);
            return;
        }

        for (Quiz quiz : quizzes) {
            logger.info("Creating card for quiz: " + quiz.getName() + " (ID: " + quiz.getId() + ")");
            VerticalLayout card = createQuizCard(quiz);
            quizCardsContainer.add(card);
        }

        logger.info("=== Quiz Cards Loading Completed ===");
    }

    private VerticalLayout createQuizCard(Quiz quiz) {
        VerticalLayout card = new VerticalLayout();
        card.setWidth("73px");
        card.setHeight("121px");
        card.setPadding(false);
        card.setSpacing(false);
        card.getStyle()
            .set("border", "1px solid #e0e0e0")
            .set("border-radius", "4px")
            .set("cursor", "pointer")
            .set("background-color", "white")
            .set("transition", "all 0.3s ease")
            .set("padding", "4px");

        Div imageContainer = new Div();
        imageContainer.setWidth("100%");
        imageContainer.setHeight("97px");
        imageContainer.getStyle()
            .set("display", "flex")
            .set("align-items", "center")
            .set("justify-content", "center")
            .set("overflow", "hidden")
            .set("border-radius", "4px");

        String imageFileName = quiz.getImageFileName();
        if (imageFileName != null && !imageFileName.isEmpty()) {
            Image image = new Image("images/" + imageFileName, quiz.getName());
            image.setWidth("100%");
            image.setHeight("100%");
            image.getStyle().set("object-fit", "cover");

            image.getElement().addEventListener("error", e -> {
                imageContainer.removeAll();
                Image fallback = new Image("images/france.svg", quiz.getName());
                fallback.setWidth("100%");
                fallback.setHeight("100%");
                fallback.getStyle().set("object-fit", "cover");
                imageContainer.add(fallback);
            });

            imageContainer.add(image);
        } else {
            Image fallback = new Image("images/france.svg", quiz.getName());
            fallback.setWidth("100%");
            fallback.setHeight("100%");
            fallback.getStyle().set("object-fit", "cover");
            imageContainer.add(fallback);
        }

        Paragraph quizName = new Paragraph(quiz.getName());
        quizName.getStyle()
            .set("text-align", "center")
            .set("font-weight", "bold")
            .set("margin-top", "2px")
            .set("margin-bottom", "0")
            .set("font-size", "7px")
            .set("color", "#333")
            .set("line-height", "1.1")
            .set("overflow", "hidden")
            .set("text-overflow", "ellipsis")
            .set("display", "-webkit-box")
            .set("-webkit-line-clamp", "2")
            .set("-webkit-box-orient", "vertical");

        card.add(imageContainer, quizName);

        card.addClickListener(event -> {
            selectQuiz(quiz);
        });

        card.getElement().addEventListener("mouseenter", e -> {
            card.getStyle()
                .set("border-color", "#1976d2")
                .set("box-shadow", "0 4px 8px rgba(0,0,0,0.2)")
                .set("transform", "translateY(-2px)");
        });

        card.getElement().addEventListener("mouseleave", e -> {
            if (selectedQuiz == null || !selectedQuiz.equals(quiz)) {
                card.getStyle()
                    .set("border-color", "#e0e0e0")
                    .set("box-shadow", "none")
                    .set("transform", "translateY(0)");
            }
        });

        return card;
    }

    private void selectQuiz(Quiz quiz) {
        selectedQuiz = quiz;
        updateShareButtonState();

        // Update visual selection of all cards
        quizCardsContainer.getChildren().forEach(component -> {
            if (component instanceof VerticalLayout) {
                VerticalLayout card = (VerticalLayout) component;
                card.getStyle()
                    .set("border-color", "#e0e0e0")
                    .set("box-shadow", "none");
            }
        });
    }

    private void updateShareButtonState() {
        shareBtn.setEnabled(selectedQuiz != null && selectedTeams.size() >= 2);
    }

    private void showShareDialog(Quiz quiz) {
        User currentUser = VaadinSession.getCurrent().getAttribute(User.class);
        if (currentUser == null || currentUser.getId() == null) {
            Notification.show(
                translationService.translate("teammode.error.login"),
                3000,
                Notification.Position.MIDDLE
            ).addThemeVariants(NotificationVariant.LUMO_ERROR);
            return;
        }

        // Create a new session with team mode enabled
        QuizSession session = sessionService.createSession(quiz, currentUser.getId());
        session.setTeamMode(true);
        session.setSelectedTeams(String.join(",", selectedTeams));
        sessionService.updateSession(session);

        Dialog dialog = new Dialog();
        dialog.setHeaderTitle(translationService.translate("session.share") + ": " + quiz.getName());
        dialog.setWidth("600px");

        VerticalLayout content = new VerticalLayout();
        content.setSpacing(true);
        content.setPadding(false);
        content.setAlignItems(VerticalLayout.Alignment.STRETCH);

        // Team Mode Info
        Div teamModeInfo = new Div();
        teamModeInfo.getStyle()
            .set("background", "var(--lumo-success-color-10pct)")
            .set("padding", "var(--lumo-space-m)")
            .set("border-radius", "var(--lumo-border-radius-m)")
            .set("margin-bottom", "var(--lumo-space-m)");

        H4 teamModeTitle = new H4(translationService.translate("teammode.enabled"));
        teamModeTitle.getStyle().set("margin", "0 0 var(--lumo-space-s) 0");

        Paragraph selectedTeamsText = new Paragraph(
            translationService.translate("teammode.selectedTeams") + ": " +
            String.join(", ", selectedTeams.stream()
                .map(t -> translationService.translate("quizSession.teamMode.team." + t))
                .toArray(String[]::new))
        );
        selectedTeamsText.getStyle().set("margin", "0");

        teamModeInfo.add(teamModeTitle, selectedTeamsText);

        H3 instructionTitle = new H3(translationService.translate("session.scan"));
        instructionTitle.getStyle().set("margin-top", "var(--lumo-space-m)");

        // Generate QR code with session URL
        Properties appProperties = new Properties();
        InputStream resourceAsStream = Thread.currentThread().getContextClassLoader().getResourceAsStream("application.properties");
        try {
            appProperties.load(resourceAsStream);
        } catch (Exception e) {
            throw new RuntimeException("Unable to load application properties", e);
        }

        String addressServer = appProperties.getProperty("server.address");
        String portServer = appProperties.getProperty("server.port");
        String sessionUrl = "https://" + addressServer + ":" + portServer + "/quiz-session/" + session.getSessionCode();

        // Generate QR Code as StreamResource
        @SuppressWarnings("deprecation")
        com.vaadin.flow.server.StreamResource qrCodeResource = QRCodeGenerator.generateQRCode(sessionUrl, 150, 150);
        Image qrCode = new Image();
        qrCode.setSrc(qrCodeResource);
        qrCode.setAlt("QR Code");
        qrCode.setWidth("150px");
        qrCode.setHeight("150px");

        Div codeContainer = new Div();
        codeContainer.getStyle()
            .set("background", "var(--lumo-contrast-5pct)")
            .set("padding", "var(--lumo-space-m)")
            .set("border-radius", "var(--lumo-border-radius-m)")
            .set("text-align", "center");

        H2 sessionCodeDisplay = new H2(translationService.translate("session.code") + ": " + session.getSessionCode());
        sessionCodeDisplay.getStyle()
            .set("margin", "0")
            .set("color", "var(--lumo-primary-color)")
            .set("font-family", "monospace");

        codeContainer.add(sessionCodeDisplay);

        Paragraph instructions = new Paragraph(translationService.translate("session.instructions"));
        instructions.getStyle()
            .set("text-align", "center")
            .set("color", "var(--lumo-secondary-text-color)");

        Button goToSessionButton = new Button(translationService.translate("session.goToRoom"), event -> {
            dialog.close();
            getUI().ifPresent(ui -> ui.navigate("quiz-session/" + session.getSessionCode()));
        });
        goToSessionButton.addThemeVariants(ButtonVariant.LUMO_PRIMARY);

        Button copyLinkButton = new Button(translationService.translate("session.copyLink"), event -> {
            getUI().ifPresent(ui -> ui.getPage().executeJs(
                "navigator.clipboard.writeText($0).then(() => {}, () => {})",
                sessionUrl
            ));
            Notification.show(
                translationService.translate("session.linkCopied"),
                2000,
                Notification.Position.BOTTOM_CENTER
            ).addThemeVariants(NotificationVariant.LUMO_SUCCESS);
        });
        copyLinkButton.addThemeVariants(ButtonVariant.LUMO_TERTIARY);

        Button closeButton = new Button(translationService.translate("session.close"), event -> dialog.close());

        HorizontalLayout buttonLayout = new HorizontalLayout(goToSessionButton, copyLinkButton, closeButton);
        buttonLayout.setSpacing(true);

        content.add(teamModeInfo, instructionTitle, qrCode, codeContainer, instructions, buttonLayout);
        dialog.add(content);
        dialog.open();
    }
}

