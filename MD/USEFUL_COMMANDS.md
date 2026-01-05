# Commandes utiles pour la gestion de l'application Quiz

## Gestion du port 8443

### Vérifier les processus écoutant sur le port 8443
```batch
netstat -ano | findstr :8443
```

### Arrêter tous les processus utilisant le port 8443
```powershell
powershell -Command "$connections = Get-NetTCPConnection -LocalPort 8443 -ErrorAction SilentlyContinue; if ($connections) { foreach ($conn in $connections) { Write-Host 'Stopping process PID:' $conn.OwningProcess; Stop-Process -Id $conn.OwningProcess -Force -ErrorAction SilentlyContinue } }"
```

### Utiliser le script batch (recommandé)
```batch
# Arrêter uniquement
cd C:\Users\athom\IdeaProjects\quizz1\scripts
stop-app-8443.bat

# Arrêter et redémarrer
cd C:\Users\athom\IdeaProjects\quizz1\scripts
stop-app-8443.bat restart
```

## Compilation et démarrage

### Compilation complète (avec nettoyage)
```batch
cd C:\Users\athom\IdeaProjects\quizz1
mvn clean compile -DskipTests
```

### Compilation incrémentale
```batch
cd C:\Users\athom\IdeaProjects\quizz1
mvn compile -DskipTests
```

### Build frontend (après mvn clean)
```batch
cd C:\Users\athom\IdeaProjects\quizz1
mvn vaadin:prepare-frontend vaadin:build-frontend
```

### Démarrer l'application
```batch
cd C:\Users\athom\IdeaProjects\quizz1
mvn spring-boot:run
```

### Démarrer dans une nouvelle fenêtre
```batch
cd C:\Users\athom\IdeaProjects\quizz1
start "Quiz Application" cmd /k "mvn spring-boot:run"
```

## Consultation des logs

### Afficher les dernières lignes du log
```powershell
powershell -Command "Get-Content C:\Users\athom\IdeaProjects\quizz1\logs\application.log -Tail 50"
```

### Rechercher dans les logs
```powershell
# Rechercher "duel"
powershell -Command "Get-Content C:\Users\athom\IdeaProjects\quizz1\logs\application.log | Select-String -Pattern 'duel'"

# Rechercher "DUEL MODE DETECTED"
powershell -Command "Get-Content C:\Users\athom\IdeaProjects\quizz1\logs\application.log | Select-String -Pattern 'DUEL MODE DETECTED'"

# Vérifier le démarrage
powershell -Command "Get-Content C:\Users\athom\IdeaProjects\quizz1\logs\application.log | Select-String -Pattern 'Started Application'"
```

### Suivre les logs en temps réel
```powershell
powershell -Command "Get-Content C:\Users\athom\IdeaProjects\quizz1\logs\application.log -Wait -Tail 20"
```

## Test de connexion

### Tester la connexion HTTPS
```powershell
powershell -Command "Test-NetConnection -ComputerName 192.168.1.138 -Port 8443"
```

### Tester avec curl
```batch
curl -k https://192.168.1.138:8443
```

## Gestion des processus Java

### Lister tous les processus Java
```powershell
powershell -Command "Get-Process java | Format-Table Id, ProcessName, StartTime"
```

### Arrêter un processus Java spécifique par PID
```batch
taskkill /F /PID [PID]
```

## Vérification des erreurs

### Vérifier les erreurs de compilation
- Ouvrir le projet dans IntelliJ IDEA
- Menu : Build → Build Project
- Vérifier la fenêtre "Problems" ou "Messages"

### Rechercher les erreurs dans les logs
```powershell
powershell -Command "Get-Content C:\Users\athom\IdeaProjects\quizz1\logs\application.log | Select-String -Pattern 'ERROR|Exception'"
```

## Base de données H2

### Accéder à la console H2
URL : https://192.168.1.138:8443/h2-console
- JDBC URL : jdbc:h2:file:./data/quizdb
- User : sa
- Password : (laisser vide)

### Localisation de la base de données
```
C:\Users\athom\IdeaProjects\quizz1\data\quizdb.mv.db
```

## URLs d'accès

### URL locale
```
https://192.168.1.138:8443
```

### URL publique
```
https://apero-quiz.duckdns.org:8443
```

## Débogage du quiz duel

### Logs à surveiller lors d'un test de duel
```
"*** DUEL MODE DETECTED ***"    → Le mode duel est bien détecté
"Starting countdown"             → Le compte à rebours démarre
"Countdown finished"             → Le compte à rebours est terminé
"Navigating to quiz"             → Navigation vers le quiz
"displayQuestion() called"       → Les questions commencent à s'afficher
```

### Commande pour surveiller en temps réel
```powershell
powershell -Command "Get-Content C:\Users\athom\IdeaProjects\quizz1\logs\application.log -Wait -Tail 20 | Select-String -Pattern 'duel|DUEL|countdown|displayQuestion'"
```

## Nettoyage

### Supprimer les fichiers compilés
```batch
cd C:\Users\athom\IdeaProjects\quizz1
mvn clean
```

### Supprimer le cache Vaadin
```batch
cd C:\Users\athom\IdeaProjects\quizz1
rmdir /s /q node_modules
rmdir /s /q target
```

## Backup rapide

### Créer une copie de la base de données
```batch
copy C:\Users\athom\IdeaProjects\quizz1\data\quizdb.mv.db C:\Users\athom\IdeaProjects\quizz1\data\quizdb_backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%.mv.db
```

### Créer un backup des logs
```batch
copy C:\Users\athom\IdeaProjects\quizz1\logs\application.log C:\Users\athom\IdeaProjects\quizz1\logs\application_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%.log
```

