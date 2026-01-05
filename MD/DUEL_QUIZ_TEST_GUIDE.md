# Guide de Test - Duel Quiz

## Date: 2026-01-05

## Prérequis
- Application compilée et démarrée
- Au moins 2 utilisateurs connectés (sur des navigateurs différents ou en navigation privée)
- Des quiz disponibles dans la base de données

## Étapes pour Tester le Duel Quiz

### 1. Démarrer l'Application
```bash
cd C:\Users\athom\IdeaProjects\quizz1
mvn spring-boot:run
```

Ou depuis votre IDE, exécutez la classe `Application.java`

### 2. Connexion de Deux Joueurs

#### Joueur 1 (Navigateur principal)
1. Ouvrir le navigateur : `https://apero-quiz.duckdns.org:8443`
2. Se connecter avec un compte utilisateur (ex: admin)
3. Vérifier que le menu "Duel Quiz" apparaît dans le menu latéral (icône trophée)

#### Joueur 2 (Navigateur privé ou autre navigateur)
1. Ouvrir une fenêtre de navigation privée ou un autre navigateur
2. Aller sur : `https://apero-quiz.duckdns.org:8443`
3. Se connecter avec un autre compte utilisateur
4. Vérifier que le menu "Duel Quiz" apparaît

### 3. Lancer un Duel

#### Sur le Navigateur du Joueur 1
1. Cliquer sur "Duel Quiz" dans le menu
2. Cliquer sur le bouton "Search for Opponent" (Chercher un Adversaire)
3. Attendre - un spinner devrait apparaître avec le message "Searching for Opponent..."

#### Sur le Navigateur du Joueur 2
1. Cliquer sur "Duel Quiz" dans le menu
2. Cliquer sur le bouton "Search for Opponent"

### 4. Match Trouvé
- Les deux joueurs devraient voir automatiquement (en 2 secondes max) :
  - Le nom de leur adversaire
  - Le nom du quiz sélectionné aléatoirement
  - Deux boutons : "Accept Duel" et "Decline"

### 5. Accepter le Duel
1. Les deux joueurs doivent cliquer sur "Accept Duel"
2. Une fois les deux acceptations, le compte à rebours de 5 secondes démarre
3. Le quiz démarre automatiquement quand le compte à rebours atteint 0

### 6. Jouer le Quiz
- Les deux joueurs répondent aux questions indépendamment
- Le timer fonctionne normalement
- Chaque joueur voit ses propres réponses

### 7. Voir les Résultats
- Quand les deux joueurs terminent :
  - Le tableau des scores s'affiche
  - Le gagnant est annoncé (ou "It's a Draw!" en cas d'égalité)
  - Option de revanche apparaît (si c'est le 1er ou 2ème match)

### 8. Revanche (Optionnel)
1. Les deux joueurs cliquent sur "Request Rematch"
2. Un nouveau quiz est sélectionné aléatoirement
3. Le compte à rebours redémarre
4. Maximum 3 matches au total (1 + 2 rematches)

### 9. Annulation
- À tout moment avant le début du quiz, un joueur peut cliquer "Cancel"
- Les deux joueurs retournent au menu principal

## Cas de Test Détaillés

### Test 1 : Matchmaking Basique
- **Objectif** : Vérifier que deux joueurs peuvent se trouver
- **Attendu** : Match trouvé en moins de 2 secondes après que le 2ème joueur lance la recherche

### Test 2 : Acceptation du Duel
- **Objectif** : Vérifier le mécanisme d'acceptation
- **Attendu** : Le compte à rebours ne démarre que quand les deux joueurs ont accepté

### Test 3 : Compte à Rebours
- **Objectif** : Vérifier le timer de 5 secondes
- **Attendu** : 
  - Affichage de 5, 4, 3, 2, 1
  - Message "GO!" à la fin
  - Démarrage automatique du quiz

### Test 4 : Synchronisation des Scores
- **Objectif** : Vérifier que les scores sont bien enregistrés
- **Attendu** : 
  - Chaque joueur voit son propre score
  - Le tableau final affiche les scores des deux joueurs
  - Le bon gagnant est désigné

### Test 5 : Revanche
- **Objectif** : Tester le système de revanche
- **Attendu** : 
  - Maximum 2 rematches (3 matches au total)
  - Nouveau quiz sélectionné à chaque fois
  - Compteur de revanche affiché correctement

### Test 6 : Annulation
- **Objectif** : Tester l'annulation à différentes étapes
- **Cas** :
  - Pendant la recherche
  - Après le match (avant acceptation)
  - Après les résultats
- **Attendu** : Retour propre au menu, pas d'erreur

### Test 7 : Duels Multiples
- **Objectif** : Vérifier que plusieurs duels peuvent avoir lieu simultanément
- **Setup** : 4 joueurs (2 paires)
- **Attendu** : Chaque paire peut jouer indépendamment

### Test 8 : Déconnexion
- **Objectif** : Tester la robustesse en cas de déconnexion
- **Cas** : Un joueur ferme son navigateur pendant un duel
- **Attendu** : L'autre joueur devrait pouvoir annuler proprement

## Vérifications de la Base de Données

### Accéder à la Console H2
1. Aller sur : `https://apero-quiz.duckdns.org:8443/h2-console`
2. Se connecter avec :
   - JDBC URL : `jdbc:h2:file:./data/quizdb;AUTO_SERVER=TRUE`
   - Username : `sa`
   - Password : (laisser vide)

### Requêtes SQL Utiles

```sql
-- Voir tous les duels
SELECT * FROM duel_match ORDER BY created_at DESC;

-- Voir les duels actifs
SELECT * FROM duel_match WHERE status IN ('SEARCHING', 'MATCHED', 'COUNTDOWN', 'IN_PROGRESS');

-- Voir les statistiques de duels
SELECT status, COUNT(*) as count FROM duel_match GROUP BY status;

-- Voir les duels d'un joueur spécifique
SELECT dm.*, u1.name as player1_name, u2.name as player2_name, q.name as quiz_name
FROM duel_match dm
LEFT JOIN user u1 ON dm.player1_id = u1.user_id
LEFT JOIN user u2 ON dm.player2_id = u2.user_id
LEFT JOIN quiz q ON dm.quiz_id = q.quiz_id
WHERE dm.player1_id = ? OR dm.player2_id = ?
ORDER BY dm.created_at DESC;
```

## Problèmes Connus et Solutions

### Problème : Le menu "Duel Quiz" n'apparaît pas
**Solution** : 
- Vérifier que l'utilisateur est connecté
- Rafraîchir la page (F5)
- Vérifier les logs pour les erreurs

### Problème : Les joueurs ne se trouvent pas
**Solution** :
- Vérifier que les deux joueurs sont sur des sessions différentes
- Vérifier les logs du serveur pour les erreurs de polling
- Vérifier que Vaadin Push est activé

### Problème : Le compte à rebours ne démarre pas
**Solution** :
- Vérifier que les deux joueurs ont bien cliqué sur "Accept"
- Vérifier les logs pour les erreurs de ScheduledExecutorService

### Problème : Les scores ne sont pas enregistrés
**Solution** :
- Vérifier que le paramètre `duel` est bien passé dans l'URL du quiz
- Vérifier les logs lors de la soumission du score
- Vérifier la table `duel_match` dans H2

## Logs à Surveiller

```
# Démarrage d'une recherche
User X starting duel search

# Match trouvé
Match found! Player1: X, Player2: Y, Quiz: Z

# Acceptation
User X accepting duel N

# Démarrage du compte à rebours
Both players ready, starting countdown for duel N

# Démarrage du quiz
Starting quiz for duel N

# Soumission du score
User X submitting score N for duel M
Duel score submitted: duelId=M, score=N

# Demande de revanche
User X requesting rematch for duel N
Both players want rematch, starting new round for duel N
```

## Checklist de Test Final

- [ ] Menu "Duel Quiz" visible
- [ ] Recherche d'adversaire fonctionne
- [ ] Matchmaking fonctionne (2 joueurs se trouvent)
- [ ] Affichage de l'adversaire et du quiz
- [ ] Acceptation du duel par les 2 joueurs
- [ ] Compte à rebours de 5 secondes
- [ ] Démarrage automatique du quiz
- [ ] Quiz jouable par les 2 joueurs
- [ ] Scores enregistrés correctement
- [ ] Tableau des scores correct
- [ ] Désignation du gagnant correcte
- [ ] Bouton de revanche apparaît (si < 3 matches)
- [ ] Revanche fonctionne (nouveau quiz)
- [ ] Limite de 3 matches respectée
- [ ] Annulation fonctionne à chaque étape
- [ ] Traductions (EN, FR, IT) correctes
- [ ] Pas d'erreur dans les logs
- [ ] Pas de fuite mémoire (executors bien fermés)

## Contact / Support
Pour tout problème, consulter les logs dans `logs/application.log` ou vérifier le fichier de documentation `MD/DUEL_QUIZ_IMPLEMENTATION.md`

