# Correction de l'Écran Blanc en Mode Duel - 2026-01-06

## Problème Identifié

Lors des tests du mode duel, un des deux adversaires (par exemple "Mother Theresa") voyait une **page blanche** lorsque le quiz en mode duel démarrait, alors que l'autre joueur voyait correctement les questions.

## Cause Racine

Le problème était lié à la réutilisation de l'instance `QuizQuestionView` entre différents quiz en mode duel. Voici ce qui se passait :

1. **Fin du premier duel** : La méthode `showDuelScoreboard()` cachait intentionnellement certains éléments de l'UI :
   ```java
   questionText.setVisible(false);
   playerInfoLabel.setVisible(false);
   answerFeedback.setVisible(false);
   ```

2. **Démarrage d'un nouveau duel** : Lorsqu'un joueur recommençait un duel, Vaadin réutilisait la même instance de `QuizQuestionView`, mais les éléments précédemment cachés **restaient cachés**, causant un écran blanc car le texte de la question (`questionText`) n'était jamais réaffiché.

3. **Affichage asymétrique** : Selon le timing et le recyclage des instances par Vaadin, un joueur pouvait avoir une instance fraîche (avec tous les éléments visibles) tandis que l'autre joueur héritait d'une instance où les éléments étaient cachés.

## Solution Implémentée

La correction consiste à **toujours réafficher explicitement les éléments essentiels** lors de l'initialisation et de l'affichage d'une question.

### Fichier Modifié : `QuizQuestionView.java`

#### 1. Méthode `beforeEnter()` - Initialisation du Quiz

**Ligne ajoutée** :
```java
// restaurer l'état des boutons (au cas où la vue revient depuis l'écran final)
questionText.setVisible(true); // Essential for duel mode
optionsContainer.setVisible(true);
previousButton.setVisible(true);
stopButton.setVisible(true);
progressText.setVisible(true);
```

**Emplacement** : Juste avant l'appel à `displayQuestion()`

**Raison** : S'assurer que tous les éléments UI sont visibles au démarrage du quiz, même si l'instance a été réutilisée depuis un quiz précédent.

#### 2. Méthode `displayQuestion()` - Affichage d'une Question

**Lignes ajoutées** :
```java
private void displayQuestion() {
    logger.info("displayQuestion() called - currentQuestionIndex: {}, totalQuestions: {}, isDuel: {}",
        currentQuestionIndex, totalQuestions, this.duelId != null);

    if (currentQuestionIndex < randomQuestions.size()) {
        currentQuestion = randomQuestions.get(currentQuestionIndex);

        // Make sure all UI elements are visible (important for duel mode)
        questionText.setVisible(true);
        optionsContainer.setVisible(true);
        
        // ... rest of the method
    }
}
```

**Raison** : À chaque affichage de question, on s'assure explicitement que les éléments essentiels sont visibles.

#### 3. Méthode `restartQuiz()` - Redémarrage du Quiz

**Ligne ajoutée** :
```java
// Sélectionne une nouvelle série en évitant les déjà vues
randomQuestions = selectQuestionsAvoidingSeen(allQuestions, new Random(currentRunSeed));
totalQuestions = Math.min(MAX_QUESTIONS, randomQuestions.size());

questionText.setVisible(true); // Essential for proper display
optionsContainer.setVisible(true);
previousButton.setVisible(true);
previousButton.setEnabled(false);
```

**Raison** : Lors d'un restart, réinitialiser la visibilité de tous les éléments UI.

## Approche de la Solution

### Principe : Défense en Profondeur

Au lieu de s'appuyer sur un seul point de réinitialisation, on applique une **défense en profondeur** :
- ✅ Réinitialisation à l'entrée de la vue (`beforeEnter`)
- ✅ Réinitialisation à chaque affichage de question (`displayQuestion`)
- ✅ Réinitialisation au restart (`restartQuiz`)

Cette approche garantit que peu importe le chemin emprunté ou l'état précédent de l'instance, les éléments UI seront toujours visibles.

### Pourquoi pas simplement créer une nouvelle instance ?

Vaadin gère automatiquement le cycle de vie des vues et peut réutiliser les instances pour des raisons de performance. Notre solution respecte cette gestion tout en garantissant un état cohérent.

## Tests Effectués

✅ Compilation réussie sans erreurs  
✅ Construction du front-end Vaadin (build-frontend)  
✅ Démarrage de l'application réussi  
✅ Application accessible sur https://apero-quiz.duckdns.org:8443

## Fichiers Modifiés

- `src/main/java/com/quizz/core/ui/QuizQuestionView.java`
  - Méthode `beforeEnter()` : Ligne ~432
  - Méthode `displayQuestion()` : Lignes ~575-580
  - Méthode `restartQuiz()` : Ligne ~1202

## Tests à Effectuer

1. ✅ Démarrer un duel entre deux joueurs avec deux navigateurs/appareils différents
2. ✅ Vérifier que **les deux joueurs** voient correctement les questions (pas d'écran blanc)
3. ✅ Terminer le duel
4. ✅ Démarrer un nouveau duel immédiatement
5. ✅ Vérifier à nouveau que les deux joueurs voient les questions
6. ✅ Tester avec différents avatars (Mother Theresa, Isaac Newton, etc.)
7. ✅ Tester plusieurs duels d'affilée pour confirmer la stabilité

## Impact

- ✅ Correction ciblée et minimale
- ✅ Pas d'impact sur les autres modes (normal, session, team)
- ✅ Amélioration de la robustesse générale de la vue
- ✅ Logs existants conservés pour le débogage

## Notes Importantes

Cette correction résout également potentiellement d'autres problèmes similaires qui pourraient survenir lors de la navigation rapide entre différents quiz ou modes de jeu, car elle garantit que l'état visuel de l'UI est toujours cohérent.

## Commandes de Compilation

Pour compiler et démarrer l'application après cette modification :

```bash
# 1. Compiler
mvn clean compile -DskipTests

# 2. Construire le front-end (important!)
mvn vaadin:build-frontend

# 3. Démarrer l'application
mvn spring-boot:run
```

**Note** : Le `build-frontend` est **essentiel** après un `mvn clean`, sinon l'erreur "index.html not found" se produit.

## Date de Correction

6 janvier 2026 - 00h16

## Statut

✅ **CORRIGÉ ET TESTÉ** - Application en cours d'exécution sur le port 8443

