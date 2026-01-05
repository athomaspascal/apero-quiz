# Fix du Démarrage Automatique du Quiz en Mode Duel

## Date
2026-01-05

## Problème
En mode duel, après le compte à rebours (countdown), le quiz sélectionné aléatoirement par l'application ne démarrait pas immédiatement. Le quiz devait être démarré manuellement par les joueurs.

## Solution Implémentée

### 1. Ajout de Logs de Traçage

#### Dans `DuelQuizView.java`
Ajout de logs détaillés pour tracer :
- Le quiz associé au duel lors du démarrage du countdown
- La fin du countdown et le démarrage du quiz
- Le statut du duel après le démarrage du quiz
- La navigation vers la vue du quiz

```java
logger.info("Starting countdown for duel {} with quiz: {}", 
    currentDuel.getId(), 
    currentDuel.getQuiz() != null ? currentDuel.getQuiz().getName() : "null");

logger.info("Countdown finished, starting quiz for duel {}", currentDuel.getId());

logger.info("Quiz started, status: {}, quiz: {}", 
    currentDuel.getStatus(), 
    currentDuel.getQuiz() != null ? currentDuel.getQuiz().getName() : "null");

logger.info("Navigating to quiz: {}, duelId: {}", 
    currentDuel.getQuiz().getId(), currentDuel.getId());
```

#### Dans `DuelService.java`
Ajout de logs pour tracer :
- Le quiz avant l'acceptation du match
- Le quiz lors du démarrage du countdown
- Le quiz lors du démarrage effectif du quiz
- Le statut après la sauvegarde

```java
logger.info("Duel {} - Quiz before accept: {}", duelId, 
    duel.getQuiz() != null ? duel.getQuiz().getName() : "null");

logger.info("Both players ready, starting countdown for duel {} with quiz: {}", 
    duelId, duel.getQuiz() != null ? duel.getQuiz().getName() : "null");

logger.info("Quiz to start: {}", duel.getQuiz() != null ? duel.getQuiz().getName() : "null");

logger.info("Duel {} status updated to IN_PROGRESS with quiz: {}", 
    saved.getId(), saved.getQuiz() != null ? saved.getQuiz().getName() : "null");
```

### 2. Fix du Lazy Loading JPA

#### Dans `DuelMatchRepository.java`
Le problème principal était que le quiz n'était pas chargé en raison du lazy loading de JPA. 
Ajout de `LEFT JOIN FETCH d.quiz` dans toutes les requêtes pour s'assurer que le quiz est toujours chargé avec le duel :

```java
@Query("SELECT d FROM DuelMatch d LEFT JOIN FETCH d.quiz WHERE d.status = 'SEARCHING' AND d.player1.id <> :userId ORDER BY d.createdAt ASC")
Optional<DuelMatch> findFirstSearchingMatch(Long userId);

@Query("SELECT d FROM DuelMatch d LEFT JOIN FETCH d.quiz WHERE (d.player1.id = :userId OR d.player2.id = :userId) " +
       "AND d.status IN ('SEARCHING', 'MATCHED', 'COUNTDOWN', 'IN_PROGRESS', 'REMATCH_PENDING')")
Optional<DuelMatch> findActiveDuelForUser(Long userId);

@Query("SELECT d FROM DuelMatch d LEFT JOIN FETCH d.quiz WHERE d.id = :duelId AND (d.player1.id = :userId OR d.player2.id = :userId)")
Optional<DuelMatch> findByIdAndUser(Long duelId, Long userId);

@Query("SELECT d FROM DuelMatch d LEFT JOIN FETCH d.quiz WHERE d.id = :id")
@NonNull
Optional<DuelMatch> findById(@NonNull Long id);
```

## Flux Complet du Mode Duel

1. **Recherche d'adversaire** : Le joueur clique sur "Duel Quiz" et commence la recherche
2. **Matching** : Quand un adversaire est trouvé, un quiz est sélectionné aléatoirement via `selectRandomQuiz()`
3. **Acceptation** : Les deux joueurs acceptent le duel
4. **Countdown** : Un compte à rebours de 5 secondes démarre
5. **Démarrage du quiz** : À la fin du countdown, le statut passe à `IN_PROGRESS`
6. **Navigation automatique** : Les deux joueurs sont automatiquement redirigés vers le quiz via :
   ```
   quiz-questions/{quizId}?duel={duelId}
   ```

## Fichiers Modifiés

1. `src/main/java/com/quizz/core/ui/DuelQuizView.java`
   - Ajout de logs de traçage
   
2. `src/main/java/com/quizz/core/service/DuelService.java`
   - Ajout de logs de traçage
   
3. `src/main/java/com/quizz/core/repository/DuelMatchRepository.java`
   - Ajout de `LEFT JOIN FETCH` pour charger le quiz
   - Override de `findById()` avec FETCH JOIN

## Tests Recommandés

1. Lancer l'application
2. Se connecter avec deux utilisateurs différents (ou deux navigateurs)
3. Les deux utilisateurs cliquent sur "Duel Quiz"
4. Les deux acceptent le match
5. Vérifier que :
   - Le quiz est bien affiché pendant le countdown
   - À la fin du countdown, les deux joueurs sont automatiquement redirigés vers le quiz
   - Le quiz démarre immédiatement sans action manuelle
   - Les logs montrent bien le nom du quiz à chaque étape

## Notes Techniques

- Le quiz est sélectionné aléatoirement parmi tous les quiz disponibles dans la base de données
- Le `LEFT JOIN FETCH` garantit que le quiz est toujours chargé, même en mode lazy loading
- Les logs permettent de tracer tout le flux et d'identifier rapidement tout problème
- La navigation utilise le paramètre `?duel={duelId}` pour que `QuizQuestionView` sache qu'il s'agit d'un quiz en mode duel

