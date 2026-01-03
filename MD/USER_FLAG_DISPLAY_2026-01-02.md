# Affichage du drapeau du pays de l'utilisateur - 2026-01-02

## Objectif
Afficher le drapeau du pays de l'utilisateur à côté de son avatar dans la vue QuizListView.

## Modifications effectuées

### Fichier modifié: QuizListView.java
**Emplacement:** `src/main/java/com/quizz/core/ui/QuizListView.java`

### Changements dans `createUserProfileSection()`

#### 1. Création d'un layout horizontal pour avatar + drapeau
Au lieu d'afficher uniquement l'avatar, un `HorizontalLayout` a été créé pour contenir :
- L'avatar de l'utilisateur (photo ou initiales)
- Le drapeau du pays (si disponible)

```java
HorizontalLayout avatarAndFlagLayout = new HorizontalLayout();
avatarAndFlagLayout.setAlignItems(HorizontalLayout.Alignment.CENTER);
avatarAndFlagLayout.setSpacing(true);
avatarAndFlagLayout.getStyle().set("gap", "10px");
```

#### 2. Affichage du drapeau du pays
Si l'utilisateur a un pays associé :
- Le SVG du drapeau est récupéré depuis `user.getCountry().getCountryFlag()`
- Le SVG est redimensionné de 30x20px à 45x30px (1.5x)
- Un conteneur avec bordure et ombre est créé pour le drapeau
- Le SVG est inséré via `innerHTML`

```java
if (currentUser != null && currentUser.getCountry() != null) {
    String flagSvg = currentUser.getCountry().getCountryFlag();
    if (flagSvg != null && !flagSvg.isEmpty()) {
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
        
        // Scale the SVG from 30x20 to 45x30 (1.5x)
        String scaledSvg = flagSvg.replace("width='30'", "width='45'").replace("height='20'", "height='30'");
        Div flagHtml = new Div();
        flagHtml.getElement().setProperty("innerHTML", scaledSvg);
        flagContainer.add(flagHtml);
        avatarAndFlagLayout.add(flagContainer);
    }
}
```

#### 3. Structure finale
```
VerticalLayout (profileSection)
  └─ HorizontalLayout (avatarAndFlagLayout)
      ├─ Div (avatarContainer) - 80x80px circulaire
      └─ Div (flagContainer) - 45x30px avec bordure [SI PAYS DISPONIBLE]
  └─ Paragraph (userName)
```

## Apparence visuelle

### Avec drapeau
```
┌─────────────────────────────┐
│                             │
│   ┌────┐  ┌──────┐         │
│   │ 👤 │  │ 🇫🇷  │         │
│   └────┘  └──────┘         │
│                             │
│   Jean Dupont              │
│                             │
└─────────────────────────────┘
```

### Sans drapeau
```
┌─────────────────────────────┐
│                             │
│      ┌────┐                │
│      │ 👤 │                │
│      └────┘                │
│                             │
│   Jean Dupont              │
│                             │
└─────────────────────────────┘
```

## Styles appliqués

### Avatar (80x80px)
- Forme circulaire (border-radius: 50%)
- Ombre portée (box-shadow: 0 4px 12px rgba(0,0,0,0.15))
- Photo de l'utilisateur OU initiales OU icône par défaut

### Drapeau (45x30px)
- Bordure fine (1px solid #e0e0e0)
- Coins arrondis (border-radius: 4px)
- Ombre légère (box-shadow: 0 2px 4px rgba(0,0,0,0.1))
- Centré verticalement avec l'avatar

### Espacement
- Gap de 10px entre l'avatar et le drapeau
- Nom de l'utilisateur à 8px en dessous

## Exemples selon les pays

### Utilisateur français (Admin)
- Avatar: "AD" sur fond rouge
- Drapeau: 🇫🇷 (bleu, blanc, rouge)
- Nom: "Administrateur"

### Utilisateur américain (Barack Obama)
- Avatar: "BO" sur fond bleu
- Drapeau: 🇺🇸 (étoiles et bandes)
- Nom: "Barack Obama"

### Utilisateur britannique (Winston Churchill)
- Avatar: "WC" sur fond violet
- Drapeau: 🇬🇧 (Union Jack)
- Nom: "Winston Churchill"

### Utilisateur sans pays
- Avatar: Initiales ou photo
- Drapeau: Aucun
- Nom: Nom de l'utilisateur

## Comportement

### Cas où le drapeau est affiché
✅ L'utilisateur est connecté  
✅ L'utilisateur a un pays associé (`user.getCountry() != null`)  
✅ Le pays a un drapeau SVG (`countryFlag != null && !countryFlag.isEmpty()`)

### Cas où le drapeau n'est pas affiché
❌ L'utilisateur n'est pas connecté  
❌ L'utilisateur n'a pas de pays associé  
❌ Le pays n'a pas de drapeau SVG

## Redimensionnement du SVG

Les drapeaux sont stockés en 30x20px dans la base de données, mais affichés en 45x30px (facteur 1.5x) pour une meilleure visibilité.

**Transformation:**
```java
String scaledSvg = flagSvg
    .replace("width='30'", "width='45'")
    .replace("height='20'", "height='30'");
```

## Compatibilité

### Navigateurs
- ✅ Chrome
- ✅ Firefox
- ✅ Edge
- ✅ Safari
- ✅ Tous les navigateurs modernes supportant SVG

### Responsive
- Le layout s'adapte automatiquement
- L'avatar et le drapeau restent côte à côte
- Sur petits écrans, le layout reste centré

## Performance

### Optimisations
- Le SVG est chargé directement depuis la base de données (pas de requête réseau)
- L'utilisateur est récupéré une seule fois depuis la session
- Pas de rechargement lors de la navigation

### Impact
- Impact minimal sur les performances
- Le SVG est léger (quelques Ko maximum)
- Chargement instantané

## Tests recommandés

### Test 1: Utilisateur avec pays
1. Se connecter en tant qu'admin
2. Vérifier que le drapeau français 🇫🇷 apparaît
3. Vérifier que l'avatar "AD" est affiché

### Test 2: Utilisateur sans pays
1. Se connecter avec un utilisateur sans pays
2. Vérifier qu'aucun drapeau n'apparaît
3. Vérifier que l'avatar est quand même affiché

### Test 3: Différents pays
1. Se connecter avec différents utilisateurs célèbres
2. Vérifier que chaque drapeau correspond au bon pays
3. Exemples à tester:
   - USA: Barack Obama 🇺🇸
   - UK: Winston Churchill 🇬🇧
   - Allemagne: Albert Einstein 🇩🇪
   - Italie: Leonardo da Vinci 🇮🇹

## Améliorations futures possibles

1. **Tooltip au survol du drapeau**
   - Afficher le nom du pays
   - Afficher le code ISO

2. **Clic sur le drapeau**
   - Naviguer vers une page de statistiques du pays
   - Afficher les autres utilisateurs du même pays

3. **Animation au chargement**
   - Fade-in du drapeau
   - Effet de vague sur le drapeau

4. **Drapeau dans d'autres vues**
   - Leaderboard (tableau des scores)
   - Liste des participants
   - Profil utilisateur

## Résultat final

✅ **L'avatar et le drapeau sont maintenant affichés côte à côte**  
✅ **Le drapeau est conditionnel (uniquement si l'utilisateur a un pays)**  
✅ **Le design est cohérent avec le reste de l'application**  
✅ **La compilation réussit sans erreurs**  

---

**Date:** 2026-01-02  
**Fichier modifié:** QuizListView.java  
**Lignes modifiées:** ~100 lignes dans `createUserProfileSection()`  
**Status:** ✅ TERMINÉ

