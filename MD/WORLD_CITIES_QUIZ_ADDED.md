# Quiz sur les Villes du Monde - Latitude & Longitude

## ✅ Ajout Complété

### Détails du Quiz

**Nom du Quiz:** World Cities - Latitude & Longitude  
**Fichier Image:** world-map.svg  
**Nombre de Questions:** 50  
**Statut:** ✅ Ajouté avec succès

### Contenu du Quiz

Le quiz teste les connaissances sur les coordonnées géographiques (latitude et longitude) de 50 villes célèbres à travers le monde, incluant:

#### Villes Couvertes
- **Europe:** Paris, Londres, Berlin, Rome, Stockholm, Oslo, Prague, Bruxelles, Amsterdam, Lisbonne, Athènes, Istanbul, Madrid, Barcelone, Vienne, Copenhague, Hambourg, Édimbourg, Munich, Varsovie, Dublin, Belgrade, Venise, Milan
- **Asie:** Tokyo, Beijing, Mumbai, New Delhi, Bangkok, Singapore, Dubai, Seoul, Hong Kong, Shanghai, Taipei, Manila, Kuala Lumpur, Hanoi, Chiang Mai, Yangon, Kolkata, Bangalore
- **Amérique du Nord:** New York, Los Angeles, Chicago, San Francisco, Mexico City, Havana, Montreal, Vancouver, Boston, Philadelphia, Washington D.C., Milwaukee, Indianapolis, Detroit
- **Amérique du Sud:** Rio de Janeiro, Buenos Aires, Lima, Santiago, Bogota, Quito
- **Afrique:** Cairo, Nairobi, Cape Town, Johannesburg
- **Océanie:** Sydney, Melbourne, Wellington, Auckland, Brisbane, Christchurch

### Types de Questions

1. **Questions sur la latitude** - "Quelle est la latitude approximative de [ville]?"
2. **Questions sur la longitude** - "Quelle est la longitude approximative de [ville]?"
3. **Questions d'identification** - "Quelle ville se trouve à environ [coordonnées]?"

### Structure des Questions

Chaque question suit la structure standard:
```json
{
  "id": 1-50,
  "uuid": "unique-identifier",
  "question": "Question text",
  "options": [
    "Option 1",
    "Option 2",
    "Option 3",
    "Option 4"
  ],
  "answer": "Correct answer"
}
```

### Fichiers Créés/Modifiés

1. ✅ **quiz-questions.json** - Quiz ajouté à la liste existante
2. ✅ **world-map.svg** - Image créée avec une carte du monde stylisée
   - Localisation: `src/main/resources/META-INF/resources/images/world-map.svg`
   - Caractéristiques:
     - Fond bleu clair représentant l'océan
     - Grille de latitude/longitude
     - Continents simplifiés en vert
     - Marqueurs de villes en rouge
     - Boussole dans le coin supérieur droit
     - Titre et sous-titre

3. ✅ **Sauvegarde créée** - `quiz-questions_[timestamp].json`

### Vérifications Effectuées

✅ Tous les attributs `id` sont présents (1-50)  
✅ Tous les attributs `uuid` sont uniques et valides  
✅ Structure JSON valide  
✅ Syntaxe conforme au template  
✅ Fichier image SVG créé  
✅ Sauvegarde du fichier original effectuée

### Statistiques Finales

- **Total de quiz dans l'application:** 12
- **Nouvelles questions ajoutées:** 50
- **Format:** Conforme au template
- **Encodage:** UTF-8

### Prochaines Étapes

Pour voir le nouveau quiz dans l'application:
1. Redémarrer l'application Spring Boot
2. Se connecter à l'application
3. Le quiz "World Cities - Latitude & Longitude" apparaîtra dans la liste des quiz disponibles

### Commandes de Vérification

```bash
# Vérifier le nombre de quiz
python -c "import json; data = json.load(open('src/main/resources/quiz-questions.json', 'r', encoding='utf-8')); print(f'Total: {len(data[\"quizzes\"])} quizzes')"

# Lister tous les quiz
python -c "import json; data = json.load(open('src/main/resources/quiz-questions.json', 'r', encoding='utf-8')); [print(f'{i+1}. {q[\"name\"]}') for i, q in enumerate(data['quizzes'])]"

# Vérifier le dernier quiz ajouté
python -c "import json; data = json.load(open('src/main/resources/quiz-questions.json', 'r', encoding='utf-8')); quiz = data['quizzes'][-1]; print(f'Name: {quiz[\"name\"]}\\nQuestions: {len(quiz[\"questions\"])}\\nImage: {quiz[\"imageFileName\"]}')"
```

---

**Date de création:** 2025-12-26  
**Créé par:** GitHub Copilot  
**Statut:** ✅ Complété

