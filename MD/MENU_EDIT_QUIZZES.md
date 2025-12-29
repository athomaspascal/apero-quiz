# Menu "Edit the quizzes" - Configuration finale

## Date : 28 Décembre 2025

## ✅ Configuration complétée

Le menu "Edit the quizzes" a été ajouté au menu de gauche de l'application et est maintenant accessible uniquement aux administrateurs.

## Fichiers modifiés

### 1. QuizEditorView.java
**Chemin** : `src/main/java/com/quizz/core/ui/QuizEditorView.java`

```java
@Route(value = "admin/quiz-editor", layout = MainLayout.class)
@PageTitle("Edit the quizzes")
@RolesAllowed("ADMIN")
@Menu(order = 5, icon = "vaadin:edit", title = "Edit the quizzes")
public class QuizEditorView extends VerticalLayout {
```

**Annotations** :
- `@Route` : URL `/admin/quiz-editor`
- `@PageTitle` : Titre de la page "Edit the quizzes"
- `@RolesAllowed("ADMIN")` : Accessible uniquement aux administrateurs
- `@Menu` : Affichage dans le menu de gauche
  - `order = 5` : Position dans le menu (après les autres items)
  - `icon = "vaadin:edit"` : Icône d'édition
  - `title = "Edit the quizzes"` : Titre du menu

### 2. Traductions ajoutées

#### messages_en.properties
```properties
# Quiz Editor
Edit the quizzes=Edit the quizzes
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

#### messages_fr.properties
```properties
# Quiz Editor
Edit the quizzes=Éditer les quiz
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

## Structure du menu de gauche

L'application affiche maintenant les menus suivants (pour un administrateur) :

1. **Un Quizz** (Order 1) - Liste des quiz
2. **Users** (Order 2) - Gestion des utilisateurs
3. **Join Session** (Order 3) - Rejoindre une session
4. **Question Logs** (Order 3) - Logs des questions
5. **Edit the quizzes** (Order 5) - ✨ **NOUVEAU** - Éditer les quiz

## Accès et sécurité

### Qui peut accéder au menu ?
- ✅ **Administrateurs uniquement** (via `@RolesAllowed("ADMIN")`)
- ❌ Utilisateurs standards ne voient pas ce menu
- ❌ Utilisateurs non connectés ne peuvent pas accéder

### Comment accéder ?
1. **Via le menu** : Cliquer sur "Edit the quizzes" / "Éditer les quiz" dans le menu de gauche
2. **Via l'URL** : Naviguer vers `/admin/quiz-editor`

## Fonctionnalités disponibles

Une fois dans le menu "Edit the quizzes", l'administrateur peut :

1. **Sélectionner un quiz**
   - Liste déroulante avec tous les quiz (16 quiz disponibles)
   - 6297 questions totales éditables

2. **Naviguer entre les questions**
   - Bouton "Précédent" pour la question précédente
   - Bouton "Suivant" pour la question suivante
   - Affichage : "1 / 138 (ID: 1)"

3. **Visualiser les détails**
   - Question complète (lecture seule)
   - Options numérotées (lecture seule)
   - Réponse correcte (lecture seule)

4. **Éditer le niveau de difficulté**
   - Radio buttons avec 4 options : 1, 2, 3, 4
   - Modification immédiate visible

5. **Sauvegarder les modifications**
   - Bouton "Mettre à jour" / "Update"
   - Sauvegarde dans `quiz-questions.json`
   - Backup automatique créé
   - Mise à jour du champ `dateUpdate`

## Apparence dans le menu

### En anglais
```
┌─────────────────────────────┐
│ 📋 Un Quizz                 │
│ 👥 Users                    │
│ 👥 Join Session             │
│ 📊 Question Logs            │
│ ✏️  Edit the quizzes        │  ← NOUVEAU
└─────────────────────────────┘
```

### En français
```
┌─────────────────────────────┐
│ 📋 Un Quizz                 │
│ 👥 Users                    │
│ 👥 Join Session             │
│ 📊 Question Logs            │
│ ✏️  Éditer les quiz         │  ← NOUVEAU
└─────────────────────────────┘
```

## Icône utilisée

L'icône `vaadin:edit` affiche un crayon ✏️ pour symboliser l'édition.

## Compilation

✅ **BUILD SUCCESS**

```
[INFO] BUILD SUCCESS
[INFO] Total time:  17.367 s
[INFO] Finished at: 2025-12-28T23:50:59+01:00
```

## Test de la fonctionnalité

Pour tester le menu :

1. Démarrer l'application
2. Se connecter avec un compte administrateur
3. Observer le menu de gauche
4. Cliquer sur "Edit the quizzes" / "Éditer les quiz"
5. Vérifier que la page d'édition s'affiche
6. Sélectionner un quiz dans la liste
7. Naviguer entre les questions
8. Modifier un niveau de difficulté
9. Cliquer sur "Update" / "Mettre à jour"
10. Vérifier le backup créé dans le répertoire racine

## Résumé des modifications

| Élément | Avant | Après |
|---------|-------|-------|
| Menu de gauche | 4 items | 5 items (+ Edit the quizzes) |
| Accès édition | Non disponible | Via menu admin uniquement |
| Traductions | N/A | EN + FR ajoutées |
| PageTitle | "Quiz Editor" | "Edit the quizzes" |
| Import Menu | Incorrect | Corrigé (`com.vaadin.flow.router.Menu`) |

## Prochaines étapes

L'administrateur peut maintenant :
- ✅ Éditer facilement tous les quiz via le menu
- ✅ Mettre à jour les niveaux de difficulté
- ✅ Sauvegarder dans le fichier JSON
- ✅ Avoir des backups automatiques

La fonctionnalité est complète et prête à l'emploi !

