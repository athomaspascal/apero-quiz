# 🚀 PLAN DE TEST - Écran Blanc Duel Quiz - 2026-01-06 02:29

## ✅ ÉTAT ACTUEL

### Ce qui a été fait :
1. ✅ Frontend rebuild (pas d'erreur index.html)
2. ✅ Application démarrée à 02:25:28
3. ✅ Utilisateur "Steve Jobs" connecté à 02:25:50
4. ✅ **Nouveau** : Logs de débogage ajoutés à DuelQuizView
5. ✅ **Nouveau** : Compilation réussie à 02:29:18

### Logs de débogage ajoutés :
```java
=== DuelQuizView Constructor CALLED ===
DuelQuizView services injected successfully
Current user: [nom]
Active duel found / No active duel
=== DuelQuizView Constructor COMPLETED ===
```

## 🔍 DIAGNOSTIC

**AUCUN log de DuelQuizView n'apparaît dans les logs actuels.**

Cela signifie que **PERSONNE n'a cliqué sur le menu "Duel Quiz"** encore, OU le menu n'est pas accessible.

## 📋 PROCÉDURE DE TEST IMMÉDIATE

### Option 1 : Test avec Logs en Temps Réel (RECOMMANDÉ)

1. **Dans un terminal**, exécutez :
   ```batch
   test-duel-realtime.bat
   ```
   Ce script affichera les logs en temps réel pendant votre test.

2. **Ouvrir 2 navigateurs** (ou 2 appareils)

3. **Connecter 2 utilisateurs** différents :
   - Ex: Charles Darwin
   - Ex: Nelson Mandela

4. **Les deux cliquent sur "Duel Quiz"** dans le menu

5. **Observer la console** du script `test-duel-realtime.bat`

### Option 2 : Test Manuel

1. Ouvrir 2 navigateurs
2. Connecter 2 utilisateurs
3. Les deux cliquent sur "Duel Quiz"
4. Après le test, exécuter :
   ```batch
   check-duel-logs.bat
   ```

## 🎯 LOGS ATTENDUS

### Si le clic sur "Duel Quiz" fonctionne :
```
02:XX:XX INFO - === DuelQuizView Constructor CALLED ===
02:XX:XX INFO - DuelQuizView services injected successfully
02:XX:XX INFO - Current user: Charles Darwin
02:XX:XX INFO - No active duel, showing initial view
02:XX:XX INFO - === DuelQuizView Constructor COMPLETED ===
```

### Si les deux joueurs trouvent un match :
```
02:XX:XX INFO - DuelService.createMatch - Creating duel between User1 and User2
02:XX:XX INFO - Opponent found: [nom]
```

### Si le countdown démarre :
```
02:XX:XX INFO - Starting countdown for duel [ID]
```

### Si la navigation vers le quiz fonctionne :
```
02:XX:XX INFO - Navigating to quiz: [ID], duelId: [ID]
02:XX:XX INFO - *** DUEL MODE DETECTED ***
02:XX:XX INFO - displayQuestion() called - currentQuestionIndex: 0
```

## ⚠️ SCÉNARIOS POSSIBLES

### Scénario A : AUCUN log DuelQuizView
**Signification** : Le menu n'est pas cliqué OU pas accessible  
**Action** : 
1. Vérifier visuellement si le menu "Duel Quiz" apparaît
2. Vérifier la console navigateur (F12) pour des erreurs JavaScript
3. Tester avec un autre utilisateur

### Scénario B : Logs DuelQuizView MAIS pas de match
**Signification** : La recherche d'adversaire ne fonctionne pas  
**Action** : Vérifier les logs du DuelService

### Scénario C : Match trouvé MAIS pas de navigation
**Signification** : Problème de navigation vers QuizQuestionView  
**Action** : Vérifier les logs "Navigating to quiz"

### Scénario D : Navigation OK MAIS écran blanc
**Signification** : QuizQuestionView n'affiche pas les questions  
**Action** : Vérifier les logs "displayQuestion()"

## 🚨 SI ÉCRAN BLANC PERSISTE

### Vérifier la visibilité des éléments UI dans QuizQuestionView

1. Vérifier que `questionText.setVisible(true)` est bien appelé
2. Vérifier que `optionsContainer.setVisible(true)` est bien appelé
3. Vérifier que `content.setVisible(true)` est bien appelé

### Vérifier dans le scoreboard

Dans `showDuelScoreboard()`, s'assurer que :
```java
// ❌ MAUVAIS
questionText.setVisible(false);

// ✅ BON
questionText.setText("");
questionText.setVisible(true);
```

## 📊 CHECKLIST DE VÉRIFICATION

Avant de tester, vérifier que :
- [ ] L'application est démarrée (port 8443)
- [ ] Pas d'erreur au démarrage dans les logs
- [ ] Le frontend a été rebuild
- [ ] La compilation des nouveaux logs est réussie
- [ ] 2 navigateurs/appareils sont prêts
- [ ] Le script `test-duel-realtime.bat` est prêt (optionnel)

## 🔄 APRÈS LE TEST

1. **Arrêter le script de logs** (Ctrl+C si utilisé)

2. **Analyser les logs** :
   ```batch
   check-duel-logs.bat
   ```

3. **Chercher les patterns clés** :
   ```batch
   findstr /C:"=== DuelQuizView" logs\application.log
   findstr /C:"DUEL MODE DETECTED" logs\application.log
   findstr /C:"displayQuestion" logs\application.log
   ```

4. **Rapporter les résultats** :
   - ✅ Les deux joueurs voient les questions → Problème résolu !
   - ⚠️ Un joueur voit, l'autre non → Problème asymétrique
   - ❌ Les deux ont écran blanc → Problème de navigation ou d'affichage

## 💡 INFORMATIONS SUPPLÉMENTAIRES

### Structure des logs ajoutés

| Classe | Méthode | Log | Objectif |
|--------|---------|-----|----------|
| DuelQuizView | Constructor | `=== DuelQuizView Constructor CALLED ===` | Confirmer l'instanciation |
| DuelQuizView | Constructor | `Current user: [nom]` | Identifier l'utilisateur |
| DuelQuizView | Constructor | `=== DuelQuizView Constructor COMPLETED ===` | Confirmer l'initialisation |

### Logs existants à surveiller

| Service | Pattern | Signification |
|---------|---------|---------------|
| DuelService | `createMatch` | Un match a été créé |
| DuelService | `acceptMatch` | Un joueur a accepté |
| DuelQuizView | `Starting countdown` | Le countdown a démarré |
| DuelQuizView | `Navigating to quiz` | Navigation lancée |
| QuizQuestionView | `DUEL MODE DETECTED` | QuizQuestionView instancié en mode duel |
| QuizQuestionView | `displayQuestion()` | Question affichée |

## 📅 HISTORIQUE

| Date | Heure | Action | Résultat |
|------|-------|--------|----------|
| 06/01 | 02:25 | Frontend rebuild + redémarrage | ✅ OK |
| 06/01 | 02:25 | Connexion Steve Jobs | ✅ OK |
| 06/01 | 02:29 | Ajout logs debug DuelQuizView | ✅ Compilé |
| 06/01 | 02:29 | **EN ATTENTE** : Test du Duel Quiz | ⏳ À faire |

## ✅ CRITÈRES DE SUCCÈS FINAL

Le problème sera résolu quand :
1. ✅ Les logs DuelQuizView apparaissent au clic sur le menu
2. ✅ Les deux joueurs trouvent un match
3. ✅ Le countdown démarre
4. ✅ La navigation vers le quiz fonctionne
5. ✅ Les logs "DUEL MODE DETECTED" apparaissent
6. ✅ Les logs "displayQuestion()" apparaissent
7. ✅ **LES DEUX JOUEURS VOIENT LES QUESTIONS (PAS D'ÉCRAN BLANC)**

---

**PROCHAINE ÉTAPE** : Tester le Duel Quiz avec 2 utilisateurs et observer les logs !

**Date de création** : 2026-01-06 02:29  
**Auteur** : GitHub Copilot

