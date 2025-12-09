# Modifications - Interface de sélection des quiz avec cartes et images

## Date : 10 décembre 2025

## Résumé des modifications

Le système de sélection des quiz a été complètement refondu pour remplacer le Grid traditionnel par une **interface de cartes cliquables avec images**.

---

## 1. Modifications de l'entité Quiz

### Fichier : `src/main/java/com/quizz/core/entity/Quiz.java`

**Ajout du champ `imageFileName`** :
```java
@Column(name = "image_file_name", length = 255)
private String imageFileName;

public String getImageFileName() { ... }
public void setImageFileName(String imageFileName) { ... }
```

---

## 2. Modifications du fichier JSON

### Fichier : `src/main/resources/quiz-questions.json`

**Ajout du champ `imageFileName`** pour chaque quiz :
```json
{
  "name": "General Knowledge",
  "imageFileName": "knowledge.svg",
  "questions": [...]
}
```

**Quiz configurés** :
- General Knowledge → `knowledge.svg`
- Physics → `physics.svg`
- US Civil War → `civilwar.svg`
- Painting → `painting.svg`

---

## 3. Modifications des classes de données

### Fichier : `src/main/java/com/quizz/core/entity/QuizQuestionsData.java`

**Ajout dans `QuizData`** :
```java
private String imageFileName;
public String getImageFileName() { ... }
public void setImageFileName(String imageFileName) { ... }
```

---

## 4. Modifications du service

### Fichier : `src/main/java/com/quizz/core/service/QuizService.java`

**Ajout de la méthode save** :
```java
@Transactional
public Quiz save(Quiz quiz) {
    return quizRepository.save(quiz);
}
```

---

## 5. Modifications de l'initialisateur

### Fichier : `src/main/java/com/quizz/core/QuizDataInitializer.java`

**Mise à jour pour sauvegarder `imageFileName`** :
```java
Quiz quiz = new Quiz(quizData.getName());
quiz.setImageFileName(quizData.getImageFileName());
quiz = quizService.save(quiz);
```

---

## 6. Refonte complète de QuizListView

### Fichier : `src/main/java/com/quizz/core/ui/QuizListView.java`

### Changements majeurs :

#### A. Remplacement du Grid par un conteneur de cartes
```java
// Avant :
final Grid<Quiz> quizGrid;

// Après :
private HorizontalLayout quizCardsContainer;
```

#### B. Nouvelle méthode `loadQuizCards()`
Charge tous les quiz et crée une carte pour chacun.

#### C. Nouvelle méthode `createQuizCard(Quiz quiz)`
Crée une carte visuelle avec :
- **Image** : 200x150px (depuis `images/` + `imageFileName`)
- **Nom du quiz** : Affiché sous l'image
- **Style** :
  - Bordure grise par défaut
  - Bordure bleue au survol
  - Effet d'élévation au survol
  - Curseur pointer
- **Comportement** :
  - Cliquable pour sélectionner le quiz
  - Active les boutons "Start" et "Share"

#### D. Gestion du placeholder
Si aucune image n'est configurée, affiche un emoji 📚 par défaut.

---

## 7. Images SVG créées

### Emplacement : `src/main/resources/META-INF/resources/images/`

**4 images SVG créées** :

1. **knowledge.svg** - 📚 avec gradient violet (#667eea → #764ba2)
2. **physics.svg** - ⚛️ avec gradient vert (#11998e → #38ef7d)
3. **civilwar.svg** - 🎖️ avec gradient rouge (#e43a15 → #e65245)
4. **painting.svg** - 🎨 avec gradient rose (#f093fb → #f5576c)

---

## 8. Documentation créée

### Fichier : `QUIZ_IMAGES_GUIDE.md`

Guide complet expliquant :
- Emplacement des images
- Formats supportés
- Configuration dans le JSON
- Sources d'images gratuites
- Comment ajouter de nouvelles images

---

## Résultat visuel

### Avant :
```
+----------------------------------+
| Name           | Action         |
+----------------------------------+
| General Knowledge | [Share]     |
| Physics          | [Share]      |
+----------------------------------+
```

### Après :
```
+----------+  +----------+  +----------+  +----------+
|   📚     |  |   ⚛️     |  |   🎖️     |  |   🎨     |
|          |  |          |  |          |  |          |
| General  |  | Physics  |  | US Civil |  | Painting |
| Knowledge|  |          |  | War      |  |          |
+----------+  +----------+  +----------+  +----------+
```

---

## Fonctionnalités

✅ **Affichage en cartes** : Interface moderne et visuelle
✅ **Images personnalisables** : Via le fichier JSON
✅ **Placeholder par défaut** : Si pas d'image configurée
✅ **Effet hover** : Bordure bleue et élévation
✅ **Sélection visuelle** : Clic pour sélectionner
✅ **Boutons contextuels** : Start et Share activés à la sélection
✅ **Responsive** : Les cartes s'adaptent (flex-wrap)

---

## Migration

### Pour mettre à jour une installation existante :

1. **Base de données** : Ajouter la colonne `image_file_name` à la table `quiz`
   ```sql
   ALTER TABLE quiz ADD COLUMN image_file_name VARCHAR(255);
   ```

2. **Images** : Copier les images SVG dans `src/main/resources/META-INF/resources/images/`

3. **JSON** : Mettre à jour `quiz-questions.json` avec les `imageFileName`

4. **Recompiler** : `mvnw clean package`

5. **Redémarrer** l'application

---

## Notes techniques

- **Format SVG** : Vectoriel, léger, redimensionnable sans perte
- **Taille des cartes** : 200x250px (image 200x150px + texte)
- **Layout** : `HorizontalLayout` avec `flex-wrap`
- **Compatibilité** : Tous navigateurs modernes

---

## Prochaines améliorations possibles

- Ajout de GIFs animés pour plus d'interactivité
- Upload d'images via interface admin
- Catégories de quiz avec filtres
- Vue grille/liste commutable
- Statistiques sur les cartes (nb de participants, difficulté)

