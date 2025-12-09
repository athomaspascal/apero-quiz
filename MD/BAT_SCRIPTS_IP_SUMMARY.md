# ✅ Scripts BAT pour Obtenir l'Adresse IP - CRÉÉS AVEC SUCCÈS

## 📦 Scripts disponibles

### 1. `my-ip-simple.bat` ⭐ RECOMMANDÉ
**Usage** : Affichage rapide des adresses IP
```batch
my-ip-simple.bat
```
**Affiche** :
- ✅ Adresse IP locale (réseau domestique)
- ✅ Adresse IP publique (Internet)

---

### 2. `show-my-ip.bat` 
**Usage** : Affichage détaillé avec émojis
```batch
show-my-ip.bat
```
**Affiche** :
- 🌐 Adresse IP locale (Wi-Fi)
- 🌍 Adresse IP publique (Internet)
- 📋 Résumé de toutes les connexions réseau

---

### 3. `show-quiz-url.bat` ⭐ SPÉCIAL QUIZ
**Usage** : Affiche les URLs pour accéder à votre application de quiz
```batch
show-quiz-url.bat
```
**Affiche** :
- 📱 URL locale : `http://localhost:8080`
- 🌐 URL réseau : `http://192.168.1.138:8080`
- 💡 Instructions pour les participants

**Parfait pour partager l'accès à votre quiz !**

---

### 4. `get-ip.bat`
**Usage** : Version avec plusieurs sections d'informations
```batch
get-ip.bat
```

---

## 🎯 Vos adresses IP actuelles

### Wi-Fi (Connexion principale)
```
IP locale  : 192.168.1.138
Masque     : 255.255.255.0
Passerelle : 192.168.1.254
```

### Autres adaptateurs
- VMware VMnet1 : `192.168.15.1`
- VMware VMnet8 : `192.168.38.1`

---

## 🚀 Utilisation pour votre application Quiz

### Accès local (depuis votre PC)
```
http://localhost:8080
```

### Accès réseau (depuis autres appareils)
```
http://192.168.1.138:8080
```

### Pour partager une session de quiz
1. Lancez `show-quiz-url.bat` pour obtenir l'URL
2. Partagez l'URL avec les participants
3. Ils doivent être sur le même réseau Wi-Fi
4. L'URL complète de session sera :
   ```
   http://192.168.1.138:8080/quiz-session/XXXXXXXX
   ```
   (où XXXXXXXX est le code de session à 8 caractères)

---

## 💡 Commandes utiles

### Dans un script .bat
```batch
:: IP locale
ipconfig | findstr /C:"Adresse IPv4"

:: IP publique
powershell -Command "(Invoke-WebRequest -Uri 'https://api.ipify.org' -UseBasicParsing).Content"

:: Toutes les infos réseau
ipconfig /all
```

### En ligne de commande directe
```cmd
ipconfig
ipconfig /all
```

---

## 🔥 Conseil PRO pour le partage de quiz

Modifiez votre classe `QRCodeGenerator` pour utiliser l'IP locale au lieu de localhost :

```java
String baseUrl = "http://192.168.1.138:8080/quiz-session/";
String qrUrl = baseUrl + sessionCode;
```

Ainsi, le QR code généré fonctionnera directement sur tous les appareils du réseau !

---

**Date de création** : 7 décembre 2025  
**Statut** : ✅ TOUS LES SCRIPTS CRÉÉS ET TESTÉS

