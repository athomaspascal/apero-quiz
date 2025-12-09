# 👤 Ajout d'un avatar utilisateur au-dessus de la liste des quiz

## Date : 10 décembre 2025

---

## 🎯 Objectif

Afficher la photo de profil de l'utilisateur (avatar) **centrée** au-dessus du label "Quiz List".

---

## ✨ Fonctionnalité ajoutée

### 1. Avatar utilisateur circulaire

Un avatar **circulaire de 80px** est affiché en haut de la page, centré :

```
        ┌──────────┐
        │    👤    │  ou  │ AB │
        └──────────┘
         John Doe
    
    ─────────────────────────
         Quiz List
    ─────────────────────────
```

### 2. Affichage intelligent

L'avatar affiche :
- **Initiales de l'utilisateur** : Si l'utilisateur est connecté et a un nom
  - 1 mot : 2 premières lettres (ex: "John" → "JO")
  - 2+ mots : Première lettre du prénom + première lettre du nom (ex: "John Doe" → "JD")
- **Icône par défaut** : 👤 si pas d'utilisateur connecté ou pas de nom

### 3. Design moderne

- **Forme** : Cercle parfait (border-radius: 50%)
- **Taille** : 80×80 pixels
- **Background** : Gradient violet (#667eea → #764ba2)
- **Texte** : Blanc, gras, 32px
- **Ombre** : Légère ombre portée pour effet 3D
- **Position** : Centré horizontalement
- **Cursor** : Pointer (préparé pour future interaction)

### 4. Nom de l'utilisateur (optionnel)

Si l'utilisateur a un nom, celui-ci est affiché sous l'avatar :
- Police : 14px, semi-gras
- Couleur : #333
- Centré
- Margin-top : 8px

---

## 🔧 Implémentation

### Méthodes ajoutées

#### `createUserProfileSection()`
Crée la section de profil utilisateur avec :
- Un conteneur vertical centré
- L'avatar circulaire
- Le nom de l'utilisateur (si disponible)

#### `getInitials(String name)`
Extrait les initiales du nom de l'utilisateur :
```java
"John" → "JO"
"John Doe" → "JD"
"Marie-Claire Martin" → "MM"
null ou "" → "?"
```

### Modifications dans le constructeur

```java
// Create user profile section
VerticalLayout userProfileSection = createUserProfileSection();

add(userProfileSection);  // Ajouté en premier
add(new ViewToolbar("Quiz List", ViewToolbar.group(name, createBtn, shareBtn)));
add(quizCardsContainer);
```

---

## 🎨 Style visuel

### Avatar

```css
width: 80px
height: 80px
border-radius: 50%
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%)
color: white
font-size: 32px
font-weight: bold
box-shadow: 0 4px 12px rgba(0,0,0,0.15)
cursor: pointer
```

### Nom utilisateur

```css
font-size: 14px
font-weight: 500
color: #333
margin-top: 8px
text-align: center
```

---

## 📱 Affichage

### Avec utilisateur connecté

```
        ┌──────────┐
        │    JD    │
        └──────────┘
         John Doe

    ════════════════════════════════
         Quiz List  [Create] [Share]
    ════════════════════════════════

    [📚]  [⚛️]  [🎖️]  [🎨]
    Gen   Phy   War   Art
```

### Sans utilisateur connecté

```
        ┌──────────┐
        │    👤    │
        └──────────┘

    ════════════════════════════════
         Quiz List  [Create] [Share]
    ════════════════════════════════

    [📚]  [⚛️]  [🎖️]  [🎨]
    Gen   Phy   War   Art
```

---

## 🔐 Intégration avec le système d'authentification

L'avatar récupère l'utilisateur connecté depuis la session Vaadin :

```java
User currentUser = VaadinSession.getCurrent().getAttribute(User.class);
```

### Cas possibles

| Situation | Affichage |
|-----------|-----------|
| Utilisateur connecté avec nom | Initiales + nom |
| Utilisateur connecté sans nom | Icône 👤 |
| Pas d'utilisateur connecté | Icône 👤 |

---

## 🚀 Évolutions futures possibles

### 1. Upload de photo
Permettre à l'utilisateur d'uploader une vraie photo de profil :
```java
if (currentUser.getProfilePhotoUrl() != null) {
    Image profileImage = new Image(currentUser.getProfilePhotoUrl(), "Profile");
    // ...
}
```

### 2. Menu déroulant
Au clic sur l'avatar, afficher un menu avec :
- Mon profil
- Paramètres
- Mes quiz
- Déconnexion

### 3. Badge de statut
Ajouter un badge indiquant le statut (en ligne, occupé, etc.)

### 4. Statistiques utilisateur
Afficher sous le nom :
- Nombre de quiz créés
- Score moyen
- Rang

---

## 📝 Fichiers modifiés

| Fichier | Modifications |
|---------|---------------|
| `QuizListView.java` | Ajout de la section profil utilisateur |

### Nouvelles méthodes

1. **`createUserProfileSection()`** - Crée la section de profil
2. **`getInitials(String name)`** - Extrait les initiales

---

## ✅ Checklist de validation

- [x] Avatar affiché au-dessus de "Quiz List"
- [x] Avatar centré horizontalement
- [x] Taille 80×80 pixels
- [x] Forme circulaire
- [x] Gradient violet
- [x] Affichage des initiales si utilisateur connecté
- [x] Affichage de l'icône par défaut si pas d'utilisateur
- [x] Nom de l'utilisateur affiché sous l'avatar
- [x] Compilation réussie
- [x] Style moderne et cohérent

---

## 🧪 Tests suggérés

### Test 1 : Avec utilisateur connecté
1. Se connecter avec un compte
2. Vérifier que les initiales s'affichent
3. Vérifier que le nom s'affiche sous l'avatar

### Test 2 : Sans utilisateur connecté
1. Se déconnecter ou supprimer la session
2. Vérifier que l'icône 👤 s'affiche

### Test 3 : Différents types de noms
- Un seul mot : "John" → "JO"
- Deux mots : "John Doe" → "JD"
- Nom composé : "Jean-Pierre Martin" → "JM"
- Nom vide : "" → "👤"

### Test 4 : Responsive
1. Tester sur différentes tailles d'écran
2. Vérifier que l'avatar reste centré

---

## 💡 Personnalisation

### Changer la couleur du gradient

Dans `createUserProfileSection()` :

```java
.set("background", "linear-gradient(135deg, #FF6B6B 0%, #FFE66D 100%)")
// Rouge-Jaune au lieu de Violet
```

### Changer la taille de l'avatar

```java
avatarContainer.getStyle()
    .set("width", "100px")    // Au lieu de 80px
    .set("height", "100px")
    .set("font-size", "40px") // Au lieu de 32px
```

### Retirer le nom sous l'avatar

Commentez cette section :

```java
// User name below avatar (optional)
if (currentUser != null && currentUser.getName() != null) {
    // ... commentez tout ce bloc
}
```

---

## 🎨 Exemple de variantes de design

### Variante 1 : Avatar carré
```java
.set("border-radius", "12px")  // Au lieu de 50%
```

### Variante 2 : Bordure
```java
.set("border", "3px solid white")
```

### Variante 3 : Gradient différent
```java
// Bleu océan
.set("background", "linear-gradient(135deg, #667eea 0%, #764ba2 100%)")

// Coucher de soleil
.set("background", "linear-gradient(135deg, #ff9a56 0%, #ff6a88 100%)")

// Forêt
.set("background", "linear-gradient(135deg, #11998e 0%, #38ef7d 100%)")
```

---

## 📊 Résumé

✅ **Avatar utilisateur ajouté**  
✅ **Centré au-dessus de la liste**  
✅ **Design moderne et élégant**  
✅ **Affichage intelligent des initiales**  
✅ **Prêt pour évolutions futures**  

---

**🎉 L'avatar utilisateur est maintenant affiché en haut de la page, centré et stylisé !**

