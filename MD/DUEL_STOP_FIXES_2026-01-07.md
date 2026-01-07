# Fix des Problèmes de Duel Quiz - Arrêt par un Joueur - 2026-01-07

## 🐛 Problèmes identifiés

Lors d'un duel entre Isaac Newton et Marie Curie, quand Isaac arrête le quiz :

### Problème 1 : Marie Curie ne reçoit pas de notification
- ❌ **Symptôme** : Marie Curie continue son quiz normalement sans savoir qu'Isaac a quitté
- **Cause** : Le duel n'était pas annulé quand Isaac cliquait sur "Arrêter"

### Problème 2 : Isaac voit "waiting an adversary" au lieu de la vue par défaut
- ❌ **Symptôme** : Isaac voit un écran d'attente alors qu'il voulait quitter
- **Cause** : L'application naviguait vers `duel-quiz` mais ne nettoyait pas le `currentDuel`

## ✅ Solutions implémentées

### Fix 1 : Annulation du duel dans `stopQuiz()`

**Fichier** : `QuizQuestionView.java`

Ajout de la gestion d'annulation du duel quand le joueur clique sur "Arrêter" :

```java
private void stopQuiz() {
    logger.info("stopQuiz() called - isDuel: {}, duelId: {}", duelId != null, duelId);
    
    // If this is a duel, cancel it
    if (duelId != null) {
        User currentUser = VaadinSession.getCurrent().getAttribute(User.class);
        if (currentUser != null && duelService != null) {
            try {
                duelService.cancelDuel(duelId, currentUser);
                logger.info("Duel {} cancelled by user {} who stopped the quiz", 
                    duelId, currentUser.getName());
                
                // Clean up session
                VaadinSession.getCurrent().setAttribute("activeDuelId", null);
                
                // Navigate back to duel view
                stopTimer();
                getUI().ifPresent(ui -> ui.navigate("duel-quiz"));
                return; // Exit early, don't show final score
            } catch (Exception e) {
                logger.error("Error cancelling duel on stop", e);
            }
        }
    }
    
    // Stop the timer
    stopTimer();
    // ... reste du code normal pour non-duel
}
```

**Comportement** :
- ✅ Détecte si c'est un duel (`duelId != null`)
- ✅ Appelle `cancelDuel()` avec l'utilisateur qui arrête
- ✅ Nettoie la session
- ✅ Redirige vers `duel-quiz` (vue initiale)
- ✅ Sort immédiatement sans afficher le score

### Fix 2 : Dialog avec bouton de fermeture pour l'adversaire

**Fichier** : `DuelQuizView.java`

Remplacement de la simple `Notification` par un **Dialog modal** avec bouton "Fermer" :

```java
// Check if duel was cancelled by opponent
if (oldDuel.getStatus() != DuelMatch.DuelStatus.CANCELLED &&
    currentDuel.getStatus() == DuelMatch.DuelStatus.CANCELLED &&
    currentDuel.getCancelledBy() != null) {
    
    User cancelledByUser = currentDuel.getCancelledBy();
    if (!cancelledByUser.getId().equals(currentUser.getId())) {
        // Opponent cancelled the duel
        logger.info("Duel cancelled by opponent: {}", cancelledByUser.getName());
        
        String message = translationService.translate("duelquiz.opponent.quit")
            .replace("{opponent}", cancelledByUser.getName());
        
        // Create a Dialog with close button
        Dialog dialog = new Dialog();
        dialog.setModal(true);
        dialog.setCloseOnEsc(false);
        dialog.setCloseOnOutsideClick(false);
        
        Div content = new Div();
        H2 title = new H2(translationService.translate("duelquiz.cancelled"));
        title.getStyle().set("margin-top", "0");
        
        Paragraph text = new Paragraph(message);
        text.getStyle()
            .set("font-size", "16px")
            .set("color", "#d32f2f");
        
        Button closeButton = new Button(
            translationService.translate("button.close"), 
            event -> {
                dialog.close();
                // Navigate to initial view after closing
                currentDuel = null;
                showInitialView();
            });
        closeButton.addThemeVariants(ButtonVariant.LUMO_PRIMARY);
        closeButton.getStyle().set("width", "100%").set("margin-top", "20px");
        
        content.add(title, text, closeButton);
        content.getStyle()
            .set("padding", "20px")
            .set("text-align", "center");
        
        dialog.add(content);
        dialog.open();
        
        return;
    }
}
```

**Comportement** :
- ✅ Affiche un **Dialog modal** (pas seulement une notification éphémère)
- ✅ Titre : "Duel Annulé"
- ✅ Message : "Isaac Newton a quitté le duel"
- ✅ Bouton "Fermer" pour fermer manuellement
- ✅ Après fermeture → Retour à la vue initiale du duel
- ✅ Impossible de fermer en cliquant à l'extérieur ou avec Échap

### Fix 3 : Traductions ajoutées

**Fichiers** : `messages_*.properties`

```properties
# Français
duelquiz.cancelled=Duel Annulé
button.close=Fermer

# Anglais
duelquiz.cancelled=Duel Cancelled
button.close=Close

# Italien
duelquiz.cancelled=Duello Annullato
button.close=Chiudi
```

## 🎬 Scénarios de test

### Scénario 1 : Isaac arrête pendant le quiz

**Avant** :
```
Isaac clique "Arrêter"
  ↓
Isaac voit "Waiting an adversary" ❌
Marie continue son quiz ❌
```

**Après** :
```
Isaac clique "Arrêter"
  ↓
Duel annulé avec Isaac comme cancelledBy
  ↓
Isaac → Vue initiale "Chercher un Adversaire" ✅
  
Marie (dans son quiz) : Polling détecte l'annulation
  ↓
Dialog s'affiche :
┌─────────────────────────────────────┐
│ Duel Annulé                         │
│                                     │
│ Isaac Newton a quitté le duel      │
│                                     │
│ [Fermer]                            │
└─────────────────────────────────────┘
  ↓
Marie clique "Fermer"
  ↓
Marie → Vue initiale "Chercher un Adversaire" ✅
```

### Scénario 2 : Isaac arrête depuis DuelQuizView

**Déjà fonctionnel**, mais maintenant cohérent :
- Isaac clique "Annuler" ou "Refuser"
- Marie voit le Dialog "Isaac Newton a quitté le duel"
- Les deux retournent à la vue initiale

### Scénario 3 : Isaac ferme le navigateur pendant le quiz

**Déjà fonctionnel** via `beforeLeave()` :
- `beforeLeave()` détecte la fermeture
- Duel annulé
- Marie voit le Dialog

## 🔄 Flux complet

```
┌─────────────────────────────────────────────────────────┐
│ Isaac Newton (pendant le quiz)                          │
│ ↓ Clique "Arrêter"                                      │
│ stopQuiz() détecte duelId != null                       │
│ ↓ Appelle cancelDuel(duelId, Isaac)                     │
│ ↓ Status = CANCELLED, cancelledBy = Isaac              │
│ ↓ Navigate("duel-quiz")                                 │
│ ↓ showInitialView() affiché                            │
│ ✅ Vue : "Chercher un Adversaire"                       │
└─────────────────────────────────────────────────────────┘
                        ↓
                  Polling toutes les 2s
                        ↓
┌─────────────────────────────────────────────────────────┐
│ Marie Curie (dans son quiz)                             │
│ ↓ Polling détecte status = CANCELLED                    │
│ ↓ cancelledBy = Isaac (pas Marie)                       │
│ ↓ Dialog s'ouvre avec message                           │
│ ┌───────────────────────────────────────┐               │
│ │ Duel Annulé                           │               │
│ │ Isaac Newton a quitté le duel        │               │
│ │ [Fermer]                              │               │
│ └───────────────────────────────────────┘               │
│ ↓ Marie clique "Fermer"                                 │
│ ↓ dialog.close()                                        │
│ ↓ currentDuel = null                                    │
│ ↓ showInitialView()                                     │
│ ✅ Vue : "Chercher un Adversaire"                       │
└─────────────────────────────────────────────────────────┘
```

## 📊 Comparaison Avant/Après

| Situation | ❌ Avant | ✅ Après |
|-----------|---------|---------|
| Isaac arrête le quiz | "Waiting adversary" | Vue initiale |
| Marie notifiée ? | Non | Oui (Dialog) |
| Type notification Marie | N/A | Dialog modal avec bouton |
| Fermeture notification | N/A | Clic sur "Fermer" |
| Après fermeture Dialog | N/A | Vue initiale |
| Duel annulé ? | Non | Oui |
| cancelledBy enregistré ? | Non | Oui (Isaac) |

## 🧪 Tests à effectuer

### Test 1 : Arrêt pendant le quiz

1. **Isaac** : Se connecter, lancer un duel avec Marie
2. **Marie** : Accepter le duel, commencer le quiz
3. **Isaac & Marie** : Répondre à 2-3 questions
4. **Isaac** : Cliquer sur "Arrêter"
5. **Vérifier Isaac** :
   - ✅ Voit immédiatement la vue initiale "Chercher un Adversaire"
   - ✅ Pas de "waiting adversary"
6. **Vérifier Marie** :
   - ✅ Voit le Dialog "Isaac Newton a quitté le duel" en < 2 secondes
   - ✅ Le Dialog est modal (ne peut pas cliquer ailleurs)
   - ✅ Bouton "Fermer" visible
7. **Marie** : Cliquer sur "Fermer"
8. **Vérifier Marie** :
   - ✅ Dialog se ferme
   - ✅ Vue initiale "Chercher un Adversaire" affichée

### Test 2 : Vérifier les logs

```bash
grep "cancelled by user.*who stopped the quiz" logs/application.log
grep "Duel cancelled by opponent" logs/application.log
```

Devrait voir :
```
Duel XXX cancelled by user Isaac Newton who stopped the quiz
Duel cancelled by opponent: Isaac Newton
```

## 📝 Fichiers modifiés

1. `QuizQuestionView.java` - Ajout de l'annulation dans `stopQuiz()`
2. `DuelQuizView.java` - Remplacement Notification → Dialog
3. `messages_fr.properties` - Traductions françaises
4. `messages_en.properties` - Traductions anglaises
5. `messages_it.properties` - Traductions italiennes

## 🎯 Améliorations implémentées

✅ **Annulation automatique** quand le joueur arrête le quiz  
✅ **Dialog modal** au lieu d'une notification éphémère  
✅ **Bouton de fermeture** explicite pour l'adversaire  
✅ **Retour à la vue initiale** pour les deux joueurs  
✅ **Cohérence** : même comportement que l'annulation depuis DuelQuizView  
✅ **Traductions** complètes FR/EN/IT  

---

**Date** : 2026-01-07  
**Status** : ✅ **CORRIGÉ ET COMPILÉ**  
**Prêt pour** : Tests et validation

