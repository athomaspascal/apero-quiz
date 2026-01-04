# Ajout de logs de débogage pour la détection du maître de session ✅

**Date :** 2026-01-03  
**Fichier modifié :** `QuizQuestionView.java`

## 📋 Problème rapporté

Quand le maître de session termine son quiz, le bouton affiché est **"Start my quiz"** au lieu de **"Restart Session"**.

## 🔍 Analyse du problème

Le code vérifie si l'utilisateur actuel est le maître de la session avec cette condition :

```java
boolean isHost = currentUser != null && currentUser.getId() != null &&
                 session != null && currentUser.getId().equals(session.getHostUserId());
```

Si `isHost` est `true`, le bouton "Restart Session" devrait s'afficher.  
Si `isHost` est `false`, le bouton est caché.

### Causes possibles du problème

1. **`session.getHostUserId()` retourne `null`** - La session n'a pas d'hôte défini
2. **`currentUser.getId()` ne correspond pas à `session.getHostUserId()`** - Mauvais ID comparé
3. **La session n'est pas récupérée correctement** - `session` est `null`
4. **L'utilisateur n'est pas récupéré correctement** - `currentUser` est `null`

## 🔧 Solution appliquée : Logs de débogage

Pour identifier la cause exacte du problème, j'ai ajouté des logs de débogage détaillés dans la méthode `showFinalScore()` :

### Logs ajoutés

```java
// Check if current user is the host of the session
boolean isHost = currentUser != null && currentUser.getId() != null &&
                 session != null && currentUser.getId().equals(session.getHostUserId());

// Debug logs to troubleshoot isHost detection
logger.info("showFinalScore - Checking isHost: currentUser={}, currentUserId={}, session={}, sessionHostUserId={}, isHost={}", 
    currentUser != null ? currentUser.getName() : "null",
    currentUser != null ? currentUser.getId() : "null",
    session != null ? session.getSessionCode() : "null",
    session != null ? session.getHostUserId() : "null",
    isHost);

// Bouton "Restart Session" for host - resets the entire session
if (isHost) {
    logger.info("Host detected - showing Restart Session button");
    // ... code pour afficher le bouton
} else {
    // Invited participants can't start a new round - hide the button
    logger.info("Not host - hiding restart button");
    stopButton.setVisible(false);
}
```

## 📊 Informations affichées dans les logs

Quand le maître termine son quiz, les logs afficheront :

```
INFO  c.q.c.ui.QuizQuestionView - showFinalScore - Checking isHost: 
  currentUser=NomUtilisateur, 
  currentUserId=123, 
  session=ABC123, 
  sessionHostUserId=123, 
  isHost=true

INFO  c.q.c.ui.QuizQuestionView - Host detected - showing Restart Session button
```

Ou si le problème persiste :

```
INFO  c.q.c.ui.QuizQuestionView - showFinalScore - Checking isHost: 
  currentUser=NomUtilisateur, 
  currentUserId=123, 
  session=ABC123, 
  sessionHostUserId=null,      ← PROBLÈME ICI
  isHost=false

INFO  c.q.c.ui.QuizQuestionView - Not host - hiding restart button
```

## 🎯 Prochaines étapes

### 1. **Tester l'application**

Redémarrez l'application et faites terminer un quiz au maître de session. Vérifiez les logs dans la console ou dans le fichier `logs/application.log`.

### 2. **Analyser les logs**

Cherchez les lignes commençant par `showFinalScore - Checking isHost:` et vérifiez :
- ✅ `currentUser` n'est pas `null`
- ✅ `currentUserId` a une valeur (ex: `123`)
- ✅ `session` n'est pas `null`
- ✅ `sessionHostUserId` a une valeur (ex: `123`)
- ✅ `currentUserId` == `sessionHostUserId`
- ✅ `isHost=true`

### 3. **Scénarios possibles**

#### Scénario A : `sessionHostUserId` est `null`
**Cause** : La session n'a pas été créée correctement avec un `hostUserId`  
**Solution** : Vérifier le code de création de session dans `QuizSessionService` ou `QuizListView`

#### Scénario B : `currentUserId` ≠ `sessionHostUserId`
**Cause** : L'utilisateur actuel n'est pas celui qui a créé la session  
**Solution** : Vérifier que le bon utilisateur est connecté ou que la session est bien associée au bon hôte

#### Scénario C : `session` est `null`
**Cause** : Le code de session n'est pas trouvé ou la session a été supprimée  
**Solution** : Vérifier que `sessionCode` est correctement stocké dans `VaadinSession`

## 📝 Commande pour vérifier les logs

### Windows (PowerShell) :
```powershell
Get-Content C:\Users\athom\IdeaProjects\quizz1\logs\application.log -Tail 50 | Select-String "isHost"
```

### Ou directement dans le fichier :
Ouvrez `C:\Users\athom\IdeaProjects\quizz1\logs\application.log` et cherchez `"showFinalScore"`.

## 🔄 Une fois le problème identifié

Une fois que les logs révèlent la cause, nous pourrons :
1. Corriger le code de création de session si `hostUserId` est `null`
2. Corriger la comparaison si les IDs ne correspondent pas
3. Vérifier le stockage de session si `session` est `null`

---

**Statut :** 🔍 Logs ajoutés - En attente des résultats de test  
**Action requise :** Redémarrer l'application et faire terminer un quiz au maître  
**Fichier de log :** `logs/application.log`

