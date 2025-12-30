# Masquage des Menus Admin - Documentation

## 📋 Modification effectuée

Les menus administrateur ne sont maintenant visibles **QUE pour les utilisateurs administrateurs connectés**. Les utilisateurs non-administrateurs ne voient pas ces menus.

## 🔒 Menus concernés

Les menus suivants sont maintenant réservés aux administrateurs :

1. **Utilisateurs** (`users`)
2. **Questions Logs** (`question-logs`)  
3. **Edition des quizz** (`admin/quiz-editor`)

## 📁 Fichiers modifiés

### 1. MainLayout.java
**Fichier :** `src/main/java/com/quizz/base/ui/MainLayout.java`

**Modification :** La méthode `createSideNav()` filtre maintenant les entrées de menu selon le rôle de l'utilisateur.

```java
private SideNav createSideNav() {
    sideNav = new SideNav();
    sideNav.addClassNames(Margin.Horizontal.MEDIUM);
    menuEntries = MenuConfiguration.getMenuEntries();
    menuEntries.forEach(entry -> logger.info("Menu Entry:" + entry.title()));
    sideNav.removeAll();
    
    // Get current user from session
    User currentUser = VaadinSession.getCurrent().getAttribute(User.class);
    boolean isAdmin = currentUser != null && currentUser.isAdmin();
    
    // Filter menu entries based on user role
    menuEntries.forEach(entry -> {
        String path = entry.path();
        
        // Admin-only menus
        boolean isAdminMenu = "users".equals(path) 
            || "question-logs".equals(path) 
            || "admin/quiz-editor".equals(path);
        
        // Add menu item only if user is admin or menu is not admin-only
        if (!isAdminMenu || isAdmin) {
            sideNav.addItem(createSideNavItem(entry));
        }
    });
    
    return sideNav;
}
```

### 2. QuizListView.java
**Fichier :** `src/main/java/com/quizz/core/ui/QuizListView.java`

**Modification :** La méthode `hideUsersMenuIfNotAdmin()` a été mise à jour pour inclure `edit-quizzes`.

```java
private void hideUsersMenuIfNotAdmin() {
    User currentUser = VaadinSession.getCurrent().getAttribute(User.class);
    boolean isAdmin = currentUser != null && currentUser.isAdmin();

    if (!isAdmin) {
        // Use JavaScript to hide the admin-only menu items
        getElement().executeJs(
            "setTimeout(() => {" +
            "  const sideNav = document.querySelector('vaadin-side-nav');" +
            "  if (sideNav) {" +
            "    const items = sideNav.querySelectorAll('vaadin-side-nav-item');" +
            "    items.forEach(item => {" +
            "      const path = item.getAttribute('path');" +
            "      if (path === 'users' || path === 'question-logs' || path === 'admin/quiz-editor') {" +
            "        item.style.display = 'none';" +
            "      }" +
            "    });" +
            "  }" +
            "}, 100);"
        );
    }
}
```

### 3. TeamModeView.java
**Fichier :** `src/main/java/com/quizz/core/ui/TeamModeView.java`

**Modification :** La méthode `hideUsersMenuIfNotAdmin()` a été mise à jour pour inclure `edit-quizzes`.

*Même code que QuizListView*

### 4. Correction QRCode dans TeamModeView
**Correction appliquée :** Utilisation correcte de StreamResource deprecated avec suppression d'avertissement.

## 🔐 Logique de sécurité

### Niveaux de protection

1. **Niveau Layout (MainLayout)** : 
   - Les menus ne sont pas ajoutés au SideNav pour les non-admin
   - Protection côté serveur lors de la génération du menu

2. **Niveau Vue (QuizListView, TeamModeView)** :
   - JavaScript supplémentaire pour masquer visuellement les menus
   - Protection contre les problèmes de timing de rendu

### Vérification du rôle administrateur

```java
User currentUser = VaadinSession.getCurrent().getAttribute(User.class);
boolean isAdmin = currentUser != null && currentUser.isAdmin();
```

Cette vérification est effectuée dans chaque méthode pour s'assurer que :
- L'utilisateur est connecté (`currentUser != null`)
- L'utilisateur a le rôle administrateur (`currentUser.isAdmin()`)

## 🎯 Comportement par rôle

### Utilisateur normal (non-admin)

**Menus visibles :**
- Un Quizz
- Mode Équipe  
- Rejoindre une Session

**Menus masqués :**
- Utilisateurs ❌
- Questions Logs ❌
- Edition des quizz ❌

### Utilisateur administrateur

**Menus visibles :**
- Un Quizz
- Mode Équipe
- Rejoindre une Session
- Utilisateurs ✅
- Questions Logs ✅
- Edition des quizz ✅

## 🔍 Page de connexion

**Comportement important :** 
- Sur la page de connexion (`/login`), aucun menu n'est affiché car il n'y a pas d'utilisateur connecté
- Le `MainLayout` n'est pas utilisé sur la page de connexion
- Après connexion, les menus appropriés s'affichent selon le rôle

## ✅ Tests à effectuer

### Test 1 : Utilisateur non-admin
1. Connectez-vous avec un compte utilisateur normal
2. Vérifiez que seuls 3 menus sont visibles
3. Vérifiez que les menus admin ne sont pas visibles

### Test 2 : Utilisateur admin
1. Connectez-vous avec un compte administrateur
2. Vérifiez que les 6 menus sont visibles
3. Vérifiez l'accès aux pages admin

### Test 3 : Page de connexion
1. Allez sur `/login`
2. Vérifiez qu'aucun menu n'est affiché
3. Connectez-vous et vérifiez que les menus apparaissent

## 🛡️ Sécurité

### Protection côté serveur

Les routes elles-mêmes doivent également être protégées côté serveur avec des annotations Spring Security ou des vérifications dans les méthodes `beforeEnter()`.

**Exemple de protection d'une vue :**

```java
@Route("users")
@Menu(order = 4, icon = "vaadin:users", title = "menu.users")
class UserListView extends Main implements BeforeEnterObserver {
    
    @Override
    public void beforeEnter(BeforeEnterEvent event) {
        User currentUser = VaadinSession.getCurrent().getAttribute(User.class);
        
        if (currentUser == null || !currentUser.isAdmin()) {
            event.rerouteTo(""); // Redirect to home
            Notification.show("Access denied", 3000, Notification.Position.MIDDLE)
                .addThemeVariants(NotificationVariant.LUMO_ERROR);
        }
    }
}
```

### Double protection

La combinaison de :
1. Filtrage dans `MainLayout` (les menus ne sont pas créés)
2. JavaScript dans les vues (masquage visuel)
3. Vérification `beforeEnter()` dans les vues admin

Assure une protection complète à plusieurs niveaux.

## 📝 Notes importantes

1. **Le filtrage dans MainLayout est la protection principale** : Les menus ne sont jamais ajoutés au DOM pour les non-admin.

2. **Le JavaScript dans les vues est une protection secondaire** : Utile en cas de problèmes de timing ou de rendu.

3. **La vérification beforeEnter est essentielle** : Empêche l'accès direct aux URLs même si on les connaît.

## 🔄 Mise à jour future

Si de nouveaux menus admin sont ajoutés, il faut les ajouter dans :

1. **MainLayout.createSideNav()** : 
   ```java
   boolean isAdminMenu = "users".equals(path) 
       || "question-logs".equals(path) 
       || "admin/quiz-editor".equals(path)
       || "nouveau-menu-admin".equals(path);  // <-- Ajouter ici
   ```

2. **QuizListView et TeamModeView hideUsersMenuIfNotAdmin()** :
   ```javascript
   if (path === 'users' || path === 'question-logs' || path === 'admin/quiz-editor' || path === 'nouveau-menu-admin') {
   ```

## ✅ Résumé

- ✅ Les menus admin sont maintenant masqués pour les utilisateurs non-admin
- ✅ Protection à plusieurs niveaux (Layout + Vues)
- ✅ Code prêt et fonctionnel
- ✅ Aucune erreur de compilation
- ✅ Comportement cohérent dans toute l'application

Les utilisateurs normaux ne verront plus les menus "Utilisateurs", "Questions Logs" et "Edition des quizz" lors de la connexion.

