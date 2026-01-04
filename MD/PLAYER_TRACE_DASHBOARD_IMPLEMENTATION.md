# Système de Traçabilité et Dashboard - Implémentation Complète
Date : 2026-01-04

## Vue d'ensemble

Un système complet de traçabilité des actions des joueurs a été implémenté avec un tableau de bord d'administration pour surveiller l'activité en temps réel.

## 📊 Entité PlayerTrace

### Structure de la table `player_trace`

| Champ | Type | Description |
|-------|------|-------------|
| id | Long | Identifiant unique |
| user_id | Long | Référence vers l'utilisateur |
| action_type | String(50) | Type d'action (LOGIN, START_QUIZ, COMPLETE_QUIZ, LOGOUT) |
| timestamp | LocalDateTime | Horodatage de l'action |
| quiz_id | Long | Référence vers le quiz (nullable) |
| quiz_mode | String(50) | Mode de quiz (NORMAL, TEAM, ...) - extensible |
| session_code | String(20) | Code de session si applicable |
| team_name | String(50) | Nom de l'équipe en mode équipe |
| score | Integer | Score obtenu (pour COMPLETE_QUIZ) |
| ip_address | String(50) | Adresse IP du joueur |
| user_agent | String(500) | User-Agent du navigateur |

### Types d'actions tracées

1. **LOGIN** - Connexion d'un joueur
2. **START_QUIZ** - Démarrage d'un quiz
3. **COMPLETE_QUIZ** - Fin d'un quiz
4. **LOGOUT** - Déconnexion (prévu pour usage futur)

### Extensibilité

Le champ `quiz_mode` est conçu pour être extensible :
- Actuellement : `NORMAL`, `TEAM`
- Facilement extensible pour de futurs modes : `SOLO`, `TOURNAMENT`, `CHALLENGE`, etc.

## 🔧 Services et Repository

### PlayerTraceRepository

Requêtes disponibles :
- `findByUserOrderByTimestampDesc()` - Historique d'un utilisateur
- `findByActionTypeOrderByTimestampDesc()` - Filtrage par type d'action
- `findByTimestampBetweenOrderByTimestampDesc()` - Filtrage par période
- `findActiveUsers()` - Utilisateurs actuellement connectés
- `countActiveUsers()` - Nombre d'utilisateurs actifs
- `findRecentQuizStarts()` - Derniers quiz démarrés
- `getQuizStatsByMode()` - Statistiques par mode de quiz
- `getMostPlayedQuizzes()` - Quiz les plus joués

### PlayerTraceService

Méthodes principales :
```java
// Enregistrement
recordLogin(User user)
recordLogout(User user)
recordQuizStart(User user, Quiz quiz, String quizMode, String sessionCode, String teamName)
recordQuizComplete(User user, Quiz quiz, String quizMode, Integer score, String sessionCode, String teamName)

// Consultation
getActiveUsers(int hoursAgo)
countActiveUsers(int hoursAgo)
getRecentQuizStarts(int hoursAgo)
getQuizStatsByMode(int hoursAgo)
getMostPlayedQuizzes(int hoursAgo, int limit)
```

## 📈 Dashboard d'Administration

### Accès

- **URL** : `/dashboard`
- **Accès** : Réservé aux administrateurs (`@RolesAllowed("ADMIN")`)
- **Menu** : Nouvel item "Dashboard" / "Tableau de Bord" / "Cruscotto"

### Fonctionnalités

#### 1. Sélecteur de période
- 1 heure
- 6 heures
- 12 heures
- 24 heures (par défaut)
- 48 heures
- 1 semaine (168 heures)

#### 2. Cartes statistiques

**Utilisateurs Actifs** 🟢
- Compte des utilisateurs connectés dans la période
- Icône : Users
- Couleur : Success (vert)

**Total Quiz** 🔵
- Nombre total de quiz démarrés
- Icône : Play
- Couleur : Primary (bleu)

**Mode Normal** ⚪
- Nombre de quiz en mode normal
- Icône : User
- Couleur : Contrast

**Mode Équipe** 🔴
- Nombre de quiz en mode équipe
- Icône : Group
- Couleur : Error (rouge)

**Quiz les Plus Joués** 📊
- Top 5 des quiz les plus populaires
- Affiche le nom et le nombre de parties

#### 3. Grille d'activité récente

Colonnes :
- **Horodatage** : Date et heure au format dd/MM/yyyy HH:mm:ss
- **Joueur** : Nom du joueur
- **Quiz** : Nom du quiz
- **Mode** : Badge coloré (NORMAL/TEAM)
- **Équipe** : Nom de l'équipe (si applicable)
- **Code Session** : Code de la session (si applicable)

### Rafraîchissement

- Bouton "Rafraîchir" manuel
- Changement automatique lors de la sélection d'une nouvelle période

## 🔗 Intégrations

### LoginView

**Points d'enregistrement** :
1. Connexion normale (email/mot de passe) → `recordLogin(user)`
2. Connexion avec avatar public → `recordLogin(user)`

### QuizQuestionView

**Points d'enregistrement** :

1. **Démarrage de quiz** (méthode `beforeEnter`) :
   ```java
   traceService.recordQuizStart(
       currentUser,
       quiz,
       quizMode,        // "NORMAL" ou "TEAM"
       sessionCode,     // Code de session ou null
       teamName         // Nom de l'équipe ou null
   );
   ```

2. **Fin de quiz** (méthode `showFinalScore`) :
   ```java
   traceService.recordQuizComplete(
       currentUser,
       currentQuiz,
       quizMode,
       correctAnswers,  // Score du joueur
       sessionCode,
       teamName
   );
   ```

## 🌍 Traductions

### Clés ajoutées

Toutes les langues (EN, FR, IT) :

```properties
# Menu
menu.dashboard=Dashboard / Tableau de Bord / Cruscotto

# Dashboard
dashboard.title=Dashboard / Tableau de Bord / Cruscotto
dashboard.timeRange=Time Range / Période / Periodo
dashboard.hours=hours / heures / ore
dashboard.day=day / jour / giorno
dashboard.days=days / jours / giorni
dashboard.activeUsers=Active Users / Utilisateurs Actifs / Utenti Attivi
dashboard.totalQuizzes=Total Quizzes / Total Quiz / Quiz Totali
dashboard.normalMode=Normal Mode / Mode Normal / Modalità Normale
dashboard.teamMode=Team Mode / Mode Équipe / Modalità Squadra
dashboard.mostPlayed=Most Played / Plus Joués / Più Giocati
dashboard.recentActivity=Recent Activity / Activité Récente / Attività Recente
dashboard.timestamp=Timestamp / Horodatage / Timestamp
dashboard.player=Player / Joueur / Giocatore
dashboard.quiz=Quiz / Quiz / Quiz
dashboard.mode=Mode / Mode / Modalità
dashboard.team=Team / Équipe / Squadra
dashboard.sessionCode=Session Code / Code Session / Codice Sessione
```

## 📊 Exemples d'utilisation

### Cas d'usage 1 : Surveiller l'activité en temps réel

L'administrateur ouvre le dashboard et sélectionne "1 heure" pour voir :
- 5 utilisateurs actifs
- 12 quiz démarrés (8 normaux, 4 en équipe)
- Top quiz : "Géographie" (5 parties), "Histoire de France" (3 parties)

### Cas d'usage 2 : Analyse hebdomadaire

L'administrateur sélectionne "1 semaine" pour analyser :
- 45 utilisateurs uniques
- 120 quiz joués
- Répartition : 70% mode normal, 30% mode équipe
- Quiz les plus populaires de la semaine

### Cas d'usage 3 : Débogage

Un joueur rapporte un problème. L'administrateur :
1. Va sur le dashboard
2. Filtre la grille par nom de joueur
3. Voit l'historique complet des actions
4. Identifie le problème (ex: démarrage de quiz mais pas de complétion)

## 🔮 Évolutions futures

### Possibilités d'extension

1. **Nouveaux modes de quiz** :
   - Mode SOLO (un joueur contre la montre)
   - Mode TOURNAMENT (élimination directe)
   - Mode CHALLENGE (défis entre joueurs)
   - → Il suffit d'ajouter le nouveau mode dans `quiz_mode`

2. **Nouvelles actions** :
   - JOIN_SESSION (rejoindre une session)
   - LEAVE_SESSION (quitter une session)
   - ANSWER_QUESTION (chaque réponse)
   - → Il suffit d'ajouter le nouveau type dans `action_type`

3. **Nouvelles statistiques** :
   - Temps moyen de quiz
   - Taux de réussite par quiz
   - Classement des joueurs
   - → Nouvelles requêtes dans le Repository

4. **Notifications** :
   - Alertes en temps réel pour l'admin
   - Détection d'activités suspectes
   - Rappels pour joueurs inactifs

5. **Export de données** :
   - Export CSV/Excel
   - Rapports PDF
   - Graphiques avancés

## 📝 Notes techniques

### Performance

- Les requêtes utilisent des index sur `timestamp` et `user_id`
- La période par défaut (24h) limite la charge
- Les statistiques sont calculées à la demande (pas de cache)

### Sécurité

- Dashboard accessible uniquement aux ADMIN
- Logs ne contiennent pas de données sensibles
- IP et User-Agent capturés mais non affichés par défaut

### Base de données

- La table `player_trace` sera créée automatiquement par JPA
- Aucune migration manuelle nécessaire
- Compatible H2 (dev) et autres SGBD (production)

## ✅ Statut

**IMPLÉMENTÉ ET FONCTIONNEL** - Le système de traçabilité est complet et le dashboard est prêt à l'emploi.

### Fichiers créés

1. `PlayerTrace.java` - Entité JPA
2. `PlayerTraceRepository.java` - Repository Spring Data
3. `PlayerTraceService.java` - Service métier
4. `DashboardView.java` - Vue d'administration

### Fichiers modifiés

1. `LoginView.java` - Ajout de l'enregistrement des connexions
2. `QuizQuestionView.java` - Ajout de l'enregistrement des quiz
3. `messages_en.properties` - Traductions anglaises
4. `messages_fr.properties` - Traductions françaises
5. `messages_it.properties` - Traductions italiennes

## 🚀 Démarrage

Après compilation :
1. L'application créera automatiquement la table `player_trace`
2. Les connexions seront automatiquement tracées
3. Les quiz seront automatiquement tracés
4. Les administrateurs pourront accéder au dashboard via `/dashboard`

Aucune configuration supplémentaire nécessaire ! 🎉

