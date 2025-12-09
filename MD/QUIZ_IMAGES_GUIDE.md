# Guide d'ajout des images de quiz

## Emplacement des images

Les images des quiz doivent être placées dans le répertoire :
```
src/main/resources/META-INF/resources/images/
```

## Format des images

- **Format recommandé** : SVG (vectoriel), PNG, GIF, ou JPG
- **Taille recommandée** : 120x80 pixels (ou ratio 3:2 similaire)
- **Nom de fichier** : Configuré dans `quiz-questions.json`
- **Note** : La vue peut afficher jusqu'à 64 quiz simultanément

## Configuration dans quiz-questions.json

Chaque quiz doit avoir un champ `imageFileName` :

```json
{
  "quizzes": [
    {
      "name": "General Knowledge",
      "imageFileName": "knowledge.svg",
      "questions": [
        ...
      ]
    }
  ]
}
```

## Images actuellement configurées

Les quiz suivants utilisent les images SVG suivantes :

1. **General Knowledge** → `knowledge.svg` (📚 - Gradient violet)
2. **Physics** → `physics.svg` (⚛️ - Gradient vert)
3. **US Civil War** → `civilwar.svg` (🎖️ - Gradient rouge)
4. **Painting** → `painting.svg` (🎨 - Gradient rose)

## Sources d'images gratuites

Vous pouvez trouver des images clipart gratuites sur :
- **Flaticon** : https://www.flaticon.com/
- **Icons8** : https://icons8.com/
- **Freepik** : https://www.freepik.com/
- **Pixabay** : https://pixabay.com/

## Comment ajouter une nouvelle image

1. Téléchargez ou créez votre image
2. Renommez-la (ex: `myquiz.gif`)
3. Copiez-la dans `src/main/resources/META-INF/resources/images/`
4. Ajoutez le nom dans `quiz-questions.json` :
   ```json
   {
     "name": "Mon Quiz",
     "imageFileName": "myquiz.gif",
     "questions": [...]
   }
   ```
5. Redémarrez l'application

## Placeholder par défaut

Si aucune image n'est configurée ou si le fichier n'existe pas, un emoji 📚 sera affiché par défaut.

## Affichage dans l'interface

Les images sont affichées sous forme de **cartes cliquables compactes** :
- **Taille carte** : 120x140 pixels
- **Image** : 120x80 pixels
- **Nom du quiz** : Affiché sous l'image (10px, 2 lignes max)
- **Effet hover** : Bordure bleue et légère élévation
- **Sélection** : Clic sur la carte pour sélectionner le quiz
- **Capacité** : Jusqu'à 64 quiz affichables simultanément

