# Implémentation OAuth2 - État actuel

## Ce qui a été fait

J'ai préparé l'infrastructure pour l'authentification OAuth2 avec Google, Facebook et LinkedIn :

### 1. Dépendances ajoutées (pom.xml)
- `spring-boot-starter-security` : Sécurité Spring
- `spring-boot-starter-oauth2-client` : Support OAuth2

### 2. Entité User mise à jour
Ajout de deux nouveaux champs :
- `oauthProvider` : Fournisseur OAuth2 (google, facebook, linkedin)
- `oauthProviderId` : ID unique de l'utilisateur chez le fournisseur

### 3. UserRepository mis à jour
Nouvelle méthode : `findByOauthProviderAndOauthProviderId()`

### 4. UserService mis à jour
Nouvelle méthode : `createOrUpdateOAuthUser()` qui :
- Crée un nouvel utilisateur OAuth2
- Lie un compte OAuth2 à un compte existant (par email)
- Met à jour les informations d'un utilisateur OAuth2 existant

### 5. LoginView mise à jour
- Boutons de connexion Google, Facebook et LinkedIn
- Design moderne avec icônes et couleurs spécifiques
- Redirection vers les endpoints OAuth2

### 6. OAuth2UserService créé
Service pour traiter les informations utilisateur OAuth2 de chaque fournisseur

### 7. Configuration OAuth2 (application.properties)
Templates de configuration pour les trois fournisseurs

## Problème actuel

Le projet nécessite Java 17 ou supérieur (spécifié dans pom.xml : `<java.version>21</java.version>`), mais Maven utilise actuellement Java 11.

## Solution : Deux options

### Option 1 : Utiliser Java 21 (Recommandé)

1. **Télécharger Java 21** : [https://www.oracle.com/java/technologies/downloads/#java21](https://www.oracle.com/java/technologies/downloads/#java21)

2. **Définir JAVA_HOME** :
   ```cmd
   setx JAVA_HOME "C:\Program Files\Java\jdk-21" /M
   setx PATH "%JAVA_HOME%\bin;%PATH%" /M
   ```

3. **Vérifier la version** :
   ```cmd
   java -version
   ```

4. **Redémarrer l'IDE** et recompiler

### Option 2 : Désactiver OAuth2 temporairement

Si vous souhaitez continuer sans OAuth2 pour le moment :

1. Retirer les dépendances OAuth2 du `pom.xml` :
   ```xml
   <!-- Commenter ou supprimer ces lignes -->
   <!-- <dependency>
       <groupId>org.springframework.boot</groupId>
       <artifactId>spring-boot-starter-security</artifactId>
   </dependency>
   <dependency>
       <groupId>org.springframework.boot</groupId>
       <artifactId>spring-boot-starter-oauth2-client</artifactId>
   </dependency> -->
   ```

2. Supprimer les boutons OAuth2 de LoginView
3. Supprimer les fichiers OAuth2UserService et OAuth2LoginSuccessController

## Étapes suivantes (après résolution du problème Java)

### 1. Obtenir les clés API

#### Google
1. [Google Cloud Console](https://console.cloud.google.com/)
2. Créer un projet
3. Activer Google+ API
4. Créer des identifiants OAuth 2.0
5. Ajouter l'URI de redirection : `http://localhost:8080/login/oauth2/code/google`

#### Facebook
1. [Facebook Developers](https://developers.facebook.com/)
2. Créer une application
3. Ajouter "Facebook Login"
4. Configurer l'URI : `http://localhost:8080/login/oauth2/code/facebook`

#### LinkedIn
1. [LinkedIn Developers](https://www.linkedin.com/developers/)
2. Créer une application
3. Demander "Sign In with LinkedIn using OpenID Connect"
4. Configurer l'URI : `http://localhost:8080/login/oauth2/code/linkedin`

### 2. Configurer application.properties

Remplacer les valeurs `YOUR_*_CLIENT_ID` et `YOUR_*_CLIENT_SECRET` par les vraies clés.

### 3. Créer VaadinWebSecurityConfig

Une fois Java 21 installé, créer la vraie configuration de sécurité Vaadin :

```java
@Configuration
@EnableWebSecurity
public class VaadinSecurityConfig extends VaadinWebSecurity {

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.oauth2Login(oauth -> oauth
            .loginPage("/login")
            .defaultSuccessUrl("/", true)
        );
        
        super.configure(http);
        setLoginView(http, LoginView.class);
    }
}
```

### 4. Tester

1. Démarrer l'application
2. Accéder à `/login`
3. Cliquer sur un bouton OAuth2
4. Se connecter avec le fournisseur
5. Être redirigé vers la page d'accueil

## Fonctionnalités OAuth2

### Connexion automatique
Les utilisateurs qui se connectent via OAuth2 sont automatiquement créés dans la base de données.

### Liaison de comptes
Si un utilisateur s'inscrit avec un email puis se connecte via OAuth2 avec le même email, les comptes sont automatiquement liés.

### Gestion des mots de passe
Les utilisateurs OAuth2 n'ont pas besoin de mot de passe (champ vide).

### Multi-connexion
Un utilisateur peut se connecter avec :
- Email/mot de passe (inscription classique)
- Google
- Facebook
- LinkedIn

## Fichiers créés/modifiés

### Modifiés
- `pom.xml` - Dépendances OAuth2
- `User.java` - Champs OAuth2
- `UserRepository.java` - Méthode de recherche OAuth2
- `UserService.java` - Méthode de création OAuth2
- `LoginView.java` - Boutons de connexion sociale
- `application.properties` - Configuration OAuth2

### Créés
- `SecurityConfig.java` - Configuration de sécurité
- `OAuth2UserService.java` - Service OAuth2
- `OAuth2LoginSuccessController.java` - Contrôleur de succès
- `OAUTH2_SETUP_GUIDE.md` - Guide complet
- `OAUTH2_STATUS.md` - Ce fichier

## Support

Pour toute question :
1. Vérifier la version Java : `java -version` (doit être 17+)
2. Vérifier les logs de l'application
3. Consulter la documentation Spring Security OAuth2 : [https://spring.io/guides/tutorials/spring-boot-oauth2](https://spring.io/guides/tutorials/spring-boot-oauth2)

