package com.quizz.core.ui;

import com.quizz.base.ui.MainLayout;
import com.quizz.base.ui.component.ViewToolbar;
import com.quizz.core.entity.QuizQuestionsData;
import com.quizz.core.service.QuizJsonService;
import com.quizz.core.service.QuizService;
import com.quizz.core.service.TranslationService;
import com.vaadin.flow.component.button.Button;
import com.vaadin.flow.component.button.ButtonVariant;
import com.vaadin.flow.component.combobox.ComboBox;
import com.vaadin.flow.component.formlayout.FormLayout;
import com.vaadin.flow.component.notification.Notification;
import com.vaadin.flow.component.notification.NotificationVariant;
import com.vaadin.flow.component.orderedlayout.HorizontalLayout;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import com.vaadin.flow.component.radiobutton.RadioButtonGroup;
import com.vaadin.flow.component.textfield.TextArea;
import com.vaadin.flow.component.textfield.TextField;
import com.vaadin.flow.i18n.LocaleChangeEvent;
import com.vaadin.flow.i18n.LocaleChangeObserver;
import com.vaadin.flow.router.Menu;
import com.vaadin.flow.router.PageTitle;
import com.vaadin.flow.router.Route;
import jakarta.annotation.security.RolesAllowed;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.util.List;

@Route(value = "admin/quiz-editor", layout = MainLayout.class)
@PageTitle("menu.editquizzes")
@RolesAllowed("ADMIN")
@Menu(order = 5, icon = "vaadin:edit", title = "menu.editquizzes")
public class QuizEditorView extends VerticalLayout implements LocaleChangeObserver {

    private static final Logger logger = LoggerFactory.getLogger(QuizEditorView.class);

    private final QuizJsonService quizJsonService;
    private final TranslationService translationService;

    private ComboBox<String> quizSelector;
    private TextField questionNumberField;
    private TextArea questionField;
    private TextArea optionsField;
    private TextField answerField;
    private RadioButtonGroup<Integer> difficultyLevelRadio;
    private Button updateButton;
    private Button previousButton;
    private Button nextButton;

    private List<QuizQuestionsData.QuestionData> currentQuestions;
    private int currentQuestionIndex = 0;
    private String currentQuizName;

    public QuizEditorView(QuizJsonService quizJsonService, QuizService quizService, TranslationService translationService) {
        this.quizJsonService = quizJsonService;
        this.translationService = translationService;

        // Log pour déboguer la locale
        logger.info("QuizEditorView constructor - Current locale: {}", translationService.getCurrentLocale());
        logger.info("QuizEditorView constructor - 'quizEditor.selectQuiz' translates to: {}", translationService.translate("quizEditor.selectQuiz"));

        setSizeFull();
        setPadding(true);
        setSpacing(true);

        // Toolbar avec titre
        add(new ViewToolbar(translationService.translate("quizEditor.title")));

        // Sélecteur de quiz
        createQuizSelector(quizService);

        // Formulaire de question
        createQuestionForm();

        // Boutons de navigation
        createNavigationButtons();

        // Bouton de mise à jour
        createUpdateButton();

        // Désactiver le formulaire au départ
        setFormEnabled(false);
    }

    private void createQuizSelector(QuizService quizService) {
        quizSelector = new ComboBox<>(translationService.translate("quizEditor.selectQuiz"));
        quizSelector.setWidthFull();

        // Charger la liste des quiz
        try {
            QuizQuestionsData data = quizJsonService.loadQuizData();
            List<String> quizNames = data.getQuizzes().stream()
                    .map(QuizQuestionsData.QuizData::getName)
                    .toList();
            quizSelector.setItems(quizNames);
        } catch (IOException e) {
            logger.error("Error loading quiz list", e);
            showErrorNotification(translationService.translate("quizEditor.error.loadingQuizList") + ": " + e.getMessage());
        }

        quizSelector.addValueChangeListener(event -> {
            if (event.getValue() != null) {
                loadQuizQuestions(event.getValue());
            }
        });

        add(quizSelector);
    }

    private void createQuestionForm() {
        FormLayout formLayout = new FormLayout();
        formLayout.setWidthFull();

        // Numéro de question (lecture seule)
        questionNumberField = new TextField(translationService.translate("quizEditor.questionNumber"));
        questionNumberField.setReadOnly(true);
        questionNumberField.setWidth("150px");

        // Question (lecture seule)
        questionField = new TextArea(translationService.translate("quizEditor.question"));
        questionField.setReadOnly(true);
        questionField.setWidthFull();
        questionField.setHeight("100px");

        // Options (lecture seule)
        optionsField = new TextArea(translationService.translate("quizEditor.options"));
        optionsField.setReadOnly(true);
        optionsField.setWidthFull();
        optionsField.setHeight("120px");

        // Réponse (lecture seule)
        answerField = new TextField(translationService.translate("quizEditor.answer"));
        answerField.setReadOnly(true);
        answerField.setWidthFull();

        // Niveau de difficulté (éditable)
        difficultyLevelRadio = new RadioButtonGroup<>();
        difficultyLevelRadio.setLabel(translationService.translate("quizEditor.difficultyLevel"));
        difficultyLevelRadio.setItems(1, 2, 3, 4);
        difficultyLevelRadio.setValue(1);

        formLayout.add(questionNumberField, questionField, optionsField, answerField, difficultyLevelRadio);
        formLayout.setColspan(questionField, 2);
        formLayout.setColspan(optionsField, 2);

        add(formLayout);
    }

    private void createNavigationButtons() {
        previousButton = new Button(translationService.translate("quizEditor.previous"));
        previousButton.addThemeVariants(ButtonVariant.LUMO_TERTIARY);
        previousButton.addClickListener(event -> navigateToPrevious());

        nextButton = new Button(translationService.translate("quizEditor.next"));
        nextButton.addThemeVariants(ButtonVariant.LUMO_TERTIARY);
        nextButton.addClickListener(event -> navigateToNext());

        HorizontalLayout navigationLayout = new HorizontalLayout(previousButton, nextButton);
        navigationLayout.setSpacing(true);
        add(navigationLayout);
    }

    private void createUpdateButton() {
        updateButton = new Button(translationService.translate("quizEditor.updateFile"));
        updateButton.addThemeVariants(ButtonVariant.LUMO_PRIMARY);
        updateButton.addClickListener(event -> updateQuestion());
        add(updateButton);
    }

    private void loadQuizQuestions(String quizName) {
        try {
            currentQuizName = quizName;
            currentQuestions = quizJsonService.getQuizQuestions(quizName);
            currentQuestionIndex = 0;

            if (currentQuestions.isEmpty()) {
                showErrorNotification(translationService.translate("quizEditor.error.noQuestions"));
                setFormEnabled(false);
            } else {
                setFormEnabled(true);
                displayQuestion(currentQuestionIndex);
                logger.info("Loaded {} questions for quiz '{}'", currentQuestions.size(), quizName);
            }
        } catch (IOException e) {
            logger.error("Error loading questions", e);
            showErrorNotification(translationService.translate("quizEditor.error.loadingQuestions") + ": " + e.getMessage());
            setFormEnabled(false);
        }
    }

    private void displayQuestion(int index) {
        if (currentQuestions == null || index < 0 || index >= currentQuestions.size()) {
            return;
        }

        QuizQuestionsData.QuestionData question = currentQuestions.get(index);

        questionNumberField.setValue(String.format("%d / %d (ID: %d)",
                index + 1, currentQuestions.size(), question.getId()));
        questionField.setValue(question.getQuestion());

        // Afficher les options numérotées
        StringBuilder optionsText = new StringBuilder();
        List<String> options = question.getOptions();
        for (int i = 0; i < options.size(); i++) {
            optionsText.append(i + 1).append(". ").append(options.get(i)).append("\n");
        }
        optionsField.setValue(optionsText.toString());

        answerField.setValue(question.getAnswer());
        difficultyLevelRadio.setValue(question.getDifficulty_level() > 0 ? question.getDifficulty_level() : 1);

        // Mettre à jour l'état des boutons de navigation
        previousButton.setEnabled(index > 0);
        nextButton.setEnabled(index < currentQuestions.size() - 1);
    }

    private void navigateToPrevious() {
        if (currentQuestionIndex > 0) {
            currentQuestionIndex--;
            displayQuestion(currentQuestionIndex);
        }
    }

    private void navigateToNext() {
        if (currentQuestions != null && currentQuestionIndex < currentQuestions.size() - 1) {
            currentQuestionIndex++;
            displayQuestion(currentQuestionIndex);
        }
    }

    private void updateQuestion() {
        if (currentQuestions == null || currentQuestionIndex < 0 || currentQuestionIndex >= currentQuestions.size()) {
            showErrorNotification(translationService.translate("quizEditor.error.noQuestionSelected"));
            return;
        }

        QuizQuestionsData.QuestionData question = currentQuestions.get(currentQuestionIndex);
        Integer newDifficultyLevel = difficultyLevelRadio.getValue();

        try {
            quizJsonService.updateQuestionDifficultyLevel(currentQuizName, question.getId(), newDifficultyLevel);

            // Mettre à jour localement
            question.setDifficulty_level(newDifficultyLevel);

            showSuccessNotification(translationService.translate("quizEditor.success.questionUpdated",
                    question.getId(), newDifficultyLevel));

            logger.info("Updated question ID {} to difficulty level {}", question.getId(), newDifficultyLevel);
        } catch (IOException e) {
            logger.error("Error updating question", e);
            showErrorNotification(translationService.translate("quizEditor.error.updatingQuestion") + ": " + e.getMessage());
        }
    }

    private void setFormEnabled(boolean enabled) {
        difficultyLevelRadio.setEnabled(enabled);
        updateButton.setEnabled(enabled);
        previousButton.setEnabled(enabled && currentQuestionIndex > 0);
        nextButton.setEnabled(enabled && currentQuestions != null && currentQuestionIndex < currentQuestions.size() - 1);
    }

    private void showSuccessNotification(String message) {
        Notification notification = Notification.show(message, 3000, Notification.Position.BOTTOM_CENTER);
        notification.addThemeVariants(NotificationVariant.LUMO_SUCCESS);
    }

    private void showErrorNotification(String message) {
        Notification notification = Notification.show(message, 5000, Notification.Position.BOTTOM_CENTER);
        notification.addThemeVariants(NotificationVariant.LUMO_ERROR);
    }

    @Override
    public void localeChange(LocaleChangeEvent event) {
        logger.info("LocaleChangeObserver triggered - new locale: {}", event.getLocale());

        // Mettre à jour tous les labels traduits
        quizSelector.setLabel(translationService.translate("quizEditor.selectQuiz"));
        questionNumberField.setLabel(translationService.translate("quizEditor.questionNumber"));
        questionField.setLabel(translationService.translate("quizEditor.question"));
        optionsField.setLabel(translationService.translate("quizEditor.options"));
        answerField.setLabel(translationService.translate("quizEditor.answer"));
        difficultyLevelRadio.setLabel(translationService.translate("quizEditor.difficultyLevel"));
        previousButton.setText(translationService.translate("quizEditor.previous"));
        nextButton.setText(translationService.translate("quizEditor.next"));
        updateButton.setText(translationService.translate("quizEditor.updateFile"));

        logger.info("All labels updated for locale: {}", event.getLocale());
    }
}

