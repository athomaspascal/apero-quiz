# Ajout de l'Avatar Utilisateur dans la Vue Initiale du Duel Quiz - 2026-01-08

## Problème
Dans la vue initiale du Duel Quiz (avec le bouton "Chercher un adversaire"), l'utilisateur ne voyait pas son avatar, son drapeau ni son nom, contrairement à la vue QuizListView.

## Solution Implémentée

### 1. Modification de `showInitialView()`
La méthode a été modifiée pour afficher le profil de l'utilisateur avant le titre et la description :

```java
private void showInitialView() {
    mainContent.removeAll();

    H2 title = new H2(translationService.translate("duelquiz.welcome"));
    Paragraph description = new Paragraph(translationService.translate("duelquiz.description"));

    // Add user profile section (avatar, flag, and name)
    User currentUser = VaadinSession.getCurrent().getAttribute(User.class);
    if (currentUser != null) {
        VerticalLayout userProfileSection = createUserProfileSection(currentUser);
        mainContent.add(userProfileSection);
    }

    Button searchButton = new Button(translationService.translate("duelquiz.search"), event -> startSearching());
    // ...
}
```

### 2. Nouvelle Méthode : `createUserProfileSection()`
Cette méthode crée une section de profil complète avec :

#### **Avatar Circulaire (80px × 80px)**
- **Si photo disponible** : Affichage de la photo en base64 comme image de fond
- **Si pas de photo** : Affichage des initiales sur un dégradé violet
- **Si pas de nom** : Icône par défaut 👤
- **Style** : Cercle avec ombre portée (`box-shadow: 0 4px 12px rgba(0,0,0,0.15)`)

#### **Drapeau du Pays (45px × 30px)**
- Affiché à côté de l'avatar si disponible
- SVG inséré via `innerHTML`
- Bordure arrondie avec ombre légère
- Aligné verticalement au centre

#### **Nom de l'Utilisateur**
- Affiché en dessous de l'avatar et du drapeau
- Police : 14px, poids 500
- Couleur : `#333`
- Marges : 8px en haut, 0 en bas

### 3. Nouvelle Méthode : `getInitials()`
Extrait les initiales du nom de l'utilisateur :
- **Un seul mot** : 2 premières lettres (ex: "John" → "JO")
- **Plusieurs mots** : Première lettre du premier et du dernier mot (ex: "John Doe" → "JD")
- **Nom vide** : "?"

### Code Ajouté

```java
private VerticalLayout createUserProfileSection(User currentUser) {
    VerticalLayout profileSection = new VerticalLayout();
    profileSection.setAlignItems(FlexComponent.Alignment.CENTER);
    profileSection.setSpacing(false);
    profileSection.setPadding(false);
    profileSection.getStyle().set("margin-bottom", "20px");

    // Avatar container
    Div avatarContainer = new Div();
    avatarContainer.getStyle()
        .set("width", "80px")
        .set("height", "80px")
        .set("border-radius", "50%")
        .set("overflow", "hidden")
        .set("display", "flex")
        .set("align-items", "center")
        .set("justify-content", "center")
        .set("box-shadow", "0 4px 12px rgba(0,0,0,0.15)")
        .set("cursor", "pointer");

    // Display photo, initials, or default icon
    if (currentUser.getPhotoBytes() != null && currentUser.getPhotoBytes().length > 0) {
        String base64Image = java.util.Base64.getEncoder().encodeToString(currentUser.getPhotoBytes());
        Div photoDiv = new Div();
        photoDiv.getStyle()
            .set("width", "100%")
            .set("height", "100%")
            .set("background-image", "url(data:image/jpeg;base64," + base64Image + ")")
            .set("background-size", "cover")
            .set("background-position", "center");
        avatarContainer.add(photoDiv);
    } else if (currentUser.getName() != null && !currentUser.getName().isEmpty()) {
        avatarContainer.getStyle()
            .set("background", "linear-gradient(135deg, #667eea 0%, #764ba2 100%)")
            .set("color", "white")
            .set("font-size", "32px")
            .set("font-weight", "bold");
        String initials = getInitials(currentUser.getName());
        Span initialsSpan = new Span(initials);
        avatarContainer.add(initialsSpan);
    }

    // Add flag if available
    if (currentUser.getCountry() != null && currentUser.getCountry().getCountryFlag() != null) {
        Div flagContainer = new Div();
        flagContainer.getStyle()
            .set("width", "45px")
            .set("height", "30px")
            .set("display", "flex")
            .set("align-items", "center")
            .set("justify-content", "center")
            .set("border", "1px solid #e0e0e0")
            .set("border-radius", "4px")
            .set("box-shadow", "0 2px 4px rgba(0,0,0,0.1)");
        flagContainer.getElement().setProperty("innerHTML", currentUser.getCountry().getCountryFlag());
        // ...
    }

    // Add user name
    Paragraph userName = new Paragraph(currentUser.getName());
    userName.getStyle()
        .set("margin-top", "8px")
        .set("margin-bottom", "0")
        .set("font-size", "14px")
        .set("font-weight", "500")
        .set("color", "#333");
    profileSection.add(userName);

    return profileSection;
}
```

## Résultat Visuel

### Avant
```
┌─────────────────────────┐
│  Bienvenue au Duel Quiz │
│  Chercher un adversaire │
│  [Button]               │
└─────────────────────────┘
```

### Après
```
┌─────────────────────────┐
│      ┌─────┐            │
│      │ 👤  │ 🇫🇷        │  ← Avatar + Drapeau
│      └─────┘            │
│    Isaac Newton         │  ← Nom
│                         │
│  Bienvenue au Duel Quiz │
│  Chercher un adversaire │
│  [Button]               │
└─────────────────────────┘
```

## Avantages
✅ **Cohérence visuelle** avec QuizListView
✅ **Identification claire** de l'utilisateur actuel
✅ **Design moderne** avec avatar circulaire et dégradé violet
✅ **Support des drapeaux** pour l'identité nationale
✅ **Gestion des cas** : photo, initiales, ou icône par défaut

## Fichiers Modifiés
- `src/main/java/com/quizz/core/ui/DuelQuizView.java`
  - Méthode `showInitialView()` modifiée
  - Nouvelle méthode `createUserProfileSection()`
  - Nouvelle méthode `getInitials()`

## Tests Recommandés
1. ✅ Tester avec un utilisateur ayant une photo
2. ✅ Tester avec un utilisateur sans photo (initiales)
3. ✅ Tester avec différents drapeaux de pays
4. ✅ Vérifier l'affichage sur mobile et desktop
5. ✅ Vérifier que l'avatar s'affiche avant le titre

## Notes Techniques
- **Base64** utilisé pour encoder la photo utilisateur
- **innerHTML** utilisé pour insérer le SVG du drapeau (évite les API dépréciées)
- **Gradient CSS** pour le fond des initiales (`#667eea` → `#764ba2`)
- **Layout centré** avec `FlexComponent.Alignment.CENTER`

