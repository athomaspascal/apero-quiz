# Duel Quiz Blank Screen Fix - UI Thread Issue
Date: 2026-01-06

## Problème
Les joueurs recevaient une page blanche lors du démarrage d'un duel quiz. Les logs montraient l'erreur suivante :
```
ERROR: UI is not present! Cannot navigate.
UI is NULL! Cannot update view
```

## Cause
Le problème était causé par un accès incorrect à l'UI Vaadin dans un thread différent du thread UI principal. Lorsque le statut du duel passait à `IN_PROGRESS`, la méthode `navigateToQuiz()` était appelée directement depuis `updateView()` en dehors de `ui.access()`, ce qui causait des problèmes de thread safety.

## Solution
1. **Modification de `updateView()`** : 
   - Déplacer la récupération de l'UI avant de vérifier le statut `IN_PROGRESS`
   - Envelopper l'appel de navigation dans `ui.access()` pour tous les cas

2. **Modification de `navigateToQuiz()`** :
   - Renommer la méthode en `navigateToQuizInUIThread(UI ui)`
   - Passer l'UI comme paramètre au lieu d'essayer de la récupérer avec `getUI()`
   - Simplifier le code en utilisant directement `ui.navigate()` sans vérifications supplémentaires

## Code modifié

### Avant
```java
// Special case: IN_PROGRESS status requires navigation OUTSIDE of ui.access()
if (currentDuel.getStatus() == DuelStatus.IN_PROGRESS) {
    navigateToQuiz();
    return;
}

UI ui = getUI().orElse(null);
if (ui == null) {
    logger.error("UI is NULL!");
    return;
}
```

```java
private void navigateToQuiz() {
    getUI().ifPresent(ui -> {
        ui.navigate(QuizQuestionView.class, ...);
    });
    
    if (!getUI().isPresent()) {
        logger.error("ERROR: UI is not present!");
    }
}
```

### Après
```java
UI ui = getUI().orElse(null);
if (ui == null) {
    logger.error("UI is NULL!");
    return;
}

// Special case: IN_PROGRESS status requires navigation
if (currentDuel.getStatus() == DuelStatus.IN_PROGRESS) {
    ui.access(() -> {
        navigateToQuizInUIThread(ui);
    });
    return;
}
```

```java
private void navigateToQuizInUIThread(UI ui) {
    stopPolling();
    VaadinSession.getCurrent().setAttribute("activeDuelId", currentDuel.getId());
    ui.navigate(QuizQuestionView.class, 
        new RouteParameters("quizId", String.valueOf(currentDuel.getQuiz().getId())));
}
```

## Principe de Thread Safety avec Vaadin
- Toutes les modifications d'UI doivent être effectuées dans le thread UI
- Utiliser `ui.access(() -> { ... })` pour accéder à l'UI depuis un autre thread
- Ne jamais appeler `getUI()` depuis un thread externe (polling, scheduler, etc.)
- Toujours récupérer l'UI dans le thread principal, puis la passer aux méthodes appelées depuis `ui.access()`

## Fichiers modifiés
- `src/main/java/com/quizz/core/ui/DuelQuizView.java`

## Test
1. Démarrer l'application
2. Connecter deux joueurs différents
3. Les deux joueurs accèdent au menu "Duel Quiz"
4. Le système les match automatiquement
5. Les deux joueurs acceptent le duel
6. Après le countdown, les deux joueurs doivent voir les questions du quiz (pas de page blanche)

## Résultat attendu
Les deux joueurs voient correctement les questions du quiz et peuvent jouer normalement sans page blanche.

