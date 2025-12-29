# Validation du Mode Équipe au démarrage d'un Quiz

## Date
30 décembre 2025

## Problème
Lorsqu'un utilisateur sélectionne la case "Mode Équipe" et clique sur le bouton "Démarrer" pour lancer un quiz directement (sans partage), le quiz démarrait normalement. Cependant, le mode équipe n'est disponible que pour les quiz partagés.

## Solution Implémentée

### 1. Validation dans QuizListView.java
Ajout d'une validation dans le gestionnaire d'événements du bouton "Start" :
- Vérifie si la case "Team Mode" est cochée
- Si oui, affiche un message d'avertissement et empêche le démarrage du quiz
- L'utilisateur doit décocher la case pour démarrer le quiz directement

```java
startButton = new Button(translationService.translate("quizlist.start"), event -> {
    if (selectedQuiz != null) {
        // Check if Team Mode is selected
        if (teamModeCheckbox.getValue()) {
            Notification notification = Notification.show(
                translationService.translate("quizlist.teamMode.warning"),
                5000,
                Notification.Position.MIDDLE
            );
            notification.addThemeVariants(NotificationVariant.LUMO_ERROR);
            return;
        }
        getUI().ifPresent(ui -> ui.navigate("quiz-questions/" + selectedQuiz.getId()));
    }
});
```

### 2. Traductions Ajoutées

#### messages.properties (Anglais par défaut)
```properties
quizlist.teamMode.warning=Team Mode is only available for shared quizzes. Please uncheck "Team Mode" to start the quiz directly.
```

#### messages_en.properties (Anglais)
```properties
quizlist.teamMode.warning=Team Mode is only available for shared quizzes. Please uncheck "Team Mode" to start the quiz directly.
```

#### messages_fr.properties (Français)
```properties
quizlist.teamMode.warning=Le mode équipe est uniquement disponible pour les quiz partagés. Veuillez décocher "Mode Équipe" pour démarrer le quiz directement.
```

#### messages_it.properties (Italien)
```properties
quizlist.teamMode.warning=La modalità squadra è disponibile solo per i quiz condivisi. Si prega di deselezionare "Modalità Squadra" per avviare direttamente il quiz.
```

## Fichiers Modifiés
1. `src/main/java/com/quizz/core/ui/QuizListView.java`
2. `src/main/resources/messages.properties`
3. `src/main/resources/messages_en.properties`
4. `src/main/resources/messages_fr.properties`
5. `src/main/resources/messages_it.properties`

## Comportement Attendu
1. L'utilisateur sélectionne un quiz
2. L'utilisateur coche la case "Mode Équipe"
3. L'utilisateur clique sur "Démarrer"
4. Un message d'erreur s'affiche pendant 5 secondes au centre de l'écran
5. Le quiz ne démarre pas
6. L'utilisateur doit décocher "Mode Équipe" pour démarrer le quiz en mode individuel

## Test de Compilation
✅ Compilation réussie avec `mvn clean compile -DskipTests`

## Notes
- Le mode équipe reste disponible lors du partage d'un quiz
- Le message d'avertissement est traduit dans les 3 langues supportées (EN, FR, IT)
- La notification utilise le variant LUMO_ERROR pour une meilleure visibilité

