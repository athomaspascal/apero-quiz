# Guide d'Accès - Smartphone via Partage de Connexion

## Date
27 décembre 2025

## Configuration Actuelle

### PC (Serveur)
- **Adresse IP WiFi** : `10.154.57.110`
- **Port HTTPS** : `8443`
- **Port HTTP** : `8089` (commenté dans application.properties)
- **SSL/HTTPS** : Activé
- **Certificat** : Auto-signé (keystore.p12)

### Configuration Réseau
- PC connecté au point d'accès mobile du smartphone
- Réseau : 10.154.57.0/24
- Passerelle: 10.154.57.31

## 🌐 URLs d'Accès depuis le Smartphone

### Option 1: HTTPS (Configuration Actuelle) ⚠️
```
https://10.154.57.110:8443
```

**⚠️ PROBLÈME** : Le smartphone affichera un avertissement de sécurité car le certificat est auto-signé.

**Solutions** :
1. **Accepter l'avertissement** sur le smartphone (Not Secure / Pas sécurisé)
   - Chrome/Safari: Cliquer sur "Avancé" puis "Continuer vers le site"
   - Firefox: Cliquer sur "Avancé" puis "Accepter le risque"

2. **Installer le certificat** sur le smartphone (recommandé pour utilisation régulière)

### Option 2: HTTP (Sans SSL) ✅ RECOMMANDÉ POUR RÉSEAU LOCAL
Pour éviter les problèmes de certificat sur réseau local privé :

```
http://10.154.57.110:8089
```

**Avantage** : Pas d'avertissement de sécurité
**Inconvénient** : Connexion non chiffrée (acceptable sur réseau privé local)

## 📋 Instructions de Configuration

### Pour activer HTTP (port 8089)

Modifier `application.properties` :

```properties
# Désactiver HTTPS
#server.ssl.enabled=true
server.ssl.enabled=false

# Utiliser le port 8089
server.port=8089
```

### Pour garder HTTPS (port 8443)

Garder la configuration actuelle et accepter l'avertissement sur le smartphone.

## 🔧 Étapes pour Connecter le Smartphone

### 1. Vérifier la Configuration Réseau

**Sur le PC** :
```bash
ipconfig
```
Vérifier que l'adresse IP WiFi est bien `10.154.57.110`

**Sur le smartphone** :
- Paramètres → WiFi → Votre point d'accès
- Vérifier que le PC est bien connecté à votre hotspot

### 2. Vérifier que l'Application est Lancée

**Sur le PC** :
```bash
# Aller dans le dossier du projet
cd C:\Users\athom\IdeaProjects\quizz1

# Lancer l'application
mvnw spring-boot:run
```

Ou utiliser le script :
```bash
run-app.bat
```

### 3. Vérifier le Pare-feu Windows

Le pare-feu doit autoriser :
- Port **8443** (HTTPS) ou
- Port **8089** (HTTP)

**Commande de vérification** :
```bash
netsh advfirewall firewall show rule name=all | findstr 8443
netsh advfirewall firewall show rule name=all | findstr 8089
```

### 4. Accéder depuis le Smartphone

**Ouvrir le navigateur** sur le smartphone et taper :
- HTTPS: `https://10.154.57.110:8443`
- HTTP: `http://10.154.57.110:8089`

## 🔍 Dépannage

### Problème 1: "Site inaccessible" ou "Connexion impossible"

**Solutions** :
1. Vérifier que le PC et le smartphone sont sur le même réseau WiFi
2. Vérifier que l'application est bien lancée sur le PC
3. Vérifier le pare-feu Windows :
   ```bash
   netsh advfirewall firewall add rule name="Quiz App HTTPS" dir=in action=allow protocol=TCP localport=8443
   netsh advfirewall firewall add rule name="Quiz App HTTP" dir=in action=allow protocol=TCP localport=8089
   ```

### Problème 2: "Certificat non sécurisé" (HTTPS uniquement)

**Sur Chrome/Safari** :
1. Cliquer sur "Avancé" ou "Advanced"
2. Cliquer sur "Continuer vers 10.154.57.110 (non sécurisé)"

**Sur Firefox** :
1. Cliquer sur "Avancé"
2. Cliquer sur "Accepter le risque et continuer"

### Problème 3: L'adresse IP change

Si l'adresse IP du PC change :
1. Exécuter `ipconfig` sur le PC
2. Noter la nouvelle adresse IPv4 de la carte WiFi
3. Utiliser cette nouvelle adresse dans l'URL

### Problème 4: Connexion lente

**Optimisations** :
1. Rapprocher le smartphone et le PC
2. Désactiver les autres appareils connectés au hotspot
3. Vérifier la qualité du signal WiFi

## 📱 Test de Connectivité

### Depuis le Smartphone

**Test 1: Ping** (avec une app de terminal ou depuis un PC sur le même réseau)
```bash
ping 10.154.57.110
```
Résultat attendu : Réponses reçues

**Test 2: Accès navigateur**
Ouvrir le navigateur et taper l'URL complète avec le port

## 🎯 Recommandation

### Pour un usage rapide et sans configuration :

1. **Modifier application.properties** pour désactiver SSL :
   ```properties
   server.ssl.enabled=false
   server.port=8089
   ```

2. **Ouvrir le pare-feu** :
   ```bash
   netsh advfirewall firewall add rule name="Quiz App HTTP" dir=in action=allow protocol=TCP localport=8089
   ```

3. **Accéder via** :
   ```
   http://10.154.57.110:8089
   ```

### Pour un usage avec sécurité SSL :

1. **Garder la configuration HTTPS actuelle**

2. **Sur le smartphone**, accepter l'avertissement de certificat une seule fois

3. **Accéder via** :
   ```
   https://10.154.57.110:8443
   ```

## 📊 Résumé des URLs

| Configuration | URL | Avantages | Inconvénients |
|--------------|-----|-----------|---------------|
| **HTTPS (actuel)** | https://10.154.57.110:8443 | Connexion sécurisée | Avertissement certificat |
| **HTTP** | http://10.154.57.110:8089 | Pas d'avertissement | Connexion non chiffrée |

## 🔐 Note sur la Sécurité

Sur un réseau local privé (partage de connexion smartphone), l'utilisation de HTTP est acceptable car :
- Le trafic ne passe pas par Internet
- Seuls vos appareils sont sur le réseau
- Pas de risque d'interception externe

## 📝 Checklist Rapide

- [ ] PC connecté au hotspot du smartphone
- [ ] Application lancée sur le PC
- [ ] Pare-feu autorise le port (8443 ou 8089)
- [ ] Adresse IP vérifiée avec `ipconfig`
- [ ] URL testée dans le navigateur du smartphone
- [ ] Avertissement certificat accepté (si HTTPS)

## 🆘 Support

En cas de problème, vérifier dans cet ordre :
1. Connexion réseau (même WiFi)
2. Application lancée
3. Pare-feu configuré
4. Adresse IP correcte
5. Port correct dans l'URL

---

**Dernière mise à jour** : 27 décembre 2025
**Adresse IP actuelle** : 10.154.57.110
**Configuration** : HTTPS sur port 8443

