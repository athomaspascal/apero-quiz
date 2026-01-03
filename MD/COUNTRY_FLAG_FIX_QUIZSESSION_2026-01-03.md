# Correction de l'affichage du drapeau du pays - 2026-01-03

## Problème
Les drapeaux des pays n'étaient pas affichés dans la vue QuizSessionView (liste des participants).

## Modifications effectuées

### 1. QuizSessionView.java
- Ajout des imports nécessaires : `StreamResource`, `ByteArrayInputStream` et `Logger`
- Ajout d'un logger dans la classe
- Modification de la méthode `updateParticipantsList()` pour afficher le drapeau du pays à côté du nom de chaque participant

Le drapeau est maintenant affiché :
- À côté du nom de l'utilisateur
- Dimensions : 30px x 20px
- Avec une bordure et une ombre légère
- En utilisant StreamResource pour charger le SVG du drapeau

### 2. DataInitializer.java
- Modification de la méthode `createAdminUser()` pour vérifier si l'utilisateur admin existant a un pays associé
- Si l'utilisateur admin existe mais n'a pas de pays, il est automatiquement lié à la France

### 3. Fichier SQL créé
- `link_admin_to_france.sql` : script SQL pour lier manuellement l'utilisateur admin à la France si nécessaire

## Comment tester

1. Redémarrer l'application :
   ```cmd
   mvn spring-boot:run
   ```

2. Se connecter avec l'utilisateur admin

3. Créer une session de quiz et inviter d'autres joueurs

4. Vérifier que les drapeaux des pays s'affichent à côté des noms des participants dans la liste

## Logs à vérifier

Dans les logs de l'application, vous devriez voir :
- `Checking country flag for participant: [nom]`
- `Participant has country: [nom du pays]`
- `Creating flag display for country: [nom du pays]`
- `Flag container added to layout for participant: [nom]`

Si vous voyez des warnings comme "Participant X has no country associated", cela signifie que l'utilisateur n'a pas de pays lié dans la base de données.

## Résultat attendu

Dans la vue QuizSessionView, chaque participant devrait maintenant avoir son drapeau de pays affiché à côté de son nom, de la même manière que dans QuizListView.

