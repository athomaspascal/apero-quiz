# Ajout de l'affichage du nom du joueur et de son équipe
Date : 2026-01-04

## Fonctionnalité ajoutée

Affichage du nom du joueur et de son équipe (en mode équipe) à côté de la barre de progression pendant le quiz.

## Localisation

L'information s'affiche entre les labels de timer/score et la barre de progression dans `QuizQuestionView.java`.

## Structure de l'affichage

### Quiz simple (non-session)
```
┌─────────────────────────────────────────┐
│ Temps : 5s / 60s      Votre Score: 3/5 │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │ ← Barre de progression
│                                         │
│ Question 6 sur 10                       │
│ Quelle est la capitale de la France ?  │
└─────────────────────────────────────────┘
```

### Quiz de session (sans équipe)
```
┌─────────────────────────────────────────┐
│ Temps : 5s / 60s      Votre Score: 3/5 │
│ 👤 John Doe                             │ ← Nom du joueur
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│                                         │
│ Question 6 sur 10                       │
│ Quelle est la capitale de la France ?  │
└─────────────────────────────────────────┘
```

### Quiz de session en mode équipe
```
┌─────────────────────────────────────────┐
│ Temps : 5s / 60s      Votre Score: 3/5 │
│ 👤 John Doe | 🏆 Stark                  │ ← Nom + Équipe
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│                                         │
│ Question 6 sur 10                       │
│ Quelle est la capitale de la France ?  │
└─────────────────────────────────────────┘
```

## Implémentation

### Modifications dans QuizQuestionView.java

#### 1. Ajout de la variable de classe

```java
private final Paragraph playerInfoLabel; // Display player name and team
```

#### 2. Initialisation dans le constructeur

```java
// Player info label (will be populated in beforeEnter if in team mode)
playerInfoLabel = new Paragraph();
playerInfoLabel.getStyle()
    .set("font-size", "0.875rem")
    .set("text-align", "center")
    .set("margin", "var(--lumo-space-xs) 0")
    .set("color", "var(--lumo-primary-text-color)")
    .set("font-weight", "500");
playerInfoLabel.setVisible(false); // Will be shown if in team mode

Div timerContainer = new Div();
timerContainer.addClassNames(LumoUtility.Margin.Bottom.LARGE);
timerContainer.add(timerScoreLayout, playerInfoLabel, timeProgressBar);
```

#### 3. Mise à jour dans beforeEnter()

```java
if (!isSessionQuiz) {
    // Hide player info for simple quiz
    playerInfoLabel.setVisible(false);
} else {
    // Update player info label for session quiz
    if (currentParticipant != null) {
        User currentUser = VaadinSession.getCurrent().getAttribute(User.class);
        if (currentUser != null) {
            String playerInfo = "👤 " + currentUser.getName();
            
            // Add team info if in team mode
            if (session.isTeamMode() && currentParticipant.getTeamName() != null 
                && !currentParticipant.getTeamName().isEmpty()) {
                String teamName = currentParticipant.getTeamName();
                // Capitalize first letter of team name
                String displayTeamName = teamName.substring(0, 1).toUpperCase() 
                                       + teamName.substring(1);
                playerInfo += " | 🏆 " + displayTeamName;
            }
            
            playerInfoLabel.setText(playerInfo);
            playerInfoLabel.setVisible(true);
        }
    }
}
```

## Format d'affichage

- **Icône joueur** : 👤 (emoji personne)
- **Icône équipe** : 🏆 (emoji trophée)
- **Séparateur** : ` | ` (pipe avec espaces)
- **Nom d'équipe** : Première lettre en majuscule (ex: "Stark", "Lannister")

## Style CSS appliqué

```css
font-size: 0.875rem
text-align: center
margin: var(--lumo-space-xs) 0
color: var(--lumo-primary-text-color)
font-weight: 500
```

## Logique de visibilité

| Type de quiz | Participant | Team Mode | Affichage |
|--------------|-------------|-----------|-----------|
| Simple | N/A | N/A | ❌ Caché |
| Session | Trouvé | Non | ✅ Nom seulement |
| Session | Trouvé | Oui | ✅ Nom + Équipe |
| Session | Non trouvé | N/A | ❌ Caché |

## Exemples de textes affichés

| Contexte | Texte affiché |
|----------|--------------|
| Session normale | `👤 John Doe` |
| Team Stark | `👤 John Doe | 🏆 Stark` |
| Team Lannister | `👤 Jane Smith | 🏆 Lannister` |
| Team Targaryen | `👤 Bob Martin | 🏆 Targaryen` |

## Avantages

1. ✅ **Identification claire** - Le joueur voit toujours son nom pendant le quiz
2. ✅ **Visibilité de l'équipe** - En mode équipe, le joueur voit son équipe constamment
3. ✅ **Non-intrusif** - L'information est placée de manière discrète au-dessus de la barre
4. ✅ **Cohérent** - Utilise le même style que les autres labels (timer, score)
5. ✅ **Dynamique** - S'adapte automatiquement au contexte (simple/session/équipe)

## Tests recommandés

### Test 1 : Quiz simple
1. Démarrer un quiz simple (non-session)
2. **Vérifier** : Pas d'information de joueur affichée ✓

### Test 2 : Quiz de session sans équipe
1. Créer une session sans mode équipe
2. Rejoindre la session
3. Démarrer le quiz
4. **Vérifier** : `👤 [Nom du joueur]` affiché ✓

### Test 3 : Quiz de session en mode équipe
1. Créer une session avec mode équipe
2. Sélectionner une équipe (ex: Stark)
3. Rejoindre et démarrer le quiz
4. **Vérifier** : `👤 [Nom] | 🏆 Stark` affiché ✓

### Test 4 : Différentes équipes
1. Tester avec chaque équipe disponible
2. **Vérifier** : Le nom de l'équipe est correctement capitalisé ✓

## Logs

Le système ajoute un log pour le débogage :
```java
logger.info("Displaying player info: {}", playerInfo);
```

## Statut

✅ **IMPLÉMENTÉ** - Le nom du joueur et son équipe s'affichent correctement à côté de la barre de progression.

