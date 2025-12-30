# Validation : Minimum 2 équipes pour le Mode Équipe

## 📋 Modification effectuée

Une validation a été ajoutée pour **exiger au moins 2 équipes sélectionnées** lorsque le "Team Mode" est activé, partout dans l'application.

## 🎯 Règle implémentée

**Règle :** Au moins 2 équipes doivent être sélectionnées pour démarrer un quiz en mode équipe.

**Message d'erreur :**
- Si **0 équipe** sélectionnée : "Veuillez sélectionner au moins une équipe avant de démarrer le quiz"
- Si **1 équipe** sélectionnée : "Veuillez sélectionner au moins 2 équipes pour le Mode Équipe (seulement 1 équipe sélectionnée actuellement)"

## 📁 Fichiers modifiés

### 1. TeamModeView.java

#### Validation dans le bouton Share
```java
shareBtn = new Button(translationService.translate("teammode.startShared"), event -> {
    if (selectedQuiz != null) {
        if (selectedTeams.size() < 2) {
            String warningMessage;
            if (selectedTeams.isEmpty()) {
                warningMessage = translationService.translate("teammode.selectTeams.warning");
            } else {
                warningMessage = translationService.translate("teammode.selectTeams.minimum")
                    .replace("{0}", String.valueOf(selectedTeams.size()));
            }
            Notification notification = Notification.show(
                warningMessage,
                5000,
                Notification.Position.MIDDLE
            );
            notification.addThemeVariants(NotificationVariant.LUMO_ERROR);
            return;
        }
        showShareDialog(selectedQuiz);
    }
});
```

#### Activation du bouton
```java
private void updateShareButtonState() {
    shareBtn.setEnabled(selectedQuiz != null && selectedTeams.size() >= 2);
}
```

Le bouton "Start Quiz (Shared)" n'est **activé** que si au moins 2 équipes sont sélectionnées.

### 2. QuizListView.java

#### Validation dans le dialogue de partage
```java
Button goToSessionButton = new Button("Go to Session Room", event -> {
    // Validate team mode requirements
    if (session.isTeamMode()) {
        java.util.List<String> selectedTeamsList = new java.util.ArrayList<>();
        teamCheckboxes.forEach((t, cb) -> {
            if (cb.getValue()) {
                selectedTeamsList.add(t);
            }
        });
        
        if (selectedTeamsList.size() < 2) {
            String warningMessage;
            if (selectedTeamsList.isEmpty()) {
                warningMessage = translationService.translate("teammode.selectTeams.warning");
            } else {
                warningMessage = translationService.translate("teammode.selectTeams.minimum")
                    .replace("{0}", String.valueOf(selectedTeamsList.size()));
            }
            Notification.show(warningMessage, 5000, Notification.Position.MIDDLE)
                .addThemeVariants(NotificationVariant.LUMO_ERROR);
            return;
        }
        
        // Update session with selected teams
        session.setSelectedTeams(String.join(",", selectedTeamsList));
        sessionService.updateSession(session);
    }
    
    dialog.close();
    getUI().ifPresent(ui -> ui.navigate("quiz-session/" + session.getSessionCode()));
});
```

### 3. Fichiers de traduction

#### messages_en.properties
```properties
teammode.selectTeams.warning=Please select at least one team before starting the quiz
teammode.selectTeams.minimum=Please select at least 2 teams for Team Mode (currently only {0} team selected)
```

#### messages_fr.properties
```properties
teammode.selectTeams.warning=Veuillez sélectionner au moins une équipe avant de démarrer le quiz
teammode.selectTeams.minimum=Veuillez sélectionner au moins 2 équipes pour le Mode Équipe (seulement {0} équipe sélectionnée actuellement)
```

#### messages_it.properties
```properties
teammode.selectTeams.warning=Seleziona almeno una squadra prima di iniziare il quiz
teammode.selectTeams.minimum=Seleziona almeno 2 squadre per la Modalità Squadra (attualmente solo {0} squadra selezionata)
```

#### messages.properties (par défaut)
```properties
teammode.selectTeams.warning=Please select at least one team before starting the quiz
teammode.selectTeams.minimum=Please select at least 2 teams for Team Mode (currently only {0} team selected)
```

## 🎯 Points de validation

La validation "minimum 2 équipes" est appliquée à **3 endroits** :

### 1. TeamModeView - Bouton désactivé
- Le bouton "Start Quiz (Shared)" est **désactivé** tant que moins de 2 équipes sont sélectionnées
- **État du bouton :** Grisé si < 2 équipes, actif si ≥ 2 équipes

### 2. TeamModeView - Click sur Share
- Si l'utilisateur clique sur le bouton alors que < 2 équipes sont sélectionnées
- **Action :** Affichage d'une notification d'erreur
- **Couleur :** Rouge (LUMO_ERROR)
- **Durée :** 5 secondes

### 3. QuizListView - Dialogue de partage
- Dans le dialogue de partage, quand l'utilisateur clique sur "Go to Session Room"
- Si le Team Mode est activé et < 2 équipes sont sélectionnées
- **Action :** Affichage d'une notification d'erreur et empêche la navigation

## 📊 Matrice de validation

| Équipes sélectionnées | Bouton Share (TeamMode) | Message | Peut démarrer ? |
|----------------------|-------------------------|---------|-----------------|
| 0 | ❌ Désactivé | "Sélectionner au moins une équipe" | ❌ Non |
| 1 | ❌ Désactivé | "Au moins 2 équipes (1 actuellement)" | ❌ Non |
| 2 | ✅ Activé | - | ✅ Oui |
| 3+ | ✅ Activé | - | ✅ Oui |

## 🌍 Messages multilingues

### Anglais
- **0 équipes :** "Please select at least one team before starting the quiz"
- **1 équipe :** "Please select at least 2 teams for Team Mode (currently only 1 team selected)"

### Français
- **0 équipes :** "Veuillez sélectionner au moins une équipe avant de démarrer le quiz"
- **1 équipe :** "Veuillez sélectionner au moins 2 équipes pour le Mode Équipe (seulement 1 équipe sélectionnée actuellement)"

### Italien
- **0 équipes :** "Seleziona almeno una squadra prima di iniziare il quiz"
- **1 équipe :** "Seleziona almeno 2 squadre per la Modalità Squadra (attualmente solo 1 squadra selezionata)"

## ✅ Comportement utilisateur

### Scénario 1 : TeamModeView
1. L'utilisateur ouvre "Team Mode"
2. Il sélectionne un quiz
3. Le bouton "Start Quiz (Shared)" est **grisé**
4. Il coche 1 équipe → Bouton toujours **grisé**
5. Il coche une 2ème équipe → Bouton **activé** ✅
6. Il peut maintenant démarrer le quiz en mode équipe

### Scénario 2 : QuizListView avec Team Mode
1. L'utilisateur ouvre "Un Quizz"
2. Il sélectionne un quiz et clique sur "Share"
3. Il coche la case "Team Mode"
4. La section de sélection des équipes apparaît
5. Il sélectionne 1 équipe et clique "Go to Session Room"
6. **Notification d'erreur** : "Au moins 2 équipes (seulement 1 actuellement)" ❌
7. Il sélectionne une 2ème équipe
8. Il clique "Go to Session Room" → **Navigation vers la session** ✅

## 🔒 Sécurité

La validation est effectuée :
- ✅ **Côté client** : Bouton désactivé (UX)
- ✅ **Avant navigation** : Vérification avant de créer/rejoindre la session
- ✅ **Dans le dialogue** : Vérification avant de naviguer vers la session

## 📝 Notes importantes

1. **Le bouton reste désactivé** tant que < 2 équipes sont sélectionnées dans TeamModeView
2. **Le message est dynamique** : affiche le nombre d'équipes actuellement sélectionnées si = 1
3. **Validation cohérente** : même règle dans TeamModeView et QuizListView
4. **Traductions complètes** : EN, FR, IT + messages.properties par défaut

## 🧪 Tests à effectuer

### Test 1 : TeamModeView
- [ ] Ouvrir "Team Mode"
- [ ] Sélectionner un quiz
- [ ] Vérifier que le bouton "Start Quiz (Shared)" est grisé
- [ ] Cocher 1 équipe → Bouton toujours grisé
- [ ] Cocher une 2ème équipe → Bouton activé
- [ ] Cliquer sur le bouton → Dialogue s'ouvre

### Test 2 : QuizListView
- [ ] Ouvrir "Un Quizz"
- [ ] Sélectionner un quiz et cliquer "Share"
- [ ] Cocher "Team Mode"
- [ ] Sélectionner 1 équipe
- [ ] Cliquer "Go to Session Room" → Erreur affichée
- [ ] Sélectionner une 2ème équipe
- [ ] Cliquer "Go to Session Room" → Navigation réussie

### Test 3 : Multilingue
- [ ] Tester en français
- [ ] Tester en anglais
- [ ] Tester en italien
- [ ] Vérifier que les messages sont correctement traduits

## ✅ Résumé

- ✅ Validation "minimum 2 équipes" implémentée partout
- ✅ Messages d'erreur clairs et traduits (EN, FR, IT)
- ✅ Bouton désactivé si < 2 équipes (TeamModeView)
- ✅ Validation avant navigation (QuizListView)
- ✅ Message dynamique affichant le nombre d'équipes sélectionnées
- ✅ Aucune erreur de compilation
- ✅ Code prêt à être utilisé

**La règle "minimum 2 équipes pour le Team Mode" est maintenant appliquée de manière cohérente dans toute l'application.**

