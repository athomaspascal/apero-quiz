# 🔄 Guide de Renouvellement Automatique - Certificat Let's Encrypt

## ⏰ Rappel important

Les certificats Let's Encrypt expirent tous les **90 jours**.

- **Date d'obtention** : 28/12/2025
- **Date d'expiration** : ~28/03/2026
- **Renouvellement recommandé** : 15/03/2026 (15 jours avant)

---

## 🤖 Configuration du renouvellement automatique

### Méthode 1 : Planificateur de tâches Windows (RECOMMANDÉ)

#### Étape 1 : Ouvrir le Planificateur de tâches

1. Appuyez sur **Windows + R**
2. Tapez : `taskschd.msc`
3. Appuyez sur **Entrée**

#### Étape 2 : Créer une nouvelle tâche

1. Dans le menu de droite, cliquez sur **"Créer une tâche..."**
2. **Nom** : `Renouvellement certificat Quiz App`
3. **Description** : `Renouvelle automatiquement le certificat Let's Encrypt tous les 2 mois`

#### Étape 3 : Onglet "Général"

- ✅ Cochez : **"Exécuter même si l'utilisateur n'est pas connecté"**
- ✅ Cochez : **"Exécuter avec les autorisations maximales"**
- Configurer pour : **Windows 10**

#### Étape 4 : Onglet "Déclencheurs"

1. Cliquez sur **"Nouveau..."**
2. **Lancer la tâche** : Selon une planification
3. **Paramètres** :
   - Périodicité : **Mensuelle**
   - Mois : Cocher **tous les mois**
   - Jours : **1** (le 1er de chaque mois)
   - Heure : **03:00:00** (3h du matin)
4. ✅ Cochez : **Activé**
5. Cliquez sur **OK**

#### Étape 5 : Onglet "Actions"

1. Cliquez sur **"Nouveau..."**
2. **Action** : Démarrer un programme
3. **Programme/script** : `C:\Users\athom\IdeaProjects\quizz1\tools\renew-cert.bat`
4. **Commencer dans** : `C:\Users\athom\IdeaProjects\quizz1`
5. Cliquez sur **OK**

#### Étape 6 : Onglet "Conditions"

- ❌ Décochez : "Démarrer la tâche uniquement si l'ordinateur est relié au secteur"
- ✅ Cochez : "Réveiller l'ordinateur pour exécuter cette tâche" (si souhaité)

#### Étape 7 : Onglet "Paramètres"

- ✅ Cochez : "Autoriser l'exécution de la tâche à la demande"
- ✅ Cochez : "Exécuter la tâche dès que possible si un démarrage planifié est manqué"
- Si la tâche échoue, recommencer tous les : **1 heure**
- Nombre de tentatives : **3**

#### Étape 8 : Valider

1. Cliquez sur **OK**
2. Entrez votre mot de passe Windows si demandé

#### Étape 9 : Tester

1. Faites un clic droit sur la tâche créée
2. Cliquez sur **"Exécuter"**
3. Vérifiez les logs : `logs\cert-renewal.log`

---

### Méthode 2 : Script PowerShell (Alternative)

Créer une tâche via PowerShell (en tant qu'administrateur) :

```powershell
# Créer la tâche planifiée
$action = New-ScheduledTaskAction -Execute "C:\Users\athom\IdeaProjects\quizz1\tools\renew-cert.bat" -WorkingDirectory "C:\Users\athom\IdeaProjects\quizz1"

$trigger = New-ScheduledTaskTrigger -Daily -At 3am

$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

Register-ScheduledTask -TaskName "Renouvellement certificat Quiz App" -Action $action -Trigger $trigger -Settings $settings -RunLevel Highest -Description "Renouvelle automatiquement le certificat Let's Encrypt tous les 2 mois"

Write-Host "Tâche planifiée créée avec succès!"
```

---

## 🔍 Vérifier le renouvellement

### Vérifier la prochaine exécution

```bat
# Voir les informations de la tâche
schtasks /query /tn "Renouvellement certificat Quiz App" /v /fo LIST
```

### Consulter les logs

```bat
# Logs de renouvellement
type logs\cert-renewal.log

# Logs Certbot
dir C:\Certbot\logs
```

### Voir l'expiration du certificat actuel

```bat
certbot certificates
```

---

## 📋 Renouvellement manuel

Si vous préférez renouveler manuellement :

### Commande simple

```bat
cd C:\Users\athom\IdeaProjects\quizz1
tools\renew-cert.bat
```

### Commandes détaillées

```bat
# 1. Renouveler le certificat
certbot renew

# 2. Vérifier le renouvellement
certbot certificates

# 3. Réinstaller dans l'application
tools\install-letsencrypt-cert-auto.bat

# 4. Redémarrer l'application
run-app.bat

# 5. Tester
# https://apero-quiz.duckdns.org:8443
```

---

## 🧪 Test de renouvellement (sans vraiment renouveler)

```bat
# Test pour vérifier que tout fonctionnera
certbot renew --dry-run
```

Si cette commande réussit, le renouvellement automatique fonctionnera.

---

## ⚠️ Notifications

### Recevoir des alertes par email

Certbot peut vous envoyer un email avant expiration :

```bat
# Configurer l'email
certbot update_account --email votre@email.com
```

Let's Encrypt vous enverra un email :
- 20 jours avant expiration
- 10 jours avant expiration
- 1 jour avant expiration

---

## 📊 Calendrier de renouvellement

| Date | Action | Statut |
|------|--------|--------|
| 28/12/2025 | Obtention du certificat | ✅ Fait |
| 01/02/2026 | Vérification auto (tâche planifiée) | ⏳ Planifié |
| 01/03/2026 | Tentative de renouvellement (trop tôt) | ⏳ Planifié |
| 15/03/2026 | **Renouvellement recommandé** | ⚠️ Important |
| 28/03/2026 | **Expiration** | ❌ À éviter |

---

## 🔧 Dépannage

### Le renouvellement échoue

```bat
# Voir les logs détaillés
type C:\Certbot\logs\letsencrypt.log

# Tester manuellement
certbot renew --dry-run
```

### Erreur de connexion

- Vérifiez que le port 80 est ouvert
- Vérifiez que DuckDNS pointe vers votre IP publique
- Vérifiez votre connexion Internet

### L'application ne redémarre pas

- Vérifiez les logs : `logs\application.log`
- Vérifiez que Java est disponible
- Redémarrez manuellement : `run-app.bat`

---

## 📝 Logs disponibles

| Fichier | Description |
|---------|-------------|
| `logs/cert-renewal.log` | Historique des renouvellements |
| `C:\Certbot\logs\letsencrypt.log` | Logs Certbot détaillés |
| `logs/application.log` | Logs de l'application |

---

## ✅ Checklist de configuration

- [ ] Tâche planifiée créée
- [ ] Test de la tâche effectué (clic droit > Exécuter)
- [ ] Email de notification configuré (optionnel)
- [ ] Test de renouvellement à blanc : `certbot renew --dry-run`
- [ ] Logs vérifiés : `logs\cert-renewal.log`
- [ ] Calendrier noté (15/03/2026 = renouvellement)

---

## 🎯 Résumé

**Configuration recommandée** :
- ✅ Tâche planifiée : Tous les mois, le 1er à 3h du matin
- ✅ Alertes email : Activées
- ✅ Renouvellement automatique : `tools\renew-cert.bat`
- ✅ Logs : `logs\cert-renewal.log`

**Intervention manuelle** :
- Seulement si le renouvellement automatique échoue
- Vérifier les logs en cas de problème

---

## 📞 Support

En cas de problème :

1. Consultez les logs : `logs\cert-renewal.log`
2. Testez le renouvellement manuel : `tools\renew-cert.bat`
3. Vérifiez Certbot : `certbot renew --dry-run`
4. Vérifiez l'expiration : `certbot certificates`

---

**✅ Le renouvellement automatique est maintenant configuré !**

**Prochaine action importante** : 15/03/2026 (vérifier que le renouvellement a bien eu lieu)

