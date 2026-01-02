# Correction du format dateUpdate - Harry Potter Quiz

## Problème Détecté

L'application ne pouvait pas charger les quizzes à cause d'une erreur de format dans le champ `dateUpdate`.

### Erreur dans les logs :
```
Cannot deserialize value of type `java.time.LocalDateTime` from String "2025-12-31"
```

### Cause :
- Le champ `dateUpdate` dans `QuizQuestionsData.java` est de type `LocalDateTime`
- Le JSON contenait le format : `"dateUpdate": "2025-12-31"` (date seule)
- Java attend le format : `"dateUpdate": "2025-12-31T00:00:00"` (date + heure)

## Solution Appliquée

**Commande PowerShell exécutée :**
```powershell
(Get-Content quiz-questions.json -Raw) -replace '"dateUpdate": "2025-12-31"', '"dateUpdate": "2025-12-31T00:00:00"' | Set-Content quiz-questions.json
```

### Résultat :
- ✅ 20+ occurrences corrigées dans le quiz Harry Potter
- ✅ Format correct : `"2025-12-31T00:00:00"`
- ✅ Compatible avec `LocalDateTime`

## Vérification

**Avant :**
```json
"dateUpdate": "2025-12-31"
```

**Après :**
```json
"dateUpdate": "2025-12-31T00:00:00"
```

## Prochaine Étape

Redémarrer l'application pour que les quizzes se chargent correctement.

---

**Date de correction :** 31 décembre 2025  
**Fichier corrigé :** `src/main/resources/quiz-questions.json`  
**Statut :** ✅ CORRIGÉ

