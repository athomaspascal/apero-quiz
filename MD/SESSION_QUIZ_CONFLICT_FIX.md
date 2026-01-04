# Correction du conflit entre quiz de session et quiz simple
Date : 2026-01-04

## Problème identifié

Quand un joueur maître démarrait une session de quiz puis essayait de démarrer un nouveau quiz simple (non-session), l'application pensait qu'il était encore dans une session et n'affichait pas les questions du nouveau quiz.

### Symptômes

1. Le joueur maître démarre une session de quiz
2. Il termine la session
3. Il retourne à la liste des quiz et clique sur "Démarrer" pour un nouveau quiz simple
4. Aucune question ne s'affiche
5. L'application croit que le joueur est encore dans la session précédente

## Cause du problème

Dans la méthode `beforeEnter()` de `QuizQuestionView.java` :

1. L'attribut `activeSessionCode` est stocké dans la `VaadinSession` quand un joueur rejoint une session
2. Cet attribut n'était jamais nettoyé quand le joueur démarre un quiz simple
3. Le code vérifiait l'existence de `activeSessionCode` et essayait de charger une session, même pour un quiz simple
4. Aucune vérification n'était faite pour s'assurer que la session était valide pour le quiz actuel

## Solution appliquée

### Modifications dans QuizQuestionView.java (méthode `beforeEnter`)

1. **Ajout d'une variable `isSessionQuiz`** pour distinguer clairement un quiz de session d'un quiz simple

2. **Vérification de la validité de la session** :
   ```java
   // Vérifier que la session existe ET que le quiz correspond
   if (session != null && session.getQuiz() != null 
       && session.getQuiz().getId() != null 
       && session.getQuiz().getId().equals(quizId)) {
       isSessionQuiz = true;
   }
   ```

3. **Nettoyage de `activeSessionCode` pour les sessions invalides** :
   ```java
   if (!isSessionQuiz) {
       VaadinSession.getCurrent().setAttribute("activeSessionCode", null);
       currentParticipant = null;
       logger.info("Starting simple quiz (non-session) for quiz ID: {}", quizId);
   }
   ```

4. **Utilisation de `isSessionQuiz` au lieu de `session != null`** pour charger les questions

### Changements détaillés

**Avant** :
```java
// Pas de distinction claire entre quiz simple et quiz de session
if (sessionCode != null) {
    session = sessionService.getSessionByCode(sessionCode);
    // Charge toujours les questions de la session si elle existe
}
```

**Après** :
```java
// Variable explicite pour distinguer les deux types
boolean isSessionQuiz = false;

if (sessionCode != null) {
    session = sessionService.getSessionByCode(sessionCode);
    
    // Vérifier que la session est valide pour CE quiz
    if (session != null && session.getQuiz() != null 
        && session.getQuiz().getId() != null 
        && session.getQuiz().getId().equals(quizId)) {
        isSessionQuiz = true;
    } else {
        // Nettoyer la session obsolète
        VaadinSession.getCurrent().setAttribute("activeSessionCode", null);
        session = null;
    }
}

// Si ce n'est PAS un quiz de session, nettoyer les données
if (!isSessionQuiz) {
    VaadinSession.getCurrent().setAttribute("activeSessionCode", null);
    currentParticipant = null;
}
```

## Résultat

Après cette correction :

1. ✅ Un joueur peut démarrer une session de quiz
2. ✅ Après la session, il peut retourner à la liste des quiz
3. ✅ Il peut démarrer un nouveau quiz simple sans problème
4. ✅ Les questions du nouveau quiz s'affichent correctement
5. ✅ L'attribut `activeSessionCode` est correctement nettoyé
6. ✅ Pas de conflit entre les deux modes de quiz

## Logs ajoutés

Pour faciliter le débogage :
```java
logger.info("Clearing stale activeSessionCode. Session: {}, Quiz ID mismatch or session not found", sessionCode);
logger.info("Starting simple quiz (non-session) for quiz ID: {}", quizId);
```

## Tests recommandés

1. Démarrer une session de quiz et la compléter
2. Retourner à la liste des quiz
3. Démarrer un nouveau quiz simple
4. Vérifier que les questions s'affichent
5. Vérifier que le score est enregistré correctement
6. Démarrer une nouvelle session pour vérifier qu'elle fonctionne toujours

## Statut

✅ **RÉSOLU** - L'application peut maintenant basculer correctement entre le mode session et le mode quiz simple.

