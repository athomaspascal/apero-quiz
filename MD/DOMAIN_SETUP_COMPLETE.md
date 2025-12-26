# ✅ CONFIGURATION DOMAINE "apero-quiz.com" - TERMINÉE

## 🎉 Résumé

Votre application Quiz est maintenant configurée pour être accessible via :
- **https://apero-quiz.com:8443**

Au lieu de :
- ~~https://192.168.1.90:8443~~

---

## 📋 Ce Qui a Été Fait

### 1. ✅ Scripts Créés

| Script | Description | Admin Requis |
|--------|-------------|--------------|
| `generate-ssl-cert-domain.bat` | Génère certificat SSL pour apero-quiz.com | Non |
| `configure-hosts-domain.bat` | Configure DNS local (fichier hosts) | **Oui** |
| `configure-firewall-8443.bat` | Ouvre le port HTTPS 8443 | **Oui** |
| `setup-domain.bat` | Script master - tout configurer | **Oui** (étape 2 et 3) |

### 2. ✅ Configuration application.properties

```properties
# Ancien
#server.address=192.168.1.90

# Nouveau - Accepte toutes les connexions
server.address=0.0.0.0

# Port HTTPS
server.port=8443

# SSL Configuration
server.ssl.enabled=true
server.ssl.key-store=classpath:keystore.p12
server.ssl.key-store-password=quiz-app-2025
server.ssl.key-store-type=PKCS12
server.ssl.key-alias=quiz-app
server.ssl.protocol=TLS
server.ssl.enabled-protocols=TLSv1.2,TLSv1.3
```

### 3. ✅ Documentation

- `MD/DOMAIN_CONFIGURATION.md` - Guide complet
- `MD/SSL_CONFIGURATION_GUIDE.md` - Guide SSL détaillé

---

## 🚀 DÉMARRAGE RAPIDE

### Option A : Configuration Automatique (Recommandé)

**Une seule commande :**
```batch
setup-domain.bat
```

Ce script va :
1. Générer le certificat SSL pour apero-quiz.com ✅
2. Configurer le fichier hosts (nécessite Admin) ⚠️
3. Configurer le pare-feu (nécessite Admin) ⚠️
4. Mettre à jour application.properties ✅

### Option B : Configuration Manuelle

**Étape par étape :**

#### 1. Générer le Certificat SSL
```batch
generate-ssl-cert-domain.bat
```

#### 2. Configurer DNS Local (en Administrateur)
```batch
# Clic droit > "Exécuter en tant qu'administrateur"
configure-hosts-domain.bat
```

#### 3. Configurer Pare-feu (en Administrateur)
```batch
# Clic droit > "Exécuter en tant qu'administrateur"
configure-firewall-8443.bat
```

#### 4. Démarrer l'Application
```batch
start_clean.bat
```

#### 5. Accéder à l'Application
Ouvrir le navigateur : **https://apero-quiz.com:8443**

---

## 🌐 URLs d'Accès

### Principales
- **https://apero-quiz.com:8443** ← Principal
- **https://www.apero-quiz.com:8443** ← Alternatif

### Fallback (IP)
- **https://192.168.1.90:8443** ← Fonctionne toujours
- **https://localhost:8443** ← Sur le serveur uniquement

---

## 📝 Configuration DNS Local

### Fichier Hosts Modifié

**Emplacement :** `C:\Windows\System32\drivers\etc\hosts`

**Contenu ajouté :**
```
# Quiz Application - apero-quiz.com
192.168.1.90    apero-quiz.com
192.168.1.90    www.apero-quiz.com
```

### Pour les Autres PC du Réseau

Chaque PC qui veut accéder au quiz doit avoir la même configuration :

**Option 1 : Script automatique (recommandé)**
```batch
# Sur chaque PC, exécuter en Administrateur :
configure-hosts-domain.bat
```

**Option 2 : Modification manuelle**
1. Ouvrir le Bloc-notes en Administrateur
2. Ouvrir `C:\Windows\System32\drivers\etc\hosts`
3. Ajouter :
   ```
   192.168.1.90    apero-quiz.com
   192.168.1.90    www.apero-quiz.com
   ```
4. Enregistrer

**Option 3 : DNS sur le routeur (tous les appareils)**
- Accéder à l'interface admin du routeur
- Ajouter dans DNS local :
  - Nom : `apero-quiz.com`
  - IP : `192.168.1.90`

---

## 🔒 Certificat SSL

### Informations

- **Type :** Auto-signé (développement/réseau local)
- **Domaine principal :** apero-quiz.com
- **Domaines alternatifs :** www.apero-quiz.com, 192.168.1.90, localhost
- **Validité :** 365 jours
- **Fichier :** `src/main/resources/keystore.p12`
- **Mot de passe :** `quiz-app-2025`
- **Alias :** `quiz-app`
- **Algorithme :** RSA 2048 bits
- **Protocoles :** TLSv1.2, TLSv1.3

### ⚠️ Avertissement du Navigateur

Le navigateur affichera un avertissement car le certificat est auto-signé :
- **Chrome/Edge :** "Votre connexion n'est pas privée"
- **Firefox :** "Avertissement : risque probable de sécurité"

**C'est NORMAL pour un certificat auto-signé.**

**Pour continuer :**
1. Cliquer sur **"Avancé"** ou **"Advanced"**
2. Cliquer sur **"Continuer vers apero-quiz.com"** ou **"Proceed to apero-quiz.com"**
3. L'application s'ouvrira normalement

---

## 🎯 Pour un Certificat VALIDE (Production)

Si vous voulez un certificat reconnu par tous les navigateurs (sans avertissement) :

### Option 1 : Acheter le Domaine + Let's Encrypt (Gratuit)

**1. Acheter "apero-quiz.com"**
- Registrars : OVH (~10€/an), Gandi, Namecheap
- Prix : environ 10-15€/an

**2. Configurer DNS**
```
Type: A
Nom: @
Valeur: Votre IP publique
TTL: 3600

Type: A
Nom: www
Valeur: Votre IP publique
TTL: 3600
```

**3. Ouvrir les Ports sur le Routeur**
- Port 80 → 192.168.1.90:8089 (ou 8080)
- Port 443 → 192.168.1.90:8443

**4. Installer Certbot**
```batch
winget install certbot
```

**5. Obtenir le Certificat**
```batch
certbot certonly --standalone -d apero-quiz.com -d www.apero-quiz.com
```

**6. Convertir en PKCS12**
```batch
openssl pkcs12 -export ^
    -in C:\Certbot\live\apero-quiz.com\fullchain.pem ^
    -inkey C:\Certbot\live\apero-quiz.com\privkey.pem ^
    -out src\main\resources\keystore.p12 ^
    -name quiz-app ^
    -passout pass:quiz-app-2025
```

**7. Configurer Renouvellement Automatique**
Les certificats Let's Encrypt expirent après 90 jours.
```batch
# Tâche planifiée Windows pour renouveler tous les 60 jours
schtasks /create /tn "Certbot Renew" /tr "certbot renew" /sc daily /st 03:00
```

**URLs finales :**
- **https://apero-quiz.com** (port 443 standard)
- Accessible depuis INTERNET

---

## 🔧 Dépannage

### Problème 1 : "apero-quiz.com" ne se résout pas

**Solution :**
```batch
# Vider le cache DNS
ipconfig /flushdns

# Tester la résolution
ping apero-quiz.com

# Doit afficher : 192.168.1.90
```

### Problème 2 : Certificat non valide

**Solution :**
- Régénérer le certificat : `generate-ssl-cert-domain.bat`
- Vérifier que le domaine est dans le certificat :
  ```batch
  keytool -list -v -keystore src\main\resources\keystore.p12 -storepass quiz-app-2025
  ```

### Problème 3 : "Connection refused"

**Vérifier :**
```batch
# Application en cours d'exécution ?
netstat -ano | findstr :8443

# Pare-feu ouvert ?
netsh advfirewall firewall show rule name="Quiz App - HTTPS 8443"
```

### Problème 4 : Fonctionne sur le serveur mais pas sur les autres PC

**Cause :** Le fichier hosts n'est pas configuré sur les autres PC

**Solution :**
- Exécuter `configure-hosts-domain.bat` en Admin sur chaque PC
- OU configurer le DNS dans le routeur

---

## 📊 Comparaison Avant/Après

| Aspect | Avant (IP) | Après (Domaine) |
|--------|-----------|-----------------|
| URL | https://192.168.1.90:8443 | https://apero-quiz.com:8443 |
| Mémorisation | ❌ Difficile | ✅ Facile |
| Professionnel | ⚠️ Non | ✅ Oui |
| QR Code | ❌ IP visible | ✅ Domaine visible |
| Certificat | Auto-signé | Auto-signé (valide avec Let's Encrypt) |
| Configuration client | Aucune | Fichier hosts OU DNS routeur |

---

## 📱 QR Code

Le QR code généré par l'application affichera maintenant :
```
https://apero-quiz.com:8443/session/ABC123
```

Au lieu de :
```
https://192.168.1.90:8443/session/ABC123
```

**Plus professionnel et plus facile à retenir !**

---

## ✅ Checklist de Vérification

- [ ] Certificat SSL généré pour apero-quiz.com
- [ ] Fichier hosts configuré sur le serveur
- [ ] Fichier hosts configuré sur les PC clients (ou DNS routeur)
- [ ] Port 8443 ouvert dans le pare-feu
- [ ] application.properties mis à jour (server.address=0.0.0.0)
- [ ] Application démarrée
- [ ] Test : https://apero-quiz.com:8443 fonctionne
- [ ] Certificat accepté dans le navigateur

---

## 🎊 RÉSUMÉ FINAL

### Configuration Actuelle

```
Domaine:     apero-quiz.com
Port HTTPS:  8443
URL Finale:  https://apero-quiz.com:8443
Certificat:  Auto-signé (365 jours)
DNS Local:   192.168.1.90 → apero-quiz.com
```

### Commandes Rapides

```batch
# Configuration complète
setup-domain.bat

# Démarrer l'application
start_clean.bat

# Accéder au quiz
https://apero-quiz.com:8443
```

### Pour Production (Optionnel)

1. Acheter le domaine (~10€/an)
2. Configurer DNS public
3. Obtenir certificat Let's Encrypt (gratuit)
4. Ouvrir ports 80 et 443 sur le routeur
5. URL finale : https://apero-quiz.com (port 443 standard)

---

**Votre application Quiz est maintenant accessible via https://apero-quiz.com:8443 ! 🎉**

**Pour démarrer, exécutez simplement : `setup-domain.bat`**

