# Résumé de la correction du quiz duel - 2026-01-05

## Problème initial
Lors du démarrage d'un quiz en mode duel, après le compte à rebours, les questions ne s'affichaient pas. Au lieu de cela, l'application affichait la liste des quiz (QuizListView) au lieu de la vue des questions (QuizQuestionView).

## Diagnostic
Les logs ont révélé que la navigation depuis un thread d'arrière-plan vers l'URL `quiz-questions/15?duel=1552` ne fonctionnait pas correctement avec Vaadin. La navigation se faisait depuis des threads du pool d'exécution (pool-2-thread-1, pool-3-thread-1) et Vaadin ne routait pas vers la bonne vue.

## Solution implémentée

### 1. Modification de DuelQuizView.java

**Changement principal** : Utilisation de RouteParameters et stockage du duelId dans la session Vaadin au lieu des paramètres de requête URL.

**Avant** :
```java
getUI().ifPresent(ui -> ui.navigate("quiz-questions/" + currentDuel.getQuiz().getId() + "?duel=" + currentDuel.getId()));
```

**Après** :
```java
VaadinSession.getCurrent().setAttribute("activeDuelId", currentDuel.getId());
getUI().ifPresent(ui -> {
    ui.navigate(QuizQuestionView.class, 
        new RouteParameters("quizId", String.valueOf(currentDuel.getQuiz().getId())));
});
```

**Import ajouté** : `import com.vaadin.flow.router.RouteParameters;`

### 2. Modification de QuizQuestionView.java

**Changement principal** : Récupération du duelId depuis la session Vaadin au lieu des paramètres de requête.

**Avant** :
```java
String duelIdParam = event.getLocation().getQueryParameters().getParameters()
    .getOrDefault("duel", List.of()).stream().findFirst().orElse(null);
if (duelIdParam != null) {
    this.duelId = Long.parseLong(duelIdParam);
    logger.info("Starting duel quiz with duel ID: {}", this.duelId);
}
```

**Après** :
```java
Object duelIdAttr = VaadinSession.getCurrent().getAttribute("activeDuelId");
if (duelIdAttr != null) {
    this.duelId = (Long) duelIdAttr;
    logger.info("*** DUEL MODE DETECTED *** Starting duel quiz with duel ID: {}", this.duelId);
    VaadinSession.getCurrent().setAttribute("activeDuelId", null);
} else {
    logger.info("Starting quiz in NORMAL mode (not a duel)");
}
```

### 3. Ajout de logs de débogage

Plusieurs logs ont été ajoutés pour faciliter le suivi :
- Détection du mode duel avec "*** DUEL MODE DETECTED ***"
- Log après chargement du quiz avec indication isDuel
- Log avant affichage de la première question
- Log au début de displayQuestion()

## Scripts créés

### stop-app-8443.bat
Script batch pour arrêter proprement les applications écoutant sur le port 8443 :
```batch
scripts\stop-app-8443.bat          # Arrêter uniquement
scripts\stop-app-8443.bat restart  # Arrêter et redémarrer
```

## Fichiers modifiés
1. `src/main/java/com/quizz/core/ui/DuelQuizView.java`
2. `src/main/java/com/quizz/core/ui/QuizQuestionView.java`

## Fichiers créés
1. `MD/DUEL_QUIZ_AUTO_START_FIX.md` - Documentation détaillée de la correction
2. `scripts/stop-app-8443.bat` - Script pour arrêter/redémarrer l'application

## État actuel
✅ L'application a été recompilée avec succès
✅ L'application a été redémarrée et fonctionne sur le port 8443
✅ Les modifications sont prêtes à être testées

## Tests à effectuer
1. Se connecter avec deux utilisateurs différents
2. Lancer un duel quiz depuis le menu "Duel Quiz"
3. Accepter le match des deux côtés
4. Vérifier que le compte à rebours démarre
5. **Vérifier que les questions s'affichent immédiatement après le compte à rebours**
6. Compléter le quiz et vérifier que les scores sont bien enregistrés

## Accès à l'application
- URL : https://apero-quiz.duckdns.org:8443
- URL locale : https://192.168.1.138:8443

## Notes importantes
- La session Vaadin est utilisée pour transférer le duelId entre les vues
- L'attribut "activeDuelId" est nettoyé immédiatement après utilisation
- La navigation utilise maintenant RouteParameters au lieu d'URLs string
- Les logs permettent de tracer précisément le mode (DUEL ou NORMAL)

## Prochaines étapes
Si le problème persiste après ces modifications, vérifier :
1. Les logs pour confirmer que "*** DUEL MODE DETECTED ***" apparaît
2. Que displayQuestion() est bien appelé
3. Que les questions sont bien chargées (totalQuestions > 0)

