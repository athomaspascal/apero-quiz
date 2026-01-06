# Correction de l'Écran Blanc en Mode Duel - Tentative 2 - 2026-01-06

## Problème Persistant

Malgré la correction précédente, l'écran blanc en mode duel continue de se produire lors du démarrage d'un quiz duel.

## Nouvelles Corrections Appliquées

### Fichier Modifié : `QuizQuestionView.java`

#### 1. Visibilité Explicite du Conteneur Principal

**Problème détecté** : Le `content` VerticalLayout qui contient tous les éléments du quiz (timer, question, options, etc.) n'avait pas de visibilité explicitement définie.

**Solution** :
```java
VerticalLayout content = new VerticalLayout(
    timerContainer,
    questionText,
    optionsContainer,
    answerFeedback,
    buttonLayout,
    progressText
);
content.addClassNames(
    LumoUtility.Padding.LARGE,
    LumoUtility.MaxWidth.SCREEN_MEDIUM
);
content.setVisible(true); // Ensure content container is always visible
```

**Ligne modifiée** : ~260

#### 2. Logs de Débogage Améliorés

Pour faciliter le diagnostic, j'ai ajouté des logs détaillés à plusieurs points critiques :

**a) Début de `beforeEnter()`** :
```java
@Override
public void beforeEnter(BeforeEnterEvent event) {
    logger.info("=== QuizQuestionView.beforeEnter() CALLED ===");
    
    String quizIdParam = event.getRouteParameters().get("quizId").orElse(null);
    logger.info("QuizIdParam received: {}", quizIdParam);
    
    if (quizIdParam == null) {
        logger.warn("QuizIdParam is null, rerouting to home");
        event.rerouteTo("");
        return;
    }
```

**b) Après `displayQuestion()`** :
```java
displayQuestion();
logger.info("First question displayed successfully");
```

**c) Fin de `beforeEnter()`** :
```java
startTimer();
logger.info("=== QuizQuestionView.beforeEnter() COMPLETED SUCCESSFULLY ===");
```

**d) Gestion d'erreur** :
```java
} catch (NumberFormatException e) {
    logger.error("NumberFormatException in beforeEnter", e);
    event.rerouteTo("");
}
```

### Éléments de Visibilité Vérifiés

L'ordre de visibilité dans `beforeEnter()` est maintenant :
1. ✅ `questionText.setVisible(true)` - Ligne ~450
2. ✅ `optionsContainer.setVisible(true)` - Ligne ~451
3. ✅ `previousButton.setVisible(true)` - Ligne ~452
4. ✅ `stopButton.setVisible(true)` - Ligne ~453
5. ✅ `progressText.setVisible(true)` - Ligne ~454
6. ✅ `content.setVisible(true)` - Ligne ~261 (dans le constructeur)

### Éléments Également Réinitialisés dans `displayQuestion()`

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

## Diagnostic Attendu

Avec ces nouveaux logs, nous pourrons identifier précisément :
1. ✅ Si `beforeEnter()` est bien appelé
2. ✅ Quelle est la valeur de `quizIdParam`
3. ✅ Si `displayQuestion()` se termine correctement
4. ✅ Si `beforeEnter()` se termine complètement
5. ✅ S'il y a une exception quelque part

## Test à Effectuer

1. Démarrer un duel entre deux joueurs
2. Observer si l'écran blanc se produit
3. **Consulter immédiatement les logs** dans `logs/application.log`
4. Rechercher les lignes contenant :
   - `=== QuizQuestionView.beforeEnter() CALLED ===`
   - `QuizIdParam received:`
   - `DUEL MODE DETECTED`
   - `First question displayed successfully`
   - `=== QuizQuestionView.beforeEnter() COMPLETED SUCCESSFULLY ===`

## Hypothèses sur la Cause

### Hypothèse 1 : Conteneur Parent Caché
Le `content` VerticalLayout n'était pas explicitement rendu visible. Vaadin peut parfois rendre invisibles les composants dont la visibilité n'est pas explicitement définie.

### Hypothèse 2 : Exception Silencieuse
Une exception se produit dans `beforeEnter()` mais n'est pas loggée, causant un arrêt prématuré de l'initialisation.

### Hypothèse 3 : Timing de Vaadin
Le contenu est ajouté avant que Vaadin n'ait fini de préparer le composant parent, causant un problème de rendu.

## Commandes de Compilation Utilisées

```bash
# Arrêt de l'application
for /f "tokens=5" %a in ('netstat -aon ^| findstr :8443 ^| findstr LISTENING') do taskkill /F /PID %a

# Compilation
mvn compile -DskipTests

# Redémarrage
mvn spring-boot:run
```

## Prochaines Étapes

Si le problème persiste après cette correction :
1. **Analyser les logs** générés pour identifier le point d'échec exact
2. Vérifier si le problème est lié à un composant spécifique (timer, progress bar, etc.)
3. Envisager de simplifier temporairement la vue pour isoler le composant problématique
4. Vérifier la configuration Vaadin Push si le problème est lié à la mise à jour asynchrone

## Fichiers Modifiés

- `src/main/java/com/quizz/core/ui/QuizQuestionView.java`
  - Ligne ~261 : Ajout de `content.setVisible(true)`
  - Ligne ~291-295 : Logs de début de `beforeEnter()`
  - Ligne ~461-463 : Logs après `displayQuestion()` et `startTimer()`
  - Ligne ~465-468 : Gestion d'erreur améliorée

## Date de Correction

6 janvier 2026 - 00h34

## Statut

🔄 **EN TEST** - Application redémarrée avec logs de débogage améliorés. En attente de tests utilisateur pour valider la correction.

## URL de l'Application

https://apero-quiz.duckdns.org:8443

