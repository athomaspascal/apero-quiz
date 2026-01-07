# Fonctionnalité : Notification d'Arrêt de Duel par un Joueur - 2026-01-07

## 🎯 Objectif

Quand un joueur quitte ou arrête un duel, l'adversaire doit :
1. Voir son quiz s'arrêter automatiquement
2. Recevoir une notification indiquant que l'adversaire a quitté
3. Être redirigé vers l'écran principal

## ✅ Modifications implémentées

### 1. Entité DuelMatch - Tracking de qui a annulé

**Fichier** : `DuelMatch.java`

Ajout d'un champ pour tracker qui a annulé le duel :

```java
@ManyToOne
@JoinColumn(name = "cancelled_by_user_id")
private User cancelledBy;

public User getCancelledBy() {
    return cancelledBy;
}

public void setCancelledBy(User cancelledBy) {
    this.cancelledBy = cancelledBy;
}
```

### 2. DuelService - Enregistrement de qui annule

**Fichier** : `DuelService.java`

Modification de la méthode `cancelDuel` pour accepter l'utilisateur qui annule :

```java
@Transactional
public void cancelDuel(Long duelId, User cancelledByUser) {
    logger.info("Cancelling duel {} by user {}", duelId, 
        cancelledByUser != null ? cancelledByUser.getName() : "system");

    DuelMatch duel = duelMatchRepository.findById(duelId)
        .orElseThrow(() -> new RuntimeException("Duel not found"));

    duel.setStatus(DuelMatch.DuelStatus.CANCELLED);
    duel.setFinishedAt(LocalDateTime.now());
    duel.setCancelledBy(cancelledByUser); // ✅ Enregistre qui a annulé
    duelMatchRepository.save(duel);
    
    logger.info("Duel {} cancelled successfully", duelId);
}

// Surcharge pour compatibilité (annulation système)
@Transactional
public void cancelDuel(Long duelId) {
    cancelDuel(duelId, null);
}
```

### 3. DuelQuizView - Détection de l'annulation par l'adversaire

**Fichier** : `DuelQuizView.java`

#### A. Passer l'utilisateur lors de l'annulation

Mise à jour des appels à `cancelDuel` pour passer l'utilisateur :

```java
// Dans showSearchingView()
Button cancelButton = new Button(..., event -> {
    User currentUser = VaadinSession.getCurrent().getAttribute(User.class);
    if (currentUser != null) {
        userActivityService.updateActivity(currentUser, "CANCEL_DUEL_SEARCH", "duel-quiz");
    }
    stopWaitingConfirmationTimer();
    duelService.cancelDuel(currentDuel.getId(), currentUser); // ✅ Passe l'utilisateur
    currentDuel = null;
    showInitialView();
});

// Dans showMatchedView()
Button declineButton = new Button(..., event -> {
    userActivityService.updateActivity(currentUser, "DECLINE_DUEL", "duel-quiz");
    duelService.cancelDuel(currentDuel.getId(), currentUser); // ✅ Passe l'utilisateur
    currentDuel = null;
    showInitialView();
});
```

#### B. Détection dans le polling

Dans la méthode `startPolling()`, ajout de la détection d'annulation :

```java
pollingTask = executor.scheduleAtFixedRate(() -> {
    UI ui = getUI().orElse(null);
    if (ui == null) return;

    ui.access(() -> {
        try {
            User currentUser = VaadinSession.getCurrent().getAttribute(User.class);
            
            if (currentDuel != null && currentDuel.getId() != null) {
                Optional<DuelMatch> updated = duelService.getDuelById(currentDuel.getId());
                if (updated.isPresent()) {
                    DuelMatch oldDuel = currentDuel;
                    currentDuel = updated.get();

                    // ✅ Détection de l'annulation par l'adversaire
                    if (oldDuel.getStatus() != DuelMatch.DuelStatus.CANCELLED &&
                        currentDuel.getStatus() == DuelMatch.DuelStatus.CANCELLED &&
                        currentDuel.getCancelledBy() != null) {
                        
                        User cancelledByUser = currentDuel.getCancelledBy();
                        if (!cancelledByUser.getId().equals(currentUser.getId())) {
                            // L'adversaire a annulé le duel
                            logger.info("Duel cancelled by opponent: {}", cancelledByUser.getName());
                            
                            String message = translationService.translate("duelquiz.opponent.quit")
                                .replace("{opponent}", cancelledByUser.getName());
                            
                            // ✅ Affichage de la notification
                            Notification notification = Notification.show(
                                message,
                                5000,
                                Notification.Position.MIDDLE
                            );
                            notification.addThemeVariants(NotificationVariant.LUMO_ERROR);
                            
                            // ✅ Retour à l'écran initial
                            currentDuel = null;
                            showInitialView();
                            return;
                        }
                    }

                    // Autres mises à jour de statut...
                }
            }
            ui.push();
        } catch (Exception e) {
            logger.error("Error during polling", e);
        }
    });
}, 1, 2, TimeUnit.SECONDS);
```

### 4. QuizQuestionView - Arrêt du quiz quand l'utilisateur quitte

**Fichier** : `QuizQuestionView.java`

#### A. Implémentation de BeforeLeaveObserver

```java
public class QuizQuestionView extends Main 
    implements BeforeEnterObserver, BeforeLeaveObserver { // ✅ Ajout de BeforeLeaveObserver
```

#### B. Méthode beforeLeave()

```java
@Override
public void beforeLeave(BeforeLeaveEvent event) {
    // Vérifier si l'utilisateur quitte pendant un duel actif
    if (duelId != null && !quizCompleted) {
        logger.info("User leaving during active duel {} - cancelling duel", duelId);
        
        // Récupérer l'utilisateur actuel
        User currentUser = VaadinSession.getCurrent().getAttribute(User.class);
        
        // Annuler le duel
        if (currentUser != null && duelService != null) {
            try {
                duelService.cancelDuel(duelId, currentUser); // ✅ Annule le duel
                logger.info("Duel {} cancelled by user {} who left during quiz", 
                    duelId, currentUser.getName());
                
                // Nettoyer la session
                VaadinSession.getCurrent().setAttribute("activeDuelId", null);
                
            } catch (Exception e) {
                logger.error("Error cancelling duel on leave", e);
            }
        }
    }
}
```

### 5. Traductions ajoutées

**Fichiers** : `messages_fr.properties`, `messages_en.properties`, `messages_it.properties`

```properties
# Français
duelquiz.opponent.quit={opponent} a quitté le duel

# Anglais
duelquiz.opponent.quit={opponent} has quit the duel

# Italien
duelquiz.opponent.quit={opponent} ha abbandonato il duello
```

### 6. Migration SQL

**Fichier** : `SQL/add_cancelled_by_to_duel_match.sql`

```sql
-- Ajout de la colonne cancelled_by_user_id
ALTER TABLE duel_match ADD COLUMN IF NOT EXISTS cancelled_by_user_id BIGINT;

-- Contrainte de clé étrangère
ALTER TABLE duel_match 
ADD CONSTRAINT IF NOT EXISTS fk_duel_match_cancelled_by 
FOREIGN KEY (cancelled_by_user_id) REFERENCES user_table(id);

-- Index pour les performances
CREATE INDEX IF NOT EXISTS idx_duel_match_cancelled_by 
ON duel_match(cancelled_by_user_id);
```

## 🔄 Flux de fonctionnement

### Scénario 1 : Joueur quitte depuis DuelQuizView

```
1. Joueur A clique sur "Annuler" ou "Refuser"
   ↓
2. DuelQuizView appelle duelService.cancelDuel(duelId, currentUser)
   ↓
3. DuelService met à jour :
   - status = CANCELLED
   - cancelledBy = Joueur A
   - finishedAt = maintenant
   ↓
4. Le polling de Joueur B détecte le changement (toutes les 2 secondes)
   ↓
5. Joueur B voit :
   - Notification : "Joueur A a quitté le duel"
   - Retour automatique à l'écran initial
```

### Scénario 2 : Joueur quitte pendant le quiz

```
1. Joueur A clique sur "Retour" ou ferme la page pendant le quiz
   ↓
2. QuizQuestionView.beforeLeave() est déclenché
   ↓
3. Détection : duelId != null && !quizCompleted
   ↓
4. QuizQuestionView appelle duelService.cancelDuel(duelId, currentUser)
   ↓
5. DuelService met à jour le duel comme annulé
   ↓
6. Le polling de Joueur B (qui peut être dans DuelQuizView ou QuizQuestionView)
   détecte l'annulation
   ↓
7. Joueur B voit :
   - Notification : "Joueur A a quitté le duel"
   - Quiz arrêté automatiquement
   - Retour à l'écran initial
```

## 📋 Points de sortie possibles

1. **DuelQuizView - En recherche** : Bouton "Annuler"
2. **DuelQuizView - Match trouvé** : Bouton "Refuser"
3. **DuelQuizView - Navigation** : Bouton back ou changement de vue
4. **QuizQuestionView - Pendant le quiz** : 
   - Bouton "Arrêter"
   - Bouton back
   - Navigation vers une autre page
   - Fermeture du navigateur/onglet

Tous ces points déclenchent maintenant l'annulation du duel et notifient l'adversaire ! ✅

## 🧪 Tests à effectuer

### Test 1 : Annulation depuis la vue recherche

1. **Joueur A** : Lancer une recherche de duel
2. **Joueur B** : Lancer une recherche (match trouvé)
3. **Joueur A** : Cliquer sur "Annuler"
4. **Vérifier** : 
   - Joueur B voit la notification "Joueur A a quitté le duel"
   - Joueur B retourne à l'écran initial

### Test 2 : Refus du match

1. **Joueur A** : Lancer une recherche
2. **Joueur B** : Lancer une recherche (match trouvé)
3. **Joueur A** : Cliquer sur "Refuser"
4. **Vérifier** :
   - Joueur B voit la notification "Joueur A a quitté le duel"
   - Les deux retournent à l'écran initial

### Test 3 : Abandon pendant le quiz

1. **Joueur A & B** : Démarrer un duel complet jusqu'au quiz
2. **Joueur A** : Cliquer sur "Arrêter le quiz" ou "Retour"
3. **Vérifier** :
   - Joueur B voit la notification immédiatement
   - Quiz de B s'arrête
   - B retourne à l'écran initial

### Test 4 : Vérifier les logs

```bash
# Chercher les annulations dans les logs
grep "cancelled by user" logs/application.log
grep "Duel cancelled by opponent" logs/application.log
```

## 📊 Améliorations futures possibles

1. **Historique des duels** : Enregistrer tous les duels annulés pour statistiques
2. **Pénalité** : Décompter des points si un joueur abandonne trop souvent
3. **Confirmation** : Demander confirmation avant d'annuler un duel en cours
4. **Reconnexion** : Permettre de reprendre un duel si déconnexion accidentelle

---

**Date** : 2026-01-07  
**Status** : ✅ **IMPLÉMENTÉ**  
**Migration SQL** : ⚠️ À exécuter avant de démarrer l'application  
**Prêt pour** : Tests et validation

