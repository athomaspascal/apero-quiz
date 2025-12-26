# 🔒 Configuration SSL/HTTPS pour l'Application Quiz

## 🎯 Objectif
Configurer HTTPS avec un certificat SSL valide pour sécuriser l'application sur https://192.168.1.90:8443

## 📋 Options Disponibles

### Option 1: Certificat Auto-Signé (Pour Développement/Test)
- ✅ Rapide à mettre en place
- ✅ Gratuit
- ⚠️ Avertissement de sécurité dans le navigateur
- ✅ Bon pour environnement local/développement

### Option 2: Let's Encrypt (Certificat Gratuit Valide)
- ✅ Certificat valide reconnu par tous les navigateurs
- ✅ Gratuit
- ⚠️ Nécessite un nom de domaine public
- ⚠️ Renouvellement tous les 90 jours

### Option 3: Certificat Payant (Autorité de Certification)
- ✅ Certificat professionnel
- ✅ Support garanti
- ⚠️ Coût annuel
- ✅ Validation étendue possible

---

## 🚀 SOLUTION RECOMMANDÉE : Certificat Auto-Signé + Let's Encrypt

Je vais vous fournir les deux configurations :
1. **Certificat auto-signé** pour démarrer immédiatement
2. **Guide Let's Encrypt** pour un certificat valide si vous avez un domaine

---

## 📝 ÉTAPE 1 : Générer un Certificat Auto-Signé

### Script de Génération Automatique

Créons un script pour générer le certificat :

```batch
@echo off
echo ============================================================
echo   GENERATION CERTIFICAT SSL AUTO-SIGNE
echo   Application Quiz - 192.168.1.90:8443
echo ============================================================
echo.

set KEYSTORE_PATH=src\main\resources\keystore.p12
set KEYSTORE_PASSWORD=quiz-app-2025
set KEYSTORE_ALIAS=quiz-app
set VALIDITY_DAYS=365

echo [1] Verification de Java...
java -version
if errorlevel 1 (
    echo [ERREUR] Java non trouve!
    pause
    exit /b 1
)
echo [OK] Java trouve
echo.

echo [2] Generation du certificat SSL...
echo     Keystore: %KEYSTORE_PATH%
echo     Alias: %KEYSTORE_ALIAS%
echo     Validite: %VALIDITY_DAYS% jours
echo.

keytool -genkeypair ^
    -alias %KEYSTORE_ALIAS% ^
    -keyalg RSA ^
    -keysize 2048 ^
    -storetype PKCS12 ^
    -keystore %KEYSTORE_PATH% ^
    -validity %VALIDITY_DAYS% ^
    -storepass %KEYSTORE_PASSWORD% ^
    -keypass %KEYSTORE_PASSWORD% ^
    -dname "CN=192.168.1.90, OU=Quiz Application, O=Quiz App, L=Paris, ST=IDF, C=FR" ^
    -ext SAN=dns:192.168.1.90,dns:localhost,ip:192.168.1.90

if errorlevel 1 (
    echo [ERREUR] Echec de generation du certificat
    pause
    exit /b 1
)

echo.
echo [3] Verification du certificat...
keytool -list -v -keystore %KEYSTORE_PATH% -storepass %KEYSTORE_PASSWORD% -alias %KEYSTORE_ALIAS%

echo.
echo ============================================================
echo [SUCCESS] Certificat SSL genere avec succes!
echo ============================================================
echo.
echo Fichier: %KEYSTORE_PATH%
echo Mot de passe: %KEYSTORE_PASSWORD%
echo Alias: %KEYSTORE_ALIAS%
echo.
echo Prochaine etape: Configurer application.properties
echo.
pause
```

---

## 📝 ÉTAPE 2 : Configuration Spring Boot

### Modifications à Apporter dans application.properties

```properties
# Ancien (HTTP)
#server.address=192.168.1.90
#server.port=8089

# Nouveau (HTTPS)
server.address=192.168.1.90
server.port=8443

# SSL Configuration
server.ssl.enabled=true
server.ssl.key-store=classpath:keystore.p12
server.ssl.key-store-password=quiz-app-2025
server.ssl.key-store-type=PKCS12
server.ssl.key-alias=quiz-app

# Force HTTPS
server.ssl.enabled=true
security.require-ssl=true

# SSL Protocol
server.ssl.protocol=TLS
server.ssl.enabled-protocols=TLSv1.2,TLSv1.3
```

---

## 📝 ÉTAPE 3 : Configuration du Pare-feu

### Script pour Ouvrir le Port 8443

```batch
@echo off
echo ============================================================
echo   CONFIGURATION PARE-FEU POUR HTTPS (Port 8443)
echo ============================================================
echo.
echo ATTENTION: Ce script doit etre execute en tant qu'Administrateur
echo.
pause

echo [1] Suppression anciennes regles...
netsh advfirewall firewall delete rule name="Quiz App - HTTPS 8443" >nul 2>&1
echo [OK]

echo.
echo [2] Creation regle HTTPS entrant (port 8443)...
netsh advfirewall firewall add rule ^
    name="Quiz App - HTTPS 8443" ^
    dir=in ^
    action=allow ^
    protocol=TCP ^
    localport=8443 ^
    profile=any

echo [OK]

echo.
echo [3] Creation regle HTTPS sortant (port 8443)...
netsh advfirewall firewall add rule ^
    name="Quiz App - HTTPS 8443 Out" ^
    dir=out ^
    action=allow ^
    protocol=TCP ^
    localport=8443 ^
    profile=any

echo [OK]

echo.
echo [4] Verification des regles...
netsh advfirewall firewall show rule name="Quiz App - HTTPS 8443"

echo.
echo ============================================================
echo [SUCCESS] Pare-feu configure pour HTTPS!
echo ============================================================
echo.
echo Port 8443 autorise pour:
echo   - Connexions entrantes
echo   - Connexions sortantes
echo.
echo URL d'acces: https://192.168.1.90:8443
echo.
pause
```

---

## 🌐 ÉTAPE 4 : Let's Encrypt (Certificat Valide)

### Prérequis
1. Nom de domaine public (ex: quiz.mondomaine.com)
2. Le domaine pointe vers votre IP publique
3. Port 80 et 443 ouverts sur votre routeur

### Installation avec Certbot

```batch
# Installer Certbot
winget install certbot

# Générer le certificat
certbot certonly --standalone -d quiz.mondomaine.com

# Les certificats sont dans:
# C:\Certbot\live\quiz.mondomaine.com\
```

### Convertir Let's Encrypt en PKCS12

```batch
@echo off
set DOMAIN=quiz.mondomaine.com
set CERT_PATH=C:\Certbot\live\%DOMAIN%
set OUTPUT=src\main\resources\keystore.p12
set PASSWORD=quiz-app-2025

openssl pkcs12 -export ^
    -in %CERT_PATH%\fullchain.pem ^
    -inkey %CERT_PATH%\privkey.pem ^
    -out %OUTPUT% ^
    -name quiz-app ^
    -passout pass:%PASSWORD%

echo Certificat converti: %OUTPUT%
```

---

## 📋 RÉCAPITULATIF DES FICHIERS À CRÉER

1. **generate-ssl-cert.bat** - Génère le certificat auto-signé
2. **configure-firewall-8443.bat** - Configure le pare-feu pour HTTPS
3. **application.properties** - Mise à jour avec configuration SSL
4. **convert-letsencrypt.bat** - Convertit Let's Encrypt (optionnel)

---

## 🔍 VÉRIFICATION

### Test de Connexion HTTPS

```batch
# Test local
curl -k https://192.168.1.90:8443

# Test depuis le navigateur
https://192.168.1.90:8443
```

### Vérifier le Certificat

```batch
keytool -list -v -keystore src\main\resources\keystore.p12 -storepass quiz-app-2025
```

---

## ⚠️ NOTES IMPORTANTES

### Certificat Auto-Signé
- Le navigateur affichera un avertissement de sécurité
- Cliquez sur "Avancé" puis "Accepter le risque"
- Normal pour un certificat auto-signé

### Migration HTTP → HTTPS
- Ancien port: 8089 (HTTP)
- Nouveau port: 8443 (HTTPS)
- Mettez à jour tous les liens/QR codes

### Renouvellement Let's Encrypt
- Les certificats expirent après 90 jours
- Automatiser avec une tâche planifiée:
```batch
certbot renew
# Puis reconvertir en PKCS12
```

---

## 🎊 URLS FINALES

**Avant (HTTP) :**
- http://192.168.1.90:8089

**Après (HTTPS) :**
- https://192.168.1.90:8443

---

**Voulez-vous que je génère tous les scripts et que je configure l'application maintenant ?**

