# Implémentation des UUID pour les Questions

## Résumé
Une propriété UUID a été ajoutée à chaque question dans le système de quiz pour permettre une identification unique et stable de chaque question, indépendamment de son ID numérique.

## Modifications effectuées

### 1. Fichier JSON (quiz-questions.json)
- **Action**: Ajout d'un UUID unique à chaque question
- **Total**: 130 questions réparties sur 4 quiz ont reçu un UUID
  - General Knowledge Quiz: 10 questions
  - Second Quiz (Physics): 10 questions  
  - US Civil War Quiz: 100 questions
  - Painting Quiz: 10 questions

**Exemple de structure**:
```json
{
    "id": 1,
    "uuid": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "question": "What is the capital of France?",
    "options": ["Berlin", "Madrid", "Paris", "Rome"],
    "answer": "Paris"
}
```

### 2. Classe Java QuizQuestionsData.java
- **Fichier**: `src/main/java/com/quizz/core/entity/QuizQuestionsData.java`
- **Action**: Ajout de la propriété `uuid` dans la classe interne `QuestionData`

**Modifications**:
```java
public static class QuestionData {
    private int id;
    private String uuid;  // ← NOUVEAU
    private String question;
    private List<String> options;
    private String answer;
    
    // Getter et Setter ajoutés
    public String getUuid() { return uuid; }
    public void setUuid(String uuid) { this.uuid = uuid; }
}
```

## Avantages de l'implémentation

1. **Identification unique**: Chaque question possède maintenant un identifiant unique qui ne change jamais
2. **Traçabilité**: Permet de suivre une question même si son ID numérique change
3. **Partage de quiz**: Facilite le partage et la synchronisation des sessions de quiz entre utilisateurs
4. **Intégration future**: Prépare le terrain pour des fonctionnalités avancées comme:
   - Tracking des statistiques par question
   - Historique des réponses
   - Partage de questions entre quiz
   - Importation/exportation de questions

## Format des UUID
- **Type**: UUID version 4 (aléatoire)
- **Format**: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`
- **Exemple**: `32cf5fb0-8a5e-4aa3-846f-81e7b45897c2`

## Validation
✅ Compilation réussie (BUILD SUCCESS)
✅ Tous les quiz ont leurs UUIDs
✅ La classe Java est synchronisée avec le JSON
✅ Aucune erreur de désérialisation

## Utilisation
Le système charge automatiquement les UUIDs depuis le fichier JSON. Aucune modification n'est nécessaire dans le code existant, car Jackson (la librairie de désérialisation JSON) gère automatiquement la nouvelle propriété.

## Script utilisé
Un script Node.js a été créé temporairement pour générer et injecter les UUIDs dans le fichier JSON de manière automatique et efficace.

---
Date d'implémentation: 7 décembre 2025

