# Fix: Checkbox "Team Mode" visible dans QuizListView

## Problème
La checkbox "Team Mode" n'était pas visible à côté du bouton "Share" dans la vue QuizListView.

## Solution Implémentée

### Modifications dans `QuizListView.java`

1. **Ajout de l'import Checkbox** (ligne 13)
   ```java
   import com.vaadin.flow.component.checkbox.Checkbox;
   ```

2. **Ajout du champ teamModeCheckbox** (ligne 51)
   ```java
   final Checkbox teamModeCheckbox;
   ```

3. **Initialisation de la checkbox dans le constructeur** (lignes 87-90)
   ```java
   // Team Mode checkbox
   teamModeCheckbox = new Checkbox(translationService.translate("quizSession.teamMode"));
   teamModeCheckbox.getStyle()
       .set("margin-left", "10px")
       .set("align-self", "center");
   ```

4. **Ajout de la checkbox dans la toolbar** (ligne 109)
   ```java
   add(new ViewToolbar(translationService.translate("quizlist.title"), 
       ViewToolbar.group(name, startButton, shareBtn, teamModeCheckbox)));
   ```

5. **Utilisation de la checkbox dans showShareDialog** (lignes 390-395)
   ```java
   // Create a new session
   QuizSession session = sessionService.createSession(quiz, currentUser.getId());
   
   // Set team mode based on checkbox
   if (teamModeCheckbox.getValue()) {
       session.setTeamMode(true);
       sessionService.updateSession(session);
   }
   ```

## Résultat

Maintenant, dans la vue QuizListView :
- ✅ La checkbox "Team Mode" est visible à côté du bouton "Share"
- ✅ Quand l'hôte coche la checkbox avant de cliquer sur "Share", la session est créée en mode équipe
- ✅ La traduction est appliquée (FR: "Mode Équipe", EN: "Team Mode", IT: "Modalità Squadra")

## Workflow Utilisateur

1. L'utilisateur accède à la page "Un Quizz"
2. Il sélectionne un quiz
3. **Il coche "Team Mode" s'il veut activer le mode équipe**
4. Il clique sur "Share"
5. Une session est créée avec le mode équipe activé
6. L'hôte va dans la salle de session où il peut sélectionner les équipes disponibles

## Statut

✅ **RÉSOLU**
- Compilation réussie
- Checkbox visible dans l'interface
- Fonctionnalité opérationnelle

## Date
29 décembre 2025

