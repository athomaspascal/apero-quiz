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
import com.vaadin.flow.server.StreamResource;
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
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.ByteArrayInputStream;
import java.io.InputStream;
import java.util.List;
import java.util.Properties;


@Route("")
@PageTitle("One Quiz")
@Menu(order = 1, icon = "vaadin:question-circle", title = "menu.quizlist")
    @SuppressWarnings({"deprecation", "removal"})
class OneQuizzView extends Main {

    private static final Logger logger = LoggerFactory.getLogger(OneQuizzView.class);

    private final QuizService quizService;
    private final QuizSessionService sessionService;
    private final TranslationService translationService;

    final TextField name;
    final Button startButton;
    final Button shareBtn;
    final Checkbox teamModeCheckbox;
    private HorizontalLayout quizCardsContainer;
    private Quiz selectedQuiz = null;

    OneQuizzView(QuizService quizService, QuizSessionService sessionService, TranslationService translationService) {
        logger.info("=== QuizListView Constructor: Starting ===");

        this.quizService = quizService;
        this.sessionService = sessionService;
        this.translationService = translationService;

        logger.info("Services injected successfully");

        name = new TextField();
        name.setPlaceholder(translationService.translate("quizlist.placeholder"));
        name.setAriaLabel(translationService.translate("quizlist.title"));
        name.setMaxLength(Quiz.NAME_MAX_LENGTH);
        name.setMinWidth("20em");

        // Team Mode checkbox - initialize before startButton
        teamModeCheckbox = new Checkbox(translationService.translate("quizSession.teamMode"));
        teamModeCheckbox.getStyle()
            .set("margin-left", "10px")
            .set("align-self", "center");

        startButton = new Button(translationService.translate("quizlist.start"), event -> {
            if (selectedQuiz != null) {
                // Check if Team Mode is selected
                if (teamModeCheckbox.getValue()) {
                    Notification notification = Notification.show(
                        translationService.translate("quizlist.teamMode.warning"),
                        5000,
                        Notification.Position.MIDDLE
                    );
                    notification.addThemeVariants(NotificationVariant.LUMO_ERROR);
                    return;
                }
                getUI().ifPresent(ui -> ui.navigate("quiz-questions/" + selectedQuiz.getId()));
            }
        });
        startButton.addThemeVariants(ButtonVariant.LUMO_PRIMARY);
        startButton.setEnabled(false);

        shareBtn = new Button(translationService.translate("quizlist.share"), event -> {
            if (selectedQuiz != null) {
                showShareDialog(selectedQuiz);
            }
        });
        shareBtn.addThemeVariants(ButtonVariant.LUMO_PRIMARY);
        shareBtn.setEnabled(false);


        // Create horizontal container for quiz cards with colored background
        quizCardsContainer = new HorizontalLayout();
        quizCardsContainer.setSpacing(true);
        quizCardsContainer.getStyle()
            .set("flex-wrap", "wrap")
            .set("gap", "10px")
            .set("padding", "15px")
            .set("background-color", "#F8D9FF")
            .set("border-radius", "12px")
            .set("box-shadow", "0 4px 12px rgba(0,0,0,0.1)");

        setSizeFull();
        addClassNames(LumoUtility.BoxSizing.BORDER, LumoUtility.Display.FLEX, LumoUtility.FlexDirection.COLUMN,
                LumoUtility.Padding.MEDIUM, LumoUtility.Gap.SMALL);
        getStyle()
            .set("overflow-y", "auto")
            .set("overflow-x", "hidden");

        // Create user profile section
        VerticalLayout userProfileSection = createUserProfileSection();

        // Create toolbar
        ViewToolbar toolbar = new ViewToolbar(translationService.translate("quizlist.title"), ViewToolbar.group(name, startButton, shareBtn, teamModeCheckbox));

        // Style toolbar for better mobile display - use vertical layout on small screens
        toolbar.getStyle()
            .set("flex-wrap", "wrap")
            .set("gap", "8px")
            .set("width", "100%");

        // Add responsive CSS via JavaScript for mobile
        toolbar.getElement().executeJs(
            "const style = document.createElement('style');" +
            "style.textContent = `" +
            "  @media (max-width: 600px) {" +
            "    .view-toolbar-group {" +
            "      flex-direction: column !important;" +
            "      width: calc(100% - 10px) !important;" +
            "      align-items: stretch !important;" +
            "      margin-right: 10px !important;" +
            "    }" +
            "    .view-toolbar-group > * {" +
            "      width: 100% !important;" +
            "      min-width: unset !important;" +
            "      box-sizing: border-box !important;" +
            "    }" +
            "  }" +
            "`;" +
            "document.head.appendChild(style);"
        );

        // Style text field for mobile - full width on small screens
        name.getStyle()
            .set("min-width", "100px")
            .set("max-width", "100%")
            .set("font-size", "12px")
            .set("flex", "1 1 auto");
        name.setMinWidth("100px");
        name.setWidthFull();

        // Style buttons for mobile - full width on small screens
        startButton.getStyle()
            .set("font-size", "12px")
            .set("padding", "8px 12px")
            .set("min-width", "auto")
            .set("flex", "1 1 auto");

        shareBtn.getStyle()
            .set("font-size", "12px")
            .set("padding", "8px 12px")
            .set("min-width", "auto")
            .set("flex", "1 1 auto");

        teamModeCheckbox.getStyle()
            .set("font-size", "11px")
            .set("--lumo-checkbox-size", "18px")
            .set("white-space", "nowrap");

        // Wrap user profile AND toolbar in a single festive container
        Div festiveHeader = createFestiveHeaderContainer(userProfileSection, toolbar);

        add(festiveHeader);
        add(quizCardsContainer);

        logger.info("UI components created, about to load quiz cards...");

        loadQuizCards();

        logger.info("Quiz cards loaded");

        // Hide Users menu if not admin
        hideUsersMenuIfNotAdmin();

        logger.info("=== QuizListView Constructor: Completed ===");
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

    private Div createFestiveHeaderContainer(VerticalLayout userProfile, ViewToolbar toolbar) {
        Div container = new Div();
        container.getStyle()
            .set("position", "relative")
            .set("background", "linear-gradient(135deg, #667eea 0%, #764ba2 100%)")
            .set("padding", "15px 25px 15px 20px")
            .set("border-radius", "12px")
            .set("box-shadow", "0 4px 12px rgba(0,0,0,0.2)")
            .set("overflow", "visible")
            .set("margin-bottom", "10px")
            .set("margin-right", "5px")
            .set("min-height", "auto")
            .set("height", "auto")
            .set("flex-shrink", "0")
            .set("isolation", "isolate");

        // Create decorations container
        Div decorations = new Div();
        decorations.getStyle()
            .set("position", "absolute")
            .set("top", "0")
            .set("left", "0")
            .set("width", "100%")
            .set("height", "100%")
            .set("pointer-events", "none")
            .set("z-index", "1");

        // Add festive decorations (stars, balloons, trophies)
        String[][] decoItems = {
            {"⭐", "2%", "10%", "16px", "0.7"},
            {"✨", "8%", "85%", "14px", "0.6"},
            {"🎈", "5%", "45%", "18px", "0.8"},
            {"⭐", "92%", "15%", "16px", "0.7"},
            {"✨", "95%", "70%", "14px", "0.6"},
            {"🎈", "97%", "40%", "18px", "0.8"},
            {"🏆", "3%", "70%", "16px", "0.7"},
            {"🏆", "96%", "85%", "16px", "0.7"},
            {"🎉", "10%", "20%", "14px", "0.6"},
            {"🎉", "88%", "25%", "14px", "0.6"},
            {"💫", "15%", "60%", "12px", "0.5"},
            {"💫", "85%", "55%", "12px", "0.5"},
            {"🎊", "6%", "30%", "12px", "0.5"},
            {"🎊", "94%", "65%", "12px", "0.5"},
        };

        for (String[] deco : decoItems) {
            Span item = new Span(deco[0]);
            item.getStyle()
                .set("position", "absolute")
                .set("left", deco[1])
                .set("top", deco[2])
                .set("font-size", deco[3])
                .set("opacity", deco[4]);
            decorations.add(item);
        }

        // Style user profile section
        userProfile.getStyle()
            .set("position", "relative")
            .set("z-index", "2")
            .set("margin-bottom", "10px")
            .set("width", "calc(100% - 20px)")
            .set("box-sizing", "border-box");

        // Style the toolbar content to be visible above decorations
        toolbar.getStyle()
            .set("position", "relative")
            .set("z-index", "2")
            .set("background", "rgba(255, 255, 255, 0.95)")
            .set("padding", "12px 16px")
            .set("border-radius", "8px")
            .set("flex-wrap", "wrap")
            .set("gap", "10px")
            .set("min-height", "auto")
            .set("height", "auto")
            .set("display", "flex")
            .set("align-items", "center")
            .set("flex-direction", "row")
            .set("width", "calc(100% - 20px)")
            .set("box-sizing", "border-box");

        // Create inner content wrapper - use VerticalLayout for proper flow
        VerticalLayout contentWrapper = new VerticalLayout();
        contentWrapper.setPadding(false);
        contentWrapper.setSpacing(true);
        contentWrapper.setAlignItems(VerticalLayout.Alignment.CENTER);
        contentWrapper.getStyle()
            .set("position", "relative")
            .set("z-index", "2")
            .set("width", "100%")
            .set("padding", "0")
            .set("box-sizing", "border-box");
        contentWrapper.add(userProfile, toolbar);

        container.add(decorations, contentWrapper);
        return container;
    }

    private VerticalLayout createUserProfileSection() {
        VerticalLayout profileSection = new VerticalLayout();
        profileSection.setAlignItems(VerticalLayout.Alignment.CENTER);
        profileSection.setPadding(true);
        profileSection.setSpacing(false);
        profileSection.getStyle()
            .set("background", "rgba(255, 255, 255, 0.9)")
            .set("border-radius", "10px")
            .set("padding", "12px")
            .set("margin-bottom", "8px");

        // Get current user
        User currentUser = VaadinSession.getCurrent().getAttribute(User.class);

        // Create horizontal layout for avatar and flag
        HorizontalLayout avatarAndFlagLayout = new HorizontalLayout();
        avatarAndFlagLayout.setAlignItems(HorizontalLayout.Alignment.CENTER);
        avatarAndFlagLayout.setSpacing(true);
        avatarAndFlagLayout.getStyle().set("gap", "10px");

        // Create avatar container - smaller for mobile
        Div avatarContainer = new Div();
        avatarContainer.getStyle()
            .set("width", "60px")
            .set("height", "60px")
            .set("border-radius", "50%")
            .set("overflow", "hidden")
            .set("display", "flex")
            .set("align-items", "center")
            .set("justify-content", "center")
            .set("box-shadow", "0 4px 12px rgba(0,0,0,0.15)")
            .set("cursor", "pointer");

        // Display user photo if available, otherwise initials or default icon
        if (currentUser != null && currentUser.getPhotoBytes() != null && currentUser.getPhotoBytes().length > 0) {
            // User has uploaded a photo - display it
            StreamResource imageResource = new StreamResource("user-photo.jpg",
                () -> new ByteArrayInputStream(currentUser.getPhotoBytes()));
            Image userPhoto = new Image(imageResource, "User photo");
            userPhoto.setWidth("100%");
            userPhoto.setHeight("100%");
            userPhoto.getStyle().set("object-fit", "cover");
            avatarContainer.add(userPhoto);
        } else if (currentUser != null && currentUser.getName() != null && !currentUser.getName().isEmpty()) {
            // No photo - display initials on gradient background
            avatarContainer.getStyle()
                .set("background", "linear-gradient(135deg, #667eea 0%, #764ba2 100%)")
                .set("color", "white")
                .set("font-size", "24px")
                .set("font-weight", "bold");
            String initials = getInitials(currentUser.getName());
            Span initialsSpan = new Span(initials);
            avatarContainer.add(initialsSpan);
        } else {
            // No user or no name - display default icon
            avatarContainer.getStyle()
                .set("background", "linear-gradient(135deg, #667eea 0%, #764ba2 100%)")
                .set("color", "white")
                .set("font-size", "24px");
            Span defaultIcon = new Span("👤");
            avatarContainer.add(defaultIcon);
        }

        avatarAndFlagLayout.add(avatarContainer);

        // Add country flag if available
        logger.info("Checking country flag for user: {}", currentUser != null ? currentUser.getName() : "null");
        if (currentUser != null && currentUser.getCountry() != null) {
            logger.info("User has country: {}", currentUser.getCountry().getCountryName());
            String flagSvg = currentUser.getCountry().getCountryFlag();
            logger.info("Flag SVG length: {}", flagSvg != null ? flagSvg.length() : 0);
            if (flagSvg != null && !flagSvg.isEmpty()) {
                logger.info("Creating flag display for country: {}", currentUser.getCountry().getCountryName());
                Div flagContainer = new Div();
                flagContainer.getStyle()
                    .set("width", "45px")
                    .set("height", "30px")
                    .set("display", "flex")
                    .set("align-items", "center")
                    .set("justify-content", "center")
                    .set("border", "1px solid #e0e0e0")
                    .set("border-radius", "4px")
                    .set("box-shadow", "0 2px 4px rgba(0,0,0,0.1)");

                // Create StreamResource from SVG content
                StreamResource flagResource = new StreamResource("flag.svg",
                    () -> new ByteArrayInputStream(flagSvg.getBytes(java.nio.charset.StandardCharsets.UTF_8)));
                flagResource.setContentType("image/svg+xml");

                Image flagImage = new Image(flagResource, "Country flag");
                flagImage.setWidth("45px");
                flagImage.setHeight("30px");
                flagImage.getStyle()
                    .set("object-fit", "contain");

                flagContainer.add(flagImage);
                avatarAndFlagLayout.add(flagContainer);
                logger.info("Flag container added to layout");
            } else {
                logger.warn("Flag SVG is null or empty for country: {}", currentUser.getCountry().getCountryName());
            }
        } else {
            if (currentUser == null) {
                logger.warn("Current user is null");
            } else {
                logger.warn("User {} has no country associated", currentUser.getName());
            }
        }

        profileSection.add(avatarAndFlagLayout);

        // User name below avatar and flag
        if (currentUser != null && currentUser.getName() != null) {
            Paragraph userName = new Paragraph(currentUser.getName());
            userName.getStyle()
                .set("margin-top", "8px")
                .set("margin-bottom", "0")
                .set("font-size", "14px")
                .set("font-weight", "500")
                .set("color", "#333");
            profileSection.add(userName);
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

    private void loadQuizCards() {
        quizCardsContainer.removeAll();

        List<Quiz> quizzes = quizService.list(org.springframework.data.domain.Pageable.unpaged());

        logger.info("=== QuizListView: Loading Quiz Cards ===");
        logger.info("Number of quizzes retrieved: " + quizzes.size());

        if (quizzes.isEmpty()) {
            logger.info("WARNING: No quizzes found in database!");
            Paragraph noQuizMessage = new Paragraph(translationService.translate("quizlist.noQuizzes"));
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
        card.setWidth("73px");  // 66px * 1.10 = 72.6 ≈ 73px
        card.setHeight("121px");  // 110px * 1.10 = 121px
        card.setPadding(false);
        card.setSpacing(false);
        card.getStyle()
            .set("border", "1px solid #e0e0e0")
            .set("border-radius", "4px")
            .set("cursor", "pointer")
            .set("background-color", "white")
            .set("transition", "all 0.3s ease")
            .set("padding", "4px");

        // Image container - keep same size as before
        Div imageContainer = new Div();
        imageContainer.setWidth("100%");
        imageContainer.setHeight("97px");  // 88px * 1.10 = 96.8 ≈ 97px
        imageContainer.getStyle()
            .set("display", "flex")
            .set("align-items", "center")
            .set("justify-content", "center")
            .set("overflow", "hidden")
            .set("border-radius", "4px");

        // Load image
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

        // Quiz name
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

        // Click handler
        card.addClickListener(event -> {
            selectQuiz(quiz);
        });

        // Hover effects
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
        startButton.setText(translationService.translate("quizlist.start"));
        startButton.setEnabled(true);
        shareBtn.setEnabled(true);
        name.setValue(quiz.getName());

        // Update visual selection of all cards
        loadQuizCards();

        // Highlight selected card
        quizCardsContainer.getChildren().forEach(component -> {
            if (component instanceof VerticalLayout) {
                VerticalLayout card = (VerticalLayout) component;
                card.getStyle()
                    .set("border-color", "#e0e0e0")
                    .set("box-shadow", "none");
            }
        });
    }

    private void createQuiz() {
        quizService.createQuiz(name.getValue());
        loadQuizCards();
        name.clear();
        Notification.show(translationService.translate("quizlist.quizAdded"), 3000, Notification.Position.BOTTOM_END)
                .addThemeVariants(NotificationVariant.LUMO_SUCCESS);
    }

    private void showShareDialog(Quiz quiz) {
        User currentUser = VaadinSession.getCurrent().getAttribute(User.class);
        if (currentUser == null || currentUser.getId() == null) {
            Notification.show(translationService.translate("quizlist.loginRequired"), 3000, Notification.Position.MIDDLE)
                .addThemeVariants(NotificationVariant.LUMO_ERROR);
            return;
        }

        // Create a new session
        QuizSession session = sessionService.createSession(quiz, currentUser.getId());

        // Set team mode based on checkbox
        if (teamModeCheckbox.getValue()) {
            session.setTeamMode(true);
            sessionService.updateSession(session);
        }

        Dialog dialog = new Dialog();
        dialog.setHeaderTitle(translationService.translate("session.share") + ": " + quiz.getName());
        dialog.setWidth("600px");

        VerticalLayout content = new VerticalLayout();
        content.setSpacing(true);
        content.setPadding(false);
        content.setAlignItems(VerticalLayout.Alignment.STRETCH);

        // Team Mode Section
        Checkbox teamModeDialogCheckbox = new Checkbox(translationService.translate("quizSession.teamMode.enable"));
        teamModeDialogCheckbox.setValue(session.isTeamMode());
        teamModeDialogCheckbox.getStyle().set("margin-bottom", "10px");

        // Team selection section
        VerticalLayout teamSelectionLayout = new VerticalLayout();
        teamSelectionLayout.setPadding(false);
        teamSelectionLayout.setSpacing(true);
        teamSelectionLayout.setVisible(session.isTeamMode());
        teamSelectionLayout.getStyle()
            .set("background", "var(--lumo-contrast-5pct)")
            .set("padding", "var(--lumo-space-m)")
            .set("border-radius", "var(--lumo-border-radius-m)");

        H4 teamSelectionTitle = new H4(translationService.translate("quizSession.teamMode.selectTeams"));
        teamSelectionTitle.getStyle().set("margin", "0 0 var(--lumo-space-s) 0");

        String[] availableTeams = {"stark", "lannister", "targaryen", "baratheon", "tyrell", "martell", "arryn", "tully", "greyjoy"};
        java.util.Set<String> selectedTeamsSet = new java.util.HashSet<>();
        if (session.getSelectedTeams() != null && !session.getSelectedTeams().isEmpty()) {
            selectedTeamsSet.addAll(java.util.Arrays.asList(session.getSelectedTeams().split(",")));
        }

        HorizontalLayout teamsCheckboxLayout = new HorizontalLayout();
        teamsCheckboxLayout.setSpacing(true);
        teamsCheckboxLayout.getStyle().set("flex-wrap", "wrap");

        java.util.Map<String, Checkbox> teamCheckboxes = new java.util.HashMap<>();

        for (String team : availableTeams) {
            Checkbox teamCheckbox = new Checkbox(
                translationService.translate("quizSession.teamMode.team." + team)
            );
            teamCheckbox.setValue(selectedTeamsSet.contains(team));
            teamCheckboxes.put(team, teamCheckbox);
            teamsCheckboxLayout.add(teamCheckbox);
        }

        teamSelectionLayout.add(teamSelectionTitle, teamsCheckboxLayout);

        // Team mode checkbox change listener
        teamModeDialogCheckbox.addValueChangeListener(event -> {
            boolean teamMode = event.getValue();
            session.setTeamMode(teamMode);
            teamSelectionLayout.setVisible(teamMode);
            if (!teamMode) {
                session.setSelectedTeams(null);
            } else {
                // Auto-select previously selected teams or default teams
                java.util.List<String> selectedTeamsList = new java.util.ArrayList<>();
                teamCheckboxes.forEach((t, cb) -> {
                    if (cb.getValue()) {
                        selectedTeamsList.add(t);
                    }
                });
                if (!selectedTeamsList.isEmpty()) {
                    session.setSelectedTeams(String.join(",", selectedTeamsList));
                }
            }
            sessionService.updateSession(session);
        });

        // Update selected teams when checkboxes change
        teamCheckboxes.forEach((team, checkbox) -> {
            checkbox.addValueChangeListener(event -> {
                if (session.isTeamMode()) {
                    java.util.List<String> selectedTeamsList = new java.util.ArrayList<>();
                    teamCheckboxes.forEach((t, cb) -> {
                        if (cb.getValue()) {
                            selectedTeamsList.add(t);
                        }
                    });
                    session.setSelectedTeams(selectedTeamsList.isEmpty() ? null : String.join(",", selectedTeamsList));
                    sessionService.updateSession(session);
                }
            });
        });

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

        String addressServer= appProperties.getProperty("server.address");
        String portServer= appProperties.getProperty("server.port");
        String sessionUrl = "http://" + addressServer + ":" + portServer +"/quiz-session/" + session.getSessionCode();

        Image qrCode = new Image(QRCodeGenerator.generateQRCode(sessionUrl, 150, 150), "QR Code");
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
            // Validate team mode requirements
            if (session.isTeamMode()) {
                java.util.List<String> selectedTeamsList = new java.util.ArrayList<>();
                teamCheckboxes.forEach((t, cb) -> {
                    if (cb.getValue()) {
                        selectedTeamsList.add(t);
                    }
                });

                if (selectedTeamsList.size() < 2) {
                    String warningMessage;
                    if (selectedTeamsList.isEmpty()) {
                        warningMessage = translationService.translate("teammode.selectTeams.warning");
                    } else {
                        warningMessage = translationService.translate("teammode.selectTeams.minimum")
                            .replace("{0}", String.valueOf(selectedTeamsList.size()));
                    }
                    Notification.show(warningMessage, 5000, Notification.Position.MIDDLE)
                        .addThemeVariants(NotificationVariant.LUMO_ERROR);
                    return;
                }

                // Update session with selected teams
                session.setSelectedTeams(String.join(",", selectedTeamsList));
                sessionService.updateSession(session);
            }

            dialog.close();
            getUI().ifPresent(ui -> ui.navigate("quiz-session/" + session.getSessionCode()));
        });
        goToSessionButton.addThemeVariants(ButtonVariant.LUMO_PRIMARY);

        Button copyLinkButton = new Button(translationService.translate("session.copyLink"), event -> {
            getUI().ifPresent(ui -> ui.getPage().executeJs(
                "navigator.clipboard.writeText($0).then(() => {}, () => {})",
                sessionUrl
            ));
            Notification.show(translationService.translate("session.linkCopied"), 2000, Notification.Position.BOTTOM_CENTER)
                .addThemeVariants(NotificationVariant.LUMO_SUCCESS);
        });
        copyLinkButton.addThemeVariants(ButtonVariant.LUMO_TERTIARY);

        Button closeButton = new Button(translationService.translate("common.close"), event -> dialog.close());

        HorizontalLayout buttonLayout = new HorizontalLayout(goToSessionButton, copyLinkButton, closeButton);
        buttonLayout.setSpacing(true);

        content.add(teamModeDialogCheckbox, teamSelectionLayout, instructionTitle, qrCode, codeContainer, instructions, buttonLayout);
        dialog.add(content);
        dialog.open();
    }

}
