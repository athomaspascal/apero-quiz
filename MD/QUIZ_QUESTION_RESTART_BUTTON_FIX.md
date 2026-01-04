# Correction du libellé du bouton "Restart Session" dans QuizQuestionView ✅

**Date :** 2026-01-03  
**Fichier modifié :** `QuizQuestionView.java`

## 📋 Problème identifié

Quand le maître de session termine son quiz et voit le scoreboard, le bouton affiché était "Start New Round" au lieu de "Restart Session" comme défini dans les règles.

### Contexte

Le maître termine son quiz dans `QuizQuestionView.java`, qui affiche le score final avec deux boutons :
1. **"View Leaderboard"** - Pour retourner à la vue session
2. **Bouton de redémarrage** - Pour réinitialiser et redémarrer la session

## 🔧 Solution appliquée

### Modification dans `showFinalScore()`

Le libellé du bouton a été corrigé pour correspondre aux règles définies :

#### Avant :
```java
// Bouton "Start New Round" for host - resets the entire session
if (isHost) {
    stopButton.setText(translationService.translate("quiz.startNewRound"));
    stopButton.setVisible(true);
    stopButton.setEnabled(true);
    stopButton.removeThemeVariants(ButtonVariant.LUMO_ERROR);
    stopButton.addThemeVariants(ButtonVariant.LUMO_PRIMARY);
    stopButton.setIcon(VaadinIcon.REFRESH.create());

    if (stopClickReg != null) stopClickReg.remove();
    stopClickReg = stopButton.addClickListener(event -> startNewRoundForSession(session, sessionCode));
}
```

#### Après :
```java
// Bouton "Restart Session" for host - resets the entire session
if (isHost) {
    // Check if this is the first session or a restart
    boolean hasBeenActiveAlready = session.getSelectedQuestionIds() != null;
    String buttonLabel = hasBeenActiveAlready ? 
        translationService.translate("quizSession.restartSession") :  // "Restart Session"
        translationService.translate("quizSession.startAll");         // "Start All" (première fois)
    
    stopButton.setText(buttonLabel);
    stopButton.setVisible(true);
    stopButton.setEnabled(true);
    stopButton.removeThemeVariants(ButtonVariant.LUMO_ERROR);
    stopButton.addThemeVariants(ButtonVariant.LUMO_PRIMARY);
    stopButton.setIcon(VaadinIcon.REFRESH.create());

    if (stopClickReg != null) stopClickReg.remove();
    stopClickReg = stopButton.addClickListener(event -> startNewRoundForSession(session, sessionCode));
}
```

## 🎯 Comportement corrigé

### Scénario : Le maître termine son quiz

1. **Le maître termine toutes les questions**
   - Arrive sur l'écran du score final
   - Voit son score et les statistiques

2. **Boutons affichés pour le maître** :
   - **"View Leaderboard"** (bouton Next) - Retourne à la page de session pour voir le classement
   - **"Restart Session"** (bouton Stop) - Redémarre la session pour tous (si ce n'est pas la première fois)
   - **"Start All"** (bouton Stop) - Démarre la session (si c'est la première fois)

3. **Quand le maître clique sur "Restart Session" ou "Start All"** :
   - La méthode `startNewRoundForSession()` est appelée
   - Elle réinitialise les scores de tous les participants
   - Efface les questions sélectionnées
   - Remet le statut de la session à `WAITING`
   - Redirige le maître vers la page de session (`quiz-session/[sessionCode]`)

4. **Sur la page de session** :
   - Le maître voit le bouton "Restart Session" (selon les règles définies dans QuizSessionView)
   - Les autres joueurs voient leur bouton "Start my quiz" désactivé
   - Quand le maître clique, tous les joueurs peuvent redémarrer

## ✅ Cohérence entre les vues

### Vue QuizQuestion (fin du quiz du maître)
- Bouton : "Restart Session" ou "Start All"
- Action : Réinitialise et redirige vers la vue session

### Vue QuizSession (page de session)
- Maître : Bouton "Restart Session" activé
- Participants : Bouton "Start my quiz" désactivé
- Quand maître démarre : Tous peuvent jouer

## 📊 Flux complet

```
┌───────────────────────┐
│ Maître termine quiz   │
│ (QuizQuestionView)    │
└──────────┬────────────┘
           │
           ▼
┌───────────────────────────────────────┐
│ Scoreboard affiché                    │
│ - View Leaderboard (Next button)     │
│ - Restart Session (Stop button) ✅   │
└──────────┬────────────────────────────┘
           │ Clic sur "Restart Session"
           ▼
┌───────────────────────────────────────┐
│ startNewRoundForSession()             │
│ - Reset scores participants           │
│ - Clear selected questions            │
│ - Set status to WAITING               │
│ - Navigate to quiz-session view      │
└──────────┬────────────────────────────┘
           │
           ▼
┌───────────────────────────────────────┐
│ Vue QuizSession (COMPLETED)           │
│ Maître: "Restart Session" activé ✅   │
│ Participants: Bouton désactivé        │
└───────────────────────────────────────┘
```

## 🔄 Logique de détection première session vs suivantes

```java
boolean hasBeenActiveAlready = session.getSelectedQuestionIds() != null;
String buttonLabel = hasBeenActiveAlready ? 
    translationService.translate("quizSession.restartSession") :  // Session déjà démarrée
    translationService.translate("quizSession.startAll");         // Première fois
```

- Si `selectedQuestionIds` est `null` → Première session → "Start All"
- Si `selectedQuestionIds` n'est pas `null` → Session déjà lancée → "Restart Session"

## 📝 Traductions utilisées

Les traductions existantes sont réutilisées :
- `quizSession.restartSession` = "Restart Session" / "Redémarrer la session" / "Riavvia Sessione"
- `quizSession.startAll` = "Start All" / "Démarrer pour tous" / "Inizia per tutti"

## 🧪 Tests recommandés

1. ✅ Maître termine son quiz → Voit "Start All" (première fois)
2. ✅ Maître termine son quiz → Voit "Restart Session" (sessions suivantes)
3. ✅ Maître clique sur le bouton → Redirigé vers page de session
4. ✅ Sur page de session → Voit le bon bouton de redémarrage
5. ✅ Participants ne voient pas le bouton de redémarrage après leur quiz
6. ✅ Le libellé est cohérent dans toutes les vues

## 📌 Notes importantes

- La méthode `startNewRoundForSession()` était déjà correcte
- Seul le **libellé du bouton** a été corrigé
- Le comportement reste identique : redirection vers la page de session
- La logique de détection première/suivante session est maintenant cohérente avec `QuizSessionView`

---

**Statut :** ✅ Corrigé  
**Impact :** Cohérence des libellés entre QuizQuestionView et QuizSessionView  
**Compatibilité :** Vaadin 24.x

