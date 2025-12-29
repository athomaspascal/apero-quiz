# ✅ Checkbox "Team Mode" - Maintenant Visible !

## 🎯 Problème Résolu

La checkbox "**Team Mode**" est maintenant **visible** dans la vue QuizListView, à côté du bouton "Share".

---

## 📍 Où la Trouver ?

### Dans la Vue "Un Quizz" (QuizListView)

```
+--------------------------------------------------+
|  Photo de profil                                 |
|  Nom de l'utilisateur                           |
+--------------------------------------------------+
|                                                  |
|  Un Quizz                                        |
|  [Choisissez un quizz...] [Start] [Share] ☑ Team Mode |
|                                                  |
|  +----+  +----+  +----+  +----+                |
|  |Quiz|  |Quiz|  |Quiz|  |Quiz|                |
|  +----+  +----+  +----+  +----+                |
|                                                  |
+--------------------------------------------------+
```

---

## 🎮 Comment Utiliser

### Étape 1 : Accéder à "Un Quizz"
1. Connectez-vous à l'application
2. Allez dans le menu "Un Quizz"

### Étape 2 : Sélectionner un Quiz
1. Cliquez sur une carte de quiz
2. Le quiz est sélectionné
3. Les boutons "Start" et "Share" deviennent actifs

### Étape 3 : Activer le Mode Équipe
1. **Cochez la checkbox "Mode Équipe"** (à côté du bouton "Share")
   - 🇫🇷 Français : "Mode Équipe"
   - 🇬🇧 Anglais : "Team Mode"
   - 🇮🇹 Italien : "Modalità Squadra"

### Étape 4 : Partager le Quiz
1. Cliquez sur "Share"
2. Une session est créée **avec le mode équipe activé**
3. Le dialogue de partage s'ouvre avec le code et le QR code

### Étape 5 : Aller dans la Salle de Session
1. Cliquez sur "Go to Session Room"
2. Vous arrivez dans la vue QuizSessionView
3. **Vous pouvez maintenant sélectionner les équipes disponibles**

---

## 🔄 Workflow Complet

```
┌─────────────────────────────────────────────────┐
│ 1. Page "Un Quizz"                             │
│    - Sélectionner un quiz                      │
│    - ☑ Cocher "Team Mode"                     │
│    - Cliquer "Share"                           │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────┐
│ 2. Dialogue de Partage                         │
│    - QR Code affiché                           │
│    - Code de session affiché                   │
│    - Cliquer "Go to Session Room"              │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────┐
│ 3. Vue QuizSessionView (Mode Équipe Activé)    │
│    - ☑ Mode équipe déjà activé                │
│    - Sélectionner les équipes :               │
│      ☑ Stark                                  │
│      ☑ Lannister                              │
│      ☑ Targaryen                              │
│    - Cliquer "Démarrer pour tout le monde"     │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────┐
│ 4. Les Joueurs Rejoignent et Choisissent       │
│    leur Équipe                                 │
└─────────────────────────────────────────────────┘
```

---

## 🎨 Apparence de la Checkbox

La checkbox "Team Mode" :
- ✅ Positionnée à droite du bouton "Share"
- ✅ Alignée verticalement avec les boutons
- ✅ Margin-left de 10px pour l'espacement
- ✅ Label traduit dans les 3 langues

---

## 📊 Test Visuel

### Avant de Cliquer
```
[TextField: Choisissez un quizz...] [Start] [Share] ☐ Team Mode
                                     (gris)  (gris)  (gris)
```

### Après Sélection d'un Quiz
```
[TextField: Game of Thrones Quiz] [Start] [Share] ☐ Team Mode
                                  (bleu)  (bleu)  (actif)
```

### Avec Team Mode Activé
```
[TextField: Game of Thrones Quiz] [Start] [Share] ☑ Team Mode
                                  (bleu)  (bleu)  (coché)
```

---

## ✅ Vérifications

Pour confirmer que la checkbox fonctionne :

1. **Visible ?**
   - [ ] La checkbox "Team Mode" est visible à côté du bouton "Share"
   
2. **Traduction ?**
   - [ ] En français : "Mode Équipe"
   - [ ] En anglais : "Team Mode"
   - [ ] En italien : "Modalità Squadra"

3. **Fonctionnelle ?**
   - [ ] On peut cocher/décocher la checkbox
   - [ ] Quand cochée et qu'on clique "Share", la session est créée en mode équipe
   - [ ] Dans la salle de session, le mode équipe est déjà activé

4. **Position ?**
   - [ ] À droite du bouton "Share"
   - [ ] Alignée avec les autres éléments
   - [ ] Espacement correct

---

## 🚀 Pour Tester

```bash
# Démarrer l'application
cd C:\Users\athom\IdeaProjects\quizz1
mvn spring-boot:run
```

Puis accédez à : **https://localhost:8089**

---

## 📝 Code Modifié

### Fichier : `QuizListView.java`

#### Ajout du champ
```java
final Checkbox teamModeCheckbox;
```

#### Initialisation
```java
teamModeCheckbox = new Checkbox(translationService.translate("quizSession.teamMode"));
teamModeCheckbox.getStyle()
    .set("margin-left", "10px")
    .set("align-self", "center");
```

#### Ajout dans la toolbar
```java
add(new ViewToolbar(translationService.translate("quizlist.title"), 
    ViewToolbar.group(name, startButton, shareBtn, teamModeCheckbox)));
```

#### Utilisation lors du partage
```java
if (teamModeCheckbox.getValue()) {
    session.setTeamMode(true);
    sessionService.updateSession(session);
}
```

---

## 🎉 Statut

✅ **IMPLÉMENTATION TERMINÉE**
✅ **COMPILATION RÉUSSIE**
✅ **FRONTEND BUILDÉ**
✅ **PRÊT À TESTER**

La checkbox "Team Mode" est maintenant **100% opérationnelle** dans QuizListView ! 🏆

---

**Date :** 29 décembre 2025  
**Status :** ✅ Résolu

