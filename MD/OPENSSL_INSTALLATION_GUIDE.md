# 🔧 Installation OpenSSL - Guide Rapide

## ⚠️ Problème

OpenSSL n'est pas installé sur votre système. Il est nécessaire pour convertir les certificats Let's Encrypt au format PKCS12.

---

## ✅ Solution Rapide (RECOMMANDÉE)

### Méthode 1 : Installation automatique

```bat
tools\install-openssl.bat
```

Choisissez l'option 1 pour télécharger et installer automatiquement.

---

## 📥 Installation manuelle (si le script ne fonctionne pas)

### Étape 1 : Télécharger OpenSSL

**Lien direct** : https://slproweb.com/download/Win64OpenSSL-3_0_13.exe

Ou allez sur : https://slproweb.com/products/Win32OpenSSL.html
- Choisissez : **Win64 OpenSSL v3.x Light** (environ 5 MB)

### Étape 2 : Installer

1. Exécutez l'installateur téléchargé
2. Acceptez la licence
3. Installez dans : `C:\Program Files\OpenSSL-Win64` (par défaut)
4. Cochez **"The OpenSSL binaries (/bin) directory"** si proposé
5. Terminez l'installation

### Étape 3 : Ajouter au PATH

**Option A : Automatique avec setx**
```bat
setx PATH "%PATH%;C:\Program Files\OpenSSL-Win64\bin"
```

**Option B : Manuel**
1. Panneau de configuration > Système > Paramètres système avancés
2. Variables d'environnement
3. Dans "Variables système", sélectionnez **PATH**
4. Cliquez sur **Modifier**
5. Cliquez sur **Nouveau**
6. Ajoutez : `C:\Program Files\OpenSSL-Win64\bin`
7. Cliquez sur **OK** partout

### Étape 4 : Vérifier

Fermez et rouvrez un nouveau terminal, puis :
```bat
openssl version
```

Devrait afficher : `OpenSSL 3.0.13 ...`

---

## 🔄 Après installation d'OpenSSL

Une fois OpenSSL installé, exécutez :

```bat
tools\install-letsencrypt-cert-auto.bat
```

Ce script va :
1. ✅ Chercher OpenSSL automatiquement (plusieurs emplacements)
2. ✅ Convertir les certificats Let's Encrypt
3. ✅ Installer dans votre application
4. ✅ Sauvegarder l'ancien keystore

---

## 🎯 Alternative : Git for Windows

Git for Windows inclut OpenSSL.

1. Téléchargez depuis : https://git-scm.com/download/win
2. Installez (installation par défaut)
3. OpenSSL sera disponible dans : `C:\Program Files\Git\usr\bin\openssl.exe`

Le script `install-letsencrypt-cert-auto.bat` détectera automatiquement cette installation.

---

## ⚡ Méthode ultra-rapide (PowerShell)

```powershell
# Télécharger et installer en une commande
$url = "https://slproweb.com/download/Win64OpenSSL-3_0_13.exe"
$output = "$env:TEMP\OpenSSL-Installer.exe"
Invoke-WebRequest -Uri $url -OutFile $output
Start-Process -FilePath $output -Wait
setx PATH "$env:PATH;C:\Program Files\OpenSSL-Win64\bin"
```

---

## 📋 Résumé - Étapes complètes

1. **Installer OpenSSL** (choisissez une méthode ci-dessus)
2. **Fermer et rouvrir le terminal**
3. **Vérifier** : `openssl version`
4. **Installer le certificat** : `tools\install-letsencrypt-cert-auto.bat`
5. **Redémarrer l'application** : `run-app.bat`
6. **Tester** : https://apero-quiz.duckdns.org:8443

---

## ❓ Problèmes courants

**Q: "openssl n'est pas reconnu..."**  
R: Le PATH n'est pas à jour. Fermez TOUS les terminaux et rouvrez-en un nouveau.

**Q: Le téléchargement échoue ?**  
R: Téléchargez manuellement depuis https://slproweb.com/products/Win32OpenSSL.html

**Q: Puis-je utiliser OpenSSL portable ?**  
R: Oui, mais ajoutez son chemin au PATH ou placez openssl.exe dans `C:\Windows\System32`

---

## 🚀 Prêt ?

**Exécutez maintenant** :
```bat
tools\install-openssl.bat
```

Ou téléchargez directement : https://slproweb.com/download/Win64OpenSSL-3_0_13.exe

