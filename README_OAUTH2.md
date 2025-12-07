# 🔐 Authentification OAuth2 - Implémentation Complète

## 📌 État actuel

✅ **Code OAuth2 implémenté**  
⚠️ **Nécessite Java 17+ pour compiler**  
📝 **Configuration requise pour chaque fournisseur**

---

## 🎯 Fonctionnalités implémentées

### Interface de connexion enrichie
- ✅ Formulaire classique email/password
- ✅ Bouton **Google** (connexion OAuth2)
- ✅ Bouton **Facebook** (connexion OAuth2)
- ✅ Bouton **LinkedIn** (connexion OAuth2)
- ✅ Lien "Mot de passe oublié"
- ✅ Lien "S'inscrire"
- ✅ Design moderne et responsive

### Gestion des utilisateurs
- ✅ Création automatique de compte OAuth2
- ✅ Liaison automatique de comptes (par email)
- ✅ Support multi-connexion (un utilisateur peut avoir plusieurs méthodes)
- ✅ Champs OAuth2 dans la base de données

### Sécurité
- ✅ Mots de passe hashés avec BCrypt
- ✅ Gestion de session
- ✅ Protection CSRF
- ✅ Support OAuth2 Client Spring Security

---

## 🚀 Démarrage rapide

### 1️⃣ Vérifier Java

```cmd
check-java.bat
```

**Requis : Java 17+**  
**Installé actuellement : Java 11.0.26** ⚠️

### 2️⃣ Installer Java 21

**Option A : Oracle JDK**
- Télécharger : https://www.oracle.com/java/technologies/downloads/#java21
- Installer
- Configurer JAVA_HOME

**Option B : Eclipse Temurin (Recommandé)**
- Télécharger : https://adoptium.net/temurin/releases/?version=21
- Installer
- Configurer JAVA_HOME

**Configuration Windows :**
```cmd
setx JAVA_HOME "C:\Program Files\Java\jdk-21"
setx PATH "%JAVA_HOME%\bin;%PATH%"
```

Redémarrer le terminal et l'IDE.

### 3️⃣ Obtenir les clés OAuth2

Consultez le guide détaillé : **[OAUTH2_QUICK_START.md](OAUTH2_QUICK_START.md)**

#### Google
- Console : https://console.cloud.google.com/
- Créer un projet → Activer Google+ API → Créer ID OAuth 2.0
- URI de redirection : `http://localhost:8080/login/oauth2/code/google`

#### Facebook
- Console : https://developers.facebook.com/
- Créer une app → Ajouter Facebook Login
- URI de redirection : `http://localhost:8080/login/oauth2/code/facebook`

#### LinkedIn
- Console : https://www.linkedin.com/developers/
- Créer une app → Activer OpenID Connect
- URI de redirection : `http://localhost:8080/login/oauth2/code/linkedin`

### 4️⃣ Configurer application.properties

Éditer `src/main/resources/application.properties` :

```properties
# Google OAuth2
spring.security.oauth2.client.registration.google.client-id=VOTRE_CLIENT_ID
spring.security.oauth2.client.registration.google.client-secret=VOTRE_CLIENT_SECRET

# Facebook OAuth2
spring.security.oauth2.client.registration.facebook.client-id=VOTRE_APP_ID
spring.security.oauth2.client.registration.facebook.client-secret=VOTRE_APP_SECRET

# LinkedIn OAuth2
spring.security.oauth2.client.registration.linkedin.client-id=VOTRE_CLIENT_ID
spring.security.oauth2.client.registration.linkedin.client-secret=VOTRE_CLIENT_SECRET
```

### 5️⃣ Créer VaadinSecurityConfig

Créer `src/main/java/com/quizz/examplefeature/security/VaadinSecurityConfig.java` :

```java
package com.quizz.core.security;

import com.vaadin.flow.spring.security.VaadinWebSecurity;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;

@Configuration
@EnableWebSecurity
public class VaadinSecurityConfig extends VaadinWebSecurity {

    @Override
    protected void configure(HttpSecurity http) throws Exception {
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

### 6️⃣ Compiler et lancer

```cmd
mvn clean install
mvn spring-boot:run
```

Ou utilisez :
```cmd
start-app.bat
```

---

## 📂 Fichiers modifiés/créés

### ✏️ Modifiés
| Fichier | Modifications |
|---------|---------------|
| `pom.xml` | Ajout dépendances Spring Security OAuth2 |
| `User.java` | Champs `oauthProvider` et `oauthProviderId` |
| `UserRepository.java` | Méthode `findByOauthProviderAndOauthProviderId()` |
| `UserService.java` | Méthode `createOrUpdateOAuthUser()` |
| `LoginView.java` | Boutons Google, Facebook, LinkedIn |
| `application.properties` | Configuration OAuth2 |

### 📄 Créés
| Fichier | Description |
|---------|-------------|
| `SecurityConfig.java` | Configuration de sécurité de base |
| `OAuth2UserService.java` | Service de traitement OAuth2 |
| `OAuth2LoginSuccessController.java` | Contrôleur de succès OAuth2 |
| `check-java.bat` | Script de vérification Java |
| `OAUTH2_SETUP_GUIDE.md` | Guide de configuration détaillé |
| `OAUTH2_STATUS.md` | État d'avancement |
| `OAUTH2_QUICK_START.md` | Guide de démarrage rapide |
| `README_OAUTH2.md` | Ce fichier |

---

## 🔍 Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     LoginView                           │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Email/Password Form                            │   │
│  │  ┌──────────────┐  ┌──────────────┐           │   │
│  │  │ Email        │  │ Password     │           │   │
│  │  └──────────────┘  └──────────────┘           │   │
│  │  [Login]  [Forgot Password?]                   │   │
│  └─────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────┐   │
│  │  OAuth2 Buttons                                 │   │
│  │  [🔵 Google]                                    │   │
│  │  [🔵 Facebook]                                  │   │
│  │  [🔵 LinkedIn]                                  │   │
│  └─────────────────────────────────────────────────┘   │
│  [Don't have an account? Sign up]                      │
└─────────────────────────────────────────────────────────┘
                         │
                         ↓
        ┌────────────────┴────────────────┐
        │                                  │
        ↓                                  ↓
┌──────────────────┐           ┌──────────────────────┐
│ Classic Login    │           │  OAuth2 Login        │
│                  │           │                      │
│ UserService      │           │ OAuth2UserService    │
│ PasswordEncoder  │           │ Spring Security      │
└──────────────────┘           └──────────────────────┘
        │                                  │
        └────────────────┬─────────────────┘
                         ↓
                ┌─────────────────┐
                │   User Entity   │
                │  ┌───────────┐  │
                │  │ name      │  │
                │  │ email     │  │
                │  │ telephone │  │
                │  │ password  │  │
                │  │ oauth...  │  │
                │  └───────────┘  │
                └─────────────────┘
```

---

## 🛠️ Dépannage

### ❌ Erreur : Java version incompatible
```
UnsupportedClassVersionError: class file version 61.0
```

**Solution :**
1. Exécuter `check-java.bat`
2. Installer Java 21
3. Configurer JAVA_HOME
4. Redémarrer IDE

### ❌ Erreur : redirect_uri_mismatch
```
Error 400: redirect_uri_mismatch
```

**Solution :**
Vérifier que l'URI dans la console du fournisseur correspond exactement :
- Format : `http://localhost:8080/login/oauth2/code/{provider}`
- Pas de slash à la fin
- Port correct

### ❌ Erreur : Invalid client credentials
```
[invalid_client] Invalid client credentials
```

**Solution :**
1. Vérifier Client ID et Secret dans `application.properties`
2. Pas d'espaces avant/après
3. Vérifier que les clés sont actives

### ❌ Les boutons OAuth2 ne répondent pas
**Solution :**
1. Vérifier que `VaadinSecurityConfig` est créé
2. Vérifier les logs pour les erreurs
3. Vérifier que Spring Security est bien configuré

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [OAUTH2_QUICK_START.md](OAUTH2_QUICK_START.md) | Guide de démarrage complet et détaillé |
| [OAUTH2_SETUP_GUIDE.md](OAUTH2_SETUP_GUIDE.md) | Configuration des fournisseurs OAuth2 |
| [OAUTH2_STATUS.md](OAUTH2_STATUS.md) | État d'avancement et prochaines étapes |

---

## ✅ Checklist

### Avant de démarrer
- [ ] Java 21 installé (`check-java.bat`)
- [ ] JAVA_HOME configuré
- [ ] IDE redémarré

### Configuration OAuth2
- [ ] Compte Google Cloud créé
- [ ] Clés Google OAuth2 obtenues
- [ ] Compte Facebook Developer créé
- [ ] Clés Facebook obtenues
- [ ] Compte LinkedIn Developer créé
- [ ] Clés LinkedIn obtenues
- [ ] `application.properties` configuré

### Code
- [ ] `VaadinSecurityConfig.java` créé
- [ ] Application compile sans erreur
- [ ] Tests de connexion effectués

### Production
- [ ] HTTPS configuré
- [ ] URI de redirection production configurées
- [ ] Variables d'environnement configurées
- [ ] Tests en production effectués

---

## 🎉 Résultat final

Une fois configuré, vos utilisateurs pourront :
- ✅ Se connecter avec email/password
- ✅ Se connecter avec Google en 1 clic
- ✅ Se connecter avec Facebook en 1 clic
- ✅ Se connecter avec LinkedIn en 1 clic
- ✅ Lier plusieurs méthodes de connexion
- ✅ Récupérer leur mot de passe
- ✅ S'inscrire facilement

---

## 🆘 Support

Pour toute question :
1. Consulter les guides dans ce répertoire
2. Vérifier les logs de l'application
3. Documentation Spring Security : https://spring.io/projects/spring-security
4. Documentation Vaadin Security : https://vaadin.com/docs/latest/security

---

**Développé pour Quiz Application** 🎯

