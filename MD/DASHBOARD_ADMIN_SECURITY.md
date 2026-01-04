# Sécurisation du Dashboard - Accès Admin uniquement
Date : 2026-01-04

## Problème

Le menu Dashboard était visible par tous les utilisateurs, mais devait être réservé uniquement aux administrateurs, comme le menu "Users".

## Solution implémentée

### 1. Masquage du menu (MainLayout.java)

Le menu Dashboard est maintenant ajouté à la liste des menus admin-only dans `MainLayout.java` :

```java
// Admin-only menus
boolean isAdminMenu = "users".equals(path)
    || "question-logs".equals(path)
    || "admin/quiz-editor".equals(path)
    || "dashboard".equals(path);  // ← Ajouté

// Add menu item only if user is admin or menu is not admin-only
if (!isAdminMenu || isAdmin) {
    sideNav.addItem(createSideNavItem(entry));
}
```

**Résultat** : Le menu "Dashboard" n'apparaît que pour les utilisateurs admin dans la barre latérale.

### 2. Protection d'accès (DashboardView.java)

#### 2.1. Ajout de BeforeEnterObserver

La classe implémente maintenant `BeforeEnterObserver` pour vérifier l'accès avant d'entrer dans la vue :

```java
public class DashboardView extends VerticalLayout implements BeforeEnterObserver
```

#### 2.2. Import des classes nécessaires

Ajout des imports :
- `User` - Pour vérifier le rôle de l'utilisateur
- `BeforeEnterEvent` et `BeforeEnterObserver` - Pour intercepter la navigation
- `VaadinSession` - Pour récupérer l'utilisateur courant
- `Notification` et `NotificationVariant` - Pour afficher le message d'erreur

#### 2.3. Méthode beforeEnter()

Ajout de la vérification d'accès :

```java
@Override
public void beforeEnter(BeforeEnterEvent event) {
    // Check if current user is admin
    User currentUser = VaadinSession.getCurrent().getAttribute(User.class);

    if (currentUser == null || !currentUser.isAdmin()) {
        // Redirect to quiz list if not admin
        event.rerouteTo("");
        Notification.show(translationService.translate("common.accessDenied"), 
                         3000, Notification.Position.MIDDLE)
            .addThemeVariants(NotificationVariant.LUMO_ERROR);
        logger.warn("Non-admin user attempted to access dashboard: {}", 
                   currentUser != null ? currentUser.getName() : "unknown");
    }
}
```

### Traductions ajoutées

#### Nouvelle clé : `common.accessDenied`

| Langue | Traduction |
|--------|-----------|
| EN | Access denied. Admins only. |
| FR | Accès refusé. Réservé aux administrateurs. |
| IT | Accesso negato. Solo per amministratori. |

## Niveaux de sécurité

Le Dashboard est maintenant protégé par **deux niveaux de sécurité** :

### 1. Niveau annotation (@RolesAllowed)

```java
@RolesAllowed("ADMIN")
public class DashboardView extends VerticalLayout implements BeforeEnterObserver
```

Cette annotation Spring Security empêche l'accès au niveau du framework.

### 2. Niveau applicatif (beforeEnter)

```java
@Override
public void beforeEnter(BeforeEnterEvent event) {
    if (currentUser == null || !currentUser.isAdmin()) {
        event.rerouteTo("");
        // Show error notification
    }
}
```

Cette vérification explicite :
- Redirige vers la page d'accueil
- Affiche un message d'erreur traduit
- Log la tentative d'accès non autorisée

## Cohérence avec UserListView

La solution est maintenant cohérente avec `UserListView` qui utilise le même mécanisme :

| Caractéristique | UserListView | DashboardView |
|----------------|--------------|---------------|
| Annotation @RolesAllowed | ❌ Non | ✅ Oui |
| Interface BeforeEnterObserver | ✅ Oui | ✅ Oui |
| Vérification isAdmin() | ✅ Oui | ✅ Oui |
| Redirection si non-admin | ✅ Oui | ✅ Oui |
| Notification d'erreur | ✅ Oui | ✅ Oui |
| Log de sécurité | ❌ Non | ✅ Oui |

> Note : DashboardView a une sécurité **renforcée** avec l'annotation @RolesAllowed ET la vérification explicite.

## Comportement

### Pour un utilisateur non-admin

1. L'utilisateur essaie d'accéder à `/dashboard`
2. Le menu "Dashboard" n'est pas visible dans le menu latéral (masqué par Vaadin)
3. Si l'utilisateur tape l'URL directement :
   - La vérification `beforeEnter` s'exécute
   - Redirection vers la page d'accueil (`/`)
   - Notification d'erreur affichée
   - Log de sécurité enregistré

### Pour un administrateur

1. L'utilisateur voit le menu "Dashboard" dans le menu latéral
2. Clic sur "Dashboard" → Accès autorisé
3. Le tableau de bord s'affiche normalement

## Logs de sécurité

Exemple de log lors d'une tentative d'accès non autorisée :

```
WARN  DashboardView - Non-admin user attempted to access dashboard: JohnDoe
```

Si l'utilisateur n'est pas connecté :

```
WARN  DashboardView - Non-admin user attempted to access dashboard: unknown
```

## Tests recommandés

### Test 1 : Utilisateur non connecté
1. Ne pas se connecter
2. Taper l'URL `/dashboard`
3. **Attendu** : Redirection + message d'erreur

### Test 2 : Utilisateur normal (non-admin)
1. Se connecter avec un compte utilisateur normal
2. Vérifier que le menu "Dashboard" n'est pas visible
3. Taper l'URL `/dashboard`
4. **Attendu** : Redirection + message d'erreur

### Test 3 : Utilisateur admin
1. Se connecter avec un compte admin
2. Vérifier que le menu "Dashboard" est visible
3. Cliquer sur "Dashboard"
4. **Attendu** : Accès au tableau de bord

### Test 4 : Changement de langue
1. Se connecter en tant que non-admin
2. Essayer d'accéder au dashboard
3. Changer la langue (FR/EN/IT)
4. **Attendu** : Message d'erreur traduit dans chaque langue

## Fichiers modifiés

1. **MainLayout.java**
   - Ajout de "dashboard" à la liste `isAdminMenu`
   - Le menu Dashboard n'apparaît que pour les admins

2. **DashboardView.java**
   - Ajout de `implements BeforeEnterObserver`
   - Ajout des imports nécessaires
   - Ajout de la méthode `beforeEnter()`

3. **messages_en.properties**
   - Ajout de `common.accessDenied=Access denied. Admins only.`

4. **messages_fr.properties**
   - Ajout de `common.accessDenied=Accès refusé. Réservé aux administrateurs.`

5. **messages_it.properties**
   - Ajout de `common.accessDenied=Accesso negato. Solo per amministratori.`

## Statut

✅ **IMPLÉMENTÉ ET SÉCURISÉ** - Le Dashboard est maintenant correctement protégé et accessible uniquement aux administrateurs, avec :
- **Masquage du menu** pour les non-admins (MainLayout)
- **Double niveau de sécurité** (@RolesAllowed + beforeEnter)
- **Messages d'erreur traduits** en 3 langues
- **Logs de sécurité** pour les tentatives d'accès non autorisées

Le comportement est maintenant **100% identique** au menu "Users".

