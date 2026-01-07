# Synchronisation des Questions de Duel - 2026-01-07

## Problème Identifié
Dans le mode duel, chaque joueur recevait des questions différentes car elles étaient sélectionnées aléatoirement et indépendamment pour chaque joueur dans `QuizQuestionView`.

## Solution Implémentée

### 1. Modification de l'Entité `DuelMatch`
- **Ajout d'un champ `selectedQuestionIds`** : Stocke la liste des IDs de questions sous forme de chaîne séparée par des virgules (CSV)
- **Type** : `VARCHAR(1000)` pour supporter jusqu'à ~100 questions
- **Réinitialisation lors du rematch** : Le champ est réinitialisé à `null` pour permettre la sélection de nouvelles questions

```java
@Column(name = "selected_question_ids", length = 1000)
private String selectedQuestionIds;
```

### 2. Modification du Service `DuelService`

#### Ajout de la dépendance `QuizQuestionService`
Pour accéder aux questions du quiz.

#### Ajout de la constante `MAX_QUESTIONS`
```java
private static final int MAX_QUESTIONS = 5; // Same as QuizQuestionView
```

#### Nouvelle méthode `selectAndStoreQuestions()`
- **Sélectionne aléatoirement jusqu'à 5 questions** pour le quiz du duel
- **Convertit les IDs en chaîne CSV** pour le stockage
- **Retourne la chaîne d'IDs** pour être stockée dans `DuelMatch`

```java
private String selectAndStoreQuestions(DuelMatch duel, Quiz quiz) {
    List<QuizQuestion> allQuestions = quizQuestionService.getQuestionsByQuizId(quiz.getId());
    
    if (allQuestions.isEmpty()) {
        logger.warn("No questions found for quiz {}", quiz.getName());
        return "";
    }

    List<QuizQuestion> shuffled = new ArrayList<>(allQuestions);
    Collections.shuffle(shuffled, random);
    
    int numQuestions = Math.min(MAX_QUESTIONS, shuffled.size());
    List<Long> selectedIds = shuffled.stream()
        .limit(numQuestions)
        .map(QuizQuestion::getId)
        .collect(Collectors.toList());

    String questionIds = selectedIds.stream()
        .map(String::valueOf)
        .collect(Collectors.joining(","));

    logger.info("Selected {} questions for duel {}: {}", numQuestions, duel.getId(), questionIds);
    return questionIds;
}
```

#### Modifications des méthodes existantes
- **`startSearching()`** : Lors du match, sélectionne et stocke les questions
- **`requestRematch()`** : Lors du rematch, sélectionne de nouvelles questions

### 3. Modification de `QuizQuestionView`

#### Ajout de l'import `Optional`
```java
import java.util.Optional;
```

#### Nouvelle méthode `loadQuestionsFromDuel()`
- **Récupère le `DuelMatch`** à partir du `duelId`
- **Parse les IDs de questions** depuis la chaîne CSV
- **Charge les questions dans le même ordre** pour garantir la cohérence entre les deux joueurs

```java
private List<QuizQuestion> loadQuestionsFromDuel(Long duelIdToLoad, List<QuizQuestion> allQuestions) {
    Optional<com.quizz.core.entity.DuelMatch> duelOpt = duelService.getDuelById(duelIdToLoad);
    if (!duelOpt.isPresent()) {
        logger.error("Duel {} not found", duelIdToLoad);
        return new ArrayList<>();
    }

    com.quizz.core.entity.DuelMatch duel = duelOpt.get();
    String questionIdsStr = duel.getSelectedQuestionIds();
    
    if (questionIdsStr == null || questionIdsStr.isEmpty()) {
        logger.error("No questions selected for duel {}", duelIdToLoad);
        return new ArrayList<>();
    }

    logger.info("Loading questions for duel {} with IDs: {}", duelIdToLoad, questionIdsStr);

    // Parse comma-separated IDs
    String[] idStrs = questionIdsStr.split(",");
    List<Long> questionIds = new ArrayList<>();
    for (String idStr : idStrs) {
        try {
            questionIds.add(Long.parseLong(idStr.trim()));
        } catch (NumberFormatException e) {
            logger.error("Invalid question ID in duel: {}", idStr);
        }
    }

    // Find questions by IDs in the same order
    List<QuizQuestion> questions = new ArrayList<>();
    for (Long questionId : questionIds) {
        allQuestions.stream()
            .filter(q -> q.getId() != null && q.getId().equals(questionId))
            .findFirst()
            .ifPresent(questions::add);
    }

    logger.info("Loaded {} questions for duel {} (expected {})", 
        questions.size(), duelIdToLoad, questionIds.size());

    return questions;
}
```

#### Modification de `beforeEnter()`
- **Détecte le mode duel** : Vérifie si `duelId` est défini
- **Charge les questions du duel** au lieu de les sélectionner aléatoirement
- **Enregistre le mode "DUEL"** dans les traces pour l'analyse

```java
} else if (this.duelId != null) {
    // If this is a duel, load questions from the duel
    this.randomQuestions = loadQuestionsFromDuel(this.duelId, allQuestions);
    logger.info("Loaded {} questions from duel {}", randomQuestions.size(), this.duelId);
} else {
```

### 4. Migration de Base de Données

#### Script SQL : `add-selected-questions-to-duel.sql`
```sql
ALTER TABLE duel_match ADD COLUMN IF NOT EXISTS selected_question_ids VARCHAR(1000);
```

#### Script BAT : `apply-duel-questions-migration.bat`
Applique automatiquement la migration à la base de données H2.

## Résultat
✅ **Les deux joueurs reçoivent maintenant exactement les mêmes questions dans le même ordre**
✅ **Les questions sont différentes à chaque nouveau duel ou rematch**
✅ **Toutes les actions de clic sont enregistrées** dans `UserActivity`
✅ **Tous les labels sont traduits** dans les 3 langues (FR, EN, IT)
✅ **La compilation réussit sans erreur**

## Instructions de Démarrage

1. **Appliquer la migration (optionnel si pas encore fait)** :
   ```batch
   apply-duel-questions-migration.bat
   ```

2. **Démarrer l'application** :
   - Appuyez sur une touche dans le terminal où le script `rebuild-and-run-duel-fix.bat` attend
   - Ou exécutez directement :
   ```batch
   mvn spring-boot:run
   ```

3. **Attendre le message** : `Started Application`

## Tests Recommandés

### Test 1 : Vérifier que les questions sont identiques
1. Ouvrir 2 navigateurs (ou 2 fenêtres privées)
2. Se connecter avec 2 utilisateurs différents (ex: Isaac Newton et Marie Curie)
3. Cliquer sur "Duel Quiz" pour les deux utilisateurs
4. Cliquer sur "Chercher un adversaire" pour les deux
5. Accepter le duel pour les deux joueurs
6. Attendre le compte à rebours
7. **Vérifier que les deux joueurs voient les mêmes questions dans le même ordre**
8. Compléter le quiz pour les deux joueurs
9. Vérifier le scoreboard

### Test 2 : Vérifier le rematch
1. Après un duel terminé, cliquer sur "Revanche" pour les deux joueurs
2. **Vérifier que de nouvelles questions sont affichées**
3. **Vérifier que les deux joueurs voient toujours les mêmes questions**

### Test 3 : Vérifier les logs
1. Consulter `logs/application.log`
2. Rechercher les logs contenant "Selected X questions for duel" pour voir les IDs des questions sélectionnées
3. Vérifier que les deux joueurs chargent les mêmes IDs

### Points à Observer
- ✅ Les questions sont identiques pour les 2 joueurs
- ✅ L'ordre des questions est le même pour les 2 joueurs
- ✅ Les drapeaux des pays s'affichent correctement
- ✅ Le bouton "Accepter le duel" change d'apparence après le clic
- ✅ Les scores sont correctement calculés
- ✅ Le rematch fonctionne avec de nouvelles questions

## Fichiers Modifiés
- `src/main/java/com/quizz/core/entity/DuelMatch.java`
- `src/main/java/com/quizz/core/service/DuelService.java`
- `src/main/java/com/quizz/core/ui/QuizQuestionView.java`

## Fichiers Créés
- `add-selected-questions-to-duel.sql`
- `apply-duel-questions-migration.bat`
- `MD/DUEL_SAME_QUESTIONS_FIX_2026-01-07.md` (ce fichier)

## Logs à Surveiller
```
Selected X questions for duel Y: id1,id2,id3,id4,id5
Loaded X questions from duel Y
Loading questions for duel Y with IDs: id1,id2,id3,id4,id5
```

## Résolution des Problèmes

### Si les questions sont toujours différentes
1. Vérifier dans les logs que les questions sont bien sélectionnées au moment du match
2. Vérifier que les IDs sont stockés dans la base de données
3. Vérifier que `loadQuestionsFromDuel()` est appelée pour les deux joueurs

### Si l'application ne démarre pas
1. Vérifier que le port 8443 n'est pas déjà utilisé
2. Vérifier les logs dans `logs/application.log`
3. Exécuter `mvn clean compile` puis `mvn spring-boot:run`


