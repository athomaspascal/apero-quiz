package com.quizz.core.ui.component;

import com.quizz.core.config.InactivityConfig;
import com.quizz.core.entity.User;
import com.quizz.core.service.TranslationService;
import com.quizz.core.service.UserActivityService;
import com.vaadin.flow.component.AttachEvent;
import com.vaadin.flow.component.DetachEvent;
import com.vaadin.flow.component.UI;
import com.vaadin.flow.component.dialog.Dialog;
import com.vaadin.flow.component.html.H2;
import com.vaadin.flow.component.html.Paragraph;
import com.vaadin.flow.component.button.Button;
import com.vaadin.flow.component.button.ButtonVariant;
import com.vaadin.flow.component.orderedlayout.FlexComponent;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import com.vaadin.flow.server.VaadinSession;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.ScheduledFuture;
import java.util.concurrent.TimeUnit;

/**
 * Component that monitors user inactivity and shows a countdown dialog before forced logout
 */
public class InactivityMonitor extends VerticalLayout {

    private static final Logger logger = LoggerFactory.getLogger(InactivityMonitor.class);

    private final UserActivityService userActivityService;
    private final TranslationService translationService;
    private final InactivityConfig inactivityConfig;

    private ScheduledExecutorService executor;
    private ScheduledFuture<?> inactivityCheckTask;
    private ScheduledFuture<?> countdownTask;
    private Dialog warningDialog;
    private Paragraph countdownText;
    private int remainingSeconds;
    private boolean isDialogOpen = false;

    public InactivityMonitor(UserActivityService userActivityService, TranslationService translationService,
                             InactivityConfig inactivityConfig) {
        this.userActivityService = userActivityService;
        this.translationService = translationService;
        this.inactivityConfig = inactivityConfig;
        setVisible(false); // This component is invisible, it just monitors
    }

    @Override
    protected void onAttach(AttachEvent attachEvent) {
        super.onAttach(attachEvent);

        User currentUser = VaadinSession.getCurrent().getAttribute(User.class);
        if (currentUser == null) {
            logger.info("InactivityMonitor: No user logged in, monitoring not started");
            return; // No user logged in, no monitoring needed
        }

        logger.info("InactivityMonitor: Starting inactivity monitor for user: {} with threshold: {} seconds, check interval: {} seconds",
            currentUser.getName(),
            inactivityConfig.getThresholdSeconds(),
            inactivityConfig.getCheckIntervalSeconds());
        executor = Executors.newScheduledThreadPool(1);
        startInactivityCheck();
    }

    @Override
    protected void onDetach(DetachEvent detachEvent) {
        super.onDetach(detachEvent);
        logger.info("InactivityMonitor: Detaching and stopping tasks");
        stopAllTasks();
        if (executor != null && !executor.isShutdown()) {
            executor.shutdown();
        }
    }

    private void startInactivityCheck() {
        if (inactivityCheckTask != null && !inactivityCheckTask.isDone()) {
            logger.info("InactivityMonitor: Check task already running");
            return;
        }

        int checkIntervalSeconds = inactivityConfig.getCheckIntervalSeconds();
        int thresholdSeconds = inactivityConfig.getThresholdSeconds();

        logger.info("InactivityMonitor: Starting scheduled check every {} seconds", checkIntervalSeconds);

        inactivityCheckTask = executor.scheduleAtFixedRate(() -> {
            try {
                UI ui = getUI().orElse(null);
                if (ui == null) {
                    logger.debug("InactivityMonitor: UI not available");
                    return;
                }

                ui.access(() -> {
                    User currentUser = VaadinSession.getCurrent().getAttribute(User.class);
                    if (currentUser == null) {
                        logger.debug("InactivityMonitor: No user in session");
                        return;
                    }

                    // Check if user is inactive
                    boolean isInactive = userActivityService.isUserInactive(currentUser.getId(), thresholdSeconds);

                    logger.debug("InactivityMonitor: Checking user {} - isInactive: {}, isDialogOpen: {}",
                        currentUser.getName(), isInactive, isDialogOpen);

                    if (isInactive && !isDialogOpen) {
                        logger.info("InactivityMonitor: User {} is inactive for {} seconds, showing warning dialog",
                            currentUser.getName(), thresholdSeconds);
                        showWarningDialog();
                    }

                    ui.push();
                });
            } catch (Exception e) {
                logger.error("InactivityMonitor: Error during inactivity check", e);
            }
        }, checkIntervalSeconds, checkIntervalSeconds, TimeUnit.SECONDS);
    }

    private void showWarningDialog() {
        if (isDialogOpen) {
            return;
        }
        isDialogOpen = true;
        remainingSeconds = inactivityConfig.getCountdownSeconds();

        warningDialog = new Dialog();
        warningDialog.setModal(true);
        warningDialog.setCloseOnEsc(false);
        warningDialog.setCloseOnOutsideClick(false);
        warningDialog.setDraggable(false);

        VerticalLayout content = new VerticalLayout();
        content.setAlignItems(FlexComponent.Alignment.CENTER);
        content.setPadding(true);
        content.setSpacing(true);

        H2 title = new H2(translationService.translate("inactivity.warning.title"));
        title.getStyle()
            .set("color", "#d32f2f")
            .set("margin", "0");

        Paragraph message = new Paragraph(translationService.translate("inactivity.warning.message"));
        message.getStyle().set("text-align", "center");

        countdownText = new Paragraph();
        updateCountdownText();
        countdownText.getStyle()
            .set("font-size", "48px")
            .set("font-weight", "bold")
            .set("color", "#d32f2f")
            .set("margin", "20px 0");

        Button stayButton = new Button(translationService.translate("inactivity.warning.stay"), event -> {
            // User is active - update activity and close dialog
            User currentUser = VaadinSession.getCurrent().getAttribute(User.class);
            if (currentUser != null) {
                String sessionId = VaadinSession.getCurrent().getSession() != null
                    ? VaadinSession.getCurrent().getSession().getId() : null;
                userActivityService.updateActivity(currentUser, "STAY_ACTIVE", "inactivity-monitor", sessionId);
                logger.info("User {} chose to stay active", currentUser.getName());
            }
            closeWarningDialog();
        });
        stayButton.addThemeVariants(ButtonVariant.LUMO_PRIMARY, ButtonVariant.LUMO_LARGE);
        stayButton.getStyle().set("margin-top", "20px");

        content.add(title, message, countdownText, stayButton);
        warningDialog.add(content);
        warningDialog.open();

        // Start countdown
        startCountdown();
    }

    private void updateCountdownText() {
        if (countdownText != null) {
            countdownText.setText(String.valueOf(remainingSeconds));
        }
    }

    private void startCountdown() {
        if (countdownTask != null && !countdownTask.isDone()) {
            countdownTask.cancel(false);
        }

        countdownTask = executor.scheduleAtFixedRate(() -> {
            UI ui = getUI().orElse(null);
            if (ui == null) {
                return;
            }

            ui.access(() -> {
                remainingSeconds--;

                if (remainingSeconds <= 0) {
                    // Time's up - force logout
                    logger.info("Countdown reached 0 - forcing logout");
                    forceLogout();
                } else {
                    updateCountdownText();
                }
                ui.push();
            });
        }, 1, 1, TimeUnit.SECONDS);
    }

    private void closeWarningDialog() {
        if (countdownTask != null && !countdownTask.isDone()) {
            countdownTask.cancel(false);
        }
        if (warningDialog != null && warningDialog.isOpened()) {
            warningDialog.close();
        }
        isDialogOpen = false;
    }

    private void forceLogout() {
        closeWarningDialog();
        stopAllTasks();

        User currentUser = VaadinSession.getCurrent().getAttribute(User.class);
        if (currentUser != null) {
            logger.info("Force logout for user: {}", currentUser.getName());
            // Remove user activity
            userActivityService.removeUserActivity(currentUser.getId());
        }

        // Clear session and redirect to login
        VaadinSession session = VaadinSession.getCurrent();
        if (session != null) {
            session.setAttribute(User.class, null);
            session.close();
        }

        // Navigate to login page
        getUI().ifPresent(ui -> ui.getPage().setLocation("/login"));
    }

    private void stopAllTasks() {
        if (inactivityCheckTask != null && !inactivityCheckTask.isDone()) {
            inactivityCheckTask.cancel(false);
        }
        if (countdownTask != null && !countdownTask.isDone()) {
            countdownTask.cancel(false);
        }
    }
}

