# 📋 RÉCAPITULATIF - Installation Certificat Let's Encrypt

## ✅ État actuel

- ✅ Certificats Let's Encrypt téléchargés dans : `C:\Certbot\live\apero-quiz.duckdns.org`
- ⏳ OpenSSL nécessaire pour la conversion
- ⏳ Installation du certificat dans l'application en attente

---

## 🔧 ÉTAPES À SUIVRE

### Étape 1 : Installer OpenSSL (EN COURS)

Le téléchargement d'OpenSSL vient de démarrer dans votre navigateur.

**Actions à faire** :
1. ✅ Le fichier `Win64OpenSSL-3_0_13.exe` se télécharge
2. ✅ Exécutez l'installateur une fois téléchargé
3. ✅ Acceptez les termes de la licence
4. ✅ Installez dans : `C:\Program Files\OpenSSL-Win64` (par défaut)
5. ✅ Terminez l'installation

**Ajouter au PATH** :
```bat
setx PATH "%PATH%;C:\Program Files\OpenSSL-Win64\bin"
```

**Ou exécutez** :
```bat
tools\install-openssl.bat
```

---

### Étape 2 : Vérifier l'installation

**Fermez et rouvrez un NOUVEAU terminal**, puis :
```bat
openssl version
```

Devrait afficher : `OpenSSL 3.0.13 ...`

---

### Étape 3 : Installer le certificat dans l'application

```bat
tools\install-letsencrypt-cert-auto.bat
```

Ce script va :
- ✅ Détecter OpenSSL automatiquement
- ✅ Convertir `fullchain.pem` + `privkey.pem` → `keystore.p12`
- ✅ Sauvegarder l'ancien keystore
- ✅ Installer le nouveau certificat Let's Encrypt
- ✅ Vérifier le keystore

---

### Étape 4 : Redémarrer l'application

```bat
run-app.bat
```

---

### Étape 5 : Tester

Ouvrez votre navigateur :
```
https://apero-quiz.duckdns.org:8443
```

**✅ Le certificat Let's Encrypt devrait être accepté sans avertissement !**

---

## 📱 Accès depuis smartphone

### Si vous utilisez le port standard 443

Modifiez `application.properties` :
```properties
server.port=443
```

Puis accédez via :
```
https://apero-quiz.duckdns.org
```

### Si vous gardez le port 8443

```
https://apero-quiz.duckdns.org:8443
```

**Note** : Configurez la redirection de port sur votre routeur :
- Port externe : 443 → Port interne : 8443

---

## 🔄 Renouvellement (tous les 90 jours)

Let's Encrypt expire tous les 90 jours. Pour renouveler :

### Renouvellement manuel

```bat
REM 1. Renouveler le certificat
certbot renew

REM 2. Réinstaller dans l'application
tools\install-letsencrypt-cert-auto.bat

REM 3. Redémarrer l'application
run-app.bat
```

### Renouvellement automatique

Créez une tâche planifiée Windows :

```bat
REM Créer un script renew-and-install.bat :
@echo off
certbot renew --quiet
if errorlevel 0 (
    call C:\Users\athom\IdeaProjects\quizz1\tools\install-letsencrypt-cert-auto.bat
    REM Redémarrer l'application
    taskkill /IM java.exe /F
    timeout /t 5
    start C:\Users\athom\IdeaProjects\quizz1\run-app.bat
)
```

Ajoutez à Planificateur de tâches :
- Tous les 2 mois
- Exécuter : `renew-and-install.bat`

---

## 📊 Vérification du certificat

### Voir les informations du certificat

```bat
certbot certificates
```

### Tester le certificat en ligne

https://www.ssllabs.com/ssltest/

Entrez : `apero-quiz.duckdns.org`

---

## 🎯 Checklist complète

- [ ] OpenSSL téléchargé
- [ ] OpenSSL installé dans `C:\Program Files\OpenSSL-Win64`
- [ ] OpenSSL ajouté au PATH
- [ ] Terminal fermé et rouvert
- [ ] `openssl version` fonctionne
- [ ] `tools\install-letsencrypt-cert-auto.bat` exécuté
- [ ] Certificat converti en PKCS12
- [ ] Application redémarrée
- [ ] Test sur `https://apero-quiz.duckdns.org:8443`
- [ ] Certificat accepté sans avertissement ✅

---

## 📞 En cas de problème

### OpenSSL non trouvé après installation

```bat
REM Vérifier l'emplacement
dir "C:\Program Files\OpenSSL-Win64\bin\openssl.exe"

REM Ajouter manuellement au PATH
set PATH=%PATH%;C:\Program Files\OpenSSL-Win64\bin
setx PATH "%PATH%;C:\Program Files\OpenSSL-Win64\bin"
```

### Conversion échoue

Vérifiez les permissions sur les fichiers :
```bat
dir C:\Certbot\live\apero-quiz.duckdns.org
```

Si nécessaire, exécutez en tant qu'administrateur.

### L'application ne démarre pas

Vérifiez que le keystore est valide :
```bat
keytool -list -keystore src\main\resources\keystore.p12 -storepass quiz-app-2025
```

---

## 🚀 RÉSUMÉ - Commandes rapides

```bat
REM 1. Installer OpenSSL (téléchargement déjà lancé)
REM    Exécuter Win64OpenSSL-3_0_13.exe

REM 2. Fermer et rouvrir le terminal

REM 3. Installer le certificat
tools\install-letsencrypt-cert-auto.bat

REM 4. Redémarrer l'application
run-app.bat

REM 5. Tester
REM https://apero-quiz.duckdns.org:8443
```

---

**📖 Documentation complète** :
- [OPENSSL_INSTALLATION_GUIDE.md](OPENSSL_INSTALLATION_GUIDE.md)
- [LETSENCRYPT_GUIDE.md](LETSENCRYPT_GUIDE.md)
- [CERTBOT_FIX_GUIDE.md](CERTBOT_FIX_GUIDE.md)

**✅ Vous êtes sur la bonne voie ! Continuez avec les étapes ci-dessus.**

