# Configuration Rapide du Pare-feu

## 🚀 Méthode Rapide (3 étapes)

### 1️⃣ Exécuter le script de configuration
- **Clic droit** sur `configure-firewall.bat`
- Sélectionner **"Exécuter en tant qu'administrateur"**
- Attendre la fin de l'exécution

### 2️⃣ Vérifier que ça fonctionne
- Exécuter `check-firewall.bat` (pas besoin d'admin)
- Ou ouvrir un navigateur : http://192.168.38.1:8089

### 3️⃣ Terminé ! 🎉

---

## ⚡ Commande Manuelle (PowerShell Admin)

Si vous préférez la ligne de commande :

```powershell
netsh advfirewall firewall add rule name="Quiz Application - Port 8089" dir=in action=allow protocol=TCP localport=8089
```

---

## 📱 Accès depuis d'autres appareils

Une fois le pare-feu configuré :
1. Les autres appareils peuvent accéder via : `http://192.168.38.1:8089`
2. Ils doivent être sur le même réseau WiFi/LAN
3. Utilisez le QR code de partage dans l'application

---

## ❌ Pour supprimer les règles

Exécuter `remove-firewall-rules.bat` en tant qu'administrateur

---

## 📖 Guide Complet

Pour plus de détails, consultez : `FIREWALL_CONFIGURATION_GUIDE.md`

