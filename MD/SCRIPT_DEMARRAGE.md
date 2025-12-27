# Scripts de Démarrage de l'Application

## Vue d'ensemble

Trois scripts batch ont été créés pour faciliter le démarrage de l'application :

## 📜 Scripts disponibles

### 1. `run-app.bat` - Démarrage complet
**Utilisation :** Double-cliquez sur `run-app.bat` ou exécutez dans le terminal
```batch
run-app.bat
```

**Ce script exécute :**
1. `mvn clean` - Nettoie le projet
2. `mvn vaadin:build-frontend` - **Construit le frontend Vaadin** (étape cruciale après un clean)
3. `mvn spring-boot:run` - Démarre l'application

**Quand l'utiliser :**
- ✅ Après avoir modifié des fichiers JSON de configuration
- ✅ Après avoir mis à jour des dépendances
- ✅ Quand vous voulez un démarrage "propre"
- ✅ En cas de problèmes avec le frontend

---

### 2. `build-app.bat` - Compilation seulement
**Utilisation :** Double-cliquez sur `build-app.bat` ou exécutez dans le terminal
```batch
build-app.bat
```

**Ce script exécute :**
1. `mvn clean` - Nettoie le projet
2. `mvn vaadin:build-frontend` - Construit le frontend Vaadin
3. `mvn compile` - Compile les sources

**Quand l'utiliser :**
- ✅ Pour vérifier que tout compile sans erreur
- ✅ Avant de commiter du code
- ✅ Pour préparer l'application sans la démarrer

---

### 3. `quick-start.bat` - Démarrage rapide
**Utilisation :** Double-cliquez sur `quick-start.bat` ou exécutez dans le terminal
```batch
quick-start.bat
```

**Ce script exécute :**
1. `mvn spring-boot:run` - Démarre directement l'application

**Quand l'utiliser :**
- ✅ Quand le projet est déjà compilé
- ✅ Pour un redémarrage rapide
- ⚠️ **NE PAS utiliser après un `mvn clean`**

---

## ⚠️ RÈGLE IMPORTANTE

### Après `mvn clean`, TOUJOURS exécuter `mvn vaadin:build-frontend`

**Pourquoi ?**
- Le `mvn clean` supprime tous les fichiers compilés, y compris le frontend Vaadin
- Sans `vaadin:build-frontend`, l'application ne trouvera pas `index.html` et échouera au démarrage
- Vous verrez l'erreur : `Unable to find index.html`

**Solution :**
- Utilisez toujours `run-app.bat` qui inclut automatiquement cette étape
- Ou exécutez manuellement les commandes dans l'ordre :
  ```batch
  mvn clean
  mvn vaadin:build-frontend
  mvn spring-boot:run
  ```

---

## 🌐 Accès à l'application

Une fois démarrée, l'application est accessible sur :
- **URL HTTPS :** https://localhost:8443
- **URL HTTP :** Redirige automatiquement vers HTTPS

---

## 🔧 Commandes Maven utiles

### Démarrage complet (recommandé après modifications)
```batch
mvn clean vaadin:build-frontend spring-boot:run
```

### Build de production
```batch
mvn clean package -Pproduction
```

### Tests
```batch
mvn test
```

---

## 📝 Notes

- Les scripts affichent des messages d'état pour chaque étape
- En cas d'erreur, le script s'arrête et affiche un message
- Utilisez `Ctrl+C` pour arrêter l'application en cours d'exécution

---

## 🆘 Dépannage

### Problème : "Unable to find index.html"
**Cause :** Frontend Vaadin non construit après un clean
**Solution :** Utilisez `run-app.bat` ou exécutez `mvn vaadin:build-frontend`

### Problème : Port 8443 déjà utilisé
**Cause :** Une instance de l'application est déjà en cours d'exécution
**Solution :** 
1. Fermez l'instance existante (Ctrl+C dans le terminal)
2. Ou tuez le processus : `netstat -ano | findstr 8443` puis `taskkill /PID <pid> /F`

### Problème : Erreurs de compilation
**Cause :** Code Java avec des erreurs
**Solution :** Utilisez `build-app.bat` pour voir les erreurs de compilation détaillées

---

Date de création : 2025-12-27

