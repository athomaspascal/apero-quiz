# Solution : Accès au navigateur bloqué sur PC

## Problème
Vous pouvez accéder à l'application depuis votre smartphone mais pas depuis Chrome ou Edge sur votre PC.

## Cause
Le certificat SSL auto-signé est accepté par votre smartphone mais rejeté par les navigateurs de votre PC.

## Solutions (par ordre de facilité)

### Solution 1 : Contourner l'avertissement du navigateur (PLUS SIMPLE)

#### Pour Chrome :
1. Ouvrez Chrome et allez sur `https://localhost:8443`
2. Vous verrez un message "Votre connexion n'est pas privée" avec un code d'erreur
3. **TAPEZ DIRECTEMENT** sur votre clavier : `thisisunsafe`
   - Ne cliquez nulle part, tapez juste ces lettres
   - Aucune boîte de texte n'apparaîtra
   - La page se rechargera automatiquement et l'application s'affichera

#### Pour Edge :
1. Ouvrez Edge et allez sur `https://localhost:8443`
2. Vous verrez "Votre connexion n'est pas privée"
3. Cliquez sur **"Avancé"**
4. Cliquez sur **"Continuer vers localhost (non sécurisé)"**

---

### Solution 2 : Importer le certificat dans Windows (PERMANENT)

Si vous voulez une solution permanente sans avertissement :

1. **Exporter le certificat du keystore :**
   ```cmd
   cd C:\Users\athom\IdeaProjects\quizz1\src\main\resources
   keytool -exportcert -alias quiz-app -keystore keystore.p12 -storetype PKCS12 -storepass quiz-app-2025 -file quiz-app-cert.cer
   ```

2. **Importer dans Windows :**
   - Double-cliquez sur le fichier `quiz-app-cert.cer` créé
   - Cliquez sur "Installer le certificat..."
   - Choisissez "Ordinateur local"
   - Sélectionnez "Placer tous les certificats dans le magasin suivant"
   - Cliquez "Parcourir" et choisissez "Autorités de certification racines de confiance"
   - Cliquez "Suivant" puis "Terminer"
   - Acceptez l'avertissement de sécurité

3. **Redémarrez vos navigateurs**

---

### Solution 3 : Utiliser le domaine DuckDNS (si configuré)

Si vous avez configuré DuckDNS et les certificats Let's Encrypt :
- Utilisez `https://apero-quiz.duckdns.org:8443`

---

## Vérification rapide

Avant tout, assurez-vous que l'application est bien en cours d'exécution :

```cmd
netstat -ano | findstr ":8443"
```

Si rien ne s'affiche, démarrez l'application d'abord !

---

## URLs à tester

1. **https://localhost:8443** (recommandé pour PC)
2. **https://127.0.0.1:8443** (alternative)
3. **https://192.168.x.x:8443** (votre IP locale)
4. **https://apero-quiz.duckdns.org:8443** (si DuckDNS configuré)

---

## Pourquoi ça marche sur smartphone mais pas sur PC ?

- Votre smartphone a probablement accepté l'exception de certificat la première fois
- Ou il utilise un navigateur moins strict sur les certificats
- Les navigateurs de bureau (Chrome/Edge) sont plus stricts par défaut

