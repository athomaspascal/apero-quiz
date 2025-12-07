# 🎯 Application Quiz - Quizz1

Application web de quiz interactif développée avec **Spring Boot** et **Vaadin**.

## 🚀 Démarrage rapide

**Pour démarrer l'application, consultez le fichier [DEMARRAGE_RAPIDE.md](DEMARRAGE_RAPIDE.md)**

La méthode recommandée est de lancer l'application depuis **IntelliJ IDEA** :
1. Ouvrir `src/main/java/com/quizz/Application.java`
2. Cliquer droit → **Run 'Application.main()'**
3. Accéder à http://localhost:8080

## ✨ Fonctionnalités

### 🔐 Authentification OAuth2
- ✅ Connexion avec Google
- ✅ Connexion avec Facebook
- ✅ Connexion avec LinkedIn
- ✅ Création automatique d'utilisateurs
- ✅ Liaison de comptes OAuth2 existants

### 👤 Gestion des Utilisateurs
- ✅ Entité User avec nom, email, téléphone, password
- ✅ Page de connexion classique (Sign-in)
- ✅ Page d'inscription (Sign-up)
- ✅ Mot de passe oublié
- ✅ Stockage sécurisé des mots de passe (BCrypt)

### 📝 Gestion des Quiz
- ✅ Créer des quiz avec un nom
- ✅ Lister tous les quiz disponibles
- ✅ Jouer à un quiz spécifique
- ✅ 8 quiz pré-chargés (General Knowledge, Second Quiz, Painting Quiz, etc.)
- ✅ Partage de sessions de quiz avec QR code
- ✅ Affichage des scores de tous les participants

### ❓ Système de Questions
- ✅ Questions liées à un quiz (relation ManyToOne)
- ✅ Affichage des questions une par une
- ✅ Choix multiples avec RadioButton colorés
- ✅ Questions chargées depuis JSON selon le nom du quiz
- ✅ Affichage du score final après la dernière question

### 🎮 Interface Utilisateur
- ✅ Navigation intuitive
- ✅ Bouton "Next" activé uniquement après sélection d'une réponse
- ✅ Feedback immédiat (✓ Correct / ✗ Incorrect)
- ✅ Navigation Previous/Next entre les questions
- ✅ Affichage de la progression (Question X sur Y)
- ✅ Boutons colorés pour les options de réponse

### 💾 Persistance
- ✅ Base de données H2 en mémoire
- ✅ JPA/Hibernate pour la gestion des entités
- ✅ Spring Data JPA pour les repositories
- ✅ Initialisation automatique des données de test

## 📂 Structure du projet

Les sources de Quizz1 ont la structure suivante:

```
src
├── main/
│   ├── frontend/
│   │   └── themes/default/
│   │       ├── styles.css
│   │       └── theme.json
│   ├── java/com/quizz/
│   │   ├── Application.java              # Point d'entrée Spring Boot
│   │   ├── base/ui/                      # Composants UI réutilisables
│   │   │   ├── component/ViewToolbar.java
│   │   │   └── MainLayout.java
│   │   └── examplefeature/
│   │       ├── ui/
│   │       │   ├── QuizListView.java     # Vue liste des quiz + création
│   │       │   └── QuizQuestionView.java # Vue affichage des questions
│   │       ├── Quiz.java                 # Entité Quiz
│   │       ├── QuizRepository.java       # Repository Quiz
│   │       ├── QuizService.java          # Service métier Quiz
│   │       ├── QuizQuestion.java         # Entité Question
│   │       ├── QuizQuestionRepository.java # Repository Questions
│   │       ├── QuizQuestionService.java  # Service métier Questions
│   │       ├── QuizQuestionsData.java    # DTO pour chargement JSON
│   │       ├── QuizDataInitializer.java  # Initialisation données
│   │       ├── Task.java                 # (exemple)
│   │       ├── TaskRepository.java       # (exemple)
│   │       └── TaskService.java          # (exemple)
│   └── resources/
│       ├── application.properties        # Configuration Spring
│       ├── quiz-questions.json           # 10 questions de test
│       └── META-INF/VAADIN/config/
│           └── flow-build-info.json      # Config Vaadin
└── test/java/
    └── com/quizz/examplefeature/
```

### 🎨 Architecture

#### Entités JPA
- **Quiz** : Représente un quiz avec un nom
- **QuizQuestion** : Représente une question liée à un quiz
  - Relation `@ManyToOne` vers Quiz
  - Liste d'options stockée avec `@ElementCollection`

#### Repositories (Spring Data JPA)
- **QuizRepository** : CRUD pour les quiz
- **QuizQuestionRepository** : CRUD pour les questions
  - Méthode `findByQuizId(Long)` pour récupérer les questions d'un quiz

#### Services
- **QuizService** : Logique métier des quiz
- **QuizQuestionService** : Logique métier des questions
- **QuizDataInitializer** : Chargement initial des données depuis JSON

#### Vues Vaadin
- **QuizListView** (`/`) : Page d'accueil avec liste et création de quiz
- **QuizQuestionView** (`/quiz-questions/:quizId`) : Interface de jeu du quiz

## 🗄️ Base de données

- **Type** : H2 (en mémoire)
- **Tables** :
  - `quiz` : id, name
  - `quiz_question` : id, quiz_id, question, answer
  - `quiz_question_options` : question_id, option_text, option_order

## 📖 Documentation complémentaire

- **[DEMARRAGE_RAPIDE.md](DEMARRAGE_RAPIDE.md)** : Guide pas-à-pas pour démarrer l'application
- **[MODIFICATIONS_SUMMARY.md](MODIFICATIONS_SUMMARY.md)** : Détail de toutes les modifications apportées
- **[SOLUTION_DEMARRAGE.md](SOLUTION_DEMARRAGE.md)** : Solutions aux problèmes de démarrage

## 🛠️ Technologies utilisées

- **Backend** : Spring Boot 3.5.8, Spring Data JPA
- **Frontend** : Vaadin 24.9.6
- **Base de données** : H2
- **Build** : Maven
- **Java** : 21 (minimum 17)

## 📝 Comment utiliser l'application

### 1. Créer un quiz
- Sur la page d'accueil, entrez un nom de quiz
- Cliquez sur "Create"

### 2. Jouer à un quiz
- Cliquez sur "Play" à côté d'un quiz
- Lisez la question
- Sélectionnez une réponse (le bouton "Next" s'active)
- Cliquez sur "Next" pour voir le feedback
- Continuez jusqu'à la fin du quiz

### 3. Données de test
Au premier démarrage, un quiz "General Knowledge Quiz" avec 10 questions est automatiquement créé.

## ⚙️ Configuration

### Configuration de base

Le fichier `application.properties` contient :
```properties
vaadin.frontend.hotdeploy=false
vaadin.productionMode=true
spring.jpa.hibernate.ddl-auto=update
```

### 🔐 Configuration OAuth2

**Pour configurer OAuth2 (Google, Facebook, LinkedIn), consultez le fichier [OAUTH2_CONFIGURATION.md](OAUTH2_CONFIGURATION.md)**

Étapes rapides :
1. Créer des applications OAuth2 sur Google Cloud Console, Facebook Developers, LinkedIn Developers
2. Copier les Client ID et Client Secret
3. Mettre à jour `src/main/resources/application.properties` avec vos identifiants
4. Démarrer l'application avec Java 21 :
   ```bash
   start-with-java21.bat
   ```

### Java 21

L'application nécessite **Java 21** (Azul Zulu 21.0.9) installé dans :
```
C:\Users\athom\.jdks\azul-21.0.9
```

Scripts disponibles :
- `compile-java21.bat` : Compiler le projet avec Java 21
- `start-with-java21.bat` : Démarrer l'application avec Java 21

## 🐛 Problèmes connus

### Maven avec Java 11
Si Maven utilise Java 11, la compilation échouera. **Solution** : Démarrer depuis IntelliJ IDEA.

### Mode développement Vaadin
Le serveur de dev Vaadin est désactivé (mode production). Pour le développement normal avec hot-reload, il faudrait Java 17+ configuré correctement dans Maven.

## 📚 Pour aller plus loin

### Fonctionnalités à ajouter
- [ ] Score et résultats sauvegardés
- [ ] Timer pour chaque question
- [ ] Catégories de quiz
- [ ] Ajout de questions via l'interface
- [ ] Modification/suppression de quiz
- [ ] Mode multijoueur
- [ ] Statistiques et graphiques

### Améliorations techniques
- [ ] Tests unitaires et d'intégration
- [ ] Migration vers une vraie base de données (PostgreSQL)
- [ ] Gestion des utilisateurs et authentification
- [ ] API REST pour les quiz
- [ ] Dockerisation

## 📄 Licence

Ce projet est un projet éducatif.

---

**Bon quiz ! 🎉**

To start the application in development mode, import it into your IDE and run the `Application` class. 
You can also start the application from the command line by running: 

```bash
./mvnw
```

## Building for Production

To build the application in production mode, run:

```bash
./mvnw -Pproduction package
```

To build a Docker image, run:

```bash
docker build -t my-application:latest .
```

If you use commercial components, pass the license key as a build secret:

```bash
docker build --secret id=proKey,src=$HOME/.vaadin/proKey .
```

## Getting Started

The [Getting Started](https://vaadin.com/docs/latest/getting-started) guide will quickly familiarize you with your new
Quizz1 implementation. You'll learn how to set up your development environment, understand the project 
structure, and find resources to help you add muscles to your skeleton — transforming it into a fully-featured 
application.
