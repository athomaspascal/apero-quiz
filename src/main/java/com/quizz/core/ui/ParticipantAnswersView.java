package com.quizz.core.ui;

import com.quizz.core.dto.ParticipantAnswerStats;
import com.quizz.core.entity.QuizParticipant;
import com.quizz.core.service.QuizAnswerService;
import com.vaadin.flow.component.button.Button;
import com.vaadin.flow.component.button.ButtonVariant;
import com.vaadin.flow.component.grid.Grid;
import com.vaadin.flow.component.html.Div;
import com.vaadin.flow.component.html.H2;
import com.vaadin.flow.component.html.H3;
import com.vaadin.flow.component.html.Paragraph;
import com.vaadin.flow.component.icon.VaadinIcon;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import com.vaadin.flow.router.BeforeEnterEvent;
import com.vaadin.flow.router.BeforeEnterObserver;
import com.vaadin.flow.router.PageTitle;
import com.vaadin.flow.router.Route;
import com.vaadin.flow.theme.lumo.LumoUtility;

/**
 * View to display detailed answer statistics for a participant
 */
@Route("participant-answers/:participantId")
@PageTitle("Answer Details")
public class ParticipantAnswersView extends VerticalLayout implements BeforeEnterObserver {

    private final QuizAnswerService answerService;
    private final H2 title;
    private final Div statsContainer;
    private final Grid<ParticipantAnswerStats.QuestionAnswerDetail> answersGrid;

    public ParticipantAnswersView(QuizAnswerService answerService) {
        this.answerService = answerService;

        // Bouton de retour en haut à gauche (visible uniquement quand le menu latéral n'est pas affiché)
        Button backButton = new Button("Back to Quiz List", VaadinIcon.ARROW_LEFT.create());
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

        title = new H2("Answer Details");
        title.addClassNames(LumoUtility.Margin.Bottom.MEDIUM);

        statsContainer = new Div();
        statsContainer.addClassNames(LumoUtility.Margin.Bottom.LARGE);

        // Create grid for detailed answers
        answersGrid = new Grid<>(ParticipantAnswerStats.QuestionAnswerDetail.class, false);
        answersGrid.addColumn(ParticipantAnswerStats.QuestionAnswerDetail::getQuestionText)
            .setHeader("Question")
            .setAutoWidth(true)
            .setFlexGrow(3);

        answersGrid.addColumn(ParticipantAnswerStats.QuestionAnswerDetail::getUserAnswer)
            .setHeader("Your Answer")
            .setAutoWidth(true)
            .setFlexGrow(1);

        answersGrid.addColumn(ParticipantAnswerStats.QuestionAnswerDetail::getCorrectAnswer)
            .setHeader("Correct Answer")
            .setAutoWidth(true)
            .setFlexGrow(1);

        answersGrid.addComponentColumn(detail -> {
            Div status = new Div();
            if (detail.isCorrect()) {
                status.setText("✓ Correct");
                status.getStyle().set("color", "green").set("font-weight", "bold");
            } else {
                status.setText("✗ Incorrect");
                status.getStyle().set("color", "red").set("font-weight", "bold");
            }
            return status;
        }).setHeader("Status").setAutoWidth(true).setFlexGrow(0);

        answersGrid.addColumn(detail -> {
            Integer time = detail.getTimeTakenSeconds();
            return time != null ? time + "s" : "-";
        }).setHeader("Time").setAutoWidth(true).setFlexGrow(0);

        addClassNames(LumoUtility.Padding.LARGE);
        add(backButton, title, statsContainer, answersGrid);
        setSizeFull();
    }

    @Override
    public void beforeEnter(BeforeEnterEvent event) {
        String participantIdParam = event.getRouteParameters().get("participantId").orElse(null);

        if (participantIdParam == null) {
            event.rerouteTo("");
            return;
        }

        try {
            Long participantId = Long.parseLong(participantIdParam);

            // Get participant stats
            // Note: We need to get the participant first
            // This is a simplified version - you might want to add a method in the service
            // to get stats by participant ID directly

            displayStats(participantId);

        } catch (NumberFormatException e) {
            event.rerouteTo("");
        }
    }

    private void displayStats(Long participantId) {
        // This is a placeholder - in a real implementation, you would:
        // 1. Get the QuizParticipant by ID
        // 2. Get the stats using answerService.getParticipantStats(participant)
        // 3. Display the stats

        statsContainer.removeAll();

        H3 statsTitle = new H3("Statistics Summary");
        Paragraph comingSoon = new Paragraph("Detailed statistics will be displayed here.");

        statsContainer.add(statsTitle, comingSoon);
    }
}

