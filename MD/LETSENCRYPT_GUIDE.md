# 🔒 Guide Let's Encrypt - Certificat SSL Gratuit et Valide

## Vue d'ensemble

Ce guide vous explique comment obtenir un **certificat SSL gratuit et reconnu** avec Let's Encrypt pour éviter les avertissements du navigateur.

---

## ⚠️ Prérequis IMPORTANTS

### 1. Nom de domaine public
- ❌ **Impossible** avec `apero-quiz.com` en local (192.168.x.x)
- ✅ **Nécessaire** : Domaine acheté et pointant vers IP publique
- 💡 **Alternatives** :
  - Acheter `apero-quiz.com` (~10€/an)
  - Utiliser un sous-domaine DuckDNS gratuit : `mon-quiz.duckdns.org`
  - Utiliser Cloudflare Tunnel (gratuit, pas besoin d'IP publique)

### 2. IP publique accessible
- Port 80 ou 443 ouvert sur votre routeur
- Let's Encrypt doit pouvoir valider votre domaine

---

## 🎯 Solution 1 : Certificat avec DuckDNS (GRATUIT + FACILE)

### Étape 1 : Créer un compte DuckDNS

1. Aller sur https://www.duckdns.org
2. Se connecter (Google, GitHub, etc.)
3. Créer un sous-domaine : `apero-quiz.duckdns.org`
4. Noter votre token

### Étape 2 : Pointer vers votre IP publique

```powershell
# Obtenir votre IP publique
curl https://api.ipify.org
```

Mettre à jour sur DuckDNS avec votre IP publique actuelle.

### Étape 3 : Installer Certbot (Windows)

```powershell
# Télécharger depuis https://certbot.eff.org/
# Ou avec chocolatey
choco install certbot
```

### Étape 4 : Obtenir le certificat

```bash
# Mode standalone (arrêter l'application Spring Boot d'abord)
certbot certonly --standalone -d apero-quiz.duckdns.org

# OU mode webroot (application en cours)
certbot certonly --webroot -w C:\chemin\vers\webroot -d apero-quiz.duckdns.org
```

### Étape 5 : Convertir le certificat pour Spring Boot

```powershell
# Certificats Let's Encrypt sont dans C:\Certbot\live\apero-quiz.duckdns.org\

# Convertir en PKCS12
openssl pkcs12 -export \
  -in C:\Certbot\live\apero-quiz.duckdns.org\fullchain.pem \
  -inkey C:\Certbot\live\apero-quiz.duckdns.org\privkey.pem \
  -out keystore.p12 \
  -name quiz-app \
  -passout pass:quiz-app-2025
```

### Étape 6 : Copier dans le projet

```bat
copy keystore.p12 src\main\resources\keystore.p12
```

### Étape 7 : Redirection de port sur le routeur

- Rediriger le port 443 externe vers 8443 interne (192.168.x.x:8443)
- Ou modifier `application.properties` pour utiliser le port 443

---

## 🎯 Solution 2 : Cloudflare Tunnel (PAS D'IP PUBLIQUE NÉCESSAIRE!)

### Avantages
- ✅ Pas besoin d'IP publique
- ✅ Pas besoin d'ouvrir de ports
- ✅ Certificat SSL automatique
- ✅ Protection DDoS gratuite
- ✅ Fonctionne derrière un NAT strict

### Étape 1 : Compte Cloudflare

1. Créer un compte sur https://cloudflare.com (gratuit)
2. Ajouter un domaine (ou utiliser un sous-domaine)

### Étape 2 : Installer cloudflared

```powershell
# Télécharger depuis https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/

# Windows : télécharger cloudflared-windows-amd64.exe
```

### Étape 3 : Authentification

```powershell
cloudflared tunnel login
```

### Étape 4 : Créer un tunnel

```powershell
# Créer le tunnel
cloudflared tunnel create quiz-app

# Noter l'ID du tunnel
```

### Étape 5 : Configurer le tunnel

Créer `config.yml` :

```yaml
tunnel: <TUNNEL-ID>
credentials-file: C:\Users\athom\.cloudflared\<TUNNEL-ID>.json

ingress:
  - hostname: apero-quiz.com
    service: https://localhost:8443
    originRequest:
      noTLSVerify: true
  - service: http_status:404
```

### Étape 6 : Router le DNS

```powershell
cloudflared tunnel route dns quiz-app apero-quiz.com
```

### Étape 7 : Démarrer le tunnel

```powershell
cloudflared tunnel run quiz-app
```

### Étape 8 : Accéder via HTTPS

```
https://apero-quiz.com
```

Le certificat SSL est géré automatiquement par Cloudflare !

---

## 🎯 Solution 3 : Certificat auto-signé de confiance (LOCAL SEULEMENT)

### Pour éviter l'avertissement en LOCAL

#### Option A : Importer dans le navigateur

```bat
# Exécuter le script fourni
tools\import-certificate-browser.bat
```

Puis suivre les instructions à l'écran.

#### Option B : Windows - Autorité de certification locale

1. Ouvrir le certificat (`src\main\resources\quiz-app-cert.crt`)
2. Installer le certificat
3. Sélectionner "Ordinateur local"
4. Choisir "Autorités de certification racines de confiance"
5. Terminer

#### Option C : Script PowerShell automatique

```powershell
# Exécuter en tant qu'administrateur
$cert = New-Object System.Security.Cryptography.X509Certificates.X509Certificate2("src\main\resources\quiz-app-cert.crt")
$store = New-Object System.Security.Cryptography.X509Certificates.X509Store("Root","LocalMachine")
$store.Open("ReadWrite")
$store.Add($cert)
$store.Close()

Write-Host "Certificat importe avec succes!"
```

---

## 📱 Solution 4 : Certificat pour smartphone

### Android

1. Transférer le certificat `.crt` sur le téléphone
2. Paramètres > Sécurité > Certificats > Installer depuis stockage
3. Sélectionner le fichier
4. Nommer : "Quiz App"
5. OK

### iOS

1. Envoyer le certificat par email
2. Ouvrir sur iPhone
3. Paramètres > Général > VPN et gestion de l'appareil
4. Installer le profil
5. Paramètres > Général > Informations > Réglages des certificats
6. Activer la confiance totale

---

## 🔄 Renouvellement automatique

### Let's Encrypt (expire tous les 90 jours)

```bat
REM Créer une tâche planifiée Windows

REM Script de renouvellement : renew-cert.bat
certbot renew --quiet
REM Convertir et copier le nouveau certificat
openssl pkcs12 -export -in ... -out keystore.p12 ...
copy keystore.p12 src\main\resources\
REM Redémarrer l'application
taskkill /IM java.exe /F
start app.bat
```

Ajouter à Planificateur de tâches Windows :
- Tous les mois
- Exécuter : `renew-cert.bat`

---

## 🎯 Recommandation finale

| Cas d'usage | Solution recommandée |
|-------------|---------------------|
| **Développement local** | Certificat auto-signé + Import navigateur |
| **Tests avec smartphone** | Import certificat sur smartphone |
| **Accès depuis Internet** | Cloudflare Tunnel (gratuit, facile) |
| **Production** | Let's Encrypt + DuckDNS ou domaine acheté |
| **Entreprise** | Certificat payant (DigiCert, etc.) |

---

## 🔍 Vérification

Après configuration, tester avec :

```bash
# Vérifier le certificat
openssl s_client -connect apero-quiz.com:443 -showcerts

# Tester depuis le navigateur
curl -v https://apero-quiz.com
```

---

## ❓ FAQ

**Q: Puis-je utiliser Let's Encrypt sans IP publique ?**  
R: Non, mais utilisez Cloudflare Tunnel à la place (gratuit et mieux).

**Q: Le certificat auto-signé est-il sécurisé ?**  
R: Oui pour le chiffrement, mais pas de validation d'identité. Bon pour le local.

**Q: Combien coûte un certificat payant ?**  
R: De 0€ (Let's Encrypt) à 300€/an (certificats EV pour entreprise).

**Q: Dois-je redémarrer l'application après import du certificat ?**  
R: Oui, si vous changez le fichier keystore.p12.

---

## 📞 Support

- Let's Encrypt : https://community.letsencrypt.org/
- Cloudflare : https://community.cloudflare.com/
- Certbot : https://eff-certbot.readthedocs.io/

---

**✅ Choisissez la solution adaptée à votre cas d'usage et suivez les étapes !**

