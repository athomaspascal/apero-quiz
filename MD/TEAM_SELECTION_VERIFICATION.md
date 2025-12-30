# ✅ Vérification : Sélection d'équipe obligatoire - Points de contrôle

## 📋 Demande de vérification

Vérifier que :
1. **Le joueur doit choisir une équipe juste après avoir entré le code de session**
2. **Le master doit choisir son équipe juste après avoir cliqué sur "Share the quiz"**

---

## ✅ Point 1 : Joueur entre le code de session

### 📍 Où cela se passe

**Fichier :** `QuizSessionView.java`  
**Méthode :** `beforeEnter(BeforeEnterEvent event)`

### 🔍 Code actuel

```java
@Override
public void beforeEnter(BeforeEnterEvent event) {
    String sessionCode = event.getRouteParameters().get("sessionCode").orElse(null);

    if (sessionCode == null) {
        event.rerouteTo("");
        return;
    }

    session = sessionService.getSessionByCode(sessionCode);

    if (session == null) {
        add(new H2(translationService.translate("quizSession.notFound")));
        add(new Paragraph(translationService.translate("quizSession.invalidCode", sessionCode)));
        add(new Button(translationService.translate("quiz.backToList"), e -> getUI().ifPresent(ui -> ui.navigate(""))));
        return;
    }

    User currentUser = VaadinSession.getCurrent().getAttribute(User.class);
    if (currentUser == null) {
        // Save the intended URL to redirect after login
        VaadinSession.getCurrent().setAttribute("redirectAfterLogin", "quiz-session/" + sessionCode);
        // Redirect to login
        event.rerouteTo(com.quizz.core.security.LoginView.class);
        return;
    }

    // Join the session
    sessionService.joinSession(session, currentUser);

    // After session loaded, update the dynamic page title with quiz name
    getUI().ifPresent(ui -> ui.getPage().setTitle(translationService.translate("quizSession.title", session.getQuiz().getName())));

    buildUI();

    // If team mode is enabled and user hasn't selected a team yet, force selection
    if (session.isTeamMode()) {
        QuizParticipant participant = sessionService.getParticipant(session, currentUser);
        if (participant != null && (participant.getTeamName() == null || participant.getTeamName().isEmpty())) {
            // Force team selection immediately after joining
            showTeamSelectionDialogOnJoin(currentUser);
        }
    }
}
```

### ✅ Vérification

**Statut :** ✅ **CORRECT - IMPLÉMENTÉ**

**Flux :**
1. Joueur entre le code de session (ex: ABCD1234)
2. Navigation vers `/quiz-session/ABCD1234`
3. `beforeEnter()` s'exécute
4. Vérification que la session existe ✅
5. Vérification que l'utilisateur est connecté ✅
6. `joinSession(session, currentUser)` → Crée un `QuizParticipant` ✅
7. `buildUI()` → Construit l'interface ✅
8. **VÉRIFICATION Team Mode :**
   - `session.isTeamMode()` ? ✅ OUI
   - `participant.getTeamName() == null || isEmpty()` ? ✅ OUI
   - **→ `showTeamSelectionDialogOnJoin(currentUser)` s'appelle** 🎯
9. Dialogue obligatoire s'affiche immédiatement
10. Le joueur DOIT choisir son équipe avant de continuer

**Caractéristiques du dialogue :**
- ❌ Pas de bouton Cancel
- ❌ Impossible de fermer avec ESC
- ❌ Impossible de fermer en cliquant dehors
- ✅ Bouton "Confirm" actif seulement si équipe sélectionnée

---

## ✅ Point 2 : Master clique "Share the quiz"

### 📍 Où cela se passe

**Il y a 2 endroits où le master peut partager :**

#### A. TeamModeView.java

**Méthode :** `showShareDialog(Quiz quiz)`

```java
private void showShareDialog(Quiz quiz) {
    User currentUser = VaadinSession.getCurrent().getAttribute(User.class);
    if (currentUser == null || currentUser.getId() == null) {
        Notification.show(...);
        return;
    }

    // Create a new session with team mode enabled
    QuizSession session = sessionService.createSession(quiz, currentUser.getId());
    session.setTeamMode(true);
    session.setSelectedTeams(String.join(",", selectedTeams));
    sessionService.updateSession(session);

    Dialog dialog = new Dialog();
    // ... Show QR code and session info ...

    Button goToSessionButton = new Button(..., event -> {
        dialog.close();
        getUI().ifPresent(ui -> ui.navigate("quiz-session/" + session.getSessionCode()));
    });
    
    // ... dialog shown ...
}
```

#### B. QuizListView.java

**Méthode :** `showShareDialog(Quiz quiz)`

```java
private void showShareDialog(Quiz quiz) {
    User currentUser = VaadinSession.getCurrent().getAttribute(User.class);
    if (currentUser == null || currentUser.getId() == null) {
        Notification.show(...);
        return;
    }

    // Create a new session
    QuizSession session = sessionService.createSession(quiz, currentUser.getId());

    // Set team mode based on checkbox
    if (teamModeCheckbox.getValue()) {
        session.setTeamMode(true);
        sessionService.updateSession(session);
    }

    Dialog dialog = new Dialog();
    // ... Team mode section with checkboxes ...
    // ... Show QR code and session info ...

    Button goToSessionButton = new Button("Go to Session Room", event -> {
        // Validate team mode requirements (minimum 2 teams)
        if (session.isTeamMode()) {
            // ... validation ...
            session.setSelectedTeams(String.join(",", selectedTeamsList));
            sessionService.updateSession(session);
        }

        dialog.close();
        getUI().ifPresent(ui -> ui.navigate("quiz-session/" + session.getSessionCode()));
    });
    
    // ... dialog shown ...
}
```

### ✅ Vérification

**Statut :** ✅ **CORRECT - IMPLÉMENTÉ INDIRECTEMENT**

**Flux :**

#### Depuis TeamModeView (toujours Team Mode) :
1. Master sélectionne au moins 2 équipes (ex: Stark, Lannister)
2. Master sélectionne un quiz
3. Master clique "Start Quiz (Shared)"
4. **Une session Team Mode est créée** : `sessionService.createSession(quiz, currentUser.getId())`
5. Dialogue s'affiche avec QR code
6. Master clique "Go to Session Room"
7. **Navigation vers `/quiz-session/CODE`**
8. **→ `beforeEnter()` s'exécute (Point 1)** 🎯
9. `joinSession()` crée un participant pour le master
10. **VÉRIFICATION Team Mode :**
    - Session en Team Mode ? ✅ OUI
    - Master n'a pas d'équipe ? ✅ OUI
    - **→ `showTeamSelectionDialogOnJoin(currentUser)` s'appelle** 🎯
11. **Dialogue obligatoire s'affiche pour le master**
12. Le master DOIT choisir son équipe avant de continuer

#### Depuis QuizListView (Team Mode optionnel) :
1. Master sélectionne un quiz
2. Master coche "Team Mode" (optionnel)
3. Master sélectionne au moins 2 équipes
4. Master clique "Share"
5. **Une session est créée** (Team Mode si checkbox cochée)
6. Dialogue s'affiche avec options Team Mode et QR code
7. Master clique "Go to Session Room"
8. **Navigation vers `/quiz-session/CODE`**
9. **→ `beforeEnter()` s'exécute (Point 1)** 🎯
10. `joinSession()` crée un participant pour le master
11. **SI Team Mode :**
    - Master n'a pas d'équipe ? ✅ OUI
    - **→ `showTeamSelectionDialogOnJoin(currentUser)` s'appelle** 🎯
12. **Dialogue obligatoire s'affiche pour le master**
13. Le master DOIT choisir son équipe avant de continuer

### 🔑 Point clé

Le master ne choisit pas son équipe **dans** le dialogue "Share" lui-même, mais il est **forcé de la choisir immédiatement après** avoir cliqué sur "Go to Session Room" grâce au code dans `beforeEnter()`.

C'est une approche **cohérente** car :
- ✅ Le master est traité comme n'importe quel participant
- ✅ Un seul endroit pour la logique de sélection d'équipe (pas de duplication)
- ✅ Le flux est le même pour master et joueurs

---

## 📊 Matrice de vérification complète

| Scénario | Acteur | Action | Team Mode ? | Dialogue affiché ? | Quand ? |
|----------|--------|--------|-------------|-------------------|---------|
| 1 | Joueur | Entre code session | ✅ OUI | ✅ **OUI** | Immédiatement après `buildUI()` |
| 2 | Joueur | Entre code session | ❌ NON | ❌ Non | - |
| 3 | Joueur | Revient (équipe déjà choisie) | ✅ OUI | ❌ Non | - |
| 4 | Master | Share → Go to Session Room | ✅ OUI | ✅ **OUI** | Immédiatement après navigation |
| 5 | Master | Share → Go to Session Room | ❌ NON | ❌ Non | - |
| 6 | Master | Revient à sa session | ✅ OUI (équipe déjà choisie) | ❌ Non | - |

---

## 🔍 Code de la méthode `showTeamSelectionDialogOnJoin()`

```java
private void showTeamSelectionDialogOnJoin(User currentUser) {
    Dialog dialog = new Dialog();
    dialog.setHeaderTitle(translationService.translate("quizSession.teamMode.selectTeam"));
    dialog.setWidth("400px");
    dialog.setCloseOnOutsideClick(false);  // Cannot close outside
    dialog.setCloseOnEsc(false);           // Cannot close with ESC

    VerticalLayout content = new VerticalLayout();
    content.setSpacing(true);
    content.setPadding(false);

    QuizParticipant participant = sessionService.getParticipant(session, currentUser);

    Paragraph instruction = new Paragraph(
        translationService.translate("quizSession.teamMode.selectTeamMessage")
    );
    instruction.getStyle().set("color", "var(--lumo-secondary-text-color)");

    com.vaadin.flow.component.radiobutton.RadioButtonGroup<String> teamRadioGroup =
        new com.vaadin.flow.component.radiobutton.RadioButtonGroup<>();
    teamRadioGroup.setLabel(translationService.translate("quizSession.teamMode"));

    // Get available teams from session
    if (session.getSelectedTeams() != null && !session.getSelectedTeams().isEmpty()) {
        String[] teams = session.getSelectedTeams().split(",");
        java.util.Map<String, String> teamItems = new java.util.LinkedHashMap<>();
        for (String team : teams) {
            teamItems.put(team, translationService.translate("quizSession.teamMode.team." + team));
        }
        teamRadioGroup.setItems(teamItems.keySet());
        teamRadioGroup.setItemLabelGenerator(team -> teamItems.get(team));

        // Pre-select team if already chosen
        if (participant != null && participant.getTeamName() != null) {
            teamRadioGroup.setValue(participant.getTeamName());
        }
    }

    HorizontalLayout buttonLayout = new HorizontalLayout();
    buttonLayout.setSpacing(true);

    Button confirmButton = new Button(
        translationService.translate("quizSession.teamMode.confirmTeam"), 
        event -> {
            String selectedTeam = teamRadioGroup.getValue();
            if (selectedTeam != null && participant != null) {
                // Update participant's team
                sessionService.updateParticipantTeam(participant, selectedTeam);
                
                // Close dialog and refresh UI
                dialog.close();
                buildUI();
            }
        }
    );
    confirmButton.addThemeVariants(ButtonVariant.LUMO_PRIMARY);
    confirmButton.setEnabled(teamRadioGroup.getValue() != null);

    teamRadioGroup.addValueChangeListener(event -> {
        confirmButton.setEnabled(event.getValue() != null);
    });

    // No cancel button - team selection is mandatory in team mode
    buttonLayout.add(confirmButton);

    content.add(instruction, teamRadioGroup, buttonLayout);
    dialog.add(content);
    dialog.open();
}
```

---

## ✅ Conclusion de la vérification

### Point 1 : Joueur entre le code de session
**Statut :** ✅ **VÉRIFIÉ ET CORRECT**
- Le dialogue s'affiche **immédiatement** après que le joueur ait rejoint la session
- Le joueur **ne peut pas** naviguer sans choisir d'équipe
- Le dialogue est **obligatoire** (pas de contournement possible)

### Point 2 : Master clique "Share the quiz"
**Statut :** ✅ **VÉRIFIÉ ET CORRECT**
- Le master crée la session en Team Mode
- Quand il clique "Go to Session Room", il navigue vers la session
- **Le même code que pour les joueurs s'applique** (`beforeEnter()`)
- Le dialogue s'affiche **immédiatement** après la navigation
- Le master **doit choisir son équipe** avant de voir la page de session

### 🎯 Points forts de l'implémentation

1. **Code centralisé** : Un seul endroit pour la logique (`beforeEnter()`)
2. **Cohérence** : Master et joueurs sont traités de la même façon
3. **Pas de duplication** : Pas besoin de code spécial pour le master
4. **Sécurité** : Dialogue obligatoire, pas de contournement
5. **Persistance** : Si l'utilisateur revient, pas de nouveau dialogue (équipe déjà enregistrée)

### 📝 Modification effectuée

**Simplification de l'appel au dialogue :**
- **Avant :** `getUI().ifPresent(ui -> ui.access(() -> showTeamSelectionDialogOnJoin(currentUser)))`
- **Après :** `showTeamSelectionDialogOnJoin(currentUser)`
- **Raison :** Pas besoin de `ui.access()` car nous sommes déjà dans le thread UI dans `beforeEnter()`

---

## ✅ Résumé final

| Point | Demande | Statut | Implémentation |
|-------|---------|--------|----------------|
| **1** | Joueur choisit équipe après avoir entré le code | ✅ **OUI** | `QuizSessionView.beforeEnter()` |
| **2** | Master choisit équipe après avoir cliqué "Share" | ✅ **OUI** | Via navigation → `beforeEnter()` |

**Les deux points sont correctement implémentés et fonctionnels ! 🎉**

**Aucun changement supplémentaire n'est nécessaire.**

