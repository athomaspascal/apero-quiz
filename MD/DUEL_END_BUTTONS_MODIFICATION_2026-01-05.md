# Modification des Boutons de Fin de Duel - 2026-01-05

## Changements Effectués

À la fin d'un quiz en mode duel, l'interface a été modifiée pour remplacer :
- ❌ Le label "Revenge available (1/3)"
- ❌ Le bouton "See the results"

Par :
- ✅ Bouton "Start a Rematch" (Démarrer une Revanche)
- ✅ Bouton "Stop the Duel" (Arrêter le Duel)

## Fichiers Modifiés

### 1. QuizQuestionView.java
**Fichier** : `src/main/java/com/quizz/core/ui/QuizQuestionView.java`

**Modifications dans la méthode `showDuelScoreboard()`** :
- Suppression du paragraphe affichant "Revanche disponible (x/3)"
- Remplacement du bouton "View Results" par deux nouveaux boutons :
  
  **Bouton "Start a Rematch"** :
  - Visible uniquement si le nombre de revanches est inférieur à 2 (max 3 matchs au total)
  - Appelle `duelService.requestRematch()` pour démarrer une nouvelle revanche
  - Navigue vers DuelQuizView pour gérer le processus de revanche
  - Style : Bouton primaire large
  
  **Bouton "Stop the Duel"** :
  - Toujours visible
  - Appelle `duelService.cancelDuel()` pour annuler le duel
  - Notifie automatiquement l'autre joueur via le système de polling
  - Navigue vers la page d'accueil
  - Style : Bouton d'erreur (rouge)

### 2. Fichiers de Traduction

Ajout des nouvelles clés de traduction dans tous les fichiers de langue :

**messages.properties** (par défaut - anglais) :
```properties
duelquiz.rematch.start=Start a Rematch
duelquiz.stop=Stop the Duel
```

**messages_fr.properties** (français) :
```properties
duelquiz.rematch.start=Démarrer une Revanche
duelquiz.stop=Arrêter le Duel
```

**messages_en.properties** (anglais) :
```properties
duelquiz.rematch.start=Start a Rematch
duelquiz.stop=Stop the Duel
```

**messages_it.properties** (italien) :
```properties
duelquiz.rematch.start=Inizia una Rivincita
duelquiz.stop=Ferma il Duello
```

## Comportement

### Lorsqu'un joueur clique sur "Start a Rematch"
1. Le système arrête le polling en cours
2. Appelle `duelService.requestRematch()` avec l'ID du duel et l'utilisateur courant
3. Navigation vers `DuelQuizView` pour gérer la logique de revanche
4. L'autre joueur reçoit une notification de demande de revanche
5. Si les deux joueurs acceptent, un nouveau compte à rebours démarre

### Lorsqu'un joueur clique sur "Stop the Duel"
1. Le système arrête le polling en cours
2. Appelle `duelService.cancelDuel()` qui met le statut du duel à `CANCELLED`
3. Navigation vers la page d'accueil
4. **L'autre joueur est automatiquement notifié** via le système de polling dans `DuelQuizView`
5. L'autre joueur voit apparaître la vue `showCancelledView()` avec le message :
   - Titre : "Duel Annulé"
   - Message : "Le duel a été annulé. Vous pouvez lancer une nouvelle recherche ou retourner au menu principal."

### Notification Automatique de l'Adversaire

Le système de polling dans `DuelQuizView` vérifie toutes les 2 secondes l'état du duel :
```java
pollingTask = executor.scheduleAtFixedRate(() -> {
    if (currentDuel != null && currentDuel.getId() != null) {
        Optional<DuelMatch> updated = duelService.getDuelById(currentDuel.getId());
        if (updated.isPresent()) {
            currentDuel = updated.get();
            // Si le statut change vers CANCELLED
            if (currentDuel.getStatus() == DuelMatch.DuelStatus.CANCELLED) {
                updateView(); // Affiche showCancelledView()
            }
        }
    }
}, 1, 2, TimeUnit.SECONDS);
```

Dès que le statut passe à `CANCELLED`, l'autre joueur voit automatiquement l'écran d'annulation sans avoir besoin de rafraîchir manuellement.

## Interface Utilisateur

### Avant
```
[Score Player 1] VS [Score Player 2]
Gagnant: Player X

Revanche disponible (1/3)

[Voir les Résultats]
```

### Après
```
[Score Player 1] VS [Score Player 2]
Gagnant: Player X

[Démarrer une Revanche]  [Arrêter le Duel]
```

## Avantages

- ✅ Interface plus claire et intuitive
- ✅ Actions directes sans navigation intermédiaire
- ✅ Notification automatique de l'adversaire lors de l'arrêt du duel
- ✅ Respect du nombre maximum de revanches (3 matchs)
- ✅ Bouton "Arrêter le Duel" toujours visible pour permettre de quitter à tout moment
- ✅ Traductions complètes en français, anglais et italien

## Tests à Effectuer

1. ✅ Terminer un duel entre deux joueurs
2. ✅ Vérifier que les deux nouveaux boutons s'affichent correctement
3. ✅ Cliquer sur "Start a Rematch" et vérifier la navigation vers DuelQuizView
4. ✅ Vérifier que l'autre joueur reçoit la demande de revanche
5. ✅ Cliquer sur "Stop the Duel" et vérifier :
   - Navigation vers la page d'accueil pour le joueur qui arrête
   - Message "Duel Annulé" pour l'autre joueur (automatiquement après max 2 secondes)
6. ✅ Vérifier que les traductions fonctionnent dans toutes les langues
7. ✅ Vérifier que le bouton "Start a Rematch" disparaît après 2 revanches

## Date de Modification

5 janvier 2026

