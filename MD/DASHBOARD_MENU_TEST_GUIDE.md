# Guide de Test - Menu Dashboard pour Utilisateurs Publics
Date : 2026-01-04

## 🎯 Objectif

Vérifier si le menu Dashboard apparaît incorrectement pour les utilisateurs non-admin (avatars publics).

## 📋 Procédure de test

### Étape 1 : Préparation

1. **Arrêter l'application** si elle est en cours d'exécution
2. **Nettoyer les logs** (optionnel) :
   ```cmd
   del C:\Users\athom\IdeaProjects\quizz1\logs\application.log
   ```

### Étape 2 : Démarrer l'application

1. **Lancer l'application**
2. **Attendre** que l'application soit complètement démarrée

### Étape 3 : Test avec avatar public

1. **Ouvrir** le navigateur et aller sur l'application
2. **Cliquer** sur "👤 Choisir un avatar public"
3. **Sélectionner** un avatar (ex: Barack Obama, Nelson Mandela, etc.)
4. **Observer** le menu latéral gauche

### Étape 4 : Vérification visuelle

#### ✅ Comportement CORRECT attendu

Le menu latéral doit afficher **UNIQUEMENT** :
```
┌─────────────────────────┐
│ 🎄 Quiz 🎄              │
├─────────────────────────┤
│ Démarrer un quizz       │
│ Rejoindre une Session   │
│ Mode Équipe             │
└─────────────────────────┘
```

**PAS** de menu :
- ❌ Utilisateurs
- ❌ Edition des quizz
- ❌ Question Logs
- ❌ **Dashboard** ← Le plus important !

#### ❌ Comportement INCORRECT

Si vous voyez le menu **Dashboard**, c'est le problème à corriger.

### Étape 5 : Vérification des logs

Ouvrir le fichier de log et chercher les lignes suivantes :

```log
MainLayout onAttach() called - refreshing menu
refreshMenu() called - rebuilding side navigation
=== createSideNav called ===
Current user: Barack Obama, isAdmin: false
Current user isPublic: true
```

Puis pour chaque menu :
```log
Menu: path=users, isAdminMenu=true, willBeAdded=false
Menu: path=dashboard, isAdminMenu=true, willBeAdded=false  ← Doit être FALSE
Menu: path=, isAdminMenu=false, willBeAdded=true
```

### Étape 6 : Test avec utilisateur admin

Pour comparer, se déconnecter et se connecter avec l'admin :

1. **Email** : `admin@quizz.com`
2. **Mot de passe** : `quizz2025!!`

#### ✅ Comportement attendu pour admin

Le menu doit afficher **TOUS** les menus, y compris :
```
┌─────────────────────────┐
│ 🎄 Quiz 🎄              │
├─────────────────────────┤
│ Démarrer un quizz       │
│ Utilisateurs            │ ← Admin only
│ Rejoindre une Session   │
│ Edition des quizz       │ ← Admin only
│ Question Logs           │ ← Admin only
│ Dashboard               │ ← Admin only (LE SUJET DU TEST)
│ Mode Équipe             │
└─────────────────────────┘
```

## 📊 Résultats à rapporter

### Si le Dashboard est CACHÉ pour l'avatar public ✅

**Résultat** : ✅ Le problème est RÉSOLU !

**Logs attendus** :
```
Menu: path=dashboard, isAdminMenu=true, willBeAdded=false
```

### Si le Dashboard est VISIBLE pour l'avatar public ❌

**Résultat** : ❌ Le problème persiste

**Logs à vérifier** :
1. Est-ce que `isAdmin` vaut bien `false` ?
2. Est-ce que `willBeAdded` vaut `false` pour dashboard ?
3. Si `willBeAdded=false` mais menu visible → Problème de cache

**Informations à fournir** :
- Extrait des logs (les 50 lignes autour de "createSideNav")
- Capture d'écran du menu visible
- Navigateur utilisé (Chrome, Firefox, Edge, etc.)

## 🔍 Cas spéciaux à tester

### Test 1 : Changement d'utilisateur

1. Se connecter avec un **avatar public**
2. Vérifier que Dashboard est **absent**
3. Se **déconnecter**
4. Se connecter avec l'**admin**
5. Vérifier que Dashboard est **présent**
6. Se **déconnecter**
7. Se reconnecter avec un **avatar public**
8. Vérifier que Dashboard est **absent**

→ Le menu doit s'adapter à chaque changement d'utilisateur

### Test 2 : Rafraîchissement de page

1. Se connecter avec un **avatar public**
2. **Actualiser** la page (F5)
3. Vérifier que Dashboard est toujours **absent**

### Test 3 : Navigation

1. Se connecter avec un **avatar public**
2. Cliquer sur "Démarrer un quizz"
3. Revenir en arrière
4. Vérifier que Dashboard est toujours **absent**

## 📝 Checklist de test

- [ ] Test avec avatar public → Dashboard absent ✅
- [ ] Test avec admin → Dashboard présent ✅
- [ ] Logs montrent `isAdmin=false` pour avatar public
- [ ] Logs montrent `willBeAdded=false` pour dashboard
- [ ] Test changement utilisateur OK
- [ ] Test rafraîchissement page OK
- [ ] Test navigation OK

## 🚀 Prochaines étapes

### Si tous les tests passent ✅
→ Le problème est résolu, mettre à jour la documentation

### Si le problème persiste ❌
→ Analyser les logs et appliquer les corrections supplémentaires

---

**Note** : Les logs détaillés permettront d'identifier précisément où se situe le problème.

