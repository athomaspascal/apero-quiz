# Correction de l'affichage redondant du Team Mode
Date : 2026-01-04

## Problème identifié

Quand le joueur maître démarrait un quiz en mode équipe depuis le menu "Team Mode" :

1. Il sélectionnait les équipes dans le menu "Team Mode"
2. Il choisissait son équipe
3. La session se créait avec `teamMode = true` et `selectedTeams` rempli
4. Quand il arrivait sur la page QuizSessionView, **la checkbox "Team Mode" et la liste de toutes les équipes s'affichaient à nouveau**
5. C'était redondant car le mode équipe était déjà configuré

### Affichage redondant

Sur l'écran de la session, on voyait :
- ☑️ Une checkbox "Activer le Mode Équipe" (déjà cochée)
- 📋 Toutes les équipes disponibles avec des checkboxes (déjà sélectionnées)
- 👥 La liste des participants
- 🚀 Le bouton "Démarrer pour tout le monde"

## Cause du problème

Dans la méthode `buildUI()` de `QuizSessionView.java`, le code affichait systématiquement la section Team Mode pour l'hôte si la session était en statut `WAITING`, **sans vérifier si les équipes avaient déjà été configurées**.

```java
// Ancien code - Affichait toujours la section Team Mode
if (isHost && session.getStatus() == QuizSession.SessionStatus.WAITING) {
    // Add Team Mode section
    VerticalLayout teamModeSection = new VerticalLayout();
    // ... affichage de la checkbox et des équipes ...
    contentWrapper.add(teamModeSection);
}
```

## Solution appliquée

Ajout d'une vérification pour ne pas afficher la section Team Mode si les équipes ont déjà été configurées :

```java
if (isHost && session.getStatus() == QuizSession.SessionStatus.WAITING) {
    // Only show Team Mode section if teams haven't been configured yet
    // (i.e., coming from regular quiz list, not from Team Mode menu)
    boolean teamsAlreadyConfigured = session.isTeamMode() && 
                                    session.getSelectedTeams() != null && 
                                    !session.getSelectedTeams().isEmpty();

    if (!teamsAlreadyConfigured) {
        // Add Team Mode section
        VerticalLayout teamModeSection = new VerticalLayout();
        // ... affichage de la checkbox et des équipes ...
        contentWrapper.add(teamModeSection);
    }

    // Le bouton "Démarrer pour tout le monde" reste affiché
    Button startButton = new Button(...);
}
```

## Logique de vérification

La variable `teamsAlreadyConfigured` est `true` si :
1. `session.isTeamMode() == true` **ET**
2. `session.getSelectedTeams() != null` **ET**
3. `session.getSelectedTeams()` n'est pas vide

Cela signifie que :
- Si on vient du menu "Team Mode" → les équipes sont déjà configurées → **pas d'affichage redondant**
- Si on vient de la liste des quiz normale → les équipes ne sont pas configurées → **affichage normal**

## Résultat

### Avant (avec redondance)

Depuis le menu "Team Mode" :
```
┌─────────────────────────────────────────┐
│ Session de Quiz: My Quiz                │
├─────────────────────────────────────────┤
│ Code: ABC123                            │
│ Statut: WAITING                         │
│                                         │
│ ☑️ Activer le Mode Équipe  ← REDONDANT │
│                                         │
│ Sélectionner les équipes:               │
│ ☑️ Stark  ☑️ Lannister  ☐ Targaryen    │
│ ← REDONDANT                             │
│                                         │
│ Participants:                           │
│ • Master Player (Stark)                 │
│                                         │
│ [Démarrer pour tout le monde]           │
└─────────────────────────────────────────┘
```

### Après (sans redondance)

Depuis le menu "Team Mode" :
```
┌─────────────────────────────────────────┐
│ Session de Quiz: My Quiz                │
├─────────────────────────────────────────┤
│ Code: ABC123                            │
│ Statut: WAITING                         │
│                                         │
│ Participants:                           │
│ • Master Player (Stark)                 │
│                                         │
│ [Démarrer pour tout le monde]           │
└─────────────────────────────────────────┘
```

### Depuis la liste des quiz normale

Le comportement reste inchangé - la section Team Mode s'affiche normalement pour permettre sa configuration :
```
┌─────────────────────────────────────────┐
│ Session de Quiz: My Quiz                │
├─────────────────────────────────────────┤
│ Code: ABC123                            │
│ Statut: WAITING                         │
│                                         │
│ ☐ Activer le Mode Équipe               │
│                                         │
│ Participants:                           │
│ • Master Player                         │
│                                         │
│ [Démarrer pour tout le monde]           │
└─────────────────────────────────────────┘
```

## Avantages de la correction

1. ✅ **Interface plus propre** - Pas de contrôles redondants
2. ✅ **Expérience utilisateur améliorée** - L'utilisateur ne voit que ce qui est pertinent
3. ✅ **Cohérence** - Le flux depuis le menu "Team Mode" est maintenant logique
4. ✅ **Pas de régression** - Le flux depuis la liste des quiz fonctionne toujours normalement

## Tests recommandés

### Scénario 1 : Depuis le menu "Team Mode"
1. Aller dans "Mode Équipe"
2. Sélectionner 2-3 équipes
3. Choisir un quiz
4. Cliquer sur "Démarrer le Quiz (Partagé)"
5. Choisir son équipe
6. **Vérifier** : Pas de checkbox Team Mode, pas de liste d'équipes
7. **Vérifier** : Le bouton "Démarrer pour tout le monde" est présent

### Scénario 2 : Depuis la liste des quiz
1. Aller dans "Démarrer un quizz"
2. Cliquer sur "Partager" sur un quiz
3. **Vérifier** : La checkbox Team Mode est visible
4. Cocher la checkbox
5. **Vérifier** : La liste des équipes apparaît
6. Sélectionner des équipes et démarrer

## Statut

✅ **RÉSOLU** - La section Team Mode ne s'affiche plus de manière redondante quand les équipes ont déjà été configurées depuis le menu "Team Mode".

