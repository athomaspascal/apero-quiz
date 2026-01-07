# Ajout du Tracking d'Activité pour tous les Boutons de Duel - 2026-01-07

## 🎯 Objectif

Tracker TOUTES les activités utilisateur dans les vues de duel pour :
1. Détecter les utilisateurs inactifs (> 60 secondes)
2. Nettoyer automatiquement les duels abandonnés
3. Avoir des statistiques complètes dans le Dashboard

## ✅ Boutons avec tracking ajouté

### DuelQuizView.java

| Bouton | Action | Type d'activité | Emplacement |
|--------|--------|----------------|-------------|
| **Chercher un Adversaire** | `startSearching()` | `START_DUEL_SEARCH` | Vue initiale ✅ (déjà présent) |
| **Retour** (vue initiale) | Navigate home | `BACK_FROM_DUEL` | Vue initiale ✅ **AJOUTÉ** |
| **Annuler** (recherche) | Cancel search | `CANCEL_DUEL_SEARCH` | Vue recherche ✅ (déjà présent) |
| **Accepter** | Accept match | `ACCEPT_DUEL` | Vue matched ✅ (déjà présent) |
| **Refuser** | Decline match | `DECLINE_DUEL` | Vue matched ✅ (déjà présent) |
| **Rematch** | Request rematch | `REQUEST_REMATCH` | Vue rematch ✅ (déjà présent) |
| **Quitter** | Exit duel | `EXIT_DUEL` | Vue rematch ✅ (déjà présent) |
| **Retour** (cancelled) | Back to initial | `BACK_FROM_CANCELLED_DUEL` | Vue cancelled ✅ **AJOUTÉ** |
| **Fermer** (dialog) | Close cancel dialog | `CLOSE_DUEL_CANCEL_DIALOG` | Dialog annulation ✅ **AJOUTÉ** |

### QuizQuestionView.java

| Bouton | Action | Type d'activité | Emplacement |
|--------|--------|----------------|-------------|
| **Arrêter** (pendant quiz) | Stop duel quiz | `STOP_DUEL_QUIZ` | Pendant le quiz ✅ **AJOUTÉ** |
| **Rematch** (scoreboard) | Request rematch | `REQUEST_REMATCH_FROM_QUIZ` | Scoreboard duel ✅ **AJOUTÉ** |
| **Arrêter** (scoreboard) | Stop duel | `STOP_DUEL_FROM_SCOREBOARD` | Scoreboard duel ✅ **AJOUTÉ** |

### Polling automatique

| Activité | Type | Fréquence |
|----------|------|-----------|
| **Polling duel** | `DUEL_POLLING` | Toutes les 2 secondes ✅ (déjà présent) |

## 📝 Code ajouté

### 1. Bouton "Retour" de la vue initiale

```java
Button cancelButton = new Button(translationService.translate("duelquiz.back"), event -> {
    User currentUser = VaadinSession.getCurrent().getAttribute(User.class);
    if (currentUser != null) {
        userActivityService.updateActivity(currentUser, "BACK_FROM_DUEL", "duel-quiz");
    }
    getUI().ifPresent(ui -> ui.navigate(""));
});
```

### 2. Bouton "Retour" de la vue cancelled

```java
Button backButton = new Button(translationService.translate("duelquiz.back"), event -> {
    User currentUser = VaadinSession.getCurrent().getAttribute(User.class);
    if (currentUser != null) {
        userActivityService.updateActivity(currentUser, "BACK_FROM_CANCELLED_DUEL", "duel-quiz");
    }
    currentDuel = null;
    showInitialView();
});
```

### 3. Bouton "Fermer" du Dialog d'annulation

```java
Button closeButton = new Button(
    translationService.translate("button.close"),
    event -> {
        // Track user activity
        if (currentUser != null) {
            userActivityService.updateActivity(currentUser, "CLOSE_DUEL_CANCEL_DIALOG", "duel-quiz");
        }
        dialog.close();
        currentDuel = null;
        showInitialView();
    });
```

### 4. Bouton "Arrêter" pendant le quiz (duel)

```java
// If this is a duel, cancel it
if (duelId != null) {
    User currentUser = VaadinSession.getCurrent().getAttribute(User.class);
    if (currentUser != null && duelService != null) {
        try {
            // Track user activity - stopping duel
            userActivityService.updateActivity(currentUser, "STOP_DUEL_QUIZ", "quiz-questions/" + quizId);
            
            duelService.cancelDuel(duelId, currentUser);
            // ...
        }
    }
}
```

### 5. Bouton "Rematch" depuis le scoreboard

```java
Button rematchButton = new Button(translationService.translate("duelquiz.rematch.start"), event -> {
    stopDuelPolling();
    try {
        // Track user activity
        if (currentUser != null) {
            userActivityService.updateActivity(currentUser, "REQUEST_REMATCH_FROM_QUIZ", "quiz-questions/" + quizId);
        }
        
        duelService.requestRematch(duel.getId(), currentUser);
        // ...
    }
});
```

### 6. Bouton "Arrêter" depuis le scoreboard

```java
Button stopDuelButton = new Button(translationService.translate("duelquiz.stop"), event -> {
    stopDuelPolling();
    try {
        // Track user activity
        if (currentUser != null) {
            userActivityService.updateActivity(currentUser, "STOP_DUEL_FROM_SCOREBOARD", "quiz-questions/" + quizId);
        }
        
        duelService.cancelDuel(duel.getId());
        // ...
    }
});
```

## 📊 Types d'activité tracking

### Activités déjà présentes (avant correction)

1. ✅ `START_DUEL_SEARCH` - Lancer une recherche de duel
2. ✅ `CANCEL_DUEL_SEARCH` - Annuler la recherche
3. ✅ `ACCEPT_DUEL` - Accepter un match
4. ✅ `DECLINE_DUEL` - Refuser un match
5. ✅ `REQUEST_REMATCH` - Demander une revanche
6. ✅ `EXIT_DUEL` - Quitter un duel
7. ✅ `DUEL_POLLING` - Polling automatique (toutes les 2s)

### Activités ajoutées (nouvelles)

8. ✅ `BACK_FROM_DUEL` - Retour depuis la vue initiale
9. ✅ `BACK_FROM_CANCELLED_DUEL` - Retour depuis la vue cancelled
10. ✅ `CLOSE_DUEL_CANCEL_DIALOG` - Fermer le dialog d'annulation
11. ✅ `STOP_DUEL_QUIZ` - Arrêter le quiz pendant un duel
12. ✅ `REQUEST_REMATCH_FROM_QUIZ` - Demander revanche depuis le scoreboard
13. ✅ `STOP_DUEL_FROM_SCOREBOARD` - Arrêter depuis le scoreboard

## 🔄 Flux complet avec tracking

### Scénario : Duel complet avec toutes les activités

```
1. Isaac : Clique "Chercher un Adversaire"
   → START_DUEL_SEARCH tracké ✅

2. Marie : Clique "Chercher un Adversaire"
   → START_DUEL_SEARCH tracké ✅
   → Match trouvé !

3. Isaac : Clique "Accepter"
   → ACCEPT_DUEL tracké ✅

4. Marie : Clique "Accepter"
   → ACCEPT_DUEL tracké ✅
   → Countdown commence

5. Pendant l'attente (countdown/quiz) :
   → DUEL_POLLING tracké toutes les 2s ✅

6. Isaac : Clique "Arrêter" pendant le quiz
   → STOP_DUEL_QUIZ tracké ✅
   → Duel annulé

7. Marie : Voit le dialog d'annulation
   → Clique "Fermer"
   → CLOSE_DUEL_CANCEL_DIALOG tracké ✅
```

## 🎯 Utilisation du tracking

### Détection d'inactivité

Le service de nettoyage (`DuelService.cancelDuelsForInactiveUsers()`) utilise ces activités pour :
1. Calculer le temps depuis la dernière activité
2. Identifier les utilisateurs inactifs (> 60 secondes)
3. Annuler automatiquement leurs duels

### Dashboard

Le Dashboard peut afficher :
- Nombre de recherches lancées
- Taux d'acceptation/refus
- Taux d'abandon (STOP_DUEL_QUIZ)
- Popularité des rematch

## 🧪 Test du tracking

### Vérifier dans les logs

Après avoir fait un duel complet, cherchez dans les logs :

```bash
grep "Updated activity for user" logs/application.log | grep -E "DUEL|START_DUEL|STOP_DUEL|REMATCH|BACK_FROM"
```

Vous devriez voir toutes les activités trackées :

```
Updated activity for user Isaac Newton - Type: START_DUEL_SEARCH
Updated activity for user Marie Curie - Type: START_DUEL_SEARCH
Updated activity for user Isaac Newton - Type: DUEL_POLLING
Updated activity for user Marie Curie - Type: DUEL_POLLING
Updated activity for user Isaac Newton - Type: ACCEPT_DUEL
Updated activity for user Marie Curie - Type: ACCEPT_DUEL
Updated activity for user Isaac Newton - Type: STOP_DUEL_QUIZ
Updated activity for user Marie Curie - Type: CLOSE_DUEL_CANCEL_DIALOG
```

## 📋 Checklist des boutons

| Vue | Bouton | Tracking | Status |
|-----|--------|----------|--------|
| **DuelQuizView** | | | |
| Initial | Chercher un Adversaire | START_DUEL_SEARCH | ✅ |
| Initial | Retour | BACK_FROM_DUEL | ✅ |
| Searching | Annuler | CANCEL_DUEL_SEARCH | ✅ |
| Matched | Accepter | ACCEPT_DUEL | ✅ |
| Matched | Refuser | DECLINE_DUEL | ✅ |
| Rematch | Rematch | REQUEST_REMATCH | ✅ |
| Rematch | Quitter | EXIT_DUEL | ✅ |
| Cancelled | Retour | BACK_FROM_CANCELLED_DUEL | ✅ |
| Dialog | Fermer | CLOSE_DUEL_CANCEL_DIALOG | ✅ |
| **QuizQuestionView** | | | |
| Quiz | Arrêter (duel) | STOP_DUEL_QUIZ | ✅ |
| Scoreboard | Rematch | REQUEST_REMATCH_FROM_QUIZ | ✅ |
| Scoreboard | Arrêter | STOP_DUEL_FROM_SCOREBOARD | ✅ |
| **Automatique** | | | |
| Polling | Toutes les 2s | DUEL_POLLING | ✅ |

## 🎉 Résultat

✅ **TOUS les boutons** des vues de duel ont maintenant un tracking d'activité  
✅ **TOUTES les actions** utilisateur sont enregistrées  
✅ **Le système de nettoyage** peut détecter les utilisateurs inactifs  
✅ **Le Dashboard** peut avoir des statistiques complètes  

---

**Date** : 2026-01-07  
**Status** : ✅ **COMPLET ET COMPILÉ**  
**Tracking ajouté** : 6 nouveaux types d'activité  
**Total des activités trackées** : 13 types + polling

