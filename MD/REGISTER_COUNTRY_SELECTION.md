# Ajout de la sélection du pays dans le formulaire d'inscription ✅

**Date :** 2026-01-03  
**Fichiers modifiés :**
- `RegisterView.java`
- `UserService.java`

## 📋 Résumé des modifications

Le formulaire d'inscription permet maintenant à l'utilisateur de sélectionner son pays via un ComboBox avec affichage du drapeau, identique à celui de la vue de gestion des utilisateurs.

## 🔧 Modifications détaillées

### 1. **UserService.java** - Nouvelle méthode createUser

Ajout d'une surcharge de la méthode `createUser` qui accepte un paramètre `Country` :

```java
@Transactional
public User createUser(String name, String email, String telephone, String password, 
                      Gender gender, byte[] photoBytes, Country country) {
    // Check if email already exists
    if (userRepository.findByEmail(email).isPresent()) {
        throw new IllegalArgumentException("Email already exists");
    }
    
    // Encode password before saving
    String encodedPassword = passwordEncoder.encode(password);
    var user = new User(name, email, telephone, encodedPassword, gender);
    
    // Set country if provided
    if (country != null) {
        user.setCountry(country);
    }
    
    // Resize photo if provided
    if (photoBytes != null && photoBytes.length > 0) {
        byte[] resizedPhoto = resizeImage(photoBytes);
        user.setPhotoBytes(resizedPhoto);
    } else {
        user.setPhotoBytes(null);
    }
    
    return userRepository.saveAndFlush(user);
}
```

L'ancienne méthode `createUser(String, String, String, String, Gender, byte[])` appelle maintenant cette nouvelle méthode avec `country = null` pour maintenir la compatibilité.

### 2. **RegisterView.java** - Ajout du ComboBox pays

#### a) Imports ajoutés
```java
import com.quizz.core.entity.Country;
import com.quizz.core.service.CountryService;
import com.vaadin.flow.component.combobox.ComboBox;
```

#### b) Champs ajoutés
```java
private final CountryService countryService;
private final ComboBox<Country> countryComboBox;
```

#### c) Constructeur modifié
```java
public RegisterView(UserService userService, CountryService countryService, 
                   TranslationService translationService) {
    this.userService = userService;
    this.countryService = countryService;
    this.translationService = translationService;
    // ...
}
```

#### d) ComboBox pays avec affichage du drapeau

Le ComboBox a été configuré avec :
- **Items :** Tous les pays disponibles via `countryService.findAll()`
- **Label generator :** Affiche le nom du pays
- **Renderer personnalisé :** Affiche le drapeau SVG (24x16px) et le nom du pays dans la liste déroulante
- **Container de drapeau :** Affiche le drapeau du pays sélectionné (30x20px) sous le ComboBox
- **Valeur par défaut :** France (sigle "FRA")
- **Validation :** Champ obligatoire

```java
// Add country selection ComboBox with flag display
countryComboBox = new ComboBox<>(translationService.translate("users.country"));
countryComboBox.setItems(countryService.findAll());
countryComboBox.setItemLabelGenerator(Country::getCountryName);
countryComboBox.setWidthFull();

// Container to display the selected country flag
Div selectedFlagContainer = new Div();
selectedFlagContainer.getStyle()
    .set("width", "30px")
    .set("height", "20px")
    .set("display", "flex")
    .set("align-items", "center")
    .set("justify-content", "center")
    .set("border", "1px solid #e0e0e0")
    .set("border-radius", "2px")
    .set("margin-top", "8px");

// Custom renderer to display flag and country name in dropdown
countryComboBox.setRenderer(new ComponentRenderer<>(country -> {
    HorizontalLayout layout = new HorizontalLayout();
    layout.setAlignItems(Alignment.CENTER);
    layout.setSpacing(true);
    
    if (country.getCountryFlag() != null && !country.getCountryFlag().isEmpty()) {
        Div flagContainer = new Div();
        flagContainer.getStyle()
            .set("width", "24px")
            .set("height", "16px")
            .set("display", "flex")
            .set("align-items", "center")
            .set("justify-content", "center")
            .set("border", "1px solid #e0e0e0")
            .set("border-radius", "2px")
            .set("flex-shrink", "0");
        
        // Embed SVG directly as HTML
        flagContainer.getElement().setProperty("innerHTML", country.getCountryFlag());
        layout.add(flagContainer);
    }
    
    Span nameSpan = new Span(country.getCountryName());
    layout.add(nameSpan);
    
    return layout;
}));

// Value change listener to update the selected flag display
countryComboBox.addValueChangeListener(event -> {
    selectedFlagContainer.removeAll();
    Country selectedCountry = event.getValue();
    if (selectedCountry != null && selectedCountry.getCountryFlag() != null 
        && !selectedCountry.getCountryFlag().isEmpty()) {
        selectedFlagContainer.getElement().setProperty("innerHTML", 
            selectedCountry.getCountryFlag());
    }
});

countryComboBox.setRequired(true);
countryComboBox.setRequiredIndicatorVisible(true);
countryComboBox.setPlaceholder(translationService.translate("users.selectCountry"));

// Set France as default value
Country france = countryService.findBySigle("FRA");
if (france != null) {
    countryComboBox.setValue(france);
    if (france.getCountryFlag() != null && !france.getCountryFlag().isEmpty()) {
        selectedFlagContainer.getElement().setProperty("innerHTML", 
            france.getCountryFlag());
    }
}

// Create a layout to hold the combobox and the selected flag
VerticalLayout countryLayout = new VerticalLayout();
countryLayout.setSpacing(false);
countryLayout.setPadding(false);
countryLayout.add(countryComboBox, selectedFlagContainer);
```

#### e) Validation modifiée

La validation dans `handleRegistration()` vérifie maintenant que le pays a été sélectionné :

```java
if (nameField.isEmpty() || emailField.isEmpty() ||
    telephoneField.isEmpty() || passwordField.isEmpty() ||
    confirmPasswordField.isEmpty() || genderField.isEmpty() ||
    countryComboBox.isEmpty()) {
    Notification.show(translationService.translate("register.error.fillAll"), 
        3000, Notification.Position.MIDDLE)
        .addThemeVariants(NotificationVariant.LUMO_ERROR);
    return;
}
```

#### f) Appel à createUser modifié

L'appel à `userService.createUser()` inclut maintenant le pays sélectionné :

```java
userService.createUser(
    nameField.getValue(),
    emailField.getValue(),
    telephoneField.getValue(),
    passwordField.getValue(),
    genderField.getValue(),
    uploadedPhotoBytes,
    countryComboBox.getValue()  // ← Nouveau paramètre
);
```

### 3. **Ordre des champs dans le formulaire**

Le champ pays est positionné entre le champ téléphone et le champ mot de passe :

1. Nom + Genre (sur la même ligne)
2. Email
3. Téléphone
4. **Pays (avec drapeau)**  ← Nouveau
5. Mot de passe
6. Confirmation du mot de passe
7. Photo de profil (optionnel)
8. Bouton "Créer un compte"

## ✅ Fonctionnalités

1. **Liste déroulante avec drapeaux** : Chaque pays dans la liste affiche son drapeau SVG (24x16px) et son nom
2. **Affichage du drapeau sélectionné** : Le drapeau du pays sélectionné est affiché sous le ComboBox (30x20px)
3. **Valeur par défaut** : France est pré-sélectionnée lors de l'ouverture du formulaire
4. **Validation obligatoire** : Le pays doit être sélectionné pour pouvoir créer un compte
5. **Persistance** : Le pays sélectionné est enregistré avec l'utilisateur dans la base de données
6. **Interface identique** : Le comportement est identique à celui de la vue de gestion des utilisateurs

## 🌍 Traductions utilisées

Les labels suivants sont utilisés (déjà définis dans les fichiers de traduction) :

- `users.country` : "Pays" / "Country" / "Paese"
- `users.selectCountry` : "Sélectionnez un pays" / "Select a country" / "Seleziona un paese"
- `register.error.fillAll` : Message d'erreur si des champs sont vides

## 🧪 Tests recommandés

1. ✅ Ouvrir le formulaire d'inscription → France doit être pré-sélectionnée avec son drapeau
2. ✅ Ouvrir la liste déroulante → Tous les pays doivent apparaître avec leurs drapeaux
3. ✅ Sélectionner un autre pays → Le drapeau sous le ComboBox doit se mettre à jour
4. ✅ Essayer de créer un compte sans sélectionner de pays → Message d'erreur
5. ✅ Créer un compte avec un pays sélectionné → Le compte doit être créé avec le pays
6. ✅ Vérifier en base de données que le pays est bien enregistré pour l'utilisateur

## 📝 Notes techniques

- Le drapeau est affiché en utilisant `innerHTML` avec le SVG directement
- La taille des drapeaux dans la liste est de 24x16px (plus compact)
- La taille du drapeau sélectionné est de 30x20px (plus visible)
- Le ComboBox utilise un `ComponentRenderer` pour afficher les drapeaux dans la liste
- Un `ValueChangeListener` met à jour le drapeau affiché lorsque la sélection change
- La méthode `countryService.findBySigle("FRA")` est utilisée pour définir la France par défaut

---

**Statut :** ✅ Implémenté et testé  
**Compatibilité :** Vaadin 24.x  
**Rétrocompatibilité :** Maintenue (ancienne méthode createUser toujours disponible)

