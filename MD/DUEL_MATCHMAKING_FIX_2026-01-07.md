# Fix pour le problème de matchmaking des duels - 2026-01-07

## Problème identifié

**Symptôme** : Marie Curie ne trouve pas Isaac Newton quand ils lancent tous les deux une recherche de duel.

**Diagnostic** :
1. Marie Curie lance une recherche à **00:33:42** → Crée le duel 14452 en statut SEARCHING
2. Isaac Newton lance une recherche à **00:33:44** → Trouve le duel 14452 et le passe en MATCHED
3. **Le problème** : Marie Curie ne reçoit **JAMAIS** de notification que le duel est passé en MATCHED

## Analyse des logs

### Logs de Marie Curie
```
2026-01-07 00:33:42.837 - User Marie Curie starting duel search
2026-01-07 00:33:42.860 - No opponent found, creating new searching duel for Marie Curie
2026-01-07 00:33:42.872 - Current duel status: SEARCHING, ID: 14452
2026-01-07 00:33:42.876 - Showing SEARCHING view
```

**Aucun log de DUEL_POLLING trouvé pour Marie Curie !**

### Logs d'Isaac Newton
```
2026-01-07 00:33:44.560 - User Isaac Newton starting duel search
2026-01-07 00:33:44.571 - Match found! Player1: Marie Curie, Player2: Isaac Newton, Quiz: Famous Manga Series
2026-01-07 00:33:44.575 - Current duel status: MATCHED, ID: 14452
2026-01-07 00:33:44.577 - Showing MATCHED view
```

Isaac Newton voit immédiatement la vue MATCHED, mais Marie Curie reste bloquée en SEARCHING.

## Cause racine

Le système de **polling** ne démarre pas correctement pour Marie Curie. Le polling devrait :
1. Vérifier toutes les 2 secondes si le statut du duel a changé
2. Appeler `updateView()` si le statut change de SEARCHING → MATCHED
3. Tracker l'activité avec `DUEL_POLLING`

**Pourquoi le polling ne fonctionne pas ?**

Plusieurs hypothèses :
1. L'executor n'est pas initialisé correctement dans `onAttach()`
2. `startPolling()` n'est pas appelé après `startSearching()`
3. Le polling task échoue silencieusement (exception non loggée)
4. Le `currentDuel` est null pendant le polling

## Solution implémentée

### 1. Ajout de logs détaillés dans `onAttach()`

```java
@Override
protected void onAttach(AttachEvent attachEvent) {
    super.onAttach(attachEvent);
    logger.info("=== onAttach() CALLED ===");
    
    User currentUser = VaadinSession.getCurrent().getAttribute(User.class);
    logger.info("Current user in onAttach: {}", currentUser != null ? currentUser.getName() : "null");
    
    logger.info("Creating executor with 2 threads");
    executor = Executors.newScheduledThreadPool(2);
    logger.info("Executor created successfully");
    
    if (currentDuel != null) {
        logger.info("View attached, updating view for active duel with ID: {}", currentDuel.getId());
        updateView();
    } else {
        logger.info("No active duel in onAttach");
    }
    
    logger.info("Calling startPolling()");
    startPolling();
    logger.info("=== onAttach() COMPLETED ===");
}
```

### 2. Ajout de vérifications et logs dans `startPolling()`

```java
private void startPolling() {
    logger.info("=== startPolling() CALLED ===");
    
    if (executor == null) {
        logger.error("EXECUTOR IS NULL! Cannot start polling. This should not happen after onAttach()");
        return;
    }
    
    if (pollingTask != null && !pollingTask.isDone()) {
        logger.info("Polling task already running, skipping");
        return;
    }
    
    logger.info("Starting polling task for currentDuel: {}", 
        currentDuel != null ? "ID=" + currentDuel.getId() : "null");
    
    pollingTask = executor.scheduleAtFixedRate(() -> {
        // Update user activity to keep them active while waiting
        User currentUser = VaadinSession.getCurrent().getAttribute(User.class);
        if (currentUser != null) {
            userActivityService.updateActivity(currentUser, "DUEL_POLLING", "duel-quiz");
        }
        
        if (currentDuel != null && currentDuel.getId() != null) {
            Optional<DuelMatch> updated = duelService.getDuelById(currentDuel.getId());
            if (updated.isPresent()) {
                DuelMatch oldStatus = currentDuel;
                currentDuel = updated.get();
                
                // Only update view if status changed
                if (oldStatus.getStatus() != currentDuel.getStatus() ||
                    (currentDuel.getStatus() == DuelMatch.DuelStatus.MATCHED && 
                     !oldStatus.isBothPlayersReady() && currentDuel.isBothPlayersReady())) {
                    logger.info("Duel status changed from {} to {}, updating view", 
                        oldStatus.getStatus(), currentDuel.getStatus());
                    updateView();
                }
            }
        }
    }, 1, 2, TimeUnit.SECONDS);
    
    logger.info("Polling task started successfully");
}
```

**Vérifications ajoutées** :
- ✅ Vérification que l'executor n'est pas null
- ✅ Log du démarrage du polling
- ✅ Log des changements de statut détectés
- ✅ Log de la confirmation que le polling démarre

### 3. Ajout de logs dans `startSearching()`

```java
private void startSearching() {
    logger.info("=== startSearching() CALLED ===");
    User currentUser = VaadinSession.getCurrent().getAttribute(User.class);
    logger.info("Current user starting search: {}", currentUser != null ? currentUser.getName() : "null");
    
    if (currentUser != null) {
        userActivityService.updateActivity(currentUser, "START_DUEL_SEARCH", "duel-quiz");
    }
    
    logger.info("Calling duelService.startSearching()");
    currentDuel = duelService.startSearching(currentUser);
    logger.info("Duel created/found: ID={}, Status={}", 
        currentDuel != null ? currentDuel.getId() : "null",
        currentDuel != null ? currentDuel.getStatus() : "null");
    
    lastConfirmationTime = LocalDateTime.now();
    logger.info("Starting waiting confirmation timer");
    startWaitingConfirmationTimer();
    
    logger.info("Calling updateView() from startSearching()");
    updateView();
    logger.info("=== startSearching() COMPLETED ===");
}
```

## Ce que les logs vont révéler

Avec ces nouveaux logs, nous pourrons identifier exactement où le problème se situe :

### Scénario 1 : L'executor est null
```
=== startPolling() CALLED ===
EXECUTOR IS NULL! Cannot start polling. This should not happen after onAttach()
```
→ **Solution** : Initialiser l'executor plus tôt

### Scénario 2 : Le polling démarre mais ne détecte pas le changement
```
=== startPolling() CALLED ===
Starting polling task for currentDuel: ID=14452
Polling task started successfully
[Pas de log "Duel status changed from SEARCHING to MATCHED"]
```
→ **Solution** : Vérifier la logique de comparaison des statuts

### Scénario 3 : Le polling ne démarre jamais
```
=== onAttach() CALLED ===
[...logs...]
[Pas de "=== startPolling() CALLED ==="]
```
→ **Solution** : `startPolling()` n'est pas appelé correctement

### Scénario 4 : currentDuel est null pendant le polling
```
Starting polling task for currentDuel: null
```
→ **Solution** : S'assurer que `currentDuel` est bien défini avant `startPolling()`

## Tests à effectuer

### Test 1 : Reproduction du problème
1. Démarrer l'application avec les nouveaux logs
2. Se connecter avec **Marie Curie**
3. Aller dans "Duel Quiz" et cliquer sur "Chercher un Adversaire"
4. Observer les logs :
   ```
   === startSearching() CALLED ===
   === onAttach() CALLED ===
   === startPolling() CALLED ===
   ```
5. Se connecter avec **Isaac Newton** (autre navigateur/session)
6. Aller dans "Duel Quiz" et cliquer sur "Chercher un Adversaire"
7. **Vérifier** : Marie Curie doit voir "Adversaire Trouvé !" automatiquement

### Test 2 : Vérification des logs de polling
Chercher dans les logs :
```bash
grep "DUEL_POLLING" application.log
grep "Duel status changed" application.log
```

Si on voit :
```
Updated activity for user Marie Curie - Type: DUEL_POLLING
Duel status changed from SEARCHING to MATCHED, updating view
```
→ ✅ Le polling fonctionne !

Si on ne voit rien :
→ ❌ Le polling ne démarre pas ou ne fonctionne pas

### Test 3 : Test de performance
Mesurer le temps entre :
- T1 : Isaac Newton lance la recherche
- T2 : Marie Curie voit "Adversaire Trouvé !"

**Temps attendu** : ≤ 2 secondes (fréquence du polling)

## Fichiers modifiés

- **DuelQuizView.java**
  - Méthode `onAttach()` : Logs détaillés
  - Méthode `startPolling()` : Vérification executor + logs
  - Méthode `startSearching()` : Logs détaillés

## Prochaines étapes

1. **Compiler le projet**
   ```bash
   mvn clean compile
   ```

2. **Reconstruire le frontend**
   ```bash
   mvn vaadin:build-frontend
   ```

3. **Démarrer l'application**
   ```bash
   mvn spring-boot:run
   ```

4. **Reproduire le problème** avec les deux utilisateurs

5. **Analyser les logs** dans `logs/application.log`

6. **Identifier la cause racine** grâce aux nouveaux logs

7. **Implémenter le fix définitif** selon ce qui est découvert

## Hypothèses sur le fix définitif

Selon ce que les logs révèleront, voici les solutions possibles :

### Si l'executor est null
```java
// Initialiser l'executor dans le constructeur au lieu de onAttach()
public DuelQuizView(...) {
    // ...
    this.executor = Executors.newScheduledThreadPool(2);
}
```

### Si le polling ne détecte pas les changements
```java
// Forcer un refresh de l'objet DuelMatch depuis la base de données
Optional<DuelMatch> updated = duelService.getDuelById(currentDuel.getId());
if (updated.isPresent()) {
    DuelMatch newDuel = updated.get();
    logger.info("Comparing: old={}, new={}", currentDuel.getStatus(), newDuel.getStatus());
    
    if (currentDuel.getStatus() != newDuel.getStatus()) {
        currentDuel = newDuel;
        updateView();
    }
}
```

### Si VaadinSession perd le contexte
```java
// Utiliser UI.access() pour garantir le contexte correct
pollingTask = executor.scheduleAtFixedRate(() -> {
    UI ui = getUI().orElse(null);
    if (ui != null) {
        ui.access(() -> {
            // ... code de polling ...
            ui.push();
        });
    }
}, 1, 2, TimeUnit.SECONDS);
```

---

**Date** : 2026-01-07  
**Status** : 🔍 Diagnostic en cours  
**Action** : Recompiler et tester avec les nouveaux logs pour identifier la cause racine

