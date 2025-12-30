# 🚀 ACCES A L'APPLICATION - GUIDE RAPIDE

## 🎯 Vous ne pouvez pas accéder à apero-quiz.duckdns.org sur votre PC ?

---

## ⚠️ MESSAGE D'ERREUR : "n'autorise pas la connexion"

### Ce message signifie que **L'APPLICATION N'EST PAS LANCÉE** !

**SOLUTION :**

1. **Démarrez l'application d'abord !**
   - Via IntelliJ IDEA : Exécutez `Application.java`
   - Via Maven : `mvn spring-boot:run`

2. **Attendez de voir dans la console :**
   ```
   Tomcat started on port(s): 8443 (https)
   ```

3. **Ensuite testez dans Chrome :**
   - `https://localhost:8443` (recommandé)
   - OU `https://apero-quiz.duckdns.org:8443`

**Pour vérifier si l'application est lancée :**
```cmd
netstat -ano | findstr ":8443"
```
Si rien ne s'affiche → L'application n'est pas lancée !

---

## ⚡ SOLUTION EN 1 SECONDE (si l'application est déjà lancée)

### Utilisez cette URL à la place :
```
https://localhost:8443
```

**C'est tout ! Ça fait exactement la même chose.**

---

## 💡 Si vous voulez absolument utiliser apero-quiz.duckdns.org

### Étape 1 : Exécutez ce script (1 minute)

1. Allez dans : `C:\Users\athom\IdeaProjects\quizz1\scripts`

2. **Clic droit** sur `add-duckdns-to-hosts.bat`

3. Choisissez **"Exécuter en tant qu'administrateur"**

4. Suivez les instructions

### Étape 2 : Testez

Ouvrez votre navigateur et allez sur :
```
https://apero-quiz.duckdns.org:8443
```

Si vous voyez une erreur de certificat :
- **Chrome** : Tapez `thisisunsafe` sur la page d'erreur
- **Edge** : Cliquez "Avancé" → "Continuer"

---

## 📱 URLs disponibles

Toutes ces URLs accèdent à la même application sur votre PC :

| URL | Fonctionne ? | Recommandé |
|-----|--------------|------------|
| `https://localhost:8443` | ✅ Toujours | ⭐⭐⭐ |
| `https://127.0.0.1:8443` | ✅ Toujours | ⭐⭐ |
| `https://apero-quiz.duckdns.org:8443` | ⚠️ Après configuration | ⭐ |

---

## 🆘 En cas de problème

### Message "n'autorise pas la connexion" dans Chrome ?

**CAUSE : L'application n'est pas lancée !**

**SOLUTION :**
1. Démarrez l'application (voir section ci-dessus)
2. Attendez que Tomcat démarre sur le port 8443
3. Retestez dans le navigateur

**Vérification rapide :**
```cmd
netstat -ano | findstr ":8443"
```
Si vide → Lancez l'application !

### L'application ne répond pas ?

Vérifiez qu'elle est lancée :
```cmd
netstat -ano | findstr ":8443"
```

Si rien ne s'affiche, démarrez l'application d'abord !

### Erreur de certificat dans le navigateur ?

**Chrome** : Tapez directement `thisisunsafe` (sans boîte de texte)
**Edge** : Cliquez "Avancé" → "Continuer vers le site"

### Le domaine DuckDNS ne fonctionne toujours pas ?

Consultez le guide complet : `MD/DUCKDNS_ACCESS_FIX.md`

---

## 📚 Documentation complète

- **`MD/DUCKDNS_ACCESS_FIX.md`** - Guide détaillé pour débloquer DuckDNS
- **`MD/BROWSER_ACCESS_SOLUTION.md`** - Solution pour les erreurs de certificat
- **`scripts/fix-duckdns-access.ps1`** - Script PowerShell automatique
- **`scripts/add-duckdns-to-hosts.bat`** - Script batch automatique

---

**✨ Conseil : Utilisez simplement `https://localhost:8443` et tout fonctionnera parfaitement !**

