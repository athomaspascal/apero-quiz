# Quiz Questions JSON Schema

Ce document décrit le schéma JSON utilisé pour valider les fichiers de quiz.

## Fichiers

- **quiz-questions-schema.json** : Le schéma JSON qui définit la structure valide
- **validate_quiz_json.py** : Script Python pour valider le fichier quiz-questions.json

## Structure du Schéma

### Niveau racine
```json
{
  "quizzes": [...]  // Array de quiz (obligatoire)
}
```

### Structure d'un Quiz
```json
{
  "name": "Nom du quiz",                    // String (obligatoire)
  "imageFileName": "image.svg",             // String avec extension .svg, .png, .jpg, .jpeg (obligatoire)
  "questions": [...]                        // Array de questions (obligatoire, min 1)
}
```

### Structure d'une Question
```json
{
  "id": 1,                                  // Integer >= 1 (obligatoire, ordre séquentiel)
  "uuid": "59c67574-8dfc-4a5a-9d19-4590b7a36d2a",  // String UUID v4 (obligatoire, unique)
  "question": "Quelle est la capitale de la France ?",  // String (obligatoire)
  "difficulty_level": 1,                    // Integer 1-10 (obligatoire, défaut: 1)
  "options": [                              // Array de strings (obligatoire, min 2, max 10)
    "Paris",
    "Londres",
    "Berlin",
    "Madrid"
  ],
  "answer": "Paris"                         // String (obligatoire, doit être dans options)
}
```

## Règles de Validation

### Validation du Schéma
1. **quizzes** : Doit être un array avec au moins 1 quiz
2. **name** : Doit être un string non vide
3. **imageFileName** : Doit avoir une extension valide (.svg, .png, .jpg, .jpeg)
4. **questions** : Doit être un array avec au moins 1 question
5. **id** : Doit être un entier >= 1 (ordre séquentiel dans le quiz)
6. **uuid** : Doit respecter le format UUID v4 : `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`
7. **question** : Doit être un string non vide
8. **difficulty_level** : Doit être un entier entre 1 et 10
9. **options** : Doit contenir entre 2 et 10 options uniques
10. **answer** : Doit être exactement l'une des options

### Validations Additionnelles
1. **Answer in Options** : Vérifie que chaque réponse est bien présente dans les options
2. **UUID Uniqueness** : Vérifie que tous les UUIDs sont uniques dans tous les quiz

## Utilisation

### Valider le fichier quiz-questions.json
```bash
python validate_quiz_json.py
```

Le script va :
1. Valider la structure JSON contre le schéma
2. Vérifier que les réponses sont dans les options
3. Vérifier l'unicité des UUIDs
4. Afficher des statistiques (nombre de quiz, nombre de questions)
5. Lister tous les quiz avec leurs caractéristiques

### Exemple de sortie
```
================================================================================
QUIZ JSON VALIDATION
================================================================================

Validating: quiz-questions.json
Using schema: quiz-questions-schema.json
--------------------------------------------------------------------------------
✓ Schema loaded successfully
✓ JSON file loaded successfully
✓ Validation successful!
--------------------------------------------------------------------------------

Statistics:
  - Total quizzes: 15
  - Total questions: 1500

Quiz names:
  1. French Revolution (50 questions) - Image: french-revolution.svg
  2. Greek Mythology (500 questions) - Image: greece-mythology.svg
  3. Europe Quiz (100 questions) - Image: europe-map.svg
  ...

================================================================================
Additional validation: Checking answers match options...
================================================================================
✓ All answers are valid (found in their options)

================================================================================
Additional validation: Checking UUID uniqueness...
================================================================================
✓ All 1500 UUIDs are unique

================================================================================
VALIDATION SUMMARY
================================================================================
Schema validation: ✓ PASS
Answer validation: ✓ PASS
UUID uniqueness:   ✓ PASS
================================================================================

✓ All validations passed!
```

## Problèmes Détectés

Lors de la validation actuelle, les problèmes suivants ont été identifiés :

### 1. Format UUID Invalide (Quiz Japan)
Les UUIDs du quiz Japan utilisent un format personnalisé `jp-xxxx-xxxxxxxx` au lieu du format UUID v4 standard.

**Solution** : Régénérer les UUIDs au format standard avec un script Python :
```python
import uuid
# Générer un UUID v4
str(uuid.uuid4())  # Ex: "59c67574-8dfc-4a5a-9d19-4590b7a36d2a"
```

### 2. UUIDs Dupliqués (Quiz Europe)
73 UUIDs sont utilisés plusieurs fois dans le quiz Europe.

**Solution** : Utiliser un script pour détecter et remplacer les UUIDs dupliqués par de nouveaux UUIDs uniques.

## Scripts Utilitaires

### Générer un UUID
```python
import uuid
print(uuid.uuid4())
```

### Corriger les UUIDs invalides
Un script de correction automatique peut être créé pour :
1. Détecter tous les UUIDs invalides ou dupliqués
2. Générer de nouveaux UUIDs uniques
3. Remplacer les anciens UUIDs dans le fichier JSON

## Intégration IDE

Le fichier `quiz-questions-schema.json` peut être utilisé dans votre IDE pour :
- Auto-complétion lors de l'édition du JSON
- Validation en temps réel
- Documentation contextuelle

### Configuration VSCode
Ajouter dans `.vscode/settings.json` :
```json
{
  "json.schemas": [
    {
      "fileMatch": ["**/quiz-questions.json"],
      "url": "./src/main/resources/quiz-questions-schema.json"
    }
  ]
}
```

### Configuration IntelliJ IDEA
1. Ouvrir Settings → Languages & Frameworks → Schemas and DTDs → JSON Schema Mappings
2. Ajouter un nouveau mapping :
   - Name: Quiz Questions Schema
   - Schema file: `src/main/resources/quiz-questions-schema.json`
   - File path pattern: `quiz-questions.json`

## Maintenance

Lorsque vous ajoutez un nouveau quiz :
1. Respectez la structure définie dans le schéma
2. Utilisez des UUIDs v4 valides et uniques
3. Assurez-vous que les IDs sont séquentiels (1, 2, 3, ...)
4. Vérifiez que les réponses correspondent exactement aux options
5. Exécutez `validate_quiz_json.py` avant de commiter

## Contact

Pour toute question sur le schéma ou la validation, consultez ce document ou exécutez le script de validation avec l'option d'aide.

