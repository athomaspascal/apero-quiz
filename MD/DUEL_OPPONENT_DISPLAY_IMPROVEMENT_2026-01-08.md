# Amélioration de l'affichage de l'adversaire dans le Duel Quiz - 2026-01-08

## Problème
Lorsqu'un duel était trouvé, l'affichage de l'adversaire était simple et n'incluait pas d'icône visuelle pour représenter le joueur.

## Solution Implémentée

### Modification de `showMatchedView()` dans `DuelQuizView.java`

L'affichage de l'adversaire a été amélioré pour correspondre au style utilisé dans la liste des quiz. Il inclut maintenant :

1. **Icône de lecture (Play)** 
   - Icône bleue de 24px
   - Couleur : `#1976d2`
   - Utilise `VaadinIcon.PLAY`

2. **Drapeau du pays**
   - Dimensions : 30px × 20px
   - Affichage du SVG du drapeau du pays de l'adversaire
   - Bordure grise arrondie avec ombre légère
   - N'apparaît que si le drapeau est disponible

3. **Nom de l'adversaire**
   - Police en **gras** (`font-weight: bold`)
   - Taille de police **20% plus grande** (`font-size: 1.2em`)
   - Couleur : couleur de texte primaire Lumo

### Code Ajouté

```java
// Add play icon
com.vaadin.flow.component.icon.Icon playIcon = com.vaadin.flow.component.icon.VaadinIcon.PLAY.create();
playIcon.setSize("24px");
playIcon.getStyle().set("color", "#1976d2");
opponentLayout.add(playIcon);

// Add country flag if available
if (opponent.getCountry() != null && opponent.getCountry().getCountryFlag() != null
    && !opponent.getCountry().getCountryFlag().isEmpty()) {
    Div flagContainer = new Div();
    flagContainer.getStyle()
        .set("width", "30px")
        .set("height", "20px")
        .set("display", "flex")
        .set("align-items", "center")
        .set("justify-content", "center")
        .set("border", "1px solid #e0e0e0")
        .set("border-radius", "2px")
        .set("box-shadow", "0 1px 3px rgba(0,0,0,0.1)");
    
    flagContainer.getElement().setProperty("innerHTML", opponent.getCountry().getCountryFlag());
    opponentLayout.add(flagContainer);
}

// Add opponent name with bold and larger font
Span opponentName = new Span(opponent.getName());
opponentName.getStyle()
    .set("font-weight", "bold")
    .set("font-size", "1.2em")
    .set("color", "var(--lumo-primary-text-color)");
opponentLayout.add(opponentName);
```

### Style du conteneur

Le conteneur `opponentLayout` a également été amélioré avec :
- Fond gris léger (`var(--lumo-contrast-5pct)`)
- Padding moyen (`var(--lumo-space-m)`)
- Bordure arrondie (`var(--lumo-border-radius-m)`)

## Résultat Visuel

Avant :
```
[Adversaire : Charles Darwin 🇬🇧]
```

Après :
```
[▶️ 🇬🇧 Charles Darwin]
```

Avec :
- ▶️ = Icône de lecture bleue
- 🇬🇧 = Drapeau SVG du pays
- **Charles Darwin** = Nom en gras et plus grand

## Fichiers Modifiés
- `src/main/java/com/quizz/core/ui/DuelQuizView.java` (méthode `showMatchedView()`)

## Tests Recommandés
1. Démarrer un duel avec 2 joueurs de pays différents
2. Vérifier que l'icône de lecture est affichée
3. Vérifier que le drapeau du pays est affiché
4. Vérifier que le nom est en gras et plus grand
5. Vérifier l'affichage sur smartphone et desktop

## Notes
- Le style est cohérent avec l'affichage des quiz dans la liste
- L'icône et le drapeau sont alignés verticalement au centre
- Le conteneur a un fond gris pour mieux distinguer l'information de l'adversaire

