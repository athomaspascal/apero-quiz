# Guide de Configuration du Pare-feu Windows
## Pour l'Application Quiz (192.168.38.1:8089)

---

## 📋 Table des Matières

1. [Méthode Automatique (Recommandée)](#méthode-automatique)
2. [Méthode Manuelle](#méthode-manuelle)
3. [Vérification de la Configuration](#vérification)
4. [Dépannage](#dépannage)
5. [Accès depuis d'autres appareils](#accès-réseau)

---

## 🚀 Méthode Automatique (Recommandée)

### Étape 1 : Exécuter le script de configuration

1. **Clic droit** sur `configure-firewall.bat`
2. Sélectionner **"Exécuter en tant qu'administrateur"**
3. Confirmer l'UAC (Contrôle de compte utilisateur)
4. Le script va automatiquement :
   - Ajouter une règle pour le port 8089 (TCP)
   - Ajouter une règle pour Java
   - Configurer les profils réseau (privé et public)

### Étape 2 : Vérifier la configuration

Exécuter `check-firewall.bat` pour vérifier que tout fonctionne correctement.

---

## 🔧 Méthode Manuelle

### Option 1 : Via l'interface graphique Windows

#### A. Ouvrir le Pare-feu Windows

1. Appuyez sur `Win + R`
2. Tapez `wf.msc` et appuyez sur Entrée
3. Ou cherchez "Pare-feu Windows Defender avec sécurité avancée"

#### B. Créer une règle entrante

1. Cliquez sur **"Règles de trafic entrant"** dans le panneau de gauche
2. Cliquez sur **"Nouvelle règle..."** dans le panneau de droite
3. Sélectionnez **"Port"** et cliquez sur Suivant
4. Sélectionnez **"TCP"**
5. Sélectionnez **"Ports locaux spécifiques"** et entrez `8089`
6. Cliquez sur Suivant
7. Sélectionnez **"Autoriser la connexion"**
8. Cliquez sur Suivant
9. Cochez **Domaine**, **Privé**, et **Public**
10. Cliquez sur Suivant
11. Donnez un nom : `Quiz Application - Port 8089`
12. Cliquez sur Terminer

#### C. Créer une règle pour le programme Java

1. Cliquez sur **"Nouvelle règle..."**
2. Sélectionnez **"Programme"** et cliquez sur Suivant
3. Sélectionnez **"Chemin d'accès du programme"**
4. Entrez le chemin de Java, par exemple :
   ```
   C:\Users\athom\.jdks\azul-21.0.9\bin\java.exe
   ```
5. Cliquez sur Suivant
6. Sélectionnez **"Autoriser la connexion"**
7. Suivez les mêmes étapes que précédemment
8. Nommez la règle : `Quiz Application - Java`

### Option 2 : Via la ligne de commande

Ouvrez **PowerShell en tant qu'administrateur** et exécutez :

```powershell
# Règle pour le port 8089
netsh advfirewall firewall add rule name="Quiz Application - Port 8089" dir=in action=allow protocol=TCP localport=8089

# Règle pour Java
netsh advfirewall firewall add rule name="Quiz Application - Java" dir=in action=allow program="C:\Users\athom\.jdks\azul-21.0.9\bin\java.exe" enable=yes

# Règle pour tous les profils réseau
netsh advfirewall firewall add rule name="Quiz Application - Network Profile" dir=in action=allow protocol=TCP localport=8089 profile=private,public
```

---

## ✅ Vérification de la Configuration

### 1. Vérifier les règles du pare-feu

Exécutez `check-firewall.bat` ou utilisez PowerShell :

```powershell
# Voir toutes les règles pour le port 8089
netsh advfirewall firewall show rule name=all | findstr "8089"

# Voir les règles spécifiques
netsh advfirewall firewall show rule name="Quiz Application - Port 8089"
```

### 2. Vérifier que le port est en écoute

```cmd
netstat -an | findstr "8089"
```

Vous devriez voir :
```
TCP    192.168.38.1:8089      0.0.0.0:0              LISTENING
```

### 3. Tester l'accès local

Ouvrez un navigateur et allez à :
```
http://192.168.38.1:8089
```

### 4. Tester avec PowerShell

```powershell
Invoke-WebRequest -Uri "http://192.168.38.1:8089" -UseBasicParsing
```

---

## 🔍 Dépannage

### Problème 1 : "Accès refusé" lors de l'exécution du script

**Solution :** Le script doit être exécuté en tant qu'administrateur
- Clic droit sur le fichier `.bat`
- Sélectionner "Exécuter en tant qu'administrateur"

### Problème 2 : Le port n'est pas en écoute

**Vérifications :**
1. L'application est-elle démarrée ?
   ```cmd
   tasklist | findstr "java"
   ```

2. Vérifier le fichier `application.properties` :
   ```properties
   server.address=192.168.38.1
   server.port=8089
   ```

3. Vérifier les logs dans `logs/start.log`

### Problème 3 : Connexion refusée depuis un autre appareil

**Solutions :**

1. **Vérifier le pare-feu :**
   - Assurez-vous que la règle pour le profil "Public" est activée

2. **Vérifier le réseau :**
   ```cmd
   ping 192.168.38.1
   ```

3. **Vérifier que l'adresse IP est correcte :**
   - Exécutez `show-my-ip.bat` ou `ipconfig`
   - L'adresse doit correspondre à celle dans `application.properties`

4. **Désactiver temporairement le pare-feu pour tester :**
   ```cmd
   netsh advfirewall set allprofiles state off
   ```
   ⚠️ **Attention :** Réactivez-le ensuite !
   ```cmd
   netsh advfirewall set allprofiles state on
   ```

### Problème 4 : "JAVA_HOME n'est pas défini"

**Solution :**
Définir la variable d'environnement JAVA_HOME :

```cmd
setx JAVA_HOME "C:\Users\athom\.jdks\azul-21.0.9"
```

---

## 🌐 Accès depuis d'autres Appareils

### Configuration pour l'accès réseau

1. **Assurez-vous que tous les appareils sont sur le même réseau**
   - Vérifiez qu'ils ont des adresses IP dans la même plage (ex: 192.168.38.x)

2. **URL d'accès depuis d'autres appareils :**
   ```
   http://192.168.38.1:8089
   ```

3. **Partager l'URL avec un QR Code :**
   - L'application génère déjà des QR codes pour les sessions partagées
   - Utilisez le bouton "Share" dans la liste des quiz

4. **Pour les appareils mobiles :**
   - Assurez-vous que le WiFi est activé
   - Connectez-vous au même réseau WiFi que l'ordinateur hôte
   - Scannez le QR code ou entrez l'URL manuellement

### Vérifier l'accessibilité depuis un autre appareil

Sur l'appareil distant, ouvrez un navigateur et testez :
```
http://192.168.38.1:8089
```

Ou depuis un terminal/cmd sur l'appareil distant :
```cmd
ping 192.168.38.1
telnet 192.168.38.1 8089
```

---

## 📝 Commandes Utiles

### Lister toutes les règles du pare-feu

```cmd
netsh advfirewall firewall show rule name=all
```

### Afficher l'état du pare-feu

```cmd
netsh advfirewall show allprofiles
```

### Désactiver une règle spécifique

```cmd
netsh advfirewall firewall set rule name="Quiz Application - Port 8089" new enable=no
```

### Activer une règle spécifique

```cmd
netsh advfirewall firewall set rule name="Quiz Application - Port 8089" new enable=yes
```

### Supprimer toutes les règles de l'application

Exécutez `remove-firewall-rules.bat` en tant qu'administrateur.

---

## 🎯 Résumé des Scripts Fournis

| Script | Description | Privilèges Admin |
|--------|-------------|------------------|
| `configure-firewall.bat` | Configure automatiquement le pare-feu | ✅ Requis |
| `check-firewall.bat` | Vérifie l'état de la configuration | ❌ Non requis |
| `remove-firewall-rules.bat` | Supprime les règles du pare-feu | ✅ Requis |
| `show-my-ip.bat` | Affiche votre adresse IP | ❌ Non requis |
| `show-quiz-url.bat` | Affiche l'URL de l'application | ❌ Non requis |

---

## 🔒 Sécurité

### Recommandations :

1. **N'autorisez que le port 8089** - Ne pas ouvrir tous les ports
2. **Utilisez le profil "Privé"** pour les réseaux de confiance uniquement
3. **Surveillez les connexions** avec `netstat -an | findstr "8089"`
4. **Fermez le port** quand l'application n'est pas utilisée
5. **Utilisez HTTPS en production** (nécessite un certificat SSL)

### Pour fermer le port après utilisation :

```cmd
netsh advfirewall firewall set rule name="Quiz Application - Port 8089" new enable=no
```

---

## 📱 Configuration OAuth2 et Pare-feu

Si vous utilisez l'authentification OAuth2 (Google, Facebook, LinkedIn), assurez-vous que :

1. **Les URLs de redirection sont correctes :**
   ```
   http://192.168.38.1:8089/login/oauth2/code/google
   http://192.168.38.1:8089/login/oauth2/code/facebook
   http://192.168.38.1:8089/login/oauth2/code/linkedin
   ```

2. **Le pare-feu autorise les connexions sortantes** (généralement activé par défaut)

3. **Les certificats SSL sont valides** (pour HTTPS)

---

## 📞 Support

En cas de problème persistant :

1. Vérifiez les logs : `logs/start.log`
2. Exécutez `check-firewall.bat` pour diagnostiquer
3. Consultez la documentation Windows Defender
4. Vérifiez les paramètres de votre routeur si vous voulez accéder depuis Internet

---

**Date de création :** 2025-12-07
**Version de l'application :** Quiz App with OAuth2
**Port :** 8089
**Adresse IP :** 192.168.38.1

