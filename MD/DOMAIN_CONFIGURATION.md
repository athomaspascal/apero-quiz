# 🌐 Configuration Domaine "apero-quiz.com"

## 🎯 Options Disponibles

### Option 1: DNS Local (Hosts File) - Réseau Local Uniquement
✅ Rapide et gratuit
✅ Fonctionne immédiatement sur votre réseau local
⚠️ Chaque utilisateur doit modifier son fichier hosts
⚠️ Ne fonctionne pas sur Internet

### Option 2: Domaine Public avec DNS
✅ Accessible depuis Internet
✅ Certificat SSL Let's Encrypt gratuit
✅ Pas de modification sur les clients
⚠️ Nécessite l'achat d'un nom de domaine (~10€/an)
⚠️ Configuration du routeur nécessaire

### Option 3: DNS Local sur le Réseau (Router/Pi-hole)
✅ Tous les appareils du réseau local voient le domaine
✅ Pas de modification manuelle sur chaque client
⚠️ Accès administrateur au routeur nécessaire
⚠️ Configuration du serveur DNS

---

## 🚀 SOLUTION 1: Configuration Hosts File (Local)

### Pour Chaque Utilisateur du Quiz

#### Sur Windows:
1. Ouvrir le Bloc-notes en tant qu'Administrateur
2. Ouvrir: `C:\Windows\System32\drivers\etc\hosts`
3. Ajouter la ligne:
   ```
   192.168.1.90    apero-quiz.com
   ```
4. Enregistrer et fermer

#### Sur Mac/Linux:
1. Terminal: `sudo nano /etc/hosts`
2. Ajouter la ligne:
   ```
   192.168.1.90    apero-quiz.com
   ```
3. Sauvegarder (Ctrl+O, Entrée, Ctrl+X)

### Régénérer le Certificat SSL

Le certificat doit inclure "apero-quiz.com":

```batch
keytool -genkeypair ^
    -alias quiz-app ^
    -keyalg RSA ^
    -keysize 2048 ^
    -storetype PKCS12 ^
    -keystore src\main\resources\keystore.p12 ^
    -validity 365 ^
    -storepass quiz-app-2025 ^
    -keypass quiz-app-2025 ^
    -dname "CN=apero-quiz.com, OU=Quiz Application, O=Apero Quiz, L=Paris, ST=IDF, C=FR" ^
    -ext "SAN=dns:apero-quiz.com,dns:www.apero-quiz.com,dns:192.168.1.90,dns:localhost,ip:192.168.1.90"
```

### URL d'Accès

**HTTP:** `http://apero-quiz.com:8089`
**HTTPS:** `https://apero-quiz.com:8443`

---

## 🚀 SOLUTION 2: Domaine Public (Recommandé pour Production)

### Étapes:

1. **Acheter le domaine "apero-quiz.com"**
   - Registrars: OVH, Gandi, Namecheap (~10€/an)

2. **Configurer les DNS**
   - Type A: `apero-quiz.com` → Votre IP publique
   - Type A: `www.apero-quiz.com` → Votre IP publique

3. **Ouvrir les ports sur votre routeur**
   - Port 80 (HTTP) → 192.168.1.90:8089
   - Port 443 (HTTPS) → 192.168.1.90:8443

4. **Obtenir un certificat Let's Encrypt gratuit**
   ```batch
   certbot certonly --standalone -d apero-quiz.com -d www.apero-quiz.com
   ```

5. **Convertir en PKCS12**
   ```batch
   openssl pkcs12 -export ^
       -in C:\Certbot\live\apero-quiz.com\fullchain.pem ^
       -inkey C:\Certbot\live\apero-quiz.com\privkey.pem ^
       -out src\main\resources\keystore.p12 ^
       -name quiz-app ^
       -passout pass:quiz-app-2025
   ```

### URL d'Accès
**HTTPS:** `https://apero-quiz.com`

---

## 🚀 SOLUTION 3: DNS sur le Routeur

### Si vous avez accès au routeur:

1. Accéder à l'interface d'administration du routeur
2. Trouver la section "DNS Local" ou "DHCP/DNS"
3. Ajouter une entrée DNS:
   - Nom: `apero-quiz.com`
   - IP: `192.168.1.90`

### Avantages:
- Tous les appareils du réseau voient automatiquement le domaine
- Pas de modification manuelle sur chaque appareil
- Fonctionne pour smartphones, tablettes, etc.

---

## 📝 Fichier application.properties

Modifier pour utiliser le domaine:

```properties
# Ancien
#server.address=192.168.1.90

# Nouveau - accepter toutes les connexions
server.address=0.0.0.0

# Port HTTPS
server.port=8443

# SSL avec domaine
server.ssl.enabled=true
server.ssl.key-store=classpath:keystore.p12
server.ssl.key-store-password=quiz-app-2025
server.ssl.key-store-type=PKCS12
server.ssl.key-alias=quiz-app
```

---

## ⚡ SCRIPTS AUTOMATIQUES

Je vais créer des scripts pour automatiser ces configurations.

