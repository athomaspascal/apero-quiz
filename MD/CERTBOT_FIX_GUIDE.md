# 🔧 Fix Certbot - Obtenir un certificat Let's Encrypt

## 🔴 Problème identifié

```
Timeout during connect (likely firewall problem)
```

Let's Encrypt ne peut pas accéder au port 80 de votre machine depuis Internet.

---

## ✅ Solution 1 : Utiliser DNS Challenge (RECOMMANDÉ - Pas besoin d'ouvrir de ports!)

### Avantages
- ✅ Pas besoin d'ouvrir le port 80
- ✅ Fonctionne derrière un firewall/NAT
- ✅ Fonctionne même si un service utilise déjà le port 80

### Étapes

#### 1. Installer le plugin DuckDNS pour Certbot

```bash
# Windows avec pip
pip install certbot-dns-duckdns
```

#### 2. Créer un fichier de credentials DuckDNS

Créer `C:\Certbot\duckdns-credentials.ini` :

```ini
dns_duckdns_token = VOTRE_TOKEN_DUCKDNS
```

Remplacer `VOTRE_TOKEN_DUCKDNS` par votre token depuis https://www.duckdns.org

#### 3. Protéger le fichier

```bash
# Windows
icacls C:\Certbot\duckdns-credentials.ini /inheritance:r
icacls C:\Certbot\duckdns-credentials.ini /grant:r "%USERNAME%:R"
```

#### 4. Obtenir le certificat avec DNS challenge

```bash
certbot certonly ^
  --dns-duckdns ^
  --dns-duckdns-credentials C:\Certbot\duckdns-credentials.ini ^
  --dns-duckdns-propagation-seconds 60 ^
  -d apero-quiz.duckdns.org
```

**✅ Cette méthode fonctionne sans ouvrir de ports !**

---

## ✅ Solution 2 : Utiliser Cloudflare Tunnel (MEILLEURE SOLUTION)

### Avantages
- ✅ Certificat SSL automatique et gratuit
- ✅ Pas besoin de Certbot
- ✅ Pas besoin d'ouvrir de ports
- ✅ Fonctionne derrière n'importe quel firewall/NAT
- ✅ Protection DDoS gratuite
- ✅ CDN global

### Étapes rapides

#### 1. Installer cloudflared

Télécharger depuis : https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/

```bash
# Télécharger cloudflared-windows-amd64.exe
# Renommer en cloudflared.exe
```

#### 2. Authentification

```bash
cloudflared tunnel login
```

#### 3. Créer le tunnel

```bash
cloudflared tunnel create quiz-app
```

#### 4. Créer config.yml

Créer `%USERPROFILE%\.cloudflared\config.yml` :

```yaml
tunnel: <TUNNEL-ID-AFFICHE-PRECEDEMMENT>
credentials-file: C:\Users\athom\.cloudflared\<TUNNEL-ID>.json

ingress:
  - hostname: apero-quiz.duckdns.org
    service: https://localhost:8443
    originRequest:
      noTLSVerify: true
  - service: http_status:404
```

#### 5. Router le DNS

```bash
cloudflared tunnel route dns quiz-app apero-quiz.duckdns.org
```

#### 6. Démarrer le tunnel

```bash
cloudflared tunnel run quiz-app
```

#### 7. Accéder via HTTPS

```
https://apero-quiz.duckdns.org
```

**✅ Le certificat SSL est géré automatiquement par Cloudflare !**

---

## ❌ Solution 3 : Ouvrir le port 80 (Complexe, non recommandé)

### Si vous voulez vraiment utiliser Certbot standalone

#### 1. Vérifier le pare-feu Windows

```bat
tools\check-port-80.bat
```

#### 2. Configurer votre routeur/box Internet

1. Se connecter au routeur (ex: http://192.168.1.1)
2. Chercher "Redirection de ports" ou "Port Forwarding"
3. Ajouter une règle :
   - **Port externe** : 80
   - **Port interne** : 80
   - **IP locale** : Votre IP locale (ex: 192.168.1.90)
   - **Protocole** : TCP
4. Sauvegarder

#### 3. Vérifier que le port est ouvert

Tester depuis : https://www.yougetsignal.com/tools/open-ports/

- IP : Votre IP publique (voir avec `curl https://api.ipify.org`)
- Port : 80

#### 4. Arrêter tout service sur le port 80

```bash
# Vérifier ce qui écoute sur le port 80
netstat -ano | findstr ":80"

# Arrêter l'application Spring Boot si elle tourne
# Arrêter IIS si installé
# Arrêter Apache/Nginx si installés
```

#### 5. Relancer Certbot

```bash
certbot certonly --standalone -d apero-quiz.duckdns.org
```

---

## 🎯 Comparaison des solutions

| Solution | Difficulté | Ports à ouvrir | Recommandation |
|----------|-----------|----------------|----------------|
| **DNS Challenge** | ⭐⭐ Moyenne | Aucun | ✅ Bon si vous voulez Certbot |
| **Cloudflare Tunnel** | ⭐ Facile | Aucun | ✅✅ MEILLEURE SOLUTION |
| **Standalone + Port 80** | ⭐⭐⭐ Difficile | Port 80 | ❌ Complexe et risqué |

---

## 📝 Ma recommandation

### Pour votre cas (PC + smartphone en hotspot)

**Utilisez Cloudflare Tunnel** car :
- Votre smartphone peut avoir un NAT CGNAT (IP partagée)
- Impossible d'ouvrir des ports sur un hotspot mobile
- Cloudflare gère tout automatiquement
- Certificat SSL gratuit et valide
- Aucune configuration complexe

---

## 🚀 Script automatique pour Cloudflare Tunnel

Voulez-vous que je crée un script automatique pour configurer Cloudflare Tunnel ?

C'est la solution la plus simple et la plus robuste pour votre configuration.

---

## ❓ FAQ

**Q: Pourquoi le port 80 ne fonctionne pas ?**  
R: Votre smartphone en hotspot bloque probablement les connexions entrantes. C'est normal.

**Q: Le DNS challenge nécessite-t-il des ports ouverts ?**  
R: Non ! Il valide via DNS uniquement.

**Q: Cloudflare Tunnel est-il gratuit ?**  
R: Oui, complètement gratuit pour usage personnel.

**Q: Mon certificat auto-signé fonctionne, pourquoi changer ?**  
R: Le certificat auto-signé fonctionne mais affiche un avertissement. Un certificat Let's Encrypt est reconnu par tous les navigateurs.

---

## 📞 Prochaine étape

**Choix recommandé** : Cloudflare Tunnel

Dites-moi si vous voulez que je crée les scripts automatiques pour Cloudflare Tunnel !

