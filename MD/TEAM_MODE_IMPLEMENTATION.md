# Mode Équipe - Guide d'Implémentation

## Vue d'ensemble

Le mode équipe a été ajouté à l'application Quiz pour permettre aux joueurs de jouer en équipes et d'agréger les scores par équipe.

## Fonctionnalités Implémentées

### 1. Configuration du Mode Équipe (Hôte)

Lorsqu'une session de quiz est créée et en statut WAITING, l'hôte peut :
- Activer le mode équipe via une checkbox "Mode Équipe"
- Sélectionner les équipes disponibles parmi 9 maisons de Game of Thrones :
  - Stark
  - Lannister
  - Targaryen
  - Baratheon
  - Tyrell
  - Martell
  - Arryn
  - Tully
  - Greyjoy

### 2. Sélection d'Équipe (Joueurs)

Lorsque le mode équipe est activé et qu'un joueur clique sur "Démarrer mon quiz" :
- Une boîte de dialogue s'ouvre pour sélectionner une équipe
- Le joueur peut choisir parmi les équipes sélectionnées par l'hôte
- Une fois l'équipe choisie, le joueur peut démarrer le quiz

### 3. Affichage des Participants

Dans la liste des participants :
- Le nom de chaque joueur est affiché
- Si le mode équipe est activé, l'équipe du joueur est affichée sous son nom
- Le statut (en cours / terminé avec score) est affiché

### 4. Classement par Équipe

Lorsque la session est terminée (COMPLETED) et que le mode équipe est activé :
- Un classement par équipe est affiché au lieu du classement individuel
- Les scores de tous les membres d'une équipe sont agrégés
- Pour chaque équipe, on affiche :
  - Le rang (🥇, 🥈, 🥉 ou numéro)
  - Le nom de l'équipe traduit
  - Le score total de l'équipe
  - La liste des membres avec leurs scores individuels

Si le mode équipe n'est pas activé, le classement individuel classique est affiché.

## Modifications de la Base de Données

### Table `quiz_session`
- `team_mode` (BOOLEAN) : Indique si le mode équipe est activé
- `selected_teams` (VARCHAR(500)) : Liste des équipes sélectionnées séparées par des virgules

### Table `quiz_participant`
- `team_name` (VARCHAR(100)) : Nom de l'équipe du participant

## Fichiers Modifiés

### Entités
1. `QuizSession.java` : Ajout des champs `teamMode` et `selectedTeams`
2. `QuizParticipant.java` : Ajout du champ `teamName`

### Service
3. `QuizSessionService.java` : 
   - Ajout de `updateParticipantTeam()` pour mettre à jour l'équipe d'un participant
   - Ajout de `getParticipant()` pour récupérer un participant spécifique

### Interface Utilisateur
4. `QuizSessionView.java` :
   - Ajout de la section mode équipe avec checkbox et sélection des équipes
   - Dialogue de sélection d'équipe pour les joueurs
   - Mise à jour de l'affichage des participants avec les équipes
   - Refonte du leaderboard pour supporter le mode équipe

### Traductions
5. `messages_fr.properties` : Traductions françaises
6. `messages_en.properties` : Traductions anglaises
7. `messages_it.properties` : Traductions italiennes

Nouvelles clés de traduction :
- `quizSession.teamMode` : Mode Équipe
- `quizSession.teamMode.enable` : Activer le mode équipe
- `quizSession.teamMode.selectTeams` : Sélectionnez les équipes
- `quizSession.teamMode.team.*` : Noms des équipes
- `quizSession.teamMode.selectTeam` : Sélectionnez votre équipe
- `quizSession.teamMode.selectTeamMessage` : Message d'instruction
- `quizSession.teamMode.confirmTeam` : Confirmer l'équipe
- `quizSession.teamMode.teamSelected` : Équipe sélectionnée
- `quizSession.leaderboard.teamTitle` : Titre du classement par équipe
- `quizSession.leaderboard.teamScore` : Score d'une équipe

## Script SQL

Le fichier `add_team_mode_columns.sql` contient les commandes SQL pour créer les nouvelles colonnes.

## Utilisation

1. **Démarrer l'application** : Les colonnes seront créées automatiquement par JPA si configuré en `update` ou `create`
2. **Alternative manuelle** : Exécuter le script SQL `add_team_mode_columns.sql`

3. **Pour l'hôte** :
   - Créer une session de quiz
   - Cocher "Activer le mode équipe"
   - Sélectionner les équipes disponibles
   - Démarrer la session

4. **Pour les joueurs** :
   - Rejoindre la session
   - Cliquer sur "Démarrer mon quiz"
   - Sélectionner une équipe dans le dialogue
   - Jouer au quiz

5. **Résultats** :
   - Les scores sont automatiquement agrégés par équipe
   - Le classement affiche les équipes avec leurs scores totaux
   - Les membres de chaque équipe sont listés sous le score de l'équipe

## Notes Techniques

- Le mode équipe ne peut être configuré que par l'hôte
- Les équipes ne peuvent être modifiées qu'avant le démarrage de la session (statut WAITING)
- Chaque joueur doit sélectionner une équipe avant de commencer le quiz en mode équipe
- Les scores individuels sont conservés et agrégés pour calculer le score d'équipe
- Le système supporte le changement d'équipe d'un joueur avant qu'il commence le quiz

## Améliorations Futures Possibles

- Permettre à l'hôte d'assigner automatiquement les joueurs aux équipes
- Ajouter des statistiques d'équipe plus détaillées
- Ajouter des badges ou des icônes pour chaque équipe
- Permettre la création d'équipes personnalisées (noms personnalisés)
- Ajouter un chat par équipe

