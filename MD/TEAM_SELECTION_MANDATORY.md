# Sélection d'équipe obligatoire en Mode Équipe

## 📋 Modification effectuée

La sélection d'équipe est maintenant **obligatoire** pour tous les joueurs (y compris le master player/host) lorsqu'une session est initiée en "Team Mode".

## 🎯 Règles implémentées

### Règle 1 : Le master player (host) doit choisir son équipe
**Avant de démarrer la session pour tout le monde**, le host doit obligatoirement sélectionner son équipe.

### Règle 2 : Les joueurs doivent choisir leur équipe  
**Avant de commencer le quiz**, chaque joueur qui rejoint une session en mode équipe doit obligatoirement choisir son équipe.

## 📁 Fichiers modifiés

### 1. QuizSessionView.java

#### A. Validation pour le host avant de démarrer

```java
private void startQuizSession() {
    // Check if team mode is enabled and host has selected a team
    if (session.isTeamMode()) {
        User currentUser = VaadinSession.getCurrent().getAttribute(User.class);
        QuizParticipant hostParticipant = sessionService.getParticipant(session, currentUser);
        
        if (hostParticipant == null || hostParticipant.getTeamName() == null || hostParticipant.getTeamName().isEmpty()) {
            // Host must select a team first
            showTeamSelectionDialogForHost(currentUser);
            return;
        }
    }
    
    sessionService.updateSessionStatus(session, QuizSession.SessionStatus.ACTIVE);
    buildUI();
}
```

**Comportement :**
- Si le host n'a pas sélectionné d'équipe et clique sur "Start All"
- Un dialogue s'affiche **obligeant** le host à choisir son équipe
- Le dialogue ne peut pas être fermé (pas de bouton Cancel, pas de clic dehors)
- Une fois l'équipe sélectionnée, la session démarre automatiquement

#### B. Nouvelle méthode showTeamSelectionDialogForHost

```java
private void showTeamSelectionDialogForHost(User currentUser) {
    Dialog dialog = new Dialog();
    dialog.setHeaderTitle(translationService.translate("quizSession.teamMode.selectTeam"));
    dialog.setWidth("400px");
    dialog.setCloseOnOutsideClick(false);  // Cannot close by clicking outside
    dialog.setCloseOnEsc(false);           // Cannot close with ESC key

    // ...existing code for team selection...

    Paragraph instruction = new Paragraph(
        translationService.translate("quizSession.teamMode.host.selectTeamBeforeStart")
    );
    instruction.getStyle()
        .set("color", "var(--lumo-error-color)")
        .set("font-weight", "bold");

    // No cancel button - team selection is mandatory
    buttonLayout.add(confirmButton);
    
    // After confirmation, start the session automatically
    Button confirmButton = new Button(..., event -> {
        String selectedTeam = teamRadioGroup.getValue();
        if (selectedTeam != null && participant != null) {
            sessionService.updateParticipantTeam(participant, selectedTeam);
            dialog.close();
            sessionService.updateSessionStatus(session, QuizSession.SessionStatus.ACTIVE);
            buildUI();
        }
    });
}
```

**Caractéristiques du dialogue pour le host :**
- ❌ **Pas de bouton "Cancel"**
- ❌ **Impossible de fermer avec ESC**
- ❌ **Impossible de fermer en cliquant dehors**
- ⚠️ **Message en rouge et gras** : "En tant qu'hôte, vous devez sélectionner votre équipe..."
- ✅ **Bouton "Confirm" actif seulement si une équipe est sélectionnée**
- ✅ **Après confirmation, la session démarre automatiquement**

#### C. Modification de showTeamSelectionDialog pour les joueurs

```java
private void showTeamSelectionDialog(User currentUser) {
    Dialog dialog = new Dialog();
    dialog.setHeaderTitle(translationService.translate("quizSession.teamMode.selectTeam"));
    dialog.setWidth("400px");
    dialog.setCloseOnOutsideClick(false);  // Cannot close by clicking outside
    dialog.setCloseOnEsc(false);           // Cannot close with ESC key

    // ...existing code...

    // No cancel button - team selection is mandatory in team mode
    buttonLayout.add(confirmButton);
}
```

**Caractéristiques du dialogue pour les joueurs :**
- ❌ **Pas de bouton "Cancel"**
- ❌ **Impossible de fermer avec ESC**
- ❌ **Impossible de fermer en cliquant dehors**
- ✅ **Bouton "Confirm" actif seulement si une équipe est sélectionnée**
- ✅ **Après confirmation, le quiz démarre**

### 2. Fichiers de traduction

#### messages_en.properties
```properties
quizSession.teamMode.selectTeam=Select your team
quizSession.teamMode.selectTeamMessage=Please choose a team before starting the quiz
quizSession.teamMode.host.selectTeamBeforeStart=As the host, you must select your team before starting the session for everyone
quizSession.teamMode.confirmTeam=Confirm Team
```

#### messages_fr.properties
```properties
quizSession.teamMode.selectTeam=Sélectionnez votre équipe
quizSession.teamMode.selectTeamMessage=Veuillez choisir une équipe avant de commencer le quiz
quizSession.teamMode.host.selectTeamBeforeStart=En tant qu'hôte, vous devez sélectionner votre équipe avant de démarrer la session pour tout le monde
quizSession.teamMode.confirmTeam=Confirmer l'Équipe
```

#### messages_it.properties
```properties
quizSession.teamMode.selectTeam=Seleziona la tua squadra
quizSession.teamMode.selectTeamMessage=Per favore scegli una squadra prima di iniziare il quiz
quizSession.teamMode.host.selectTeamBeforeStart=Come host, devi selezionare la tua squadra prima di avviare la sessione per tutti
quizSession.teamMode.confirmTeam=Conferma Squadra
```

#### messages.properties (par défaut)
```properties
quizSession.teamMode.selectTeam=Select your team
quizSession.teamMode.selectTeamMessage=Please choose a team before starting the quiz
quizSession.teamMode.host.selectTeamBeforeStart=As the host, you must select your team before starting the session for everyone
quizSession.teamMode.confirmTeam=Confirm Team
```

## 🎯 Flux d'utilisation

### Scénario 1 : Master player (Host)

1. **Le host crée une session en mode équipe**
2. **Il active "Team Mode" et sélectionne les équipes disponibles** (ex: Stark, Lannister)
3. **Il clique sur "Start for everyone"**
4. **❌ Validation : Le host n'a pas encore choisi son équipe**
5. **📝 Un dialogue s'affiche avec un message en rouge** : "En tant qu'hôte, vous devez sélectionner votre équipe..."
6. **Le host ne peut pas fermer ce dialogue** (pas de cancel, pas d'ESC, pas de clic dehors)
7. **Le host sélectionne son équipe** (ex: Stark)
8. **Le bouton "Confirm" devient actif**
9. **Le host clique sur "Confirm"**
10. **✅ La session démarre automatiquement pour tous les joueurs**

### Scénario 2 : Joueur qui rejoint

1. **Un joueur rejoint une session en mode équipe**
2. **Il voit la liste des participants et le statut "WAITING" ou "ACTIVE"**
3. **Il clique sur "Start Mine" (Démarrer mon quiz)**
4. **📝 Un dialogue s'affiche** : "Veuillez choisir une équipe avant de commencer le quiz"
5. **Le joueur ne peut pas fermer ce dialogue** (pas de cancel, pas d'ESC, pas de clic dehors)
6. **Le joueur sélectionne son équipe** (ex: Lannister)
7. **Le bouton "Confirm" devient actif**
8. **Le joueur clique sur "Confirm"**
9. **✅ Son équipe est enregistrée et le quiz démarre**

## 📊 Matrice de validation

| Acteur | Mode | Équipe sélectionnée | Action | Résultat |
|--------|------|---------------------|--------|----------|
| **Host** | Team Mode | ❌ Non | Clic "Start All" | Dialogue obligatoire s'affiche |
| **Host** | Team Mode | ✅ Oui | Clic "Start All" | Session démarre directement |
| **Host** | Normal | - | Clic "Start All" | Session démarre directement |
| **Joueur** | Team Mode | ❌ Non | Clic "Start Mine" | Dialogue obligatoire s'affiche |
| **Joueur** | Team Mode | ✅ Oui | Clic "Start Mine" | Quiz démarre directement |
| **Joueur** | Normal | - | Clic "Start Mine" | Quiz démarre directement |

## 🔒 Protection

### Dialogue non fermable

Les dialogues de sélection d'équipe sont configurés pour être **obligatoires** :

```java
dialog.setCloseOnOutsideClick(false);  // Impossible de fermer en cliquant dehors
dialog.setCloseOnEsc(false);           // Impossible de fermer avec ESC
// Pas de bouton "Cancel" dans le layout
```

### Validation côté serveur

La méthode `startQuizSession()` vérifie **côté serveur** que le host a bien une équipe avant de démarrer :

```java
if (session.isTeamMode()) {
    QuizParticipant hostParticipant = sessionService.getParticipant(session, currentUser);
    if (hostParticipant == null || hostParticipant.getTeamName() == null || hostParticipant.getTeamName().isEmpty()) {
        // Force team selection
        showTeamSelectionDialogForHost(currentUser);
        return;
    }
}
```

## 🎨 Interface utilisateur

### Pour le host (message d'erreur en rouge)

```
┌─────────────────────────────────────┐
│ Sélectionnez votre équipe          │
├─────────────────────────────────────┤
│                                     │
│ ⚠️ En tant qu'hôte, vous devez     │
│    sélectionner votre équipe avant │
│    de démarrer la session pour     │
│    tout le monde                   │
│                                     │
│ Mode Équipe                         │
│ ○ Stark                            │
│ ○ Lannister                        │
│ ○ Targaryen                        │
│                                     │
│       [Confirmer l'Équipe]         │
└─────────────────────────────────────┘
```

### Pour les joueurs (message normal)

```
┌─────────────────────────────────────┐
│ Sélectionnez votre équipe          │
├─────────────────────────────────────┤
│                                     │
│ Veuillez choisir une équipe avant  │
│ de commencer le quiz               │
│                                     │
│ Mode Équipe                         │
│ ○ Stark                            │
│ ○ Lannister                        │
│ ○ Targaryen                        │
│                                     │
│       [Confirmer l'Équipe]         │
└─────────────────────────────────────┘
```

## ✅ Résumé des modifications

- ✅ **Host obligé de choisir son équipe** avant de démarrer la session
- ✅ **Joueurs obligés de choisir leur équipe** avant de commencer le quiz
- ✅ **Dialogues non fermables** (pas de cancel, pas d'ESC, pas de clic dehors)
- ✅ **Message spécial en rouge pour le host** (plus visible)
- ✅ **Traductions complètes** (EN, FR, IT + messages.properties)
- ✅ **Validation côté serveur** pour le host
- ✅ **Bouton "Confirm" actif seulement** si une équipe est sélectionnée
- ✅ **Aucune erreur de compilation** (que des warnings mineurs)

## 🧪 Tests à effectuer

### Test 1 : Host sans équipe
- [ ] Créer une session en Team Mode
- [ ] Sélectionner des équipes (ex: Stark, Lannister)
- [ ] Ne PAS choisir son équipe
- [ ] Cliquer sur "Start for everyone"
- [ ] ✅ Dialogue obligatoire s'affiche avec message en rouge
- [ ] ✅ Impossible de fermer avec ESC ou clic dehors
- [ ] ✅ Bouton "Confirm" grisé
- [ ] Sélectionner une équipe
- [ ] ✅ Bouton "Confirm" activé
- [ ] Cliquer "Confirm"
- [ ] ✅ Session démarre automatiquement

### Test 2 : Host avec équipe
- [ ] Créer une session en Team Mode
- [ ] Choisir son équipe d'abord (via le dialogue joueur)
- [ ] Cliquer sur "Start for everyone"
- [ ] ✅ Session démarre directement sans dialogue

### Test 3 : Joueur sans équipe
- [ ] Rejoindre une session en Team Mode
- [ ] Cliquer sur "Start Mine"
- [ ] ✅ Dialogue obligatoire s'affiche
- [ ] ✅ Impossible de fermer avec ESC ou clic dehors
- [ ] Sélectionner une équipe
- [ ] Cliquer "Confirm"
- [ ] ✅ Quiz démarre

### Test 4 : Joueur avec équipe
- [ ] Rejoindre une session en Team Mode
- [ ] Cliquer sur "Start Mine" une première fois (choisir équipe)
- [ ] Terminer le quiz
- [ ] Cliquer à nouveau sur "Start Mine"
- [ ] ✅ Quiz démarre directement (équipe déjà enregistrée)

## 📝 Notes importantes

1. **Le choix d'équipe est persistant** : Une fois qu'un joueur a choisi son équipe, il n'a pas besoin de la rechoisir pour les prochains quiz de la même session.

2. **Le host est un participant** : Le host doit aussi choisir une équipe car il peut aussi jouer au quiz.

3. **Équipes pré-sélectionnées** : Si le joueur a déjà une équipe enregistrée, elle est pré-sélectionnée dans le dialogue.

4. **Message différent pour le host** : Le message pour le host est en rouge et gras pour qu'il soit plus visible et explicite.

5. **Pas de contournement possible** : Les dialogues ne peuvent pas être fermés sans sélectionner une équipe.

---

**🎉 La sélection d'équipe est maintenant obligatoire pour tous les joueurs en mode équipe !**

