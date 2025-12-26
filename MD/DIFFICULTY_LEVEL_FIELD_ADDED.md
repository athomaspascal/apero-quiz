# Ajout du Champ difficulty_level à QuizQuestion ✅

**Date :** 26 décembre 2025  
**Statut :** ✅ TERMINÉ AVEC SUCCÈS

## Résumé

Un nouveau champ `difficulty_level` de type `Integer` a été ajouté à l'entité `QuizQuestion` pour permettre de classer les questions par niveau de difficulté.

## Modifications Effectuées

### Fichier Modifié
- **Emplacement :** `src/main/java/com/quizz/core/entity/QuizQuestion.java`

### 1. Ajout du Champ dans l'Entité

```java
@Column(name = "difficulty_level")
private Integer difficultyLevel;
```

**Caractéristiques :**
- Type : `Integer` (nullable)
- Colonne en base de données : `difficulty_level`
- Permet `null` (pas de contrainte `nullable = false`)

### 2. Mise à Jour des Constructeurs

#### Constructeur Original (maintenu pour la rétrocompatibilité)
```java
public QuizQuestion(Quiz quiz, String question, List<String> options, String answer) {
    this.quiz = quiz;
    this.question = question;
    this.options = options;
    this.answer = answer;
    this.difficultyLevel = null; // Default value
}
```

#### Nouveau Constructeur avec difficultyLevel
```java
public QuizQuestion(Quiz quiz, String question, List<String> options, String answer, Integer difficultyLevel) {
    this.quiz = quiz;
    this.question = question;
    this.options = options;
    this.answer = answer;
    this.difficultyLevel = difficultyLevel;
}
```

### 3. Ajout des Getters et Setters

```java
public Integer getDifficultyLevel() {
    return difficultyLevel;
}

public void setDifficultyLevel(Integer difficultyLevel) {
    this.difficultyLevel = difficultyLevel;
}
```

## Utilisation Possible

### Niveaux de Difficulté Suggérés

Le champ `Integer` peut être utilisé pour représenter différents niveaux de difficulté :

```java
// Exemples de niveaux
public static final Integer DIFFICULTY_EASY = 1;
public static final Integer DIFFICULTY_MEDIUM = 2;
public static final Integer DIFFICULTY_HARD = 3;
public static final Integer DIFFICULTY_EXPERT = 4;
public static final Integer DIFFICULTY_MASTER = 5;
```

### Exemples de Création de Questions

#### Question sans niveau de difficulté (valeur par défaut : null)
```java
QuizQuestion question = new QuizQuestion(
    quiz,
    "Quelle est la capitale de la France ?",
    Arrays.asList("Paris", "Londres", "Berlin", "Madrid"),
    "Paris"
);
```

#### Question avec niveau de difficulté
```java
QuizQuestion question = new QuizQuestion(
    quiz,
    "Quelle est la capitale de la France ?",
    Arrays.asList("Paris", "Londres", "Berlin", "Madrid"),
    "Paris",
    1  // Niveau facile
);
```

#### Modification du niveau de difficulté
```java
question.setDifficultyLevel(3); // Passer en niveau difficile
```

## Impact sur la Base de Données

### Migration SQL Nécessaire

Une migration de base de données sera nécessaire pour ajouter la nouvelle colonne :

```sql
-- Pour PostgreSQL, MySQL, MariaDB
ALTER TABLE quiz_question 
ADD COLUMN difficulty_level INTEGER NULL;

-- Pour H2
ALTER TABLE quiz_question 
ADD COLUMN difficulty_level INT NULL;
```

### Stratégie de Migration

1. **Valeurs Existantes :** Toutes les questions existantes auront `difficulty_level = NULL`
2. **Rétrocompatibilité :** Le constructeur original fonctionne toujours
3. **Nullable :** Le champ peut être `null`, donc pas de contrainte sur les données existantes

## Fonctionnalités Futures Possibles

### 1. Filtrage par Difficulté
```java
// Exemple de requête JPQL
@Query("SELECT q FROM QuizQuestion q WHERE q.quiz = :quiz AND q.difficultyLevel = :level")
List<QuizQuestion> findByQuizAndDifficultyLevel(Quiz quiz, Integer level);
```

### 2. Quiz Adaptatif
- Commencer avec des questions faciles
- Augmenter la difficulté si l'utilisateur répond correctement
- Diminuer si l'utilisateur fait des erreurs

### 3. Statistiques
- Taux de réussite par niveau de difficulté
- Temps moyen par niveau
- Progression de l'utilisateur

### 4. Interface Utilisateur
- Badge indiquant le niveau de difficulté (⭐ ⭐⭐ ⭐⭐⭐)
- Filtre pour choisir le niveau de quiz
- Système de points basé sur la difficulté

## Compilation

Le projet compile avec succès :

```
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  11.166 s
[INFO] Finished at: 2025-12-26T21:37:07+01:00
```

## Vérifications Effectuées

✅ **Champ ajouté** : `difficulty_level` de type `Integer`  
✅ **Annotation JPA** : `@Column(name = "difficulty_level")`  
✅ **Constructeurs** : 2 constructeurs (avec et sans difficultyLevel)  
✅ **Getters/Setters** : `getDifficultyLevel()` et `setDifficultyLevel()`  
✅ **Compilation** : Aucune erreur de compilation  
✅ **Rétrocompatibilité** : Code existant non impacté  

## Prochaines Étapes Recommandées

1. **Migration de Base de Données**
   - Créer un script Liquibase ou Flyway
   - Ajouter la colonne `difficulty_level` à la table `quiz_question`

2. **Mise à Jour du DataInitializer**
   - Ajouter des niveaux de difficulté aux questions existantes
   - Exemples :
     ```java
     new QuizQuestion(quiz, "Question facile", options, answer, 1);
     new QuizQuestion(quiz, "Question difficile", options, answer, 3);
     ```

3. **Mise à Jour de l'Interface Utilisateur**
   - Afficher le niveau de difficulté sur les cartes de quiz
   - Ajouter un filtre par niveau dans QuizListView
   - Afficher des badges visuels (★☆☆☆☆ pour niveau 1, etc.)

4. **Service de Sélection de Questions**
   - Créer une méthode pour sélectionner des questions par niveau
   - Implémenter un système de quiz adaptatif

5. **Tests**
   - Tester la création de questions avec et sans difficultyLevel
   - Tester les requêtes de filtrage par niveau
   - Tester la migration de base de données

## Structure de QuizQuestion après Modification

```java
@Entity
@Table(name = "quiz_question")
public class QuizQuestion {
    private Long id;                    // ID unique
    private Quiz quiz;                  // Quiz parent
    private String question;            // Texte de la question
    private List<String> options;       // Options de réponse
    private String answer;              // Réponse correcte
    private Integer difficultyLevel;    // ⭐ NOUVEAU : Niveau de difficulté
}
```

---

**Mission accomplie ! Le champ difficulty_level a été ajouté avec succès à l'entité QuizQuestion ! 🎉**

