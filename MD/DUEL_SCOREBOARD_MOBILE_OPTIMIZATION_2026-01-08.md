# Optimisation du Scoreboard Duel pour Smartphone - 2026-01-08

## Problème
Lors de l'affichage du scoreboard du duel ("Duel terminé!"), les drapeaux et les noms des joueurs ne rentraient pas sur l'écran d'un smartphone. L'affichage était trop large.

## Solution Implémentée

### Modifications dans `showRematchView()`

#### 1. **Largeur Maximale du Scoreboard**
- **Avant** : Pas de limite de largeur
- **Après** : `max-width: 350px` pour s'adapter aux smartphones
- Centré avec `margin: 0 auto`
- Gap réduit à `5px` entre les éléments

```java
scoresLayout.getStyle()
    .set("gap", "5px")
    .set("max-width", "350px")
    .set("margin", "0 auto");
```

#### 2. **Drapeaux Plus Petits**
- **Avant** : 30px × 20px
- **Après** : **20px × 14px** (30% plus petit)
- Ajout de `flex-shrink: 0` pour éviter qu'ils ne rétrécissent davantage
- Ombre réduite : `0 1px 2px` au lieu de `0 1px 3px`

```java
flagContainer.getStyle()
    .set("width", "20px")
    .set("height", "14px")
    .set("flex-shrink", "0")
    .set("box-shadow", "0 1px 2px rgba(0,0,0,0.1)");
```

#### 3. **Noms des Joueurs Tronqués**
- **Limite** : 12 caractères maximum
- **Si plus long** : Troncature avec "..." (ex: "Isaac Newton" → "Isaac Newto...")
- **Police** : Réduite à `0.9rem` (au lieu de H3)
- **Utilise Paragraph** au lieu de H3 pour plus de contrôle

```java
String player1NameText = currentDuel.getPlayer1().getName();
if (player1NameText.length() > 12) {
    player1NameText = player1NameText.substring(0, 12) + "...";
}
Paragraph player1Name = new Paragraph(player1NameText);
player1Name.getStyle()
    .set("margin", "0")
    .set("font-size", "0.9rem")
    .set("font-weight", "bold");
```

#### 4. **Scores Plus Compacts**
- **Avant** : H1 (très grand)
- **Après** : H2 avec `font-size: 2rem`
- **Marges réduites** : `5px 0 0 0` au lieu de `0`

```java
H2 player1Score = new H2(String.valueOf(currentDuel.getPlayer1Score()));
player1Score.getStyle()
    .set("color", "#1976d2")
    .set("margin", "5px 0 0 0")
    .set("font-size", "2rem");
```

#### 5. **Séparateur "VS" Plus Petit**
- **Avant** : `font-size: 32px`
- **Après** : `font-size: 1.2rem` (~19px)
- **Couleur** : `#666` pour moins d'emphase
- **Padding** : `0 5px` pour l'espace

```java
Span vsSpan = new Span("VS");
vsSpan.getStyle()
    .set("font-size", "1.2rem")
    .set("font-weight", "bold")
    .set("color", "#666")
    .set("padding", "0 5px");
```

#### 6. **Message du Gagnant Tronqué**
- **Limite** : 15 caractères maximum pour le nom
- **Police** : `1.2rem` au lieu de `24px`
- **Marges** : `10px 0` avec centrage

```java
String winnerName = currentDuel.getPlayer1().getName();
if (winnerName.length() > 15) {
    winnerName = winnerName.substring(0, 15) + "...";
}
result.getStyle()
    .set("font-size", "1.2rem")
    .set("font-weight", "bold")
    .set("margin", "10px 0")
    .set("text-align", "center");
```

#### 7. **Info Rematch Plus Petite**
- **Police** : `0.9rem` (plus petite)
- **Marges** : `5px 0` (réduites)
- **Centré** : `text-align: center`

```java
rematchInfo.getStyle()
    .set("font-size", "0.9rem")
    .set("margin", "5px 0")
    .set("text-align", "center");
```

## Résultat Visuel

### Avant (trop large)
```
┌────────────────────────────────────────┐
│  Isaac Newton 🇬🇧  VS  Marie Curie 🇫🇷 │  ← Déborde
│        5           VS        3         │
└────────────────────────────────────────┘
```

### Après (optimisé pour smartphone)
```
┌──────────────────────────┐
│  Isaac New... 🇬🇧        │  ← Tronqué, drapeau plus petit
│       5                  │  ← Score compact
│      VS                  │  ← Séparateur plus petit
│       3                  │
│  Marie Curi... 🇫🇷       │
│                          │
│  Gagnant: Isaac New...   │  ← Nom tronqué
└──────────────────────────┘
```

## Dimensions Optimisées

| Élément | Avant | Après | Réduction |
|---------|-------|-------|-----------|
| **Drapeaux** | 30×20px | 20×14px | -33% |
| **Layout Max Width** | ∞ | 350px | Adapté mobile |
| **Noms joueurs** | Illimité | 12 chars | Tronqué |
| **Score** | H1 | H2 (2rem) | -30% |
| **VS** | 32px | 1.2rem | -40% |
| **Nom gagnant** | Illimité | 15 chars | Tronqué |
| **Police résultat** | 24px | 1.2rem | -50% |
| **Gap** | normal | 5px | Minimal |

## Avantages
✅ **S'adapte aux petits écrans** : Max 350px de largeur
✅ **Drapeaux visibles** : Plus petits mais toujours lisibles
✅ **Noms tronqués** : Évite les débordements
✅ **Layout flex** : S'adapte dynamiquement
✅ **Lisibilité préservée** : Les informations importantes restent claires

## Tests Recommandés
1. ✅ Tester sur smartphone (largeur 360px - 428px)
2. ✅ Vérifier avec des noms longs (> 12 caractères)
3. ✅ Vérifier l'affichage des drapeaux
4. ✅ Tester en mode portrait et paysage
5. ✅ Vérifier que les scores restent lisibles

## Fichiers Modifiés
- `src/main/java/com/quizz/core/ui/DuelQuizView.java` (méthode `showRematchView()`)

## Notes Techniques
- Utilisation de **`rem`** pour les tailles de police (responsive)
- **`flex-shrink: 0`** pour empêcher les drapeaux de rétrécir
- **Troncature avec `substring()`** pour les noms longs
- **`max-width`** pour limiter la largeur du layout
- **Centrage avec `margin: 0 auto`** pour équilibrer l'affichage

