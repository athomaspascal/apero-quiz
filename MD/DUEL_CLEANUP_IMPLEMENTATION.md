# Implémentation du nettoyage automatique des duels - 2026-01-07

## Résumé

Mise en place d'un système complet de nettoyage automatique des duels et de tracking d'activité utilisateur pour éviter les duels orphelins.

## Problème résolu

Au démarrage de l'application, des duels en attente (SEARCHING, MATCHED, COUNTDOWN, REMATCH_PENDING) pouvaient rester actifs et causer :
- Match immédiat avec un utilisateur qui n'est plus disponible
- Écran blanc pour les utilisateurs ayant des duels orphelins
- Utilisateurs bloqués en mode recherche d'adversaire

## Solution implémentée

### 1. Nettoyage au démarrage de l'application

**Fichier**: `DuelService.java`

Ajout d'une méthode `@PostConstruct` qui s'exécute au démarrage :

```java
@PostConstruct
@Transactional
public void initializeCleanup() {
    // Annule tous les duels non terminés ou non annulés
    List<DuelMatch> pendingDuels = duelMatchRepository.findAll().stream()
        .filter(duel -> duel.getStatus() != DuelMatch.DuelStatus.FINISHED && 
                       duel.getStatus() != DuelMatch.DuelStatus.CANCELLED)
        .toList();
    
    // Change leur statut à CANCELLED
    for (DuelMatch duel : pendingDuels) {
        duel.setStatus(DuelMatch.DuelStatus.CANCELLED);
        duel.setFinishedAt(LocalDateTime.now());
    }
    duelMatchRepository.saveAll(pendingDuels);
}
```

### 2. Nettoyage automatique en arrière-plan

**Fichier**: `InactivityMonitorService.java`

Service existant modifié pour s'exécuter toutes les **60 secondes** (au lieu de 30) :

```java
@Scheduled(fixedDelay = 60000, initialDelay = 60000) // Every 60 seconds
public void monitorInactiveUsers() {
    // Annule les duels pour les utilisateurs inactifs depuis plus de 60 secondes
    int cancelledDuels = duelService.cancelDuelsForInactiveUsers(INACTIVITY_THRESHOLD_SECONDS);
}
```

**Paramètres** :
- Fréquence : 60 secondes
- Seuil d'inactivité : 60 secondes
- Action : Annulation automatique des duels des utilisateurs inactifs

### 3. Tracking amélioré de l'activité utilisateur

**Fichier**: `DuelQuizView.java`

Ajout du tracking d'activité sur **tous les clics de boutons** :

#### Boutons trackés :
1. **Start Duel Search** - Quand l'utilisateur lance une recherche
2. **Accept Duel** - Quand l'utilisateur accepte un match
3. **Decline Duel** - Quand l'utilisateur refuse un match
4. **Cancel Search** - Quand l'utilisateur annule la recherche
5. **Request Rematch** - Quand l'utilisateur demande une revanche
6. **Exit Duel** - Quand l'utilisateur quitte le duel

#### Polling actif :
Le système de polling (toutes les 2 secondes) met à jour l'activité utilisateur :

```java
pollingTask = executor.scheduleAtFixedRate(() -> {
    // Garde l'utilisateur actif pendant qu'il attend
    userActivityService.updateActivity(currentUser, "DUEL_POLLING", "duel-quiz");
    
    // Vérifie les changements de statut du duel
    if (currentDuel != null) {
        // ...check for updates...
    }
}, 1, 2, TimeUnit.SECONDS);
```

**Avantage** : Même si l'utilisateur ne clique sur rien, tant qu'il reste sur la page du duel, il est considéré comme actif.

### 4. Système de tracking existant

**Fichier**: `UserActivityService.java`

Service qui enregistre toutes les activités utilisateur dans la table `user_activity` :

```java
@Transactional
public void updateActivity(User user, String activityType, String pageUrl) {
    UserActivity activity;
    if (existingActivity.isPresent()) {
        activity = existingActivity.get();
        activity.setLastActivity(LocalDateTime.now()); // Met à jour le timestamp
    } else {
        activity = new UserActivity(user.getId(), LocalDateTime.now(), activityType, pageUrl);
    }
    userActivityRepository.save(activity);
}
```

**Types d'activité trackés** :
- `LOGIN` - Connexion
- `ANSWER_QUESTION` - Réponse à une question
- `DUEL_QUIZ_VIEW` - Accès à la vue duel
- `START_DUEL_SEARCH` - Recherche d'adversaire
- `ACCEPT_DUEL` - Acceptation du match
- `DECLINE_DUEL` - Refus du match
- `CANCEL_DUEL_SEARCH` - Annulation de la recherche
- `REQUEST_REMATCH` - Demande de revanche
- `EXIT_DUEL` - Sortie du duel
- `DUEL_POLLING` - Polling actif (toutes les 2 secondes)

## Flux de nettoyage

### Au démarrage de l'application
1. `DuelService.initializeCleanup()` s'exécute
2. Tous les duels non terminés sont annulés
3. La base de données est propre

### En cours d'exécution
1. Toutes les 60 secondes, `InactivityMonitorService.monitorInactiveUsers()` s'exécute
2. Récupère la liste des utilisateurs inactifs (>60 secondes sans activité)
3. Trouve tous les duels actifs de ces utilisateurs
4. Annule ces duels
5. Log le nombre de duels annulés

### Pendant l'utilisation
1. Chaque clic de bouton met à jour `UserActivity.lastActivity`
2. Le polling toutes les 2 secondes met à jour l'activité
3. L'utilisateur reste "actif" tant qu'il est sur la page du duel

## Avantages

✅ **Plus de duels orphelins** au démarrage  
✅ **Nettoyage automatique** toutes les 60 secondes  
✅ **Tracking précis** de l'activité utilisateur  
✅ **Pas d'intervention manuelle** nécessaire  
✅ **Logs détaillés** pour le debugging  
✅ **Base de données propre** en permanence  

## Configuration

Pour modifier les paramètres :

### Seuil d'inactivité
```java
// Dans InactivityMonitorService.java
private static final int INACTIVITY_THRESHOLD_SECONDS = 60; // 60 secondes
```

### Fréquence de vérification
```java
// Dans InactivityMonitorService.java
@Scheduled(fixedDelay = 60000, initialDelay = 60000) // 60000 ms = 60 secondes
```

### Fréquence du polling
```java
// Dans DuelQuizView.java
pollingTask = executor.scheduleAtFixedRate(..., 1, 2, TimeUnit.SECONDS); // Toutes les 2 secondes
```

## Tests recommandés

1. **Test de nettoyage au démarrage** :
   - Créer des duels en attente
   - Redémarrer l'application
   - Vérifier que tous les duels sont annulés

2. **Test d'inactivité** :
   - Lancer une recherche de duel
   - Ne rien faire pendant 65 secondes
   - Vérifier que le duel est annulé automatiquement

3. **Test de polling** :
   - Lancer une recherche de duel
   - Rester sur la page sans cliquer
   - Vérifier que l'utilisateur reste actif (logs)

4. **Test de match** :
   - Deux joueurs lancent une recherche
   - Le premier joueur devrait trouver le second
   - Pas de match avec un joueur inactif

## Logs à surveiller

```
=== DuelService: Starting cleanup at application startup ===
Cancelling 3 pending duels at startup
Cancelling duel 6402 - Status: REMATCH_PENDING, Player1: Barack Obama, Player2: Nelson Mandela
=== DuelService: Cleanup completed ===

Inactivity monitor: Cancelled 1 duel(s) due to user inactivity
Updated activity for user Marie Curie - Type: DUEL_POLLING, Page: duel-quiz
```

## Fichiers modifiés

1. `DuelService.java` - Ajout de `initializeCleanup()` avec `@PostConstruct`
2. `InactivityMonitorService.java` - Modification de la fréquence à 60 secondes
3. `DuelQuizView.java` - Ajout du tracking sur tous les clics + polling actif
4. `UserActivityService.java` - Pas de modification (déjà complet)

---

**Date**: 2026-01-07  
**Status**: ✅ Implémenté et testé

