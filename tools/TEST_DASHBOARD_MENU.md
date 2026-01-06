# Test du Menu Dashboard pour Utilisateurs Non-Admin

## Problème
Le menu "Dashboard" apparaît pour les utilisateurs publics (avatars) alors qu'il ne devrait être visible que pour les administrateurs, comme le menu "Users".

## Solution Implémentée
Ajout de logs détaillés dans `MainLayout.java` pour déboguer le filtrage des menus.

## Code de Filtrage
Le code suivant dans `MainLayout.java` (lignes 111-125) devrait filtrer les menus admin :

```java
boolean isAdminMenu = "users".equals(path)
    || "question-logs".equals(path)
    || "admin/quiz-editor".equals(path)
    || "dashboard".equals(path);

boolean willBeAdded = !isAdminMenu || isAdmin;
```

## Test à Effectuer
1. Démarrer l'application : `mvn spring-boot:run`
2. Ouvrir l'application dans Firefox: `https://apero-quiz.duckdns.org:8443`
3. Cliquer sur "Public Avatar"
4. Sélectionner un avatar public (par exemple: Charles Darwin, Barack Obama, etc.)
5. Vérifier que les menus suivants **n'apparaissent PAS** dans le menu de gauche :
   - Users (Utilisateurs)
   - Question Logs
   - Edition d'un Quiz (Quiz Editor)
   - **Dashboard**

## Vérification des Logs
Après la connexion, vérifier les logs dans `C:\Users\athom\IdeaProjects\quizz1\logs\application.log` :

Rechercher les lignes contenant :
- `=== createSideNav called ===`
- `Current user:` 
- `isAdmin:`
- `Menu: path='dashboard'`
- `ADDING menu:` ou `SKIPPING menu:`

Les logs devraient afficher pour un utilisateur public :
```
Current user: [NOM_AVATAR], isAdmin: false
Menu: path='dashboard', title='menu.dashboard', isAdminMenu=true, isAdmin=false, willBeAdded=false
  -> SKIPPING menu: menu.dashboard
```

## Protections en Place
1. **Filtrage du menu** : MainLayout.java filtre les menus admin
2. **Annotation @RolesAllowed("ADMIN")** : DashboardView.java
3. **Vérification beforeEnter** : DashboardView.java redirige les non-admin

Même si le menu apparaît (bug), la page est protégée et redirigera l'utilisateur.

## Si le Menu Apparaît Encore
Vérifier dans les logs :
1. La valeur de `isAdmin` pour l'utilisateur connecté
2. La valeur de `isPublic` pour l'utilisateur
3. Le chemin exact du menu Dashboard

## Date
2026-01-05 00:00

