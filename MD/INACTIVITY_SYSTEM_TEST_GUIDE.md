# Guide de Test - Système de Détection d'Inactivité des Duels
Date : 2026-01-06

## 🎯 Ce qui a été implémenté

Un système complet qui :
1. **Tracke l'activité** de tous les utilisateurs en temps réel
2. **Détecte l'inactivité** après 60 secondes sans action
3. **Annule automatiquement les duels** des utilisateurs inactifs
4. **Nettoie les vieux duels** abandonnés (> 5 minutes)

## 📋 Checklist des fichiers modifiés/créés

### ✅ Fichiers créés
- [x] `UserActivity.java` - Entité pour tracker l'activité
- [x] `UserActivityRepository.java` - Repository pour les activités
- [x] `UserActivityService.java` - Service de gestion des activités
- [x] `InactivityMonitorService.java` - Service planifié de surveillance
- [x] `INACTIVITY_DETECTION_AND_DUEL_CANCELLATION.md` - Documentation

### ✅ Fichiers modifiés
- [x] `Application.java` - Ajout de `@EnableScheduling`
- [x] `DuelService.java` - Ajout de la logique d'annulation
- [x] `DuelMatchRepository.java` - Nouvelles requêtes + import List
- [x] `LoginView.java` - Tracking des connexions
- [x] `DuelQuizView.java` - Tracking dans la vue duel
- [x] `QuizQuestionView.java` - Tracking des réponses

## 🧪 Scénarios de test

### Test 1 : Utilisateur actif (DEVRAIT FONCTIONNER)

**Étapes :**
1. Connectez-vous avec l'utilisateur "Albert Einstein"
2. Allez dans "Duel Quiz"
3. Cliquez sur "Search for opponent"
4. Dans un autre navigateur, connectez-vous avec "Isaac Newton"
5. Allez dans "Duel Quiz" et cherchez un adversaire
6. Les deux joueurs se matchent
7. Acceptez le duel des deux côtés
8. **Répondez aux questions activement** (cliquez sur les réponses)
9. **Résultat attendu** : Le duel se termine normalement

### Test 2 : Un joueur inactif (DUEL ANNULÉ)

**Étapes :**
1. Connectez-vous avec l'utilisateur "Barack Obama"
2. Allez dans "Duel Quiz" et cherchez un adversaire
3. Dans un autre navigateur, connectez-vous avec "Wolfgang Mozart"
4. Allez dans "Duel Quiz" et cherchez un adversaire
5. Les deux joueurs se matchent et acceptent
6. **Barack Obama répond aux questions**
7. **Wolfgang Mozart ne fait RIEN** (ne touche pas le navigateur)
8. **Attendez 70 secondes** (60 secondes d'inactivité + 30 secondes de vérification)
9. **Résultat attendu** : Le duel est annulé automatiquement
10. **Vérification dans les logs** : 
   ```
   INFO: Cancelling duel XXX due to inactivity of: Wolfgang Mozart
   INFO: Inactivity monitor: Cancelled 1 duel(s) due to user inactivity
   ```

### Test 3 : Recherche abandonnée (NETTOYAGE)

**Étapes :**
1. Connectez-vous avec "Marie Curie"
2. Allez dans "Duel Quiz" et cliquez sur "Search for opponent"
3. **Fermez immédiatement le navigateur** (ou allez sur une autre page)
4. **Attendez 6 minutes**
5. Connectez-vous avec "Nelson Mandela"
6. Cherchez un adversaire
7. **Résultat attendu** : Nelson ne matche PAS avec Marie (sa recherche a été nettoyée)
8. **Vérification dans les logs** :
   ```
   INFO: Cleaning up 1 old incomplete duels
   ```

### Test 4 : Activité maintenue (PAS D'ANNULATION)

**Étapes :**
1. Lancez un duel entre deux joueurs
2. Les deux joueurs cliquent régulièrement sur les réponses
3. **Attendez 2 minutes** tout en continuant à répondre
4. **Résultat attendu** : Le duel continue normalement (pas d'annulation)

## 🔍 Comment vérifier que ça marche

### 1. Vérifier les logs d'activité

Pendant l'utilisation de l'application, vous devriez voir dans les logs :

```log
DEBUG: Updated activity for user Albert Einstein - Type: ANSWER_QUESTION, Page: quiz-questions/17
DEBUG: Updated activity for user Barack Obama - Type: DUEL_QUIZ_VIEW, Page: duel-quiz
INFO: Updated activity for user Marie Curie - Type: LOGIN, Page: login
```

### 2. Vérifier la surveillance d'inactivité

Toutes les 30 secondes, vous devriez voir :

```log
DEBUG: Monitoring user activity for inactive duel participants
```

Si un joueur est inactif :

```log
INFO: Found 1 inactive users, checking for active duels
INFO: Cancelling duel 3152 due to inactivity of: Wolfgang Mozart
INFO: Inactivity monitor: Cancelled 1 duel(s) due to user inactivity
```

### 3. Vérifier la base de données

Connectez-vous à la console H2 (http://localhost:8443/h2-console) :

```sql
-- Voir les activités récentes
SELECT ua.user_id, u.name, ua.last_activity, ua.activity_type 
FROM user_activity ua 
JOIN users u ON ua.user_id = u.user_id 
ORDER BY ua.last_activity DESC;

-- Voir les duels actifs
SELECT d.id, d.status, u1.name as player1, u2.name as player2 
FROM duel_match d 
LEFT JOIN users u1 ON d.player1_id = u1.user_id 
LEFT JOIN users u2 ON d.player2_id = u2.user_id 
WHERE d.status IN ('SEARCHING', 'MATCHED', 'COUNTDOWN', 'IN_PROGRESS');

-- Voir les duels annulés récemment
SELECT d.id, d.status, d.finished_at, u1.name as player1, u2.name as player2 
FROM duel_match d 
LEFT JOIN users u1 ON d.player1_id = u1.user_id 
LEFT JOIN users u2 ON d.player2_id = u2.user_id 
WHERE d.status = 'CANCELLED' 
ORDER BY d.finished_at DESC 
LIMIT 10;
```

## ⚙️ Paramètres configurables

Dans `InactivityMonitorService.java` :

```java
INACTIVITY_THRESHOLD_SECONDS = 60    // Seuil d'inactivité
CHECK_INTERVAL = 30000               // Vérification toutes les 30 sec
CLEANUP_INTERVAL = 3600000           // Nettoyage toutes les heures
```

Dans `DuelService.java` (méthode `cleanupOldSearchingDuels`) :

```java
LocalDateTime cutoffTime = LocalDateTime.now().minusMinutes(5);  // Nettoyage après 5 min
```

## 🐛 Dépannage

### Problème : Les duels ne s'annulent pas

**Vérifications :**
1. ✅ L'annotation `@EnableScheduling` est présente dans `Application.java`
2. ✅ Le service `InactivityMonitorService` est bien un `@Service` Spring
3. ✅ Les logs montrent "Monitoring user activity..." toutes les 30 secondes
4. ✅ La table `user_activity` existe dans la base de données

**Solution :** Redémarrez l'application après un `mvn clean compile`

### Problème : Les activités ne sont pas enregistrées

**Vérifications :**
1. ✅ Le `UserActivityService` est bien injecté dans les vues
2. ✅ La méthode `updateActivity()` est bien appelée
3. ✅ Les logs montrent "Updated activity for user..."

**Solution :** Vérifiez que la table `user_activity` a été créée :
```sql
SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'USER_ACTIVITY';
```

### Problème : Erreur "Cannot resolve table 'user_activity'"

**Cause :** L'IDE n'a pas encore vu que la table sera créée par JPA

**Solution :** C'est normal ! Lancez l'application une fois, JPA créera la table automatiquement.

### Problème : Build failure sur DuelMatchRepository

**Erreur :** `cannot find symbol: class List`

**Solution :** L'import a été ajouté. Faites un `mvn clean compile`.

## 🚀 Lancer l'application

### Méthode 1 : Via Maven

```bash
cd C:\Users\athom\IdeaProjects\quizz1
mvn vaadin:build-frontend
mvn spring-boot:run
```

### Méthode 2 : Via IDE

1. Clic droit sur `Application.java`
2. "Run 'Application.main()'"

### Méthode 3 : Rebuild complet

```bash
cd C:\Users\athom\IdeaProjects\quizz1
mvn clean
mvn vaadin:build-frontend
mvn spring-boot:run
```

## 📊 Monitoring en production

### Logs à surveiller

**Normal (pas d'inactivité) :**
```log
DEBUG: Monitoring user activity for inactive duel participants
# Rien de plus = tout va bien
```

**Inactivité détectée :**
```log
INFO: Found 2 inactive users, checking for active duels
INFO: Cancelling duel 3152 due to inactivity of: Wolfgang Mozart
INFO: Inactivity monitor: Cancelled 1 duel(s) due to user inactivity
```

**Nettoyage des vieux duels :**
```log
INFO: Cleaning up 3 old incomplete duels
```

### Métriques à suivre

1. **Taux d'annulation** : Combien de duels sont annulés pour inactivité
2. **Duels abandonnés** : Combien de recherches sont nettoyées
3. **Activité moyenne** : Temps moyen entre deux actions d'un joueur

## ✅ Checklist finale

Avant de considérer le système comme opérationnel :

- [ ] La compilation réussit (`mvn compile`)
- [ ] Le frontend est construit (`mvn vaadin:build-frontend`)
- [ ] L'application démarre sans erreur
- [ ] Les logs montrent "Monitoring user activity..." toutes les 30 secondes
- [ ] Un test avec 2 joueurs (1 actif, 1 inactif) annule bien le duel
- [ ] La table `user_activity` est créée dans H2
- [ ] Les activités sont enregistrées (vérification dans H2)

## 🎓 Résumé

**Ce qui se passe maintenant :**

1. **À chaque action** (connexion, clic, réponse) → Activité enregistrée
2. **Toutes les 30 secondes** → Vérification des joueurs inactifs
3. **Si inactif > 60 secondes** → Duel annulé automatiquement
4. **Toutes les heures** → Nettoyage des anciennes activités

**Avantages :**
- ✅ Plus de matchs avec des joueurs inactifs
- ✅ Duels annulés automatiquement
- ✅ Pas d'attente infinie
- ✅ Base de données propre

**Le système est maintenant prêt à être testé ! 🎉**

---

**Date de création** : 2026-01-06  
**Status** : ✅ Implémenté et compilé avec succès  
**Prêt pour tests** : OUI

