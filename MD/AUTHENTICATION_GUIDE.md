# Quiz Application - Authentication Guide

## Page de connexion (Login)

L'application dispose maintenant d'un système d'authentification complet avec les fonctionnalités suivantes :

### Fonctionnalités

1. **Page de connexion** (`/login`)
   - Formulaire de connexion avec email et mot de passe
   - Lien vers la page d'inscription
   - Lien "Mot de passe oublié"
   - Design moderne avec dégradé violet

2. **Page d'inscription** (`/register`)
   - Création de compte avec nom, email, téléphone et mot de passe
   - Validation des champs
   - Vérification que les mots de passe correspondent
   - Encodage sécurisé des mots de passe avec BCrypt

3. **Page mot de passe oublié** (`/forgot-password`)
   - Formulaire pour demander la réinitialisation du mot de passe
   - (Note : L'envoi d'email n'est pas implémenté, c'est une démo)

4. **Déconnexion**
   - Bouton de déconnexion dans le menu latéral
   - Affiche l'utilisateur connecté

### Utilisateur de test

Un utilisateur de test est créé automatiquement au démarrage :

- **Email**: `test@example.com`
- **Mot de passe**: `password123`

### Sécurité

- Les mots de passe sont encodés avec BCrypt
- Protection des pages : seules les pages annotées avec `@AnonymousAllowed` sont accessibles sans connexion
- Session utilisateur gérée avec VaadinSession
- Redirection automatique vers la page de connexion si non authentifié

### Accès aux pages

- `/login` - Page de connexion (accès public)
- `/register` - Page d'inscription (accès public)
- `/forgot-password` - Mot de passe oublié (accès public)
- `/` - Page principale des quiz (nécessite authentification)
- `/users` - Gestion des utilisateurs (nécessite authentification)
- `/quiz-questions/{id}` - Questions du quiz (nécessite authentification)

### Développement

Pour ajouter une page accessible sans authentification, ajoutez l'annotation `@AnonymousAllowed` :

```java
@Route("ma-page-publique")
@AnonymousAllowed
public class MaPagePubliqueView extends VerticalLayout {
    // ...
}
```

Pour obtenir l'utilisateur connecté dans une vue :

```java
User currentUser = VaadinSession.getCurrent().getAttribute(User.class);
if (currentUser != null) {
    // L'utilisateur est connecté
    String userName = currentUser.getName();
}
```

