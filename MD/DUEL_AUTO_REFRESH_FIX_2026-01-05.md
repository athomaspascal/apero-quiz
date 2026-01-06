# Correction du Rafraîchissement Automatique du Scoreboard en Mode Duel - 2026-01-05

## Problème Identifié

Lorsque le joueur 1 terminait son quiz en mode duel avant le joueur 2 :
- Le joueur 1 voyait un message d'attente "En attente de l'adversaire..."
- Le joueur 2, en terminant, voyait correctement l'écran final avec "Duel terminé !" et les scores
- **Le joueur 1 ne voyait JAMAIS automatiquement l'écran final** même quand le joueur 2 avait terminé

Le joueur 1 devait manuellement cliquer sur "Voir les résultats" pour naviguer vers DuelQuizView et voir le scoreboard.

## Cause du Problème

Dans `QuizQuestionView.java`, lorsque le premier joueur terminait et que l'autre joueur n'avait pas encore terminé, l'application affichait un message d'attente mais **ne mettait pas en place de mécanisme de polling** pour détecter automatiquement quand le second joueur terminait.

La vérification des scores se faisait uniquement une fois, au moment où le joueur terminait son quiz.

## Solution Implémentée

### 1. Ajout d'un système de polling dans QuizQuestionView

**Fichier modifié** : `src/main/java/com/quizz/core/ui/QuizQuestionView.java`

#### a) Ajout d'une variable pour la tâche de polling
```java
// Duel polling task
private ScheduledFuture<?> duelPollingTask;
```

#### b) Démarrage du polling quand un joueur attend l'autre
Dans la méthode `showFinalScore()`, après avoir soumis le score du duel :
```java
} else {
    // Waiting for other player
    questionText.setText(translationService.translate("duelquiz.waiting.opponent"));

    // Show button to return to duel view
    nextButton.setText(translationService.translate("duelquiz.viewresults"));
    nextButton.setVisible(true);
    nextButton.setEnabled(true);

    if (nextClickReg != null) nextClickReg.remove();
    nextClickReg = nextButton.addClickListener(event -> {
        stopDuelPolling(); // Stop polling before navigating
        getUI().ifPresent(ui -> ui.navigate("duel-quiz"));
    });

    // Start polling to check when the other player finishes
    startDuelPolling(duelId);
}
```

#### c) Méthode de polling
```java
/**
 * Start polling to check if the other player has finished the duel
 */
private void startDuelPolling(Long duelIdToCheck) {
    if (duelPollingTask != null && !duelPollingTask.isDone()) {
        logger.info("Duel polling already running for duel {}", duelIdToCheck);
        return;
    }

    logger.info("Starting duel polling for duel {}", duelIdToCheck);
    
    duelPollingTask = scheduler.scheduleAtFixedRate(() -> {
        try {
            var duelOpt = duelService.getDuelById(duelIdToCheck);
            if (duelOpt.isPresent()) {
                var duel = duelOpt.get();
                
                // Check if both players have finished
                if (duel.getPlayer1Score() != null && duel.getPlayer2Score() != null) {
                    logger.info("Both players finished! Player1: {}, Player2: {}", 
                        duel.getPlayer1Score(), duel.getPlayer2Score());
                    
                    // Stop polling
                    stopDuelPolling();
                    
                    // Update UI on the UI thread
                    UI ui = getUI().orElse(null);
                    if (ui != null) {
                        ui.access(() -> {
                            User currentUser = VaadinSession.getCurrent().getAttribute(User.class);
                            showDuelScoreboard(duel, currentUser);
                            ui.push();
                        });
                    }
                }
            }
        } catch (Exception e) {
            logger.error("Error during duel polling", e);
        }
    }, 2, 2, TimeUnit.SECONDS); // Poll every 2 seconds
}
```

#### d) Méthode d'arrêt du polling
```java
/**
 * Stop duel polling
 */
private void stopDuelPolling() {
    if (duelPollingTask != null && !duelPollingTask.isDone()) {
        logger.info("Stopping duel polling");
        duelPollingTask.cancel(false);
        duelPollingTask = null;
    }
}
```

#### e) Nettoyage lors du détachement de la vue
```java
addDetachListener((DetachEvent detachEvent) -> {
    startNewRun();
    cancelPendingDelay();
    stopTimer();
    stopDuelPolling(); // Stop duel polling if active
});
```

## Résultat

Maintenant, lorsque le joueur 1 termine son quiz en premier :
1. Il voit le message "En attente de l'adversaire..."
2. Un système de polling vérifie toutes les 2 secondes si le joueur 2 a terminé
3. Dès que le joueur 2 termine, **l'écran du joueur 1 se met automatiquement à jour**
4. Les deux joueurs voient simultanément l'écran "Duel terminé !" avec les scores

## Avantages

- ✅ Expérience utilisateur améliorée : pas besoin de cliquer manuellement pour voir les résultats
- ✅ Synchronisation automatique entre les deux joueurs
- ✅ Utilisation du scheduler existant (pas de nouveau thread)
- ✅ Nettoyage approprié lors du détachement de la vue
- ✅ Gestion des erreurs et logs pour le débogage

## Tests à Effectuer

1. Démarrer un duel entre deux joueurs
2. Le joueur 1 termine son quiz en premier
3. Vérifier que le joueur 1 voit le message d'attente
4. Le joueur 2 termine son quiz
5. **Vérifier que le joueur 1 voit automatiquement l'écran final avec les scores sans intervention manuelle**
6. Les deux joueurs doivent voir les mêmes informations (scores, gagnant, options de rematch)

## Fichiers Modifiés

- `src/main/java/com/quizz/core/ui/QuizQuestionView.java`

## Date de Correction

5 janvier 2026

