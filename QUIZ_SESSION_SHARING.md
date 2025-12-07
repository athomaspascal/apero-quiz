# Quiz Session Sharing - Documentation

## 🎯 Fonctionnalité : Sessions de Quiz Partagées

Cette fonctionnalité permet à plusieurs utilisateurs de participer au même quiz et de comparer leurs scores sur un leaderboard en temps réel.

## 📋 Composants Créés

### 1. Entités

#### QuizSession
- **Fichier**: `QuizSession.java`
- **Champs**:
  - `id` - Identifiant unique
  - `sessionCode` - Code de session unique (8 caractères)
  - `quiz` - Quiz associé
  - `createdAt` - Date de création
  - `status` - Statut (WAITING, ACTIVE, COMPLETED)
  - `hostUserId` - ID de l'hôte qui a créé la session

#### QuizParticipant
- **Fichier**: `QuizParticipant.java`
- **Champs**:
  - `id` - Identifiant unique
  - `session` - Session à laquelle le participant appartient
  - `user` - Utilisateur participant
  - `score` - Score obtenu
  - `completed` - Quiz terminé ou non

### 2. Repositories

- `QuizSessionRepository.java` - Gestion des sessions
- `QuizParticipantRepository.java` - Gestion des participants

### 3. Services

#### QuizSessionService
- `createSession()` - Crée une nouvelle session
- `getSessionByCode()` - Récupère une session par son code
- `joinSession()` - Ajoute un participant à une session
- `getParticipants()` - Liste les participants d'une session
- `updateParticipantScore()` - Met à jour le score d'un participant
- `updateSessionStatus()` - Change le statut de la session

### 4. Utilitaires

#### QRCodeGenerator
- **Fichier**: `util/QRCodeGenerator.java`
- Génère des QR codes pour les URLs de session
- Utilise la bibliothèque ZXing

### 5. Vues

#### QuizListView (modifié)
- **Bouton "Share"** ajouté dans la colonne Action
- Affiche un dialogue avec :
  - QR code à scanner
  - Code de session
  - Bouton pour copier le lien
  - Bouton pour aller à la salle de session

#### QuizSessionView
- **Route**: `/quiz-session/:sessionCode`
- **Fonctionnalités**:
  - Affiche les informations de la session
  - Liste les participants en temps réel
  - Bouton "Start Quiz for All" (pour l'hôte)
  - Bouton "Start My Quiz" (pour les participants)
  - Affichage du leaderboard en fin de session
  - Rafraîchissement des participants

#### JoinSessionView
- **Route**: `/join-session`
- **Menu**: "Join Session"
- Permet de rejoindre une session en entrant le code

#### QuizQuestionView (modifié)
- Enregistre automatiquement le score dans la session active
- Affiche un bouton "View Leaderboard" à la fin du quiz
- Redirige vers la session pour voir le classement

## 🔄 Flux d'Utilisation

### Pour l'Hôte (Créateur de Session)

1. **Créer une session**:
   - Aller sur la liste des quiz
   - Cliquer sur "Share" à côté d'un quiz
   - Un dialogue s'ouvre avec le QR code et le code de session

2. **Partager la session**:
   - Scanner le QR code avec les autres participants
   - OU partager le code de session manuellement
   - OU copier le lien direct

3. **Démarrer le quiz**:
   - Aller dans la salle de session
   - Attendre que les participants rejoignent
   - Cliquer sur "Start Quiz for All"

4. **Faire le quiz**:
   - Cliquer sur "Start My Quiz"
   - Répondre aux questions

5. **Voir les résultats**:
   - Le leaderboard s'affiche automatiquement
   - Classement avec médailles (🥇🥈🥉)
   - Scores de tous les participants

### Pour les Participants

1. **Rejoindre une session**:
   - **Option A**: Scanner le QR code avec un smartphone
   - **Option B**: Aller sur "Join Session" et entrer le code
   - **Option C**: Cliquer sur le lien partagé

2. **Attendre le démarrage**:
   - La salle de session affiche tous les participants
   - Attendre que l'hôte démarre le quiz

3. **Faire le quiz**:
   - Cliquer sur "Start My Quiz"
   - Répondre aux questions
   - Le score est enregistré automatiquement

4. **Voir le leaderboard**:
   - À la fin du quiz, cliquer sur "View Leaderboard"
   - Voir son classement et celui des autres

## 🎨 Interface Utilisateur

### Dialogue de Partage
```
┌─────────────────────────────────┐
│  Share Quiz: General Knowledge  │
├─────────────────────────────────┤
│  Scan QR Code to Join           │
│                                 │
│  ┌─────────────────────┐       │
│  │                     │       │
│  │     [QR CODE]       │       │
│  │                     │       │
│  └─────────────────────┘       │
│                                 │
│  ┌───────────────────┐         │
│  │ Code: ABC12345    │         │
│  └───────────────────┘         │
│                                 │
│  Share this code with others    │
│                                 │
│  [Go to Session] [Copy] [Close] │
└─────────────────────────────────┘
```

### Leaderboard Final
```
🏆 Final Leaderboard

┌──────────────────────────────┐
│ 🥇 Alice Smith    Score: 8   │
├──────────────────────────────┤
│ 🥈 Bob Jones      Score: 7   │
├──────────────────────────────┤
│ 🥉 Carol White    Score: 6   │
├──────────────────────────────┤
│ 4  David Brown    Score: 5   │
└──────────────────────────────┘
```

## 🛠️ Technologies Utilisées

- **ZXing** (version 3.5.3) - Génération de QR codes
- **JPA/Hibernate** - Persistance des données
- **Vaadin Flow** - Interface utilisateur
- **Spring Boot** - Framework backend

## 📦 Dépendances Ajoutées

```xml
<dependency>
    <groupId>com.google.zxing</groupId>
    <artifactId>core</artifactId>
    <version>3.5.3</version>
</dependency>
<dependency>
    <groupId>com.google.zxing</groupId>
    <artifactId>javase</artifactId>
    <version>3.5.3</version>
</dependency>
```

## 🔐 Sécurité

- Les sessions sont liées à un utilisateur hôte
- Seuls les utilisateurs connectés peuvent rejoindre une session
- Les codes de session sont uniques et générés aléatoirement
- Les scores sont enregistrés côté serveur (pas de manipulation client)

## 🚀 Démarrage Rapide

1. **Lancer l'application**:
   ```bash
   start-app.bat
   ```

2. **Se connecter**:
   - Email: `test@example.com`
   - Mot de passe: `password123`

3. **Créer une session**:
   - Aller sur "New Quiz"
   - Cliquer sur "Share" à côté d'un quiz
   - Partager le code ou le QR code

4. **Tester avec plusieurs utilisateurs**:
   - Ouvrir plusieurs navigateurs/onglets
   - Se connecter avec différents comptes
   - Rejoindre la même session
   - Comparer les scores !

## 📝 Notes Importantes

- Le leaderboard se met à jour uniquement quand les participants ont terminé leur quiz
- L'hôte peut démarrer le quiz même si personne n'a rejoint
- Les participants peuvent rejoindre à tout moment (même après le démarrage)
- Les sessions persistent en base de données (pas d'expiration automatique)
- Pour un environnement de production, remplacer `localhost:8080` par votre domaine

## 🎯 Améliorations Futures Possibles

- [ ] Rafraîchissement automatique du leaderboard (websockets)
- [ ] Minuteur pour les questions
- [ ] Mode compétition en temps réel
- [ ] Historique des sessions
- [ ] Statistiques détaillées par question
- [ ] Export des résultats en PDF
- [ ] Notifications push pour les participants
- [ ] Mode spectateur pour voir les réponses en direct

