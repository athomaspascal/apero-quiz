# Mise à jour : Sélection d'équipe obligatoire DÈS l'arrivée

## 📋 Modification effectuée

Le joueur doit maintenant **choisir son équipe immédiatement** lorsqu'il rejoint une session en mode équipe, **PAS** seulement quand il clique sur "Start Mine".

## 🎯 Comportement antérieur vs Nouveau comportement

### ❌ AVANT (problème)
1. Joueur rejoint une session en Team Mode
2. Joueur voit la liste des participants
3. **Joueur peut naviguer dans la page sans avoir choisi d'équipe**
4. Joueur clique sur "Start Mine"
5. **Seulement à ce moment**, le dialogue de sélection s'affiche

**Problème :** Le joueur pouvait voir la session sans être assigné à une équipe.

### ✅ APRÈS (corrigé)
1. Joueur rejoint une session en Team Mode
2. **IMMÉDIATEMENT**, un dialogue obligatoire s'affiche
3. Le joueur **DOIT** choisir son équipe avant de pouvoir faire quoi que ce soit
4. Le dialogue **ne peut pas être fermé** (pas de cancel, ESC, clic dehors)
5. Après confirmation, le joueur voit la page de session avec son équipe affichée
6. Quand il clique sur "Start Mine", le quiz démarre directement (équipe déjà sélectionnée)

## 📁 Modifications apportées

### 1. Méthode `beforeEnter()` - Ajout de la validation

```java
@Override
public void beforeEnter(BeforeEnterEvent event) {
    // ...existing validation code...
    
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
            getUI().ifPresent(ui -> ui.access(() -> {
                showTeamSelectionDialogOnJoin(currentUser);
            }));
        }
    }
}
```

**Ce qui se passe :**
- Après que le joueur ait rejoint la session (`joinSession`)
- ET après que l'UI soit construite (`buildUI`)
- Si le mode équipe est activé ET que le joueur n'a pas d'équipe
- **→ Le dialogue de sélection s'affiche automatiquement**

### 2. Nouvelle méthode `showTeamSelectionDialogOnJoin()`

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

    // Get participant
    QuizParticipant participant = sessionService.getParticipant(session, currentUser);

    Paragraph instruction = new Paragraph(
        translationService.translate("quizSession.teamMode.selectTeamMessage")
    );
    instruction.getStyle().set("color", "var(--lumo-secondary-text-color)");

    com.vaadin.flow.component.radiobutton.RadioButtonGroup<String> teamRadioGroup =
        new com.vaadin.flow.component.radiobutton.RadioButtonGroup<>();
    teamRadioGroup.setLabel(translationService.translate("quizSession.teamMode"));

    // Get available teams
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

**Différence avec `showTeamSelectionDialog()` :**

| Méthode | Quand ? | Action après confirmation |
|---------|---------|---------------------------|
| `showTeamSelectionDialogOnJoin()` | **À l'arrivée** du joueur | Ferme le dialogue et **rafraîchit l'UI** |
| `showTeamSelectionDialog()` | Clic sur "Start Mine" | Ferme le dialogue et **lance le quiz** |
| `showTeamSelectionDialogForHost()` | Host clique "Start All" sans équipe | Ferme le dialogue et **démarre la session** |

## 🎯 Flux d'utilisation complet

### Scénario : Joueur rejoint une session Team Mode

1. **Le joueur scanne le QR code ou entre le code de session**
2. **Il est redirigé vers `/quiz-session/ABCD1234`**
3. **Méthode `beforeEnter()` s'exécute :**
   - Vérifie que la session existe ✅
   - Vérifie que l'utilisateur est connecté ✅
   - Appelle `joinSession()` → Le joueur est ajouté à la session
   - Appelle `buildUI()` → L'interface se construit
   - **VÉRIFICATION Team Mode :**
     - Session en mode équipe ? ✅
     - Joueur n'a pas d'équipe ? ✅
     - **→ Dialogue s'affiche IMMÉDIATEMENT** 🎯
4. **Le dialogue s'affiche :**
   - Titre : "Sélectionnez votre équipe"
   - Message : "Veuillez choisir une équipe avant de commencer le quiz"
   - Liste des équipes disponibles (ex: Stark, Lannister, Targaryen)
   - Bouton "Confirmer" (désactivé si aucune sélection)
   - ❌ **Impossible de fermer le dialogue** (pas de cancel, ESC, clic dehors)
5. **Le joueur sélectionne une équipe** (ex: Stark)
6. **Le bouton "Confirmer" devient actif**
7. **Le joueur clique sur "Confirmer"**
8. **Son équipe est enregistrée** : `updateParticipantTeam(participant, "stark")`
9. **Le dialogue se ferme**
10. **L'UI se rafraîchit** : `buildUI()`
11. **Le joueur voit maintenant :**
    - La liste des participants avec **son nom et son équipe affichée**
    - Les boutons d'action disponibles
12. **Plus tard, quand il clique sur "Start Mine" :**
    - Pas de nouveau dialogue (équipe déjà sélectionnée)
    - Le quiz démarre directement ✅

### Scénario : Joueur rejoint une session normale (pas Team Mode)

1. **Le joueur rejoint la session**
2. **Méthode `beforeEnter()` s'exécute :**
   - `joinSession()` ✅
   - `buildUI()` ✅
   - **VÉRIFICATION Team Mode :**
     - Session en mode équipe ? ❌ **NON**
     - **→ Aucun dialogue** ✅
3. **Le joueur voit directement la page de session**
4. **Il peut cliquer sur "Start Mine" quand il veut**
5. **Le quiz démarre**

### Scénario : Joueur quitte et revient à la session Team Mode

1. **Le joueur a déjà sélectionné son équipe lors de sa première visite**
2. **Il quitte la page**
3. **Il revient à `/quiz-session/ABCD1234`**
4. **Méthode `beforeEnter()` s'exécute :**
   - `joinSession()` ✅ (rejoindre ou rester dans la session)
   - `buildUI()` ✅
   - **VÉRIFICATION Team Mode :**
     - Session en mode équipe ? ✅
     - Joueur n'a pas d'équipe ? ❌ **Il a déjà une équipe**
     - **→ Pas de dialogue** ✅
5. **Le joueur voit directement la page avec son équipe**

## 📊 Matrice de validation

| Situation | Mode | Équipe joueur | Dialogue affiché ? | Quand ? |
|-----------|------|---------------|-------------------|---------|
| Joueur arrive (1ère fois) | Team Mode | ❌ Aucune | ✅ **OUI** | **Immédiatement** après `buildUI()` |
| Joueur arrive (1ère fois) | Normal | - | ❌ Non | - |
| Joueur revient | Team Mode | ✅ Stark | ❌ Non | - |
| Joueur revient | Normal | - | ❌ Non | - |
| Joueur clique "Start Mine" | Team Mode | ✅ Stark | ❌ Non | - |
| Joueur clique "Start Mine" | Team Mode | ❌ Aucune | ✅ **OUI** | Clic sur "Start Mine" |
| Joueur clique "Start Mine" | Normal | - | ❌ Non | - |
| Host clique "Start All" | Team Mode | ❌ Aucune | ✅ **OUI** (spécial host) | Clic sur "Start All" |
| Host clique "Start All" | Team Mode | ✅ Stark | ❌ Non | - |

## 🔒 Protection

### Moment de la vérification
```java
if (session.isTeamMode()) {
    QuizParticipant participant = sessionService.getParticipant(session, currentUser);
    if (participant != null && (participant.getTeamName() == null || participant.getTeamName().isEmpty())) {
        // Force team selection
        showTeamSelectionDialogOnJoin(currentUser);
    }
}
```

### Dialogue non fermable
```java
dialog.setCloseOnOutsideClick(false);  // Impossible de fermer en cliquant dehors
dialog.setCloseOnEsc(false);           // Impossible de fermer avec ESC
// Pas de bouton "Cancel" dans le layout
```

## ✅ Avantages de cette approche

1. **Obligation immédiate** : Le joueur ne peut pas naviguer sans équipe
2. **Expérience utilisateur claire** : Dès l'arrivée, le joueur sait qu'il doit choisir une équipe
3. **Données cohérentes** : Tous les participants en Team Mode ont toujours une équipe
4. **Pas de duplication** : Si le joueur revient, pas de nouveau dialogue
5. **Persistance** : L'équipe est enregistrée en base de données immédiatement

## 🧪 Tests à effectuer

### Test 1 : Première arrivée en Team Mode
- [ ] Créer une session en Team Mode avec équipes (Stark, Lannister)
- [ ] Scanner le QR code avec un autre joueur
- [ ] ✅ Le dialogue s'affiche IMMÉDIATEMENT après l'arrivée
- [ ] ✅ Impossible de fermer avec ESC
- [ ] ✅ Impossible de fermer en cliquant dehors
- [ ] Sélectionner "Stark"
- [ ] ✅ Bouton "Confirmer" actif
- [ ] Cliquer "Confirmer"
- [ ] ✅ Dialogue se ferme
- [ ] ✅ La page affiche le joueur avec "Équipe : Stark"

### Test 2 : Retour à la session (équipe déjà choisie)
- [ ] Quitter la page de session
- [ ] Revenir à la même session
- [ ] ✅ Pas de dialogue (équipe déjà enregistrée)
- [ ] ✅ La page affiche directement l'équipe "Stark"

### Test 3 : Session normale (pas Team Mode)
- [ ] Créer une session SANS Team Mode
- [ ] Rejoindre la session
- [ ] ✅ Pas de dialogue
- [ ] ✅ Page s'affiche directement

### Test 4 : Clic sur "Start Mine" après avoir choisi l'équipe
- [ ] Dans une session Team Mode (équipe déjà choisie)
- [ ] Cliquer sur "Start Mine"
- [ ] ✅ Pas de nouveau dialogue
- [ ] ✅ Quiz démarre directement

## 📝 Notes importantes

1. **La vérification se fait dans `beforeEnter()`** : C'est le point d'entrée de la page, donc c'est l'endroit idéal pour forcer la sélection.

2. **Utilisation de `ui.access()`** : Nécessaire pour ouvrir le dialogue de manière asynchrone après que l'UI soit construite.

3. **Deux dialogues différents** :
   - `showTeamSelectionDialogOnJoin()` : À l'arrivée, rafraîchit juste l'UI
   - `showTeamSelectionDialog()` : Au clic "Start Mine", lance le quiz

4. **Le host aussi** : Si le host rejoint sa propre session sans équipe, il doit aussi choisir.

## ✅ Résumé

- ✅ **Sélection d'équipe obligatoire DÈS l'arrivée** dans une session Team Mode
- ✅ **Dialogue automatique** si le joueur n'a pas d'équipe
- ✅ **Dialogue non fermable** (pas de contournement possible)
- ✅ **Pas de duplication** si le joueur revient (équipe déjà enregistrée)
- ✅ **Expérience utilisateur améliorée** : tout est clair dès le début
- ✅ **Code prêt** : Aucune erreur de compilation

**Le joueur doit maintenant choisir son équipe immédiatement lorsqu'il rejoint une session en mode équipe ! 🎉**

