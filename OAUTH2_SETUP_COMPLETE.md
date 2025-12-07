# ✅ Récapitulatif Configuration OAuth2

## 🎉 Configuration Terminée

L'application **Quizz1** est maintenant configurée pour l'authentification OAuth2 avec :
- ✅ Google OAuth2
- ✅ Facebook OAuth2
- ✅ LinkedIn OAuth2

## 📁 Fichiers Créés

### Classes Java

1. **CustomOAuth2UserService.java**
   - Service pour charger les utilisateurs OAuth2
   - Extraction des informations selon le provider
   - Création/liaison automatique des comptes

2. **CustomOAuth2User.java**
   - Wrapper pour OAuth2User avec notre entité User
   - Permet de stocker l'utilisateur dans la session

3. **OAuth2LoginSuccessHandler.java**
   - Gestionnaire de succès de connexion OAuth2
   - Stockage de l'utilisateur dans VaadinSession

4. **SecurityConfig.java** (modifié)
   - Configuration Spring Security avec OAuth2
   - Extension de VaadinWebSecurity
   - Configuration des endpoints OAuth2

### Scripts

1. **start-with-java21.bat**
   - Configure JAVA_HOME pour Java 21
   - Compile et démarre l'application

2. **compile-java21.bat**
   - Compile uniquement le projet avec Java 21

### Documentation

1. **OAUTH2_CONFIGURATION.md**
   - Guide complet de configuration OAuth2
   - Instructions pour Google, Facebook, LinkedIn
   - Dépannage et ressources

2. **oauth2-credentials.properties.template**
   - Template pour les credentials OAuth2
   - À copier et remplir avec vos vraies credentials

## 🔧 Configuration pom.xml

Le fichier `pom.xml` a été mis à jour avec :
```xml
<properties>
    <java.version>21</java.version>
    <maven.compiler.source>21</maven.compiler.source>
    <maven.compiler.target>21</maven.compiler.target>
    <maven.compiler.release>21</maven.compiler.release>
</properties>

<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-compiler-plugin</artifactId>
            <version>3.11.0</version>
            <configuration>
                <release>21</release>
                <source>21</source>
                <target>21</target>
            </configuration>
        </plugin>
    </plugins>
</build>
```

## 📝 Prochaines Étapes

### 1. Obtenir les Credentials OAuth2

#### Google
1. Aller sur https://console.cloud.google.com/
2. Créer un projet ou sélectionner un existant
3. **APIs & Services** → **Credentials** → **Create Credentials** → **OAuth client ID**
4. Type : **Web application**
5. **Authorized redirect URIs** : `http://localhost:8080/login/oauth2/code/google`
6. Copier **Client ID** et **Client Secret**

#### Facebook
1. Aller sur https://developers.facebook.com/
2. Créer une application ou utiliser une existante
3. **Settings** → **Basic**
4. Ajouter **Facebook Login** comme produit
5. **Facebook Login** → **Settings** → **Valid OAuth Redirect URIs** : `http://localhost:8080/login/oauth2/code/facebook`
6. Copier **App ID** et **App Secret**

#### LinkedIn
1. Aller sur https://www.linkedin.com/developers/
2. Créer une nouvelle application
3. **Auth** → **Redirect URLs** : `http://localhost:8080/login/oauth2/code/linkedin`
4. **Products** → Demander **Sign In with LinkedIn using OpenID Connect**
5. Copier **Client ID** et **Client Secret**

### 2. Configurer application.properties

Ouvrir `src/main/resources/application.properties` et remplacer :

```properties
# Google OAuth2
spring.security.oauth2.client.registration.google.client-id=VOTRE_VRAI_CLIENT_ID
spring.security.oauth2.client.registration.google.client-secret=VOTRE_VRAI_CLIENT_SECRET

# Facebook OAuth2
spring.security.oauth2.client.registration.facebook.client-id=VOTRE_VRAI_APP_ID
spring.security.oauth2.client.registration.facebook.client-secret=VOTRE_VRAI_APP_SECRET

# LinkedIn OAuth2
spring.security.oauth2.client.registration.linkedin.client-id=VOTRE_VRAI_CLIENT_ID
spring.security.oauth2.client.registration.linkedin.client-secret=VOTRE_VRAI_CLIENT_SECRET
```

### 3. Démarrer l'Application

#### Option A : Script Batch (Recommandé pour Windows)
```cmd
start-with-java21.bat
```

#### Option B : IntelliJ IDEA
1. **File** → **Project Structure** → **Project**
   - SDK : `C:\Users\athom\.jdks\azul-21.0.9`
   - Language Level : `21`

2. **Run** → **Edit Configurations** → **+** → **Application**
   - Name : `Quizz Application`
   - Main class : `com.quizz.Application`
   - JRE : `azul-21.0.9`

3. Cliquer sur le bouton **Run**

#### Option C : Ligne de commande
```cmd
set JAVA_HOME=C:\Users\athom\.jdks\azul-21.0.9
mvnw.cmd spring-boot:run
```

### 4. Tester OAuth2

1. Accéder à http://localhost:8080
2. Vous serez redirigé vers `/login`
3. Trois boutons OAuth2 sont disponibles :
   - **Google** (bleu Google)
   - **Facebook** (bleu Facebook)
   - **LinkedIn** (bleu LinkedIn)
4. Cliquer sur un bouton pour vous connecter
5. Autoriser l'application sur le provider OAuth2
6. Vous serez redirigé vers la page d'accueil

## 🎯 Architecture OAuth2

### Flux de Connexion

```
1. Utilisateur clique sur "Google"
   ↓
2. Redirection vers Google OAuth2
   ↓
3. Utilisateur s'authentifie sur Google
   ↓
4. Google redirige vers /login/oauth2/code/google avec un code
   ↓
5. Spring Security échange le code contre un token
   ↓
6. CustomOAuth2UserService charge les infos utilisateur
   ↓
7. User créé/récupéré dans la base de données
   ↓
8. OAuth2LoginSuccessHandler stocke User dans VaadinSession
   ↓
9. Redirection vers la page d'accueil (/)
```

### Base de Données

Table **users** :
- `user_id` : Long (PK)
- `name` : String (200)
- `email` : String (255) UNIQUE
- `telephone` : String (20)
- `password` : String (255) - vide pour OAuth2
- `oauth_provider` : String (50) - google/facebook/linkedin
- `oauth_provider_id` : String (255) - ID unique du provider

### Sécurité

- Mots de passe hashés avec **BCrypt**
- Comptes OAuth2 automatiquement liés par email
- Session sécurisée avec Spring Security
- Protection CSRF activée

## 🐛 Dépannage

### Erreur: "redirect_uri_mismatch"
**Solution** : Vérifier que l'URL de redirection dans la console du provider correspond exactement à :
- Google : `http://localhost:8080/login/oauth2/code/google`
- Facebook : `http://localhost:8080/login/oauth2/code/facebook`
- LinkedIn : `http://localhost:8080/login/oauth2/code/linkedin`

### Erreur: "Client authentication failed"
**Solution** : Vérifier que le Client ID et Client Secret sont corrects dans `application.properties`

### Erreur: "Email not available"
**Solution** : 
- Vérifier que les scopes incluent `email`
- Sur Google, l'email doit être public dans les paramètres du compte

### Application ne démarre pas
**Solution** : 
1. Vérifier que Java 21 est bien installé : `C:\Users\athom\.jdks\azul-21.0.9\bin\java.exe -version`
2. Utiliser le script `start-with-java21.bat`
3. Ou configurer IntelliJ pour utiliser Java 21

### Erreur de compilation Maven
**Solution** : 
1. Utiliser le script `compile-java21.bat`
2. Vérifier que `pom.xml` contient bien les propriétés Java 21

## 📚 Ressources

- [Spring Security OAuth2 Client](https://docs.spring.io/spring-security/reference/servlet/oauth2/client/index.html)
- [Vaadin with Spring Security](https://vaadin.com/docs/latest/security/enabling-security)
- [Google OAuth2 Documentation](https://developers.google.com/identity/protocols/oauth2)
- [Facebook Login Documentation](https://developers.facebook.com/docs/facebook-login/)
- [LinkedIn OAuth2 Documentation](https://learn.microsoft.com/en-us/linkedin/shared/authentication/authentication)

## ✨ Fonctionnalités Additionnelles Possibles

- [ ] Ajouter GitHub OAuth2
- [ ] Ajouter Microsoft OAuth2
- [ ] Implémenter le refresh token
- [ ] Gérer la révocation de token
- [ ] Ajouter des rôles et permissions
- [ ] Logger les tentatives de connexion
- [ ] Implémenter 2FA
- [ ] Gérer les erreurs OAuth2 personnalisées

---

**Configuration OAuth2 terminée ! 🎉**

Pour toute question, consultez [OAUTH2_CONFIGURATION.md](OAUTH2_CONFIGURATION.md)

