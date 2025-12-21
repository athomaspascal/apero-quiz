package com.quizz.core.ui;

import com.quizz.base.ui.component.ViewToolbar;
import com.quizz.core.entity.User;
import com.quizz.core.entity.Gender;
import com.quizz.core.service.UserService;
import com.quizz.core.service.TranslationService;
import com.vaadin.flow.component.AttachEvent;
import com.vaadin.flow.component.button.Button;
import com.vaadin.flow.component.button.ButtonVariant;
import com.vaadin.flow.component.dialog.Dialog;
import com.vaadin.flow.component.formlayout.FormLayout;
import com.vaadin.flow.component.grid.Grid;
import com.vaadin.flow.component.html.Main;
import com.vaadin.flow.component.notification.Notification;
import com.vaadin.flow.component.notification.NotificationVariant;
import com.vaadin.flow.component.orderedlayout.HorizontalLayout;
import com.vaadin.flow.component.textfield.EmailField;
import com.vaadin.flow.component.textfield.PasswordField;
import com.vaadin.flow.component.textfield.TextField;
import com.vaadin.flow.router.Menu;
import com.vaadin.flow.router.PageTitle;
import com.vaadin.flow.router.Route;
import com.vaadin.flow.theme.lumo.LumoUtility;

import static com.vaadin.flow.spring.data.VaadinSpringDataHelpers.toSpringPageRequest;

@Route("users")
@PageTitle("Users")
@Menu(order = 2, icon = "vaadin:users", title = "menu.users")
class UserListView extends Main {

    private final UserService userService;
    private final TranslationService translationService;
    private final Grid<User> userGrid;

    UserListView(UserService userService, TranslationService translationService) {
        this.userService = userService;
        this.translationService = translationService;

        Button createUserBtn = new Button(translationService.translate("users.create"), event -> openUserDialog(null));
        createUserBtn.addThemeVariants(ButtonVariant.LUMO_PRIMARY);

        userGrid = new Grid<>();
        userGrid.setItems(query -> userService.list(toSpringPageRequest(query)).stream());
        userGrid.addColumn(User::getName).setHeader(translationService.translate("users.name")).setSortable(true);
        userGrid.addColumn(User::getEmail).setHeader(translationService.translate("users.email")).setSortable(true);
        userGrid.addColumn(User::getTelephone).setHeader(translationService.translate("users.telephone"));
        userGrid.addComponentColumn(user -> {
            Button editButton = new Button(translationService.translate("common.edit"), event -> openUserDialog(user));
            editButton.addThemeVariants(ButtonVariant.LUMO_SMALL);

            Button deleteButton = new Button(translationService.translate("common.delete"), event -> deleteUser(user));
            deleteButton.addThemeVariants(ButtonVariant.LUMO_ERROR, ButtonVariant.LUMO_SMALL);

            HorizontalLayout actions = new HorizontalLayout(editButton, deleteButton);
            actions.setSpacing(true);
            return actions;
        }).setHeader(translationService.translate("common.actions")).setAutoWidth(true);

        userGrid.setSizeFull();

        setSizeFull();
        addClassNames(LumoUtility.BoxSizing.BORDER, LumoUtility.Display.FLEX, LumoUtility.FlexDirection.COLUMN,
                LumoUtility.Padding.MEDIUM, LumoUtility.Gap.SMALL);

        add(new ViewToolbar(translationService.translate("users.toolbarTitle"), createUserBtn));
        add(userGrid);

        // Set initial dynamic page title
        getUI().ifPresent(ui -> ui.getPage().setTitle(translationService.translate("users.pageTitle")));
    }

    @Override
    protected void onAttach(AttachEvent attachEvent) {
        super.onAttach(attachEvent);
        // Update dynamic page title on attach
        getUI().ifPresent(ui -> ui.getPage().setTitle(translationService.translate("users.pageTitle")));
    }

    private void openUserDialog(User user) {
        Dialog dialog = new Dialog();
        dialog.setHeaderTitle(user == null ? translationService.translate("users.createDialogTitle") : translationService.translate("users.editDialogTitle"));

        TextField nameField = new TextField(translationService.translate("users.name"));
        nameField.setMaxLength(User.NAME_MAX_LENGTH);
        nameField.setRequired(true);

        EmailField emailField = new EmailField(translationService.translate("users.email"));
        emailField.setMaxLength(User.EMAIL_MAX_LENGTH);
        emailField.setRequired(true);

        TextField telephoneField = new TextField(translationService.translate("users.telephone"));
        telephoneField.setMaxLength(User.TELEPHONE_MAX_LENGTH);
        telephoneField.setRequired(true);

        PasswordField passwordField = new PasswordField(translationService.translate("users.password"));
        passwordField.setMaxLength(User.PASSWORD_MAX_LENGTH);
        passwordField.setRequired(true);

        if (user != null) {
            nameField.setValue(user.getName());
            emailField.setValue(user.getEmail());
            telephoneField.setValue(user.getTelephone());
            passwordField.setValue(user.getPassword());
        }

        FormLayout formLayout = new FormLayout();
        formLayout.add(nameField, emailField, telephoneField, passwordField);
        formLayout.setResponsiveSteps(
            new FormLayout.ResponsiveStep("0", 1),
            new FormLayout.ResponsiveStep("500px", 2)
        );

        Button saveButton = new Button(translationService.translate("common.save"), event -> {
            try {
                if (user == null) {
                    userService.createUser(
                        nameField.getValue(),
                        emailField.getValue(),
                        telephoneField.getValue(),
                        passwordField.getValue(),
                        Gender.MALE  // Default gender for admin-created users
                    );
                    Notification.show(translationService.translate("users.created"), 3000, Notification.Position.BOTTOM_END)
                        .addThemeVariants(NotificationVariant.LUMO_SUCCESS);
                } else {
                    if (user.getId() == null) {
                        throw new IllegalStateException("User ID cannot be null");
                    }
                    userService.updateUser(
                        user.getId(),
                        nameField.getValue(),
                        emailField.getValue(),
                        telephoneField.getValue(),
                        passwordField.getValue()
                    );
                    Notification.show(translationService.translate("users.updated"), 3000, Notification.Position.BOTTOM_END)
                        .addThemeVariants(NotificationVariant.LUMO_SUCCESS);
                }
                userGrid.getDataProvider().refreshAll();
                dialog.close();
            } catch (IllegalArgumentException e) {
                Notification.show(getTranslation("common.errorWithMessage", e.getMessage()), 3000, Notification.Position.BOTTOM_END)
                    .addThemeVariants(NotificationVariant.LUMO_ERROR);
            }
        });
        saveButton.addThemeVariants(ButtonVariant.LUMO_PRIMARY);

        Button cancelButton = new Button(translationService.translate("common.cancel"), event -> dialog.close());

        HorizontalLayout buttonLayout = new HorizontalLayout(saveButton, cancelButton);
        buttonLayout.setSpacing(true);

        dialog.add(formLayout);
        dialog.getFooter().add(buttonLayout);
        dialog.open();
    }

    private void deleteUser(User user) {
        try {
            if (user.getId() == null) {
                throw new IllegalStateException("User ID cannot be null");
            }
            userService.deleteUser(user.getId());
            userGrid.getDataProvider().refreshAll();
            Notification.show(translationService.translate("users.deleted"), 3000, Notification.Position.BOTTOM_END)
                .addThemeVariants(NotificationVariant.LUMO_SUCCESS);
        } catch (Exception e) {
            Notification.show(getTranslation("common.errorWithMessage", e.getMessage()), 3000, Notification.Position.BOTTOM_END)
                .addThemeVariants(NotificationVariant.LUMO_ERROR);
        }
    }
}
