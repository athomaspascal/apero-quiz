# Investigation : Menu Dashboard visible pour utilisateur non-admin
Date : 2026-01-04

## 🐛 Problème rapporté

Un utilisateur s'est connecté avec un **avatar public** et le menu "Dashboard" était **visible**, alors qu'il ne devrait être visible que pour les administrateurs.

## 🔍 Investigation effectuée

### 1. Vérification du code de filtrage (MainLayout.java)

Le code de filtrage semble correct :

```java
// Admin-only menus
boolean isAdminMenu = "users".equals(path)
    || "question-logs".equals(path)
    || "admin/quiz-editor".equals(path)
    || "dashboard".equals(path);  // ✅ Dashboard est bien dans la liste

// Add menu item only if user is admin or menu is not admin-only
if (!isAdminMenu || isAdmin) {
    sideNav.addItem(createSideNavItem(entry));
}
```

### 2. Vérification des utilisateurs publics

Les utilisateurs publics (avatars célèbres) sont créés dans `DataInitializer.java` :
- ✅ Ils ont `isPublic = true`
- ✅ Ils n'ont PAS `isAdmin = true`
- ✅ Mot de passe par défaut : "public123"

### 3. Logs de débogage ajoutés

Pour identifier le problème, des logs supplémentaires ont été ajoutés dans `MainLayout.createSideNav()` :

```java
logger.info("=== createSideNav called ===");
logger.info("Current user: " + (currentUser != null ? currentUser.getName() : "null") + ", isAdmin: " + isAdmin);
logger.info("Current user isPublic: " + (currentUser != null ? currentUser.isPublic() : "n/a"));

// Pour chaque menu
logger.info("Menu: path=" + path + ", isAdminMenu=" + isAdminMenu + ", willBeAdded=" + willBeAdded);
```

## 🎯 Tests à effectuer

### Test 1 : Vérifier les logs après connexion avec avatar public

1. Arrêter l'application
2. Redémarrer l'application
3. Se connecter avec un avatar public (ex: Barack Obama)
4. Vérifier dans les logs :
   ```
   === createSideNav called ===
   Current user: Barack Obama, isAdmin: false    ← Doit être false
   Current user isPublic: true                   ← Doit être true
   Menu: path=dashboard, isAdminMenu=true, willBeAdded=false  ← Doit être false
   ```

5. Si `willBeAdded=true` pour dashboard → Le problème est confirmé
6. Si `willBeAdded=false` mais le menu est visible → Problème de cache

### Test 2 : Vérifier la méthode isAdmin()

Ajouter un log temporaire dans `LoginView.java` après l'authentification :

```java
User user = authenticationService.getCurrentUser();
logger.info("User logged in: " + user.getName() + ", isAdmin=" + user.isAdmin() + ", isPublic=" + user.isPublic());
```

### Test 3 : Forcer le rafraîchissement du menu

Le menu est rafraîchi dans `onAttach()`. Il faut vérifier que :
1. `onAttach()` est bien appelé après la connexion
2. `refreshMenu()` recrée bien le menu avec l'état actuel de l'utilisateur

## 🔄 Causes possibles

### Hypothèse 1 : Cache du menu
- Le menu est créé AVANT la connexion
- Le menu n'est pas rafraîchi APRÈS la connexion
- **Solution** : Forcer le rafraîchissement du menu après connexion

### Hypothèse 2 : isAdmin() retourne incorrectement true
- Un utilisateur public a par erreur `isAdmin=true` dans la base
- **Solution** : Vérifier la base de données

### Hypothèse 3 : Problème de session
- L'utilisateur admin précédent est toujours en session
- **Solution** : Vérifier que la session est bien nettoyée avant nouvelle connexion

### Hypothèse 4 : Problème de navigation
- Le menu est créé avec l'ancien utilisateur (ou null)
- Le rafraîchissement intervient trop tard
- **Solution** : Forcer le rafraîchissement immédiatement après connexion

## 📝 Actions recommandées

### Action immédiate
1. Lancer l'application
2. Se connecter avec un avatar public
3. Vérifier les logs pour identifier quelle hypothèse est correcte

### Si Hypothèse 1 (cache) :
Ajouter un rafraîchissement explicite dans `LoginView` après connexion :

```java
// After successful authentication
getUI().ifPresent(ui -> {
    ui.access(() -> {
        // Force menu refresh
        MainLayout layout = (MainLayout) ui.getChildren()
            .filter(component -> component instanceof MainLayout)
            .findFirst()
            .orElse(null);
        if (layout != null) {
            layout.refreshMenu(); // Need to make this method public
        }
    });
});
```

### Si Hypothèse 2 (base de données) :
Exécuter une requête SQL pour vérifier :

```sql
SELECT name, email, is_admin, is_public FROM user WHERE is_public = true;
```

Tous doivent avoir `is_admin = false`.

### Si Hypothèse 3 (session) :
Ajouter un nettoyage de session avant nouvelle connexion :

```java
// Before authentication
VaadinSession.getCurrent().getSession().invalidate();
```

## 🎯 Prochaines étapes

1. ✅ **Logs ajoutés** - Attendre les résultats des tests
2. ⏳ **Test avec avatar public** - À effectuer
3. ⏳ **Analyse des logs** - Identifier la cause
4. ⏳ **Correction** - Appliquer la solution appropriée

## 📊 Statut

**EN INVESTIGATION** - Logs de débogage ajoutés. Attente des résultats de tests pour identifier la cause exacte.

---

**Note** : Les logs supplémentaires permettront d'identifier précisément où et quand le problème se produit.

