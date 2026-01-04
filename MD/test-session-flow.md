# Test du flux de session de quiz

## Étapes de test

### 1. Démarrer l'application
```
mvn clean
mvn compile
mvn spring-boot:run
```

### 2. Ouvrir deux navigateurs
- **Navigateur 1 (Hôte)** : Firefox
- **Navigateur 2 (Participant)** : Chrome ou onglet privé

### 3. Se connecter
- **Navigateur 1** : Se connecter en tant qu'admin
- **Navigateur 2** : Se connecter en tant qu'autre utilisateur (ex: Barack Obama)

### 4. Créer une session
- **Navigateur 1** : Aller sur "Start a quiz"
- Cliquer sur un quiz (ex: "General Knowledge")
- Cliquer sur "Share this quiz"
- Noter le code de session qui s'affiche

### 5. Rejoindre la session
- **Navigateur 2** : Aller sur "Join a quiz"
- Entrer le code de session
- Cliquer sur "Join"
- **VÉRIFIER** : Le bouton "Start my quiz" devrait être visible mais DÉSACTIVÉ avec un message d'aide

### 6. Démarrer la session
- **Navigateur 1** : Cliquer sur "Start for all"
- **VÉRIFIER** : Le bouton devrait disparaître pour l'hôte

### 7. Vérifier l'auto-refresh
- **Navigateur 2** : Attendre 2 secondes maximum
- **VÉRIFIER** : Le bouton "Start my quiz" devrait devenir ACTIVÉ (bleu)
- **VÉRIFIER** : Le message d'aide devrait disparaître

### 8. Démarrer le quiz
- **Navigateur 2** : Cliquer sur "Start my quiz"
- **VÉRIFIER** : Le quiz devrait démarrer

## Vérification des logs

Pendant le test, surveiller les logs dans `logs/application.log` :

```powershell
Get-Content C:\Users\athom\IdeaProjects\quizz1\logs\application.log -Wait -Tail 50
```

Vous devriez voir :
1. `Starting auto-refresh for session: [CODE]` - Quand un participant rejoint
2. `startQuizSession() called` - Quand l'hôte clique sur "Start for all"
3. `Session status updated to: ACTIVE` - Confirmation du changement
4. `Auto-refresh: current status=WAITING, new status=ACTIVE, changed=true` - Détection par l'auto-refresh
5. `Session status changed to: ACTIVE. Rebuilding UI` - Reconstruction de l'UI
6. `Session is ACTIVE - enabling button` - Activation du bouton

## En cas de problème

Si le bouton ne s'active pas :
1. Vérifier que l'auto-refresh démarre bien dans les logs
2. Vérifier que le changement de statut est détecté
3. Vérifier que buildUI() est appelé pour le participant
4. Vérifier qu'il n'y a pas d'erreur JavaScript dans la console du navigateur (F12)

