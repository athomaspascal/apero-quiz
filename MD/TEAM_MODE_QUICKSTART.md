# Guide de Démarrage Rapide - Mode Équipe

## Démarrer l'Application

```bash
cd C:\Users\athom\IdeaProjects\quizz1
mvn spring-boot:run
```

L'application sera disponible sur : `https://localhost:8089` ou `https://apero-quiz.duckdns.org:8089`

## Tester le Mode Équipe

### Étape 1 : Créer une Session (Hôte)

1. Connectez-vous à l'application
2. Allez dans le menu "Un Quizz"
3. Choisissez un quiz (ex: "Game of Thrones Quiz")
4. Cliquez sur "Partager"
5. Notez le code de session (ex: ABCD1234)

### Étape 2 : Activer le Mode Équipe (Hôte)

Sur la page de session qui s'affiche :

1. **Cochez la case "Activer le mode équipe"**
2. **Sélectionnez les équipes** que vous voulez pour ce quiz :
   - ☑ Stark
   - ☑ Lannister  
   - ☑ Targaryen
   - ☐ Baratheon
   - ☐ Tyrell
   - ☐ Martell
   - ☐ Arryn
   - ☐ Tully
   - ☐ Greyjoy

3. Les modifications sont automatiquement sauvegardées

### Étape 3 : Inviter les Joueurs

Partagez le code de session ou le QR code avec les autres joueurs.

**Les joueurs peuvent rejoindre de 2 façons :**

**Option A - Par code :**
1. Menu "Rejoindre une Session"
2. Entrer le code (ex: ABCD1234)
3. Cliquer sur "Rejoindre la Session"

**Option B - Par QR code :**
1. Scanner le QR code affiché sur l'écran de l'hôte
2. Être redirigé automatiquement vers la session

### Étape 4 : Les Joueurs Rejoignent

Chaque joueur :
1. Se connecte à l'application
2. Rejoint la session avec le code
3. Voit la liste des participants
4. Attend que l'hôte démarre la session

### Étape 5 : Démarrer la Session (Hôte)

Quand tous les joueurs ont rejoint :
1. Cliquez sur **"Démarrer pour tout le monde"**
2. La session passe en mode ACTIVE
3. Les joueurs peuvent maintenant commencer leur quiz

### Étape 6 : Sélectionner une Équipe (Joueurs)

Chaque joueur :
1. Clique sur **"Démarrer mon quiz"**
2. **Une boîte de dialogue s'ouvre** avec les équipes disponibles
3. Sélectionne son équipe (ex: Stark)
4. Clique sur **"Confirmer l'équipe"**
5. Le quiz commence

**Affichage :**
- Dans la liste des participants, l'équipe de chaque joueur apparaît sous son nom
- Exemple : 
  ```
  Jean Dupont
  Équipe : Stark
  En cours
  ```

### Étape 7 : Jouer au Quiz

Chaque joueur :
1. Répond aux questions
2. Son score est enregistré
3. À la fin, il voit son score personnel

### Étape 8 : Voir le Classement (Tous)

Quand tous les joueurs ont terminé :

**Le classement par équipe s'affiche automatiquement :**

```
🏆 Classement des Équipes

🥇 Stark
   Équipe Stark : 85 points
   - Jean Dupont - Score : 45
   - Marie Martin - Score : 40

🥈 Lannister
   Équipe Lannister : 70 points
   - Pierre Dubois - Score : 40
   - Sophie Bernard - Score : 30

🥉 Targaryen
   Équipe Targaryen : 55 points
   - Luc Petit - Score : 30
   - Anne Durand - Score : 25
```

## Exemple Complet avec 6 Joueurs

### Configuration Hôte
- Quiz : "Game of Thrones"
- Mode équipe : ✅ Activé
- Équipes sélectionnées : Stark, Lannister, Targaryen

### Répartition des Joueurs
- **Équipe Stark** : Jean (45 pts) + Marie (40 pts) = **85 points** 🥇
- **Équipe Lannister** : Pierre (40 pts) + Sophie (30 pts) = **70 points** 🥈
- **Équipe Targaryen** : Luc (30 pts) + Anne (25 pts) = **55 points** 🥉

### Résultat Final
L'équipe Stark remporte la partie avec 85 points !

## Mode Normal (Sans Équipe)

Si la case "Activer le mode équipe" n'est **PAS cochée** :

1. Les joueurs cliquent sur "Démarrer mon quiz" directement (pas de sélection d'équipe)
2. Le classement final affiche les joueurs individuellement :
   ```
   🥇 Jean Dupont - Score : 45
   🥈 Pierre Dubois - Score : 40
   🥉 Marie Martin - Score : 40
   4  Sophie Bernard - Score : 30
   5  Luc Petit - Score : 30
   6  Anne Durand - Score : 25
   ```

## Recommencer une Partie

L'hôte peut cliquer sur **"Nouvelle partie"** pour :
- Réinitialiser tous les scores
- Permettre aux joueurs de rejouer
- Le mode équipe et la sélection des équipes sont conservés

Les joueurs peuvent changer d'équipe pour la nouvelle partie.

## Vérifications à Faire

✅ La checkbox "Mode équipe" apparaît pour l'hôte en statut WAITING
✅ Les checkboxes des équipes apparaissent quand le mode équipe est activé
✅ Le dialogue de sélection d'équipe apparaît pour les joueurs en mode équipe
✅ L'équipe du joueur s'affiche dans la liste des participants
✅ Le classement par équipe s'affiche correctement en fin de partie
✅ Les traductions fonctionnent (FR, EN, IT)

## Dépannage

### La checkbox "Mode équipe" n'apparaît pas
- Vérifiez que vous êtes bien l'hôte de la session
- Vérifiez que la session est en statut WAITING (pas encore démarrée)

### Les équipes ne s'affichent pas dans le dialogue
- Vérifiez que l'hôte a bien sélectionné des équipes
- Vérifiez que le mode équipe est activé

### Le classement par équipe ne s'affiche pas
- Vérifiez que la session est en statut COMPLETED
- Vérifiez que le mode équipe était activé au démarrage
- Vérifiez que les joueurs ont bien sélectionné une équipe

### Erreur de base de données
Si vous obtenez une erreur sur les colonnes manquantes :
```bash
# Exécutez le script SQL
psql -U votre_user -d votre_database -f add_team_mode_columns.sql
```

Ou configurez JPA en mode `update` dans `application.properties` :
```properties
spring.jpa.hibernate.ddl-auto=update
```

## Logs pour le Débogage

Les logs sont dans : `logs/application.log`

Pour voir les logs en temps réel :
```bash
tail -f logs/application.log
```

## Support

Consultez la documentation complète dans :
- `MD/TEAM_MODE_IMPLEMENTATION.md` : Guide technique complet
- `MD/TEAM_MODE_SUMMARY.md` : Résumé des modifications

Bon jeu ! 🎮🏆

