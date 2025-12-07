# 🚀 Démarrage Rapide OAuth2

## ⚡ En 5 minutes

### 1️⃣ Vérifier Java 21
```cmd
C:\Users\athom\.jdks\azul-21.0.9\bin\java.exe -version
```
Résultat attendu : `openjdk version "21.0.9"`

### 2️⃣ (Optionnel) Obtenir les Credentials OAuth2

Si vous voulez tester OAuth2, créez rapidement une app Google :

1. Aller sur https://console.cloud.google.com/
2. **APIs & Services** → **Credentials** → **Create Credentials** → **OAuth client ID**
3. Type : **Web application**
4. **Authorized redirect URIs** : `http://localhost:8080/login/oauth2/code/google`
5. Copier le **Client ID** et **Client Secret**

### 3️⃣ Configurer (si vous avez des credentials)

Ouvrir `src/main/resources/application.properties` :

```properties
spring.security.oauth2.client.registration.google.client-id=VOTRE_CLIENT_ID_ICI
spring.security.oauth2.client.registration.google.client-secret=VOTRE_SECRET_ICI
```

**Note** : Si vous ne configurez pas OAuth2, l'application fonctionnera quand même avec la connexion classique (email/password).

### 4️⃣ Démarrer l'Application

**Option A** : Double-cliquer sur `start-with-java21.bat`

**Option B** : IntelliJ IDEA
1. Ouvrir le projet
2. **File** → **Project Structure** → **Project** → SDK : Azul Java 21
3. Run `Application.main()`

**Option C** : Ligne de commande
```cmd
start-with-java21.bat
```

### 5️⃣ Tester

1. Ouvrir http://localhost:8080
2. Vous verrez la page de connexion avec :
   - Formulaire classique (email/password)
   - Bouton **Google** (si configuré)
   - Bouton **Facebook** (si configuré)
   - Bouton **LinkedIn** (si configuré)
   - Lien **Sign up** pour créer un compte

## 📱 Créer un Compte Test

Si vous n'avez pas configuré OAuth2 :

1. Cliquer sur **Sign up** sur la page de connexion
2. Remplir :
   - Nom : `Test User`
   - Email : `test@example.com`
   - Téléphone : `0123456789`
   - Mot de passe : `Test1234!`
3. Cliquer sur **Register**
4. Vous êtes connecté !

## 🎮 Jouer à un Quiz

1. Sur la page d'accueil, cliquer sur **Play** à côté d'un quiz
2. Lire la question
3. Sélectionner une réponse
4. Cliquer sur **Next**
5. Continuer jusqu'à la fin
6. Voir votre score final

## 📖 Documentation Complète

- **OAUTH2_CONFIGURATION.md** : Guide complet OAuth2
- **OAUTH2_RESUME.md** : Récapitulatif détaillé
- **README.md** : Documentation générale

## 🆘 Problèmes ?

### L'application ne démarre pas
```cmd
# Vérifier Java 21
C:\Users\athom\.jdks\azul-21.0.9\bin\java.exe -version

# Compiler d'abord
compile-java21.bat

# Puis démarrer
start-with-java21.bat
```

### Port 8080 déjà utilisé
Modifier dans `src/main/resources/application.properties` :
```properties
server.port=8081
```

### OAuth2 ne fonctionne pas
C'est normal si vous n'avez pas configuré les credentials. Utilisez la connexion classique ou créez un compte.

---

**Bon quiz ! 🎉**

