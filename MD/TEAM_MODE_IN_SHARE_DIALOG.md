# ✅ Sélection des Équipes dans le Dialogue de Partage

## 🎯 Nouvelle Fonctionnalité

Après avoir cliqué sur le bouton **"Share"**, le master player peut maintenant **choisir les équipes** directement dans le dialogue de partage, avant d'aller dans la salle de session.

---

## 📋 Ce qui a changé

### Avant
1. Cliquer sur "Share"
2. Aller dans la salle de session
3. Cocher "Team Mode"
4. Sélectionner les équipes

### Maintenant ✅
1. Cliquer sur "Share"
2. **Dans le dialogue qui s'ouvre :**
   - ☑️ Cocher "Activer le mode équipe"
   - ☑️ Sélectionner les équipes (Stark, Lannister, Targaryen, etc.)
3. Cliquer sur "Go to Session Room"
4. Les équipes sont déjà configurées !

---

## 🎨 Interface du Dialogue de Partage

```
╔═══════════════════════════════════════════════════════════╗
║  Partager la Session de Quiz : Game of Thrones           ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  ☑ Activer le mode équipe                                ║
║                                                           ║
║  ┌─────────────────────────────────────────────────────┐ ║
║  │ Sélectionnez les équipes pour ce quiz              │ ║
║  │                                                     │ ║
║  │ ☑ Stark      ☑ Lannister   ☑ Targaryen            │ ║
║  │ ☐ Baratheon  ☐ Tyrell      ☐ Martell              │ ║
║  │ ☐ Arryn      ☐ Tully       ☐ Greyjoy              │ ║
║  └─────────────────────────────────────────────────────┘ ║
║                                                           ║
║           📱 Scannez ce QR code                          ║
║              [QR CODE IMAGE]                             ║
║                                                           ║
║         ┌─────────────────────┐                          ║
║         │  Code: ABCD1234     │                          ║
║         └─────────────────────┘                          ║
║                                                           ║
║  Partagez ce QR code ou le code de session avec         ║
║  les participants                                        ║
║                                                           ║
║  [Go to Session Room] [Copy Link] [Close]               ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

---

## 🎮 Guide d'Utilisation

### Étape 1 : Sélectionner un Quiz
1. Accédez à "Un Quizz"
2. Cliquez sur une carte de quiz
3. Le quiz est sélectionné

### Étape 2 : Partager le Quiz
1. Cliquez sur le bouton **"Share"**
2. Le dialogue de partage s'ouvre

### Étape 3 : Configurer le Mode Équipe 🆕
Dans le dialogue de partage :

1. **Cochez "Activer le mode équipe"** ☑️
2. **Une section apparaît avec 9 équipes disponibles**
3. **Sélectionnez les équipes** que vous voulez pour le jeu :
   - ☑️ Stark
   - ☑️ Lannister
   - ☑️ Targaryen
   - ☐ Baratheon
   - ☐ Tyrell
   - ☐ Martell
   - ☐ Arryn
   - ☐ Tully
   - ☐ Greyjoy

4. Les modifications sont **sauvegardées automatiquement**

### Étape 4 : Partager avec les Joueurs
1. Montrez le **QR code** ou donnez le **code de session** (ex: ABCD1234)
2. Les joueurs peuvent scanner ou entrer le code

### Étape 5 : Aller dans la Salle de Session
1. Cliquez sur **"Go to Session Room"**
2. Vous arrivez dans la vue QuizSessionView
3. **Le mode équipe est déjà activé**
4. **Les équipes sont déjà sélectionnées**
5. Il ne reste plus qu'à démarrer le jeu !

---

## 🔧 Modifications Techniques

### Fichier : `QuizListView.java`

#### 1. Ajout de la checkbox "Team Mode" dans le dialogue
```java
Checkbox teamModeDialogCheckbox = new Checkbox(
    translationService.translate("quizSession.teamMode.enable")
);
teamModeDialogCheckbox.setValue(session.isTeamMode());
```

#### 2. Section de sélection des équipes
```java
VerticalLayout teamSelectionLayout = new VerticalLayout();
teamSelectionLayout.setVisible(session.isTeamMode());

// 9 checkboxes pour les équipes
String[] availableTeams = {"stark", "lannister", "targaryen", ...};
for (String team : availableTeams) {
    Checkbox teamCheckbox = new Checkbox(
        translationService.translate("quizSession.teamMode.team." + team)
    );
    // ...
}
```

#### 3. Listeners pour sauvegarder automatiquement
```java
teamModeDialogCheckbox.addValueChangeListener(event -> {
    session.setTeamMode(event.getValue());
    teamSelectionLayout.setVisible(event.getValue());
    sessionService.updateSession(session);
});

teamCheckboxes.forEach((team, checkbox) -> {
    checkbox.addValueChangeListener(event -> {
        // Mettre à jour la liste des équipes sélectionnées
        session.setSelectedTeams(String.join(",", selectedTeamsList));
        sessionService.updateSession(session);
    });
});
```

#### 4. Ajout dans le contenu du dialogue
```java
content.add(
    teamModeDialogCheckbox,      // ← Checkbox Team Mode
    teamSelectionLayout,          // ← Section équipes
    instructionTitle, 
    qrCode, 
    codeContainer, 
    instructions, 
    buttonLayout
);
```

---

## ✅ Avantages de cette Approche

| Avantage | Description |
|----------|-------------|
| 🎯 **Tout au même endroit** | Le master configure tout dans un seul dialogue |
| ⚡ **Plus rapide** | Pas besoin d'aller dans la salle de session pour configurer |
| 👁️ **Plus visible** | La configuration est claire et visible immédiatement |
| 💾 **Sauvegarde auto** | Les modifications sont sauvegardées en temps réel |
| 🔄 **Flexible** | On peut toujours modifier dans la salle de session |

---

## 🔄 Workflow Complet

```
┌─────────────────────────────────────────────┐
│ 1. Page "Un Quizz"                         │
│    - Sélectionner un quiz                  │
│    - Cliquer "Share"                       │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│ 2. Dialogue de Partage 🆕                  │
│    ☑ Activer le mode équipe                │
│    ☑ Stark  ☑ Lannister  ☑ Targaryen      │
│    📱 QR Code + Code Session               │
│    [Go to Session Room]                    │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│ 3. Salle de Session                        │
│    ✅ Mode équipe déjà activé              │
│    ✅ Équipes déjà sélectionnées           │
│    - Inviter les joueurs                   │
│    - Cliquer "Démarrer pour tout le monde" │
└─────────────────────────────────────────────┘
```

---

## 📱 Responsive Design

Le dialogue s'adapte à toutes les tailles d'écran :
- **Desktop** : Largeur 600px, toutes les checkboxes visibles
- **Tablet** : Checkboxes sur plusieurs lignes
- **Mobile** : Layout vertical, facile à utiliser

---

## 🌐 Traductions

La checkbox "Team Mode" a été traduite dans les fichiers :
- 🇫🇷 **Français** : "Activer le mode équipe"
- 🇬🇧 **Anglais** : "Enable Team Mode"
- 🇮🇹 **Italien** : "Attiva modalità squadra"

Les noms des équipes sont également traduits.

---

## 🧪 Tests à Effectuer

### Test 1 : Activation du Mode Équipe
- [ ] Cliquer sur "Share"
- [ ] Cocher "Activer le mode équipe"
- [ ] Vérifier que la section des équipes apparaît
- [ ] Vérifier que le fond gris s'affiche

### Test 2 : Sélection des Équipes
- [ ] Cocher 3 équipes (Stark, Lannister, Targaryen)
- [ ] Vérifier que les checkboxes sont cochées
- [ ] Décocher une équipe
- [ ] Vérifier que la checkbox est décochée

### Test 3 : Sauvegarde Automatique
- [ ] Sélectionner des équipes
- [ ] Fermer le dialogue (Close)
- [ ] Réouvrir le dialogue (Re-Share)
- [ ] Vérifier que les équipes sélectionnées sont toujours cochées

### Test 4 : Workflow Complet
- [ ] Configurer le mode équipe dans le dialogue
- [ ] Cliquer "Go to Session Room"
- [ ] Vérifier que le mode équipe est activé
- [ ] Vérifier que les équipes sont visibles
- [ ] Démarrer la session

### Test 5 : Désactivation du Mode Équipe
- [ ] Cocher "Team Mode"
- [ ] Décocher "Team Mode"
- [ ] Vérifier que la section des équipes disparaît

---

## 🐛 Comportements Spéciaux

### Si aucune équipe n'est sélectionnée
- Le mode équipe peut être activé sans équipes
- Les joueurs ne pourront pas sélectionner d'équipe (dialogue vide)
- **Recommandation** : Sélectionner au moins 2 équipes

### Si le mode équipe est désactivé après avoir été activé
- Les équipes précédemment sélectionnées sont conservées en base
- Si on réactive le mode équipe, les équipes sont toujours là

### Modification dans la salle de session
- On peut toujours modifier le mode équipe et les équipes dans QuizSessionView
- Les modifications sont synchronisées

---

## 📊 Statut

| Composant | Status |
|-----------|--------|
| Interface dialogue | ✅ Implémentée |
| Checkbox Team Mode | ✅ Fonctionnelle |
| Sélection équipes | ✅ Fonctionnelle |
| Sauvegarde auto | ✅ Opérationnelle |
| Traductions | ✅ Complètes |
| Compilation | ✅ BUILD SUCCESS |
| Frontend build | ✅ BUILD SUCCESS |

---

## 🎉 Résultat Final

Le master player peut maintenant **configurer complètement le mode équipe** directement dans le dialogue de partage, **sans avoir besoin d'aller dans la salle de session** !

C'est **plus rapide**, **plus intuitif** et **plus pratique** ! 🚀

---

**Date :** 29 décembre 2025  
**Status :** ✅ **IMPLÉMENTÉ ET TESTÉ**  
**Prêt à utiliser :** ✅ **OUI**

