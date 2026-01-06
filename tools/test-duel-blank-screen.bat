@echo off
echo ========================================
echo DUEL QUIZ - Test de Page Blanche
echo ========================================
echo.

REM Arreter l'application si elle tourne
echo [1/5] Arret de l'application en cours...
taskkill /F /IM java.exe 2>nul
if %errorlevel% equ 0 (
    echo Application arretee
    timeout /t 2 /nobreak >nul
) else (
    echo Aucune application en cours
)

REM Compiler l'application
echo.
echo [2/5] Compilation de l'application...
cd /d C:\Users\athom\IdeaProjects\quizz1
call mvn clean package -DskipTests
if %errorlevel% neq 0 (
    echo ERREUR: Echec de la compilation
    pause
    exit /b 1
)

REM Build frontend
echo.
echo [3/5] Build du frontend Vaadin...
call mvn vaadin:build-frontend
if %errorlevel% neq 0 (
    echo ERREUR: Echec du build frontend
    pause
    exit /b 1
)

REM Nettoyer les anciens logs
echo.
echo [4/5] Nettoyage des logs...
del logs\application.log 2>nul
echo Logs nettoyes

REM Demarrer l'application
echo.
echo [5/5] Demarrage de l'application...
echo Attendre environ 15 secondes pour le demarrage complet
start "Quizz Application" java -jar target\quizz1-2.12.jar

echo.
echo ========================================
echo Application en cours de demarrage...
echo URL: https://192.168.1.138:8443
echo ========================================
echo.
echo Instructions de test:
echo 1. Ouvrir 2 navigateurs (ou 1 normal + 1 incognito)
echo 2. Navigateur 1: Connecter Charles Darwin
echo 3. Navigateur 2: Connecter Nelson Mandela
echo 4. Les deux: Cliquer sur "Duel Quiz"
echo 5. Accepter le match
echo 6. Observer apres le countdown
echo.
echo Pour voir les logs en temps reel:
echo   powershell Get-Content logs\application.log -Wait -Tail 50
echo.
pause

