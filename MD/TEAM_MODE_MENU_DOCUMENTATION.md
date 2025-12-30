# Nouveau Menu "Team Mode" - Documentation

## 📋 Vue d'ensemble

Un nouveau menu **"Team Mode"** a été créé pour faciliter le démarrage de quiz en mode équipe. Ce menu permet de :
- Sélectionner les équipes participant au jeu
- Choisir un quiz parmi tous les quiz disponibles
- Démarrer le quiz en mode partagé avec les équipes sélectionnées

## 🎯 Fonctionnalités

### 1. Sélection des équipes
- Interface avec checkboxes pour sélectionner les équipes Game of Thrones :
  - Stark, Lannister, Targaryen, Baratheon, Tyrell, Martell, Arryn, Tully, Greyjoy
- Au moins une équipe doit être sélectionnée pour activer le bouton de démarrage

### 2. Sélection du quiz
- Affichage de tous les quiz disponibles sous forme de cartes
- Interface identique à celle de QuizListView (code réutilisé)
- Sélection visuelle du quiz avec mise en surbrillance

### 3. Démarrage du quiz
- Bouton "Start Quiz (Shared)" qui :
  - Crée une session de quiz
  - Active automatiquement le mode équipe
  - Enregistre les équipes sélectionnées
  - Affiche le dialogue de partage avec QR code

## 📁 Fichiers créés/modifiés

### Nouveau fichier Java
- **`src/main/java/com/quizz/core/ui/TeamModeView.java`**
  - Nouvelle vue pour le menu Team Mode
  - Route : `/team-mode`
  - Ordre dans le menu : 2 (après "One Quiz")
  - Icône : `vaadin:users`

### Fichiers de traduction modifiés
- **`src/main/resources/messages.properties`** (par défaut)
- **`src/main/resources/messages_en.properties`** (anglais)
- **`src/main/resources/messages_fr.properties`** (français)
- **`src/main/resources/messages_it.properties`** (italien)

## 🌍 Traductions ajoutées

### Clés de traduction principales

#### Menu
- `menu.teammode` : Titre du menu

#### Titres et labels
- `teammode.title` : Titre de la page
- `teammode.selectTeams` : Titre de la section de sélection d'équipes
- `teammode.selectQuiz` : Titre de la section de sélection de quiz
- `teammode.startShared` : Label du bouton de démarrage

#### Messages
- `teammode.selectTeams.warning` : Avertissement si aucune équipe n'est sélectionnée
- `teammode.noQuizzes` : Message si aucun quiz n'est disponible
- `teammode.error.login` : Erreur si l'utilisateur n'est pas connecté
- `teammode.enabled` : Indication que le mode équipe est activé
- `teammode.selectedTeams` : Label pour afficher les équipes sélectionnées

#### Session (traductions complémentaires)
- `session.share` : Partager le quiz
- `session.scan` : Scanner le QR code
- `session.code` : Code
- `session.instructions` : Instructions de partage
- `session.goToRoom` : Aller à la salle de session
- `session.copyLink` : Copier le lien
- `session.close` : Fermer
- `session.linkCopied` : Lien copié

### Traductions par langue

#### Anglais (EN)
```
menu.teammode=Team Mode
teammode.title=Team Mode - Select Quiz
teammode.selectTeams=Select Teams for the Game
teammode.startShared=Start Quiz (Shared)
```

#### Français (FR)
```
menu.teammode=Mode Équipe
teammode.title=Mode Équipe - Sélection du Quiz
teammode.selectTeams=Sélectionner les Équipes pour la Partie
teammode.startShared=Démarrer le Quiz (Partagé)
```

#### Italien (IT)
```
menu.teammode=Modalità Squadra
teammode.title=Modalità Squadra - Selezione Quiz
teammode.selectTeams=Seleziona le Squadre per la Partita
teammode.startShared=Avvia Quiz (Condiviso)
```

## 🔧 Réutilisation du code

Le code de `TeamModeView` réutilise plusieurs méthodes de `QuizListView` :

### Méthodes réutilisées
1. **`createUserProfileSection()`** : Affichage du profil utilisateur avec avatar
2. **`getInitials()`** : Génération des initiales pour l'avatar
3. **`createQuizCard()`** : Création des cartes de quiz
4. **`loadQuizCards()`** : Chargement de tous les quiz
5. **`selectQuiz()`** : Sélection d'un quiz
6. **`showShareDialog()`** : Affichage du dialogue de partage (adapté pour Team Mode)
7. **`hideUsersMenuIfNotAdmin()`** : Masquage des menus admin

### Code factorisé
Le comportement est identique à celui de `QuizListView` avec la checkbox "Team Mode" cochée, mais l'interface est plus claire et dédiée au mode équipe.

## 🎨 Interface utilisateur

### Structure de la page
1. **En-tête** : Profil utilisateur avec avatar
2. **Toolbar** : Titre + Bouton "Start Quiz (Shared)"
3. **Section Équipes** : 
   - Titre "Select Teams for the Game"
   - Checkboxes pour les 9 équipes GoT
   - Fond coloré pour distinction visuelle
4. **Section Quiz** :
   - Titre "Select a Quiz"
   - Cartes de quiz disposées horizontalement avec wrapping
   - Effet hover et sélection visuelle

### Comportement
- Le bouton "Start Quiz (Shared)" n'est actif que si :
  - Un quiz est sélectionné
  - Au moins une équipe est sélectionnée
- La sélection d'une équipe met à jour l'état du bouton
- La sélection d'un quiz met en surbrillance la carte

## 🔄 Flux d'utilisation

1. L'utilisateur accède au menu "Team Mode"
2. Il sélectionne les équipes qui vont participer (au moins 1)
3. Il choisit un quiz en cliquant sur une carte
4. Il clique sur "Start Quiz (Shared)"
5. Un dialogue s'affiche avec :
   - Confirmation du mode équipe activé
   - Liste des équipes sélectionnées
   - QR code pour rejoindre la session
   - Code de session
   - Boutons d'action (Go to Room, Copy Link, Close)

## ✅ Avantages

1. **Interface dédiée** : Plus claire que la checkbox dans QuizListView
2. **Flux simplifié** : Sélection des équipes avant le quiz
3. **Code réutilisé** : Pas de duplication, maintenance facilitée
4. **Multilingue** : Toutes les traductions sont en place (EN, FR, IT)
5. **Cohérence** : Même look & feel que les autres vues

## 📝 Notes techniques

### Dépendances
- `QuizService` : Pour charger les quiz
- `QuizSessionService` : Pour créer et gérer les sessions
- `TranslationService` : Pour les traductions multilingues
- `QRCodeGenerator` : Pour générer le QR code de session

### Corrections appliquées
- Remplacement de `StreamResource` (deprecated) par l'encodage Base64 pour les images
- Utilisation de `setSrc()` au lieu des constructeurs deprecated de `Image`

### Sécurité
- Vérification de l'authentification utilisateur avant de créer une session
- Masquage des menus admin pour les utilisateurs non-admin

## 🚀 Prochaines étapes suggérées

1. Ajouter la possibilité de pré-sélectionner des équipes favorites
2. Permettre la création d'équipes personnalisées
3. Ajouter un historique des sessions Team Mode
4. Statistiques par équipe sur plusieurs sessions

## 📌 Résumé

Le nouveau menu "Team Mode" offre une expérience utilisateur optimisée pour les quiz en équipe, avec :
- ✅ Une interface claire et intuitive
- ✅ Toutes les traductions en place (EN, FR, IT)
- ✅ Réutilisation du code existant (pas de duplication)
- ✅ Comportement cohérent avec QuizListView
- ✅ Support complet du mode équipe Game of Thrones

Le menu est maintenant disponible dans le menu latéral, entre "One Quiz" et "Join Session".

