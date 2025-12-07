# Résumé des modifications apportées au projet Quiz

## Objectif
Lier les questions de quiz à des entités Quiz spécifiques, permettant à l'utilisateur de sélectionner un quiz avant de répondre aux questions.

## Modifications effectuées

### 1. **QuizQuestion** - Conversion en entité JPA
**Fichier**: `src/main/java/com/quizz/examplefeature/QuizQuestion.java`
- Converti de POJO simple en entité JPA
- Ajout de l'annotation `@Entity` et `@Table(name = "quiz_question")`
- Ajout d'une relation `@ManyToOne` vers l'entité `Quiz`
- Utilisation de `@ElementCollection` pour stocker la liste d'options
- Ajout des méthodes `equals()` et `hashCode()`

### 2. **QuizQuestionRepository** - Nouveau repository
**Fichier**: `src/main/java/com/quizz/examplefeature/QuizQuestionRepository.java` (NOUVEAU)
- Interface JPA Repository pour gérer les questions
- Méthode `findByQuizId(Long quizId)` pour récupérer les questions d'un quiz
- Méthode `countByQuizId(Long quizId)` pour compter les questions

### 3. **QuizQuestionService** - Refactorisation
**Fichier**: `src/main/java/com/quizz/examplefeature/QuizQuestionService.java`
- Remplacé la lecture du fichier JSON par l'accès à la base de données via le repository
- Nouvelles méthodes:
  - `getQuestionsByQuizId(Long quizId)` - Récupère toutes les questions d'un quiz
  - `getQuestionByQuizIdAndIndex(Long quizId, int index)` - Récupère une question spécifique
  - `getTotalQuestionsByQuizId(Long quizId)` - Compte les questions d'un quiz
  - `createQuestion(Quiz quiz, String question, List<String> options, String answer)` - Crée une nouvelle question

### 4. **QuizService** - Ajout de méthodes
**Fichier**: `src/main/java/com/quizz/examplefeature/QuizService.java`
- Modification de `createQuiz()` pour retourner l'entité Quiz créée
- Ajout de `getById(Long id)` pour récupérer un quiz par son ID

### 5. **QuizQuestionsData** - Mise à jour
**Fichier**: `src/main/java/com/quizz/examplefeature/QuizQuestionsData.java`
- Ajout d'une classe interne `QuestionData` pour mapper le JSON
- Cette classe est utilisée uniquement lors de l'initialisation des données

### 6. **QuizDataInitializer** - Nouveau composant
**Fichier**: `src/main/java/com/quizz/examplefeature/QuizDataInitializer.java` (NOUVEAU)
- Composant Spring avec `@PostConstruct` pour initialiser les données au démarrage
- Charge les questions du fichier `quiz-questions.json`
- Crée un quiz par défaut "General Knowledge Quiz"
- Insère toutes les questions dans la base de données
- Ne s'exécute que si aucun quiz n'existe déjà

### 7. **QuizListView** - Ajout du bouton "Play"
**Fichier**: `src/main/java/com/quizz/examplefeature/ui/QuizListView.java`
- Ajout d'une colonne "Action" dans la grille
- Bouton "Play" pour chaque quiz qui navigue vers `/quiz-questions/{quizId}`
- Le bouton utilise un thème SUCCESS et une taille SMALL

### 8. **QuizQuestionView** - Refactorisation majeure
**Fichier**: `src/main/java/com/quizz/examplefeature/ui/QuizQuestionView.java`
- **Route modifiée**: `@Route("quiz-questions/:quizId")` - Accepte maintenant un paramètre de route
- **Suppression de @Menu**: La vue n'est plus dans le menu principal
- **Implémentation de BeforeEnterObserver**: Validation et récupération du quizId depuis l'URL
- **Injection de QuizService**: Pour valider l'existence du quiz
- **Bouton "Next" désactivé par défaut**: S'active uniquement quand une réponse est sélectionnée
- **Listener sur RadioButtonGroup**: Active/désactive le bouton "Next" selon la sélection
- Toutes les méthodes utilisent maintenant `quizId` pour filtrer les questions

## Fonctionnement du flux

1. **Page d'accueil** (`/`) - QuizListView
   - Affiche la liste des quiz disponibles
   - Formulaire pour créer un nouveau quiz
   - Bouton "Play" pour chaque quiz

2. **Sélection d'un quiz**
   - Clic sur "Play" → Navigation vers `/quiz-questions/{quizId}`
   - Validation que le quiz existe, sinon redirection vers l'accueil

3. **Affichage des questions**
   - Les questions sont affichées une par une
   - Le bouton "Next" est désactivé tant qu'aucune réponse n'est sélectionnée
   - Feedback immédiat sur la justesse de la réponse
   - Navigation entre les questions avec "Previous" et "Next"

## Base de données

### Nouvelles tables créées automatiquement par JPA:
- **quiz_question**: Contient les questions (id, quiz_id, question, answer)
- **quiz_question_options**: Table de jointure pour les options (question_id, option_text, option_order)

### Relations:
- Quiz (1) → (N) QuizQuestion
- Une question appartient à un seul quiz
- Un quiz peut avoir plusieurs questions

## Points importants

### ✅ Fonctionnalités implémentées:
- Liaison questions ↔ quiz
- Sélection du quiz avant les questions
- Bouton "Next" conditionnel (activé uniquement si réponse sélectionnée)
- Initialisation automatique des données depuis JSON
- Navigation fluide entre les vues

### ⚠️ Prérequis:
- **Java 17+** requis (le projet est configuré pour Java 21)
- Si Maven utilise Java 11, l'application ne se compilera pas
- Solution: Configurer `JAVA_HOME` pour pointer vers Java 17 ou supérieur

### 🚀 Pour démarrer l'application:
```bash
# Vérifier la version de Java
java -version

# Si Java 17+ est installé, démarrer avec:
mvnw spring-boot:run

# Ou via IntelliJ IDEA: Exécuter la classe Application.java
```

## Fichiers JSON

Le fichier `src/main/resources/quiz-questions.json` contient 10 questions de culture générale qui sont automatiquement chargées au premier démarrage de l'application.

## Tests recommandés

1. ✅ Créer plusieurs quiz via l'interface
2. ✅ Cliquer sur "Play" pour chaque quiz
3. ✅ Vérifier que les questions correspondent au bon quiz
4. ✅ Vérifier que le bouton "Next" ne s'active qu'après sélection d'une réponse
5. ✅ Tester la navigation Previous/Next
6. ✅ Compléter un quiz jusqu'au message de fin

## Extensions possibles

- Ajouter un score/résultat à la fin du quiz
- Permettre d'ajouter des questions via l'interface
- Ajouter une fonctionnalité de modification/suppression de quiz
- Stocker les résultats des utilisateurs
- Ajouter des catégories de quiz
- Timer pour chaque question
- Mode multijoueur

