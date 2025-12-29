# Éditeur de Quiz - Interface d'Administration

## Date de création : 28 Décembre 2025

## Vue d'ensemble

Une nouvelle interface d'administration a été créée pour permettre l'édition du niveau de difficulté de chaque question de quiz. Cette interface permet de :
- Sélectionner un quiz parmi tous les quiz disponibles
- Parcourir toutes les questions du quiz (avant/arrière)
- Visualiser les détails de chaque question dans un formulaire
- Modifier uniquement le niveau de difficulté (1, 2, 3 ou 4)
- Sauvegarder les modifications directement dans le fichier `quiz-questions.json`

## Fichiers créés

### 1. QuizJsonService.java
**Chemin** : `src/main/java/com/quizz/core/service/QuizJsonService.java`

Service pour gérer les opérations sur le fichier JSON :
- ✅ Lecture du fichier `quiz-questions.json`
- ✅ Support de `LocalDateTime` avec Jackson (JavaTimeModule)
- ✅ Mise à jour du niveau de difficulté d'une question
- ✅ Mise à jour automatique du champ `dateUpdate`
- ✅ Création automatique de backups avant chaque modification
- ✅ Sauvegarde formatée du JSON (pretty print)

**Méthodes principales** :
- `updateQuestionDifficultyLevel(quizName, questionId, difficultyLevel)` : Met à jour une question
- `loadQuizData()` : Charge toutes les données du JSON
- `getQuizQuestions(quizName)` : Récupère les questions d'un quiz spécifique

### 2. QuizEditorView.java
**Chemin** : `src/main/java/com/quizz/core/ui/QuizEditorView.java`

Interface utilisateur pour l'édition des questions :
- ✅ Accessible uniquement aux administrateurs (`@RolesAllowed("ADMIN")`)
- ✅ Route : `/admin/quiz-editor`
- ✅ Titre de page : "Quiz Editor"

**Composants UI** :
1. **ComboBox de sélection** : Liste déroulante de tous les quiz
2. **Formulaire de question** :
   - Numéro de question (lecture seule)
   - Texte de la question (lecture seule)
   - Options de réponse (lecture seule)
   - Réponse correcte (lecture seule)
   - Niveau de difficulté (éditable) - Radio buttons : 1, 2, 3, 4
3. **Boutons de navigation** :
   - Précédent : Passe à la question précédente
   - Suivant : Passe à la question suivante
4. **Bouton de mise à jour** : Sauvegarde le niveau de difficulté dans le JSON

## Traductions ajoutées

### Anglais (messages_en.properties)
```properties
Quiz Editor=Quiz Editor
Select Quiz=Select Quiz
Question Number=Question Number
Question=Question
Options=Options
Answer=Answer
Difficulty Level=Difficulty Level
Previous=Previous
Next=Next
Update JSON File=Update
```

### Français (messages_fr.properties)
```properties
Quiz Editor=Éditeur de Quiz
Select Quiz=Sélectionner un Quiz
Question Number=Numéro de Question
Question=Question
Options=Options
Answer=Réponse
Difficulty Level=Niveau de Difficulté
Previous=Précédent
Next=Suivant
Update JSON File=Mettre à jour
```

## Fonctionnalités

### Sélection du quiz
1. L'utilisateur voit une liste déroulante avec tous les quiz disponibles
2. À la sélection d'un quiz, toutes ses questions sont chargées
3. La première question est automatiquement affichée

### Navigation entre questions
- **Bouton "Précédent"** : Désactivé sur la première question
- **Bouton "Suivant"** : Désactivé sur la dernière question
- Le numéro de question affiche : `1 / 138 (ID: 1)` par exemple

### Affichage des questions
- **Question** : Texte complet de la question (lecture seule)
- **Options** : Liste numérotée des options (lecture seule)
  ```
  1. Option A
  2. Option B
  3. Option C
  4. Option D
  ```
- **Réponse** : La bonne réponse (lecture seule)
- **Niveau de difficulté** : Radio buttons pour choisir 1, 2, 3 ou 4

### Mise à jour
1. L'utilisateur modifie le niveau de difficulté avec les radio buttons
2. Clic sur le bouton "Mettre à jour"
3. Le fichier JSON est mis à jour avec :
   - Le nouveau niveau de difficulté
   - La date/heure actuelle dans `dateUpdate`
4. Un backup est créé automatiquement : `quiz-questions-backup-YYYYMMDD-HHMMSS.json`
5. Une notification de succès s'affiche

## Sécurité

- ✅ Accessible uniquement aux administrateurs (`@RolesAllowed("ADMIN")`)
- ✅ Seuls les champs éditables sont modifiables
- ✅ Backup automatique avant chaque modification
- ✅ Validation des données avant sauvegarde

## Gestion des erreurs

Le système affiche des notifications en cas de :
- ❌ Erreur de chargement du fichier JSON
- ❌ Quiz non trouvé
- ❌ Question non trouvée
- ❌ Erreur lors de la sauvegarde
- ✅ Succès de la mise à jour

## Exemple d'utilisation

1. **Connexion** : Se connecter avec un compte administrateur
2. **Navigation** : Aller sur `/admin/quiz-editor` ou cliquer sur "Quiz Editor" dans le menu
3. **Sélection** : Choisir "Game of Thrones - Complete" dans la liste
4. **Visualisation** : La question 1/138 s'affiche
5. **Édition** : Modifier le niveau de difficulté de 1 à 3
6. **Sauvegarde** : Cliquer sur "Mettre à jour"
7. **Navigation** : Cliquer sur "Suivant" pour passer à la question 2
8. **Répéter** : Continuer l'édition pour toutes les questions

## Modifications du fichier JSON

Avant :
```json
{
  "question": "Qui est connu comme le 'Roi de la Nuit' ?",
  "options": [...],
  "answer": "...",
  "id": 1,
  "uuid": "...",
  "difficulty_level": 1,
  "dateUpdate": "2025-12-28T23:15:36.505091"
}
```

Après mise à jour :
```json
{
  "question": "Qui est connu comme le 'Roi de la Nuit' ?",
  "options": [...],
  "answer": "...",
  "id": 1,
  "uuid": "...",
  "difficulty_level": 3,
  "dateUpdate": "2025-12-28T23:45:12.123456"
}
```

## Backups

Les backups sont créés automatiquement dans le répertoire racine du projet :
- Format : `quiz-questions-backup-20251228-234512.json`
- Contenu : Copie complète du fichier JSON avant modification
- Création : Avant chaque sauvegarde

## Compilation

✅ Le projet compile avec succès :
```
[INFO] BUILD SUCCESS
[INFO] Total time:  16.057 s
```

## Statistiques

- **Fichiers Java créés** : 2
- **Lignes de code ajoutées** : ~400
- **Traductions ajoutées** : 20 (10 × 2 langues)
- **Quiz supportés** : Tous (16 quiz disponibles)
- **Questions totales** : 6297

## Prochaines améliorations possibles

1. Édition en masse (plusieurs questions à la fois)
2. Filtrage des questions par niveau de difficulté
3. Statistiques sur les niveaux de difficulté
4. Prévisualisation des modifications avant sauvegarde
5. Historique des modifications
6. Édition d'autres champs (question, options, réponse)
7. Ajout/suppression de questions
8. Import/export de quiz

## Notes techniques

⚠️ **Important** : 
- Le service utilise le fichier dans `src/main/resources/` en développement
- En production, le fichier est lu depuis le classpath
- Les backups sont créés dans le répertoire courant de l'application
- Jackson nécessite le module `jackson-datatype-jsr310` pour `LocalDateTime`

