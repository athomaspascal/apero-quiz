# 🌐 Comment obtenir son adresse IP avec un script .BAT

## 📝 Scripts créés

### 1. `my-ip-simple.bat` - Version simple
Script basique qui affiche :
- Votre adresse IP locale (réseau domestique)
- Votre adresse IP publique (Internet)

**Utilisation** :
```bash
my-ip-simple.bat
```

### 2. `show-my-ip.bat` - Version complète
Script détaillé avec :
- Adresse IP locale Wi-Fi
- Adresse IP publique
- Résumé de toutes les connexions réseau

**Utilisation** :
```bash
show-my-ip.bat
```

### 3. `get-ip.bat` - Version détaillée
Script avec plusieurs sections d'informations réseau.

---

## 🔧 Commandes utiles dans un script .BAT

### Obtenir l'IP locale (toutes les cartes)
```batch
ipconfig | findstr /C:"Adresse IPv4"
```

### Obtenir l'IP locale (une seule ligne)
```batch
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /C:"Adresse IPv4"') do echo %%a
```

### Obtenir l'IP publique
```batch
powershell -Command "(Invoke-WebRequest -Uri 'https://api.ipify.org' -UseBasicParsing).Content"
```

### Obtenir toutes les informations réseau
```batch
ipconfig /all
```

---

## 📊 Vos adresses IP actuelles

D'après la commande `ipconfig` :

### 🔌 Connexion Wi-Fi principale
- **IP locale** : `192.168.1.138`
- **Masque** : `255.255.255.0`
- **Passerelle** : `192.168.1.254`

### 💻 VMware Network Adapter VMnet1
- **IP locale** : `192.168.15.1`

### 💻 VMware Network Adapter VMnet8
- **IP locale** : `192.168.38.1`

---

## 🎯 Pour votre application de Quiz

Si vous souhaitez que les utilisateurs se connectent à votre application via le réseau local :

### URL d'accès depuis d'autres appareils
```
http://192.168.1.138:8080
```

### Créer un script pour afficher l'URL de connexion
```batch
@echo off
echo ========================================
echo   URL DE CONNEXION AU QUIZ
echo ========================================
echo.
echo Depuis ce PC :
echo   http://localhost:8080
echo.
echo Depuis d'autres appareils du réseau :
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /C:"Adresse IPv4"') do (
    echo   http:%%a:8080
)
echo.
echo ========================================
pause
```

---

## 💡 Conseil pour le partage de quiz

Pour permettre à d'autres utilisateurs de rejoindre votre quiz via QR code, vous devriez :

1. **Utiliser votre IP locale** (`192.168.1.138`) pour le réseau local
2. **Générer le QR code** avec l'URL : `http://192.168.1.138:8080/quiz-session/{session-code}`
3. **Configurer le pare-feu** pour autoriser les connexions sur le port 8080

---

**Date** : 7 décembre 2025

