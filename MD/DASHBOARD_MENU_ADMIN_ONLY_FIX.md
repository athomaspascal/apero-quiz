# Correction du menu Dashboard - Affichage Admin uniquement

**Date:** 2026-01-05  
**Problème:** Le menu "Dashboard" apparaissait pour tous les utilisateurs, y compris les avatars publics non-admin.

## Symptômes

- Le menu "Dashboard" était visible dans la navigation gauche pour les utilisateurs publics
- Les autres menus admin ("Users", "Question Logs", "Edit Quizzes") étaient correctement filtrés
- L'annotation `@RolesAllowed("ADMIN")` sur `DashboardView` ne suffisait pas à cacher le menu

## Cause

L'annotation `@Menu` de Vaadin génère automatiquement les entrées de menu, mais elle ne respecte pas automatiquement les restrictions de sécurité définies par `@RolesAllowed`. 

Dans `MainLayout.java`, la logique de filtrage vérifiait uniquement le **chemin** (`path`) des menus pour déterminer s'ils sont réservés aux admins. Cependant, pour certains menus, le système Vaadin peut utiliser une convention différente, et la vérification du titre du menu (`title`) était nécessaire en complément.

## Solution

### Fichier modifié: `src/main/java/com/quizz/base/ui/MainLayout.java`

Ajout de la vérification du **titre du menu** en plus du chemin dans la méthode `createSideNav()` :

```java
// Filter menu entries based on user role
menuEntries.forEach(entry -> {
    String path = entry.path();
    String title = entry.title();

    // Admin-only menus - check both path and title
    boolean isAdminMenu = "users".equals(path)
        || "question-logs".equals(path)
        || "admin/quiz-editor".equals(path)
        || "dashboard".equals(path)
        || "menu.users".equals(title)
        || "menu.questionlogs".equals(title)
        || "menu.editquizzes".equals(title)
        || "menu.dashboard".equals(title);

    boolean willBeAdded = !isAdminMenu || isAdmin;
    logger.info("Menu: path='" + path + "', title='" + title + "', isAdminMenu=" + isAdminMenu + ", isAdmin=" + isAdmin + ", willBeAdded=" + willBeAdded);

    // Add menu item only if user is admin or menu is not admin-only
    if (willBeAdded) {
        logger.info("  -> ADDING menu: " + title);
        sideNav.addItem(createSideNavItem(entry));
    } else {
        logger.info("  -> SKIPPING menu: " + title);
    }
});
```

### Changements clés

1. **Ajout d'une variable `title`** pour récupérer le titre du menu
2. **Double vérification** : path ET title pour identifier les menus admin
3. **Menus admin identifiés par titre** :
   - `"menu.users"`
   - `"menu.questionlogs"`
   - `"menu.editquizzes"`
   - `"menu.dashboard"` ⭐ (nouveau)

## Menus concernés

Les menus suivants sont maintenant correctement filtrés pour les non-admins :

| Menu | Path | Title | Admin Only |
|------|------|-------|------------|
| Users | `users` | `menu.users` | ✅ Oui |
| Question Logs | `question-logs` | `menu.questionlogs` | ✅ Oui |
| Edit Quizzes | `admin/quiz-editor` | `menu.editquizzes` | ✅ Oui |
| Dashboard | `dashboard` | `menu.dashboard` | ✅ Oui |
| Start a quizz | `quiz-list` | `menu.quizlist` | ❌ Non |
| Team mode | `team-mode` | `menu.teammode` | ❌ Non |
| Join Session | `join-session` | `menu.joinSession` | ❌ Non |

## Tests effectués

✅ **Test 1 - Utilisateur public (avatar)**
- Connexion avec avatar public (ex: Charles Darwin)
- Vérification : Menus "Users", "Question Logs", "Edit Quizzes", "Dashboard" **non visibles**
- Résultat : ✅ **PASS**

✅ **Test 2 - Utilisateur admin**
- Connexion avec compte admin
- Vérification : Tous les menus visibles, y compris "Dashboard"
- Résultat : ✅ **PASS**

## Logs de vérification

Lors de la connexion d'un utilisateur public, les logs affichent :

```
=== createSideNav called ===
Current user: Charles Darwin, isAdmin: false
Current user isPublic: true
Menu: path='dashboard', title='menu.dashboard', isAdminMenu=true, isAdmin=false, willBeAdded=false
  -> SKIPPING menu: menu.dashboard
```

Lors de la connexion d'un admin, les logs affichent :

```
=== createSideNav called ===
Current user: admin, isAdmin: true
Current user isPublic: false
Menu: path='dashboard', title='menu.dashboard', isAdminMenu=true, isAdmin=true, willBeAdded=true
  -> ADDING menu: menu.dashboard
```

## Points d'attention pour l'avenir

1. **Tout nouveau menu admin** doit être ajouté dans la liste `isAdminMenu` avec :
   - Son chemin (`path`)
   - Son titre traduit (`title`)

2. **Annotations requises** pour un menu admin :
   ```java
   @Route("mon-menu-admin")
   @PageTitle("Mon Menu Admin")
   @Menu(order = X, icon = "vaadin:icon", title = "menu.monmenuadmin")
   @RolesAllowed("ADMIN")  // Sécurité au niveau de la route
   public class MonMenuAdminView extends VerticalLayout {
       // ...
   }
   ```

3. **Ajouter le filtrage dans MainLayout** :
   ```java
   boolean isAdminMenu = "users".equals(path)
       || "mon-menu-admin".equals(path)  // Ajouter le path
       || "menu.monmenuadmin".equals(title);  // Ajouter le title
   ```

## Fichiers liés

- `src/main/java/com/quizz/base/ui/MainLayout.java` - Gestion de l'affichage des menus
- `src/main/java/com/quizz/core/ui/DashboardView.java` - Vue Dashboard avec `@RolesAllowed("ADMIN")`
- `src/main/java/com/quizz/core/ui/UserListView.java` - Exemple de menu admin
- `src/main/java/com/quizz/core/ui/QuestionLogsView.java` - Exemple de menu admin
- `src/main/java/com/quizz/core/ui/QuizEditorView.java` - Exemple de menu admin

## Corrections similaires

Cette approche (double vérification path + title) peut être utilisée pour tout problème similaire où :
- Un menu apparaît pour des utilisateurs non autorisés
- L'annotation `@RolesAllowed` ne suffit pas à cacher le menu
- Le filtrage doit être fait au niveau de `MainLayout.createSideNav()`

## Statut

✅ **RÉSOLU** - Le menu Dashboard n'apparaît plus pour les utilisateurs non-admin.

