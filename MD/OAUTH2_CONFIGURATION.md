# 🔐 Configuration OAuth2 - Guide Complet

## ✅ Configuration Complète avec Java 21

L'application est maintenant configurée pour OAuth2 avec Java 21 (Azul).

## 📋 Étapes de Configuration

### 1. Créer les Applications OAuth2

#### 🔴 Google OAuth2

1. Aller sur [Google Cloud Console](https://console.cloud.google.com/)
2. Créer un nouveau projet ou sélectionner un projet existant
3. Aller dans **APIs & Services** → **Credentials**
4. Cliquer sur **Create Credentials** → **OAuth client ID**
5. Type d'application : **Web application**
6. **Authorized redirect URIs** : 
   - `http://localhost:8080/login/oauth2/code/google`
7. Copier **Client ID** et **Client Secret**

#### 🔵 Facebook OAuth2

1. Aller sur [Facebook Developers](https://developers.facebook.com/)
2. Créer une nouvelle application ou utiliser une existante
3. Dans le tableau de bord, aller à **Settings** → **Basic**
4. Ajouter **Facebook Login** comme produit
5. Dans **Facebook Login** → **Settings** :
   - **Valid OAuth Redirect URIs** : `http://localhost:8080/login/oauth2/code/facebook`
6. Copier **App ID** (Client ID) et **App Secret** (Client Secret)

#### 🔵 LinkedIn OAuth2

1. Aller sur [LinkedIn Developers](https://www.linkedin.com/developers/)
2. Créer une nouvelle application
3. Dans l'onglet **Auth** :
   - **Redirect URLs** : `http://localhost:8080/login/oauth2/code/linkedin`
4. Dans **Products**, demander l'accès à **Sign In with LinkedIn using OpenID Connect**
5. Copier **Client ID** et **Client Secret**

### 2. Configurer application.properties

Ouvrir `src/main/resources/application.properties` et remplacer les valeurs :

```properties
# Google OAuth2
spring.security.oauth2.client.registration.google.client-id=VOTRE_GOOGLE_CLIENT_ID
spring.security.oauth2.client.registration.google.client-secret=VOTRE_GOOGLE_CLIENT_SECRET

# Facebook OAuth2
spring.security.oauth2.client.registration.facebook.client-id=VOTRE_FACEBOOK_APP_ID
spring.security.oauth2.client.registration.facebook.client-secret=VOTRE_FACEBOOK_APP_SECRET

# LinkedIn OAuth2
spring.security.oauth2.client.registration.linkedin.client-id=VOTRE_LINKEDIN_CLIENT_ID
spring.security.oauth2.client.registration.linkedin.client-secret=VOTRE_LINKEDIN_CLIENT_SECRET
```

### 3. Démarrer l'Application avec Java 21

#### Option A : Via le script batch (Recommandé)

```bash
start-with-java21.bat
```

#### Option B : Via IntelliJ IDEA

1. **File** → **Project Structure** → **Project Settings** → **Project**
   - SDK : `C:\Users\athom\.jdks\azul-21.0.9`
   - Language Level : `21`

2. **File** → **Project Structure** → **Modules** → **Dependencies**
   - Module SDK : `Project SDK`

3. **Run** → **Edit Configurations** → **Application**
   - JRE : Choisir `azul-21.0.9`

4. Lancer `Application.java`

#### Option C : Ligne de commande

```cmd
set JAVA_HOME=C:\Users\athom\.jdks\azul-21.0.9
set PATH=%JAVA_HOME%\bin;%PATH%
mvnw.cmd clean spring-boot:run
```

### 4. Tester la Connexion OAuth2

1. Accéder à http://localhost:8080
2. Vous serez redirigé vers la page de login
3. Trois boutons OAuth2 sont disponibles :
   - **Google** (bleu)
   - **Facebook** (bleu foncé)
   - **LinkedIn** (bleu cyan)
4. Cliquer sur l'un des boutons pour vous connecter

## 🏗️ Architecture OAuth2

### Classes Créées

1. **CustomOAuth2UserService** : Gère le chargement et la création des utilisateurs OAuth2
2. **CustomOAuth2User** : Encapsule l'utilisateur OAuth2 avec notre entité User
3. **OAuth2LoginSuccessHandler** : Gère le succès de la connexion OAuth2
4. **SecurityConfig** : Configuration Spring Security avec OAuth2

### Flux OAuth2

1. L'utilisateur clique sur un bouton OAuth2 (Google/Facebook/LinkedIn)
2. Redirection vers le provider OAuth2
3. L'utilisateur s'authentifie sur le provider
4. Redirection vers l'application avec un code d'autorisation
5. L'application échange le code contre un token d'accès
6. **CustomOAuth2UserService** charge les informations utilisateur
7. Un **User** est créé ou récupéré dans la base de données
8. **OAuth2LoginSuccessHandler** stocke l'utilisateur dans la session
9. Redirection vers la page d'accueil

### Base de Données

L'entité **User** stocke :
- `name` : Nom complet
- `email` : Email (unique)
- `telephone` : Téléphone (optionnel)
- `password` : Mot de passe (vide pour OAuth2)
- `oauth_provider` : Provider OAuth2 (google/facebook/linkedin)
- `oauth_provider_id` : ID unique du provider

## 🔒 Sécurité

### Endpoints Publics
- `/login` : Page de connexion
- `/register` : Page d'inscription
- `/forgot-password` : Mot de passe oublié
- `/oauth2/**` : Endpoints OAuth2
- `/login/oauth2/**` : Callbacks OAuth2

### Endpoints Protégés
- Tous les autres endpoints nécessitent une authentification

## 🐛 Dépannage

### Erreur : "redirect_uri_mismatch"
- Vérifier que l'URL de redirection est correcte dans la console du provider
- Format : `http://localhost:8080/login/oauth2/code/{provider}`

### Erreur : "Client authentication failed"
- Vérifier le Client ID et Client Secret dans `application.properties`

### Erreur : "Email not available"
- S'assurer que les scopes incluent `email`
- Vérifier que l'email est public dans les paramètres du compte

### Application ne démarre pas avec Java 11
- Utiliser le script `start-with-java21.bat`
- Ou configurer IntelliJ pour utiliser Java 21

### OAuth2 ne fonctionne pas en mode production
- Mettre à jour les redirect URIs avec votre domaine de production
- Exemple : `https://votredomaine.com/login/oauth2/code/google`

## 📚 Ressources

- [Spring Security OAuth2 Client](https://docs.spring.io/spring-security/reference/servlet/oauth2/client/index.html)
- [Vaadin with Spring Security](https://vaadin.com/docs/latest/security/enabling-security)
- [Google OAuth2](https://developers.google.com/identity/protocols/oauth2)
- [Facebook Login](https://developers.facebook.com/docs/facebook-login/)
- [LinkedIn OAuth2](https://learn.microsoft.com/en-us/linkedin/shared/authentication/authentication)

## ✨ Fonctionnalités Implémentées

✅ Connexion avec Google
✅ Connexion avec Facebook
✅ Connexion avec LinkedIn
✅ Création automatique d'utilisateurs
✅ Liaison de comptes OAuth2 existants
✅ Stockage dans la session Vaadin
✅ Configuration Java 21
✅ Page de connexion personnalisée

## 🚀 Prochaines Étapes

- [ ] Ajouter plus de providers (GitHub, Microsoft, etc.)
- [ ] Gérer la déconnexion OAuth2
- [ ] Ajouter des rôles et permissions
- [ ] Implémenter le refresh token
- [ ] Gérer les erreurs OAuth2 personnalisées
- [ ] Ajouter des tests pour OAuth2

---

**Bon développement ! 🎉**

