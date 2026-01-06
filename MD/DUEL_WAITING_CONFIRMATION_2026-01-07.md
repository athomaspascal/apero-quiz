# Système de Confirmation d'Attente pour les Duels - 2026-01-07

## Résumé

Implémentation d'un système de confirmation automatique toutes les 60 secondes pour les joueurs en attente d'un adversaire dans les duels, avec tracking complet de toutes les interactions.

## Problème résolu

Lorsqu'un joueur lance une recherche d'adversaire et attend longtemps sans résultat :
- Le joueur peut oublier qu'il est en recherche
- Le système ne sait pas si le joueur souhaite toujours attendre
- Pas de feedback sur la durée d'attente

## Solution implémentée

### 1. Timer de confirmation automatique (60 secondes)

**Fichier**: `DuelQuizView.java`

#### Nouvelles variables ajoutées

```java
private ScheduledFuture<?> waitingConfirmationTask;
private LocalDateTime lastConfirmationTime;
```

- `waitingConfirmationTask` : Tâche planifiée qui vérifie toutes les 10 secondes si 60 secondes se sont écoulées
- `lastConfirmationTime` : Timestamp de la dernière confirmation du joueur

#### Initialisation du timer

Lors du lancement de la recherche :

```java
private void startSearching() {
    // ...existing code...
    lastConfirmationTime = LocalDateTime.now();
    startWaitingConfirmationTimer();
    updateView();
}
```

### 2. Méthode de gestion du timer

```java
private void startWaitingConfirmationTimer() {
    if (waitingConfirmationTask != null && !waitingConfirmationTask.isDone()) {
        return; // Timer déjà en cours
    }

    waitingConfirmationTask = executor.scheduleAtFixedRate(() -> {
        if (currentDuel != null && currentDuel.getStatus() == DuelMatch.DuelStatus.SEARCHING) {
            long secondsWaiting = Duration.between(lastConfirmationTime, LocalDateTime.now()).getSeconds();
            
            if (secondsWaiting >= 60) {
                // Demander confirmation après 60 secondes
                UI ui = getUI().orElse(null);
                if (ui != null) {
                    ui.access(() -> {
                        showWaitingConfirmationDialog();
                        ui.push();
                    });
                }
            }
        }
    }, 10, 10, TimeUnit.SECONDS); // Vérification toutes les 10 secondes
}
```

**Paramètres** :
- Délai initial : 10 secondes
- Intervalle : toutes les 10 secondes
- Seuil d'attente : 60 secondes
- Action : Affichage de la boîte de dialogue de confirmation

### 3. Boîte de dialogue de confirmation

```java
private void showWaitingConfirmationDialog() {
    User currentUser = VaadinSession.getCurrent().getAttribute(User.class);
    
    ConfirmDialog dialog = new ConfirmDialog();
    dialog.setHeader(translationService.translate("duelquiz.waiting.confirmation.title"));
    dialog.setText(translationService.translate("duelquiz.waiting.confirmation.text"));
    
    dialog.setCancelable(false);
    dialog.setConfirmText(translationService.translate("duelquiz.waiting.confirmation.continue"));
    dialog.setCancelText(translationService.translate("duelquiz.waiting.confirmation.cancel"));
    
    dialog.addConfirmListener(event -> {
        // Track : l'utilisateur choisit de continuer à attendre
        userActivityService.updateActivity(currentUser, "CONTINUE_WAITING", "duel-quiz");
        
        // Réinitialiser le timer
        lastConfirmationTime = LocalDateTime.now();
        logger.info("User {} chose to continue waiting for opponent", 
            currentUser != null ? currentUser.getName() : "unknown");
    });
    
    dialog.addCancelListener(event -> {
        // Track : l'utilisateur annule la recherche
        userActivityService.updateActivity(currentUser, "CANCEL_WAITING", "duel-quiz");
        
        // Annuler le duel et retourner à la vue initiale
        stopWaitingConfirmationTimer();
        if (currentDuel != null) {
            duelService.cancelDuel(currentDuel.getId());
        }
        currentDuel = null;
        showInitialView();
        logger.info("User {} cancelled waiting for opponent", 
            currentUser != null ? currentUser.getName() : "unknown");
    });
    
    dialog.open();
}
```

**Caractéristiques** :
- Non annulable par clic en dehors (setCancelable(false))
- Deux boutons : "Continuer à Attendre" et "Annuler la Recherche"
- Tracking complet des deux actions
- Réinitialisation du timer si l'utilisateur choisit de continuer

### 4. Arrêt du timer

Le timer est automatiquement arrêté dans plusieurs situations :

#### Quand un adversaire est trouvé (MATCHED)
```java
case MATCHED:
    stopWaitingConfirmationTimer(); // Arrêt du timer
    showMatchedView();
    break;
```

#### Quand le compte à rebours commence (COUNTDOWN)
```java
case COUNTDOWN:
    stopWaitingConfirmationTimer(); // Arrêt du timer
    showCountdownView();
    break;
```

#### Quand le joueur annule la recherche
```java
Button cancelButton = new Button(translationService.translate("duelquiz.cancel"), event -> {
    // ...track activity...
    stopWaitingConfirmationTimer(); // Arrêt du timer
    duelService.cancelDuel(currentDuel.getId());
    // ...
});
```

#### Lors du détachement de la vue
```java
@Override
protected void onDetach(DetachEvent detachEvent) {
    super.onDetach(detachEvent);
    stopPolling();
    stopWaitingConfirmationTimer(); // Nettoyage
    // ...
}
```

### 5. Tracking des activités

Tous les clics de boutons sont trackés dans la table `user_activity` :

| Action | Type d'activité | Description |
|--------|----------------|-------------|
| Continuer à attendre | `CONTINUE_WAITING` | Le joueur confirme qu'il veut continuer |
| Annuler l'attente | `CANCEL_WAITING` | Le joueur annule via la boîte de dialogue |
| Annuler la recherche | `CANCEL_DUEL_SEARCH` | Le joueur annule via le bouton |
| Accepter le duel | `ACCEPT_DUEL` | Le joueur accepte un adversaire |
| Décliner le duel | `DECLINE_DUEL` | Le joueur refuse un adversaire |
| Demander revanche | `REQUEST_REMATCH` | Le joueur demande une revanche |
| Quitter le duel | `EXIT_DUEL` | Le joueur quitte le duel |
| Polling actif | `DUEL_POLLING` | Activité automatique (toutes les 2 secondes) |

### 6. Traductions

#### Français (messages_fr.properties)
```properties
duelquiz.waiting.confirmation.title=Toujours en attente ?
duelquiz.waiting.confirmation.text=Vous attendez un adversaire depuis plus d'une minute. Voulez-vous continuer à attendre ?
duelquiz.waiting.confirmation.continue=Continuer à Attendre
duelquiz.waiting.confirmation.cancel=Annuler la Recherche
```

#### Anglais (messages_en.properties)
```properties
duelquiz.waiting.confirmation.title=Still Waiting?
duelquiz.waiting.confirmation.text=You've been waiting for an opponent for over a minute. Do you want to keep waiting?
duelquiz.waiting.confirmation.continue=Keep Waiting
duelquiz.waiting.confirmation.cancel=Cancel Search
```

#### Italien (messages_it.properties)
```properties
duelquiz.waiting.confirmation.title=Stai ancora aspettando?
duelquiz.waiting.confirmation.text=Stai aspettando un avversario da più di un minuto. Vuoi continuare ad aspettare?
duelquiz.waiting.confirmation.continue=Continua ad Aspettare
duelquiz.waiting.confirmation.cancel=Annulla Ricerca
```

## Flux d'utilisation

### Scénario 1 : Joueur continue à attendre

1. Le joueur lance une recherche d'adversaire
2. Timer démarre (lastConfirmationTime = now)
3. Après 60 secondes sans adversaire → Boîte de dialogue s'affiche
4. Le joueur clique sur "Continuer à Attendre"
5. Activity trackée : `CONTINUE_WAITING`
6. Timer réinitialisé (lastConfirmationTime = now)
7. Après 60 secondes de plus → Boîte de dialogue s'affiche à nouveau
8. Le cycle peut se répéter indéfiniment

### Scénario 2 : Joueur annule via la boîte de dialogue

1. Le joueur lance une recherche d'adversaire
2. Timer démarre
3. Après 60 secondes → Boîte de dialogue s'affiche
4. Le joueur clique sur "Annuler la Recherche"
5. Activity trackée : `CANCEL_WAITING`
6. Timer arrêté
7. Duel annulé dans le service
8. Retour à la vue initiale

### Scénario 3 : Adversaire trouvé avant 60 secondes

1. Le joueur lance une recherche d'adversaire
2. Timer démarre
3. Après 30 secondes → Un adversaire est trouvé
4. Statut change à MATCHED
5. Timer arrêté automatiquement
6. Vue "Adversaire Trouvé" s'affiche
7. Aucune boîte de dialogue ne s'affiche

### Scénario 4 : Joueur annule manuellement

1. Le joueur lance une recherche d'adversaire
2. Timer démarre
3. Après 20 secondes → Le joueur clique sur "Annuler la Recherche"
4. Activity trackée : `CANCEL_DUEL_SEARCH`
5. Timer arrêté
6. Duel annulé
7. Retour à la vue initiale

## Avantages

✅ **Feedback régulier** : Le joueur est consulté toutes les 60 secondes  
✅ **Évite les attentes inutiles** : Le joueur peut décider d'arrêter  
✅ **Tracking complet** : Toutes les actions sont enregistrées  
✅ **Non intrusif** : Le timer ne s'affiche que si aucun adversaire n'est trouvé  
✅ **Multilingue** : Traductions en français, anglais et italien  
✅ **Automatique** : Aucune intervention manuelle nécessaire  
✅ **Nettoyage automatique** : Le timer s'arrête dès qu'il n'est plus nécessaire  

## Configuration

Pour modifier les paramètres :

### Délai de confirmation (actuellement 60 secondes)
```java
// Dans showWaitingConfirmationDialog()
if (secondsWaiting >= 60) { // Modifier cette valeur
    // Afficher la boîte de dialogue
}
```

### Fréquence de vérification (actuellement 10 secondes)
```java
// Dans startWaitingConfirmationTimer()
waitingConfirmationTask = executor.scheduleAtFixedRate(..., 10, 10, TimeUnit.SECONDS);
// Modifier les deux valeurs 10
```

## Tests recommandés

1. **Test de confirmation après 60 secondes** :
   - Lancer une recherche d'adversaire
   - Attendre 65 secondes sans adversaire
   - Vérifier que la boîte de dialogue s'affiche
   - Cliquer sur "Continuer à Attendre"
   - Vérifier que le timer redémarre

2. **Test d'annulation via la boîte de dialogue** :
   - Lancer une recherche d'adversaire
   - Attendre 65 secondes
   - Cliquer sur "Annuler la Recherche"
   - Vérifier le retour à la vue initiale
   - Vérifier le tracking dans les logs

3. **Test avec adversaire trouvé rapidement** :
   - Deux joueurs lancent une recherche
   - Vérifier qu'ils se trouvent rapidement
   - Vérifier qu'aucune boîte de dialogue ne s'affiche
   - Vérifier que le timer s'est arrêté

4. **Test d'annulation manuelle** :
   - Lancer une recherche d'adversaire
   - Attendre 30 secondes
   - Cliquer sur "Annuler la Recherche"
   - Vérifier que la boîte de dialogue ne s'affiche pas après

5. **Test de tracking** :
   - Lancer une recherche
   - Attendre 65 secondes et continuer
   - Vérifier les logs : `CONTINUE_WAITING`
   - Annuler ensuite
   - Vérifier les logs : `CANCEL_WAITING`

## Logs à surveiller

```
User Barack Obama chose to continue waiting for opponent
User Marie Curie cancelled waiting for opponent
Updated activity for user Isaac Newton - Type: CONTINUE_WAITING, Page: duel-quiz
Updated activity for user Coco Chanel - Type: CANCEL_WAITING, Page: duel-quiz
```

## Fichiers modifiés

1. **DuelQuizView.java**
   - Ajout de `waitingConfirmationTask` et `lastConfirmationTime`
   - Ajout de l'import `ConfirmDialog`
   - Méthode `startWaitingConfirmationTimer()`
   - Méthode `stopWaitingConfirmationTimer()`
   - Méthode `showWaitingConfirmationDialog()`
   - Modification de `startSearching()` pour initialiser le timer
   - Modification de `updateView()` pour arrêter le timer si MATCHED ou COUNTDOWN
   - Modification de `onDetach()` pour arrêter le timer
   - Modification du bouton Cancel pour arrêter le timer

2. **messages_fr.properties**
   - `duelquiz.waiting.confirmation.title`
   - `duelquiz.waiting.confirmation.text`
   - `duelquiz.waiting.confirmation.continue`
   - `duelquiz.waiting.confirmation.cancel`

3. **messages_en.properties**
   - `duelquiz.waiting.confirmation.title`
   - `duelquiz.waiting.confirmation.text`
   - `duelquiz.waiting.confirmation.continue`
   - `duelquiz.waiting.confirmation.cancel`

4. **messages_it.properties**
   - `duelquiz.waiting.confirmation.title`
   - `duelquiz.waiting.confirmation.text`
   - `duelquiz.waiting.confirmation.continue`
   - `duelquiz.waiting.confirmation.cancel`

## Intégration avec le système existant

Cette fonctionnalité s'intègre parfaitement avec :

- **InactivityMonitorService** : Les utilisateurs qui ne cliquent sur aucun bouton sont marqués comme inactifs et leurs duels sont annulés
- **DuelService** : Le nettoyage au démarrage annule tous les duels orphelins
- **UserActivityService** : Toutes les actions sont trackées dans la base de données
- **Système de polling** : Le polling toutes les 2 secondes maintient l'utilisateur actif

---

**Date**: 2026-01-07  
**Status**: ✅ Implémenté et prêt pour les tests

