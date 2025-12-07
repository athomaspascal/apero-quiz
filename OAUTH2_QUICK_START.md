# Guide de démarrage rapide - Authentification OAuth2

## ⚠️ Prérequis Important

**Java 17 ou supérieur requis !**

Exécutez `check-java.bat` pour vérifier votre version de Java.

## 📋 Résumé des modifications

### 1. Base de données
L'entité `User` a été enrichie avec :
- `oauthProvider` : Le fournisseur OAuth2 (google, facebook, linkedin)
- `oauthProviderId` : L'identifiant unique chez le fournisseur

### 2. Interface de connexion
La page `/login` affiche maintenant :
- ✅ Formulaire classique (email/password)
- ✅ Lien "Mot de passe oublié"
- ✅ Lien "S'inscrire"
- ✅ Bouton "Google" (bleu)
- ✅ Bouton "Facebook" (bleu foncé)
- ✅ Bouton "LinkedIn" (bleu LinkedIn)

### 3. Dépendances Maven
Ajoutées :
- `spring-boot-starter-security`
- `spring-boot-starter-oauth2-client`

## 🚀 Configuration OAuth2

### Étape 1 : Vérifier Java

```cmd
check-java.bat
```

Si Java < 17, installer Java 21 :
- [Oracle JDK 21](https://www.oracle.com/java/technologies/downloads/#java21)
- [Eclipse Temurin 21](https://adoptium.net/temurin/releases/?version=21)

### Étape 2 : Obtenir les clés OAuth2

#### 🔵 Google OAuth2

1. Accédez à [Google Cloud Console](https://console.cloud.google.com/)
2. Créez un projet ou sélectionnez-en un
3. Activez "Google+ API"
4. Allez dans **API et services** → **Identifiants**
5. Cliquez sur **Créer des identifiants** → **ID client OAuth 2.0**
6. Type d'application : **Application Web**
7. URI de redirection autorisées :
   ```
   http://localhost:8080/login/oauth2/code/google
   ```
8. Copiez le **Client ID** et le **Client Secret**

#### 🔵 Facebook OAuth2

1. Accédez à [Facebook Developers](https://developers.facebook.com/)
2. Créez une application ou sélectionnez-en une
3. Ajoutez le produit **Facebook Login**
4. Dans **Paramètres** → **Facebook Login** → **Paramètres**
5. URI de redirection OAuth valides :
   ```
   http://localhost:8080/login/oauth2/code/facebook
   ```
6. Dans **Paramètres** → **Général**, copiez :
   - **ID de l'application** (App ID)
   - **Clé secrète de l'application** (App Secret)

#### 🔵 LinkedIn OAuth2

1. Accédez à [LinkedIn Developers](https://www.linkedin.com/developers/)
2. Créez une application
3. Dans l'onglet **Auth** :
4. URL de redirection autorisées :
   ```
   http://localhost:8080/login/oauth2/code/linkedin
   ```
5. Demandez l'accès au produit : **Sign In with LinkedIn using OpenID Connect**
6. Copiez le **Client ID** et le **Client Secret**

### Étape 3 : Configurer application.properties

Ouvrez `src/main/resources/application.properties` et remplacez :

```properties
# Google
spring.security.oauth2.client.registration.google.client-id=VOTRE_GOOGLE_CLIENT_ID
spring.security.oauth2.client.registration.google.client-secret=VOTRE_GOOGLE_CLIENT_SECRET

# Facebook
spring.security.oauth2.client.registration.facebook.client-id=VOTRE_FACEBOOK_APP_ID
spring.security.oauth2.client.registration.facebook.client-secret=VOTRE_FACEBOOK_APP_SECRET

# LinkedIn
spring.security.oauth2.client.registration.linkedin.client-id=VOTRE_LINKEDIN_CLIENT_ID
spring.security.oauth2.client.registration.linkedin.client-secret=VOTRE_LINKEDIN_CLIENT_SECRET
```

### Étape 4 : Créer la configuration de sécurité Vaadin

Une fois Java 21 installé, créez `src/main/java/com/quizz/examplefeature/security/VaadinSecurityConfig.java` :

```java
package com.quizz.examplefeature.security;

import com.vaadin.flow.spring.security.VaadinWebSecurity;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;

@Configuration
@EnableWebSecurity
public class VaadinSecurityConfig extends VaadinWebSecurity {

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        // Configure OAuth2 login
        http.oauth2Login(oauth2 -> oauth2
            .loginPage("/login")
            .defaultSuccessUrl("/", true)
            .failureUrl("/login?error")
        );
        
        super.configure(http);
        setLoginView(http, LoginView.class);
    }
}
```

### Étape 5 : Compiler et démarrer

```cmd
mvn clean install
mvn spring-boot:run
```

Ou utilisez le script de démarrage :
```cmd
start-app.bat
```

## 🧪 Test de l'authentification

1. Ouvrez votre navigateur : `http://localhost:8080`
2. Vous serez redirigé vers `/login`
3. Testez les différentes méthodes :

### Test avec email/password
- Cliquez sur "Sign up" pour créer un compte
- Connectez-vous avec email et mot de passe

### Test avec Google
- Cliquez sur le bouton "Google"
- Connectez-vous avec votre compte Google
- Vous serez redirigé vers l'application
- Un compte sera créé automatiquement

### Test avec Facebook
- Cliquez sur le bouton "Facebook"
- Connectez-vous avec votre compte Facebook
- Vous serez redirigé vers l'application

### Test avec LinkedIn
- Cliquez sur le bouton "LinkedIn"
- Connectez-vous avec votre compte LinkedIn
- Vous serez redirigé vers l'application

## 🔐 Sécurité et comportements

### Création automatique de compte
Quand un utilisateur se connecte via OAuth2 pour la première fois :
- Un compte est créé automatiquement
- Les informations (nom, email) sont extraites du profil OAuth2
- Pas de mot de passe requis

### Liaison de comptes
Si un utilisateur :
1. S'inscrit avec email : `john@example.com`
2. Puis se connecte via Google avec le même email

→ Les comptes sont **automatiquement liés**

### Gestion des mots de passe
- Utilisateurs OAuth2 : mot de passe vide (non requis)
- Utilisateurs classiques : mot de passe hashé avec BCrypt

### Multi-connexion
Un utilisateur peut se connecter avec plusieurs méthodes :
- Email/password
- Google
- Facebook
- LinkedIn

## 🐛 Dépannage

### Problème : Java version incompatible
**Symptôme** : Erreur `UnsupportedClassVersionError` ou `class file version 61.0`

**Solution** : 
```cmd
check-java.bat
```
Installer Java 21 et configurer JAVA_HOME

### Problème : OAuth2 redirect URI mismatch
**Symptôme** : Erreur `redirect_uri_mismatch` après clic sur un bouton OAuth2

**Solution** :
- Vérifier que l'URI dans la console du fournisseur correspond exactement
- Format : `http://localhost:8080/login/oauth2/code/{provider}`
- Pas de slash à la fin
- Port 8080 (ou celui configuré)

### Problème : Invalid client credentials
**Symptôme** : Erreur d'authentification OAuth2

**Solution** :
- Vérifier que les Client ID et Secret sont corrects dans `application.properties`
- Pas d'espaces avant/après les valeurs
- Vérifier que les clés sont actives dans la console du fournisseur

### Problème : L'application ne démarre pas
**Symptôme** : Erreur au démarrage Maven

**Solution** :
```cmd
mvn clean
mvn install -DskipTests
mvn spring-boot:run
```

### Problème : Les boutons OAuth2 ne fonctionnent pas
**Symptôme** : Rien ne se passe au clic

**Solution** :
1. Vérifier que Spring Security est bien configuré
2. Vérifier les logs de l'application
3. Vérifier que les URLs `/oauth2/authorization/{provider}` sont accessibles

## 📊 Base de données

### Table users - Nouveaux champs

| Champ | Type | Description |
|-------|------|-------------|
| oauth_provider | VARCHAR(50) | Nom du fournisseur (google, facebook, linkedin) |
| oauth_provider_id | VARCHAR(255) | ID unique chez le fournisseur |

### Requêtes utiles

Lister les utilisateurs OAuth2 :
```sql
SELECT * FROM users WHERE oauth_provider IS NOT NULL;
```

Lister les utilisateurs par fournisseur :
```sql
SELECT * FROM users WHERE oauth_provider = 'google';
```

Trouver les comptes liés :
```sql
SELECT email, oauth_provider, COUNT(*) 
FROM users 
GROUP BY email 
HAVING COUNT(*) > 1;
```

## 🌐 Production

### Configuration HTTPS
Pour la production, OAuth2 nécessite HTTPS :

1. Obtenir un certificat SSL
2. Configurer Spring Boot pour HTTPS
3. Mettre à jour les URI de redirection chez les fournisseurs :
   ```
   https://votre-domaine.com/login/oauth2/code/google
   https://votre-domaine.com/login/oauth2/code/facebook
   https://votre-domaine.com/login/oauth2/code/linkedin
   ```

### Variables d'environnement
Pour la production, utilisez des variables d'environnement :

```properties
spring.security.oauth2.client.registration.google.client-id=${GOOGLE_CLIENT_ID}
spring.security.oauth2.client.registration.google.client-secret=${GOOGLE_CLIENT_SECRET}
```

## 📚 Ressources

- [Spring Security OAuth2](https://spring.io/guides/tutorials/spring-boot-oauth2)
- [Google OAuth2 Setup](https://developers.google.com/identity/protocols/oauth2)
- [Facebook Login](https://developers.facebook.com/docs/facebook-login)
- [LinkedIn OAuth2](https://learn.microsoft.com/en-us/linkedin/shared/authentication/authentication)
- [Vaadin Security](https://vaadin.com/docs/latest/security)

## ✅ Checklist de déploiement

- [ ] Java 21 installé et configuré
- [ ] Clés OAuth2 obtenues pour Google
- [ ] Clés OAuth2 obtenues pour Facebook
- [ ] Clés OAuth2 obtenues pour LinkedIn
- [ ] `application.properties` configuré avec les vraies clés
- [ ] `VaadinSecurityConfig.java` créé
- [ ] Application compile sans erreur
- [ ] Test de connexion email/password OK
- [ ] Test de connexion Google OK
- [ ] Test de connexion Facebook OK
- [ ] Test de connexion LinkedIn OK
- [ ] URI de redirection configurées en production
- [ ] HTTPS configuré en production
- [ ] Variables d'environnement configurées en production

## 🎉 Prêt !

Une fois ces étapes complétées, votre application supportera :
- ✅ Connexion classique (email/password)
- ✅ Connexion via Google
- ✅ Connexion via Facebook
- ✅ Connexion via LinkedIn
- ✅ Liaison automatique de comptes
- ✅ Gestion sécurisée des utilisateurs

