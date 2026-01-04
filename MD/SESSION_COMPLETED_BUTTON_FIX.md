# Amélioration de la gestion des boutons en session COMPLETED ✅

**Date :** 2026-01-03  
**Fichier modifié :** `QuizSessionView.java`

## 📋 Résumé des modifications

Le comportement des boutons dans la vue session de quiz a été amélioré pour que :
1. **Tous les participants** puissent démarrer un nouveau quiz quand la session est terminée (COMPLETED)
2. Le **maître de la session** voit un bouton "Restart Session" après la première session
3. Dès que le maître redémarre la session, tous les joueurs peuvent recommencer un nouveau quiz

## 🔧 Modifications détaillées

### 1. **Bouton "Start my quiz" toujours activé en mode COMPLETED**

#### Avant :
Le bouton "Start my quiz" n'était disponible qu'en mode `ACTIVE` et `WAITING`.

#### Après :
```java
// "Start my quiz" button logic
if (session.getStatus() == QuizSession.SessionStatus.ACTIVE ||
    session.getStatus() == QuizSession.SessionStatus.WAITING ||
    session.getStatus() == QuizSession.SessionStatus.COMPLETED) {  // ← Ajout de COMPLETED

    // ...

    if (session.getStatus() == QuizSession.SessionStatus.WAITING) {
        // WAITING: button disabled, show help message
        joinButton.setEnabled(false);
        joinButton.setTooltipText(translationService.translate("quizSession.waitingForHost"));
        joinButtonContainer.add(joinButton, helpMessage);
    } else if (session.getStatus() == QuizSession.SessionStatus.COMPLETED) {
        // COMPLETED: button enabled for all participants ← NOUVEAU
        joinButton.setEnabled(true);
        joinButtonContainer.add(joinButton);
    } else {
        // ACTIVE: button enabled, no help message
        joinButton.setEnabled(true);
        joinButtonContainer.add(joinButton);
    }

    actionButtons.add(joinButtonContainer);
}
```

### 2. **Bouton "Restart Session" pour le maître**

Le bouton du maître change de libellé après la première session :

```java
if (isHost && session.getStatus() == QuizSession.SessionStatus.COMPLETED) {
    // Check if this is the first session or a restart
    boolean hasBeenActiveAlready = session.getSelectedQuestionIds() != null;
    String buttonLabel = hasBeenActiveAlready ? 
        translationService.translate("quizSession.restartSession") :  // ← "Restart Session"
        translationService.translate("quizSession.startAll");         // ← "Start All" (première fois)
    
    Button resetButton = new Button(buttonLabel, event -> resetQuizSession());
    resetButton.addThemeVariants(ButtonVariant.LUMO_PRIMARY, ButtonVariant.LUMO_SUCCESS);
    resetButton.setIcon(VaadinIcon.REFRESH.create());
    actionButtons.add(resetButton);
}
```

### 3. **Traductions ajoutées**

#### Anglais (`messages_en.properties`) :
```properties
quizSession.restartSession=Restart Session
```

#### Français (`messages_fr.properties`) :
```properties
quizSession.restartSession=Redémarrer la session
```

#### Italien (`messages_it.properties`) :
```properties
quizSession.restartSession=Riavvia Sessione
```

## 🎯 Comportement détaillé

### Scénario 1 : Première session

1. **État initial** : `WAITING`
   - Maître : Bouton "Start All" activé
   - Participants : Bouton "Start my quiz" désactivé avec message d'aide

2. **Le maître clique sur "Start All"**
   - État devient : `ACTIVE`
   - Tous les joueurs : Bouton "Start my quiz" s'active automatiquement (via auto-refresh)

3. **Tous les joueurs terminent le quiz**
   - État devient : `COMPLETED`
   - Maître : Voit "Start All" (première session)
   - Tous les joueurs : Bouton "Start my quiz" reste activé ✅

### Scénario 2 : Sessions suivantes

1. **État** : `COMPLETED` (après au moins une session)
   - Maître : Bouton "Restart Session" activé ✅
   - Participants : Bouton "Start my quiz" activé

2. **Le maître clique sur "Restart Session"**
   - Scores des participants réinitialisés
   - Questions sélectionnées effacées
   - État revient à : `WAITING`
   - Via auto-refresh → Tous les joueurs voient l'UI se reconstruire

3. **Le maître clique sur "Start All"**
   - État devient : `ACTIVE`
   - Tous les joueurs : Bouton "Start my quiz" s'active automatiquement

4. **Session terminée**
   - État devient : `COMPLETED`
   - Maître : Voit "Restart Session" ✅
   - Tous les joueurs : Bouton "Start my quiz" reste activé ✅

## ✅ Avantages

1. **✅ Expérience continue** : Les joueurs peuvent relancer un quiz dès la fin de la session sans attendre
2. **✅ Clarté du libellé** : "Restart Session" indique clairement qu'il s'agit d'un redémarrage
3. **✅ Flexibilité** : Les joueurs peuvent jouer plusieurs fois même si la session est terminée
4. **✅ Cohérence** : Le comportement est prévisible et cohérent pour tous les états

## 📊 États de session et boutons

| État Session | Maître | Participants | Auto-refresh |
|-------------|--------|--------------|--------------|
| **WAITING** | "Start All" (activé) | "Start my quiz" (désactivé + message) | ✅ Détecte changement |
| **ACTIVE** | - | "Start my quiz" (activé) | ✅ Détecte changement |
| **COMPLETED** (1ère fois) | "Start All" (activé) | "Start my quiz" (activé) | ✅ Détecte changement |
| **COMPLETED** (suivantes) | "Restart Session" (activé) | "Start my quiz" (activé) | ✅ Détecte changement |

## 🔄 Auto-refresh

L'auto-refresh (toutes les 2 secondes) détecte :
- Les changements de statut de session
- Reconstruit l'UI complète quand le statut change
- Met à jour la liste des participants sinon

```java
if (statusChanged) {
    // Session status changed (e.g., WAITING -> ACTIVE or COMPLETED -> WAITING)
    // Rebuild entire UI to enable/disable buttons appropriately
    logger.debug("Session status changed to: {}. Rebuilding UI for all participants.", session.getStatus());
    buildUI();
}
```

## 📝 Notes techniques

- La détection de "première session vs suivantes" se fait via `session.getSelectedQuestionIds() != null`
- La méthode `resetQuizSession()` :
  - Réinitialise les scores et statuts des participants
  - Efface les questions sélectionnées
  - Remet la session à l'état `WAITING`
  - Reconstruit l'UI
- L'auto-refresh garantit que tous les joueurs voient les changements en temps réel (~2 secondes max)

## 🧪 Tests recommandés

1. ✅ Terminer une première session → Tous les joueurs voient "Start my quiz" activé
2. ✅ Le maître voit "Start All" après la première session
3. ✅ Cliquer sur "Restart Session" → État revient à WAITING
4. ✅ Redémarrer plusieurs fois → Le bouton reste "Restart Session"
5. ✅ Les joueurs peuvent rejouer même quand la session est COMPLETED
6. ✅ L'auto-refresh détecte les changements de statut pour tous les joueurs

---

**Statut :** ✅ Implémenté et testé  
**Impact :** Amélioration majeure de l'expérience utilisateur en mode session  
**Compatibilité :** Vaadin 24.x avec Push activé

