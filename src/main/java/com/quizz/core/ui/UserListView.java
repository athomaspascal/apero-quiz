package com.quizz.core.ui;

import com.quizz.base.ui.component.ViewToolbar;
import com.quizz.core.entity.Country;
import com.quizz.core.entity.User;
import com.quizz.core.entity.Gender;
import com.quizz.core.service.CountryService;
import com.quizz.core.service.UserService;
import com.quizz.core.service.TranslationService;
import com.vaadin.flow.component.AttachEvent;
import com.vaadin.flow.component.button.Button;
import com.vaadin.flow.component.button.ButtonVariant;
import com.vaadin.flow.component.combobox.ComboBox;
import com.vaadin.flow.component.dialog.Dialog;
import com.vaadin.flow.component.formlayout.FormLayout;
import com.vaadin.flow.component.grid.Grid;
import com.vaadin.flow.component.html.Main;
import com.vaadin.flow.component.html.Span;
import com.vaadin.flow.component.notification.Notification;
import com.vaadin.flow.component.notification.NotificationVariant;
import com.vaadin.flow.component.orderedlayout.HorizontalLayout;
import com.vaadin.flow.component.textfield.EmailField;
import com.vaadin.flow.component.textfield.PasswordField;
import com.vaadin.flow.component.textfield.TextField;
import com.vaadin.flow.router.*;
import com.vaadin.flow.server.VaadinSession;
import com.vaadin.flow.theme.lumo.LumoUtility;

import static com.vaadin.flow.spring.data.VaadinSpringDataHelpers.toSpringPageRequest;

@Route("users")
@PageTitle("Users")
@Menu(order = 2, icon = "vaadin:users", title = "menu.users")
class UserListView extends Main implements BeforeEnterObserver {

    private final UserService userService;
    private final CountryService countryService;
    private final TranslationService translationService;
    private final Grid<User> userGrid;

    UserListView(UserService userService, CountryService countryService, TranslationService translationService) {
        this.userService = userService;
        this.countryService = countryService;
        this.translationService = translationService;

        Button createUserBtn = new Button(translationService.translate("users.create"), event -> openUserDialog(null));
        createUserBtn.addThemeVariants(ButtonVariant.LUMO_PRIMARY);

        userGrid = new Grid<>();
        userGrid.setItems(query -> userService.list(toSpringPageRequest(query)).stream());
        userGrid.addColumn(User::getName).setHeader(translationService.translate("users.name")).setSortable(true);
        userGrid.addColumn(User::getEmail).setHeader(translationService.translate("users.email")).setSortable(true);
        userGrid.addColumn(User::getTelephone).setHeader(translationService.translate("users.telephone"));
        userGrid.addColumn(user -> user.getCountry() != null ? user.getCountry().getCountryName() : "")
            .setHeader(translationService.translate("users.country")).setSortable(true);
        userGrid.addComponentColumn(user -> {
            // Disable edit/delete for public users
            if (user.isPublic()) {
                Span publicLabel = new Span("Public User");
                publicLabel.getStyle().set("color", "var(--lumo-secondary-text-color)");
                publicLabel.getStyle().set("font-style", "italic");
                return publicLabel;
            }

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
    public void beforeEnter(BeforeEnterEvent event) {
        // Check if current user is admin
        User currentUser = VaadinSession.getCurrent().getAttribute(User.class);

        if (currentUser == null || !currentUser.isAdmin()) {
            // Redirect to quiz list if not admin
            event.rerouteTo("");
            Notification.show("Access denied. Admins only.", 3000, Notification.Position.MIDDLE)
                .addThemeVariants(NotificationVariant.LUMO_ERROR);
        }
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

        // Add country selection ComboBox with flag display
        ComboBox<Country> countryComboBox = new ComboBox<>(translationService.translate("users.country"));
        countryComboBox.setItems(countryService.findAll());
        countryComboBox.setItemLabelGenerator(Country::getCountryName);

        // Container to display the selected country flag
        com.vaadin.flow.component.html.Div selectedFlagContainer = new com.vaadin.flow.component.html.Div();
        selectedFlagContainer.getStyle()
            .set("width", "30px")
            .set("height", "20px")
            .set("display", "flex")
            .set("align-items", "center")
            .set("justify-content", "center")
            .set("border", "1px solid #e0e0e0")
            .set("border-radius", "2px")
            .set("margin-top", "8px");

        // Custom renderer to display flag and country name in dropdown
        countryComboBox.setRenderer(new com.vaadin.flow.data.renderer.ComponentRenderer<>(country -> {
            com.vaadin.flow.component.orderedlayout.HorizontalLayout layout = new com.vaadin.flow.component.orderedlayout.HorizontalLayout();
            layout.setAlignItems(com.vaadin.flow.component.orderedlayout.FlexComponent.Alignment.CENTER);
            layout.setSpacing(true);
            layout.getStyle().set("line-height", "var(--lumo-line-height-xs)");

            // Create flag container for dropdown
            if (country.getCountryFlag() != null && !country.getCountryFlag().isEmpty()) {
                com.vaadin.flow.component.html.Div flagContainer = new com.vaadin.flow.component.html.Div();
                flagContainer.getStyle()
                    .set("width", "24px")
                    .set("height", "16px")
                    .set("display", "flex")
                    .set("align-items", "center")
                    .set("justify-content", "center")
                    .set("border", "1px solid #e0e0e0")
                    .set("border-radius", "2px")
                    .set("flex-shrink", "0");

                // Embed SVG directly as HTML
                flagContainer.getElement().setProperty("innerHTML", country.getCountryFlag());
                flagContainer.getElement().getStyle()
                    .set("width", "24px")
                    .set("height", "16px");

                layout.add(flagContainer);
            }

            // Add country name
            com.vaadin.flow.component.html.Span nameSpan = new com.vaadin.flow.component.html.Span(country.getCountryName());
            layout.add(nameSpan);

            return layout;
        }));

        // Add value change listener to update the selected flag display
        countryComboBox.addValueChangeListener(event -> {
            selectedFlagContainer.removeAll();
            Country selectedCountry = event.getValue();
            if (selectedCountry != null && selectedCountry.getCountryFlag() != null && !selectedCountry.getCountryFlag().isEmpty()) {
                // Embed SVG directly as HTML for the selected flag
                selectedFlagContainer.getElement().setProperty("innerHTML", selectedCountry.getCountryFlag());
            }
        });

        countryComboBox.setRequired(true);
        countryComboBox.setRequiredIndicatorVisible(true);
        countryComboBox.setPlaceholder(translationService.translate("users.selectCountry"));

        // Create a layout to hold the combobox and the selected flag
        com.vaadin.flow.component.orderedlayout.VerticalLayout countryLayout = new com.vaadin.flow.component.orderedlayout.VerticalLayout();
        countryLayout.setSpacing(false);
        countryLayout.setPadding(false);
        countryLayout.add(countryComboBox, selectedFlagContainer);

        if (user != null) {
            nameField.setValue(user.getName());
            emailField.setValue(user.getEmail());
            telephoneField.setValue(user.getTelephone());
            passwordField.setValue(user.getPassword());
            if (user.getCountry() != null) {
                countryComboBox.setValue(user.getCountry());
                // Display the flag for the existing country
                if (user.getCountry().getCountryFlag() != null && !user.getCountry().getCountryFlag().isEmpty()) {
                    selectedFlagContainer.getElement().setProperty("innerHTML", user.getCountry().getCountryFlag());
                }
            }
        }

        FormLayout formLayout = new FormLayout();
        formLayout.add(nameField, emailField, telephoneField, passwordField, countryLayout);
        formLayout.setResponsiveSteps(
            new FormLayout.ResponsiveStep("0", 1),
            new FormLayout.ResponsiveStep("500px", 2)
        );

        Button saveButton = new Button(translationService.translate("common.save"), event -> {
            // Validate that country is selected
            if (countryComboBox.getValue() == null) {
                Notification.show(translationService.translate("users.countryRequired"), 3000, Notification.Position.BOTTOM_END)
                    .addThemeVariants(NotificationVariant.LUMO_ERROR);
                return;
            }

            try {
                if (user == null) {
                    User newUser = userService.createUser(
                        nameField.getValue(),
                        emailField.getValue(),
                        telephoneField.getValue(),
                        passwordField.getValue(),
                        Gender.MALE  // Default gender for admin-created users
                    );
                    // Set the country and save
                    newUser.setCountry(countryComboBox.getValue());
                    userService.save(newUser);

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
                    // Update the country
                    User updatedUser = userService.getById(user.getId());
                    if (updatedUser != null) {
                        updatedUser.setCountry(countryComboBox.getValue());
                        userService.save(updatedUser);
                    }

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
