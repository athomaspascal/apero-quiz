@echo off
REM ========================================================
REM Script de Rebuild Complet - Fix Écran Blanc Duel Quiz
REM Date: 2026-01-06
REM ========================================================

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║  FIX ÉCRAN BLANC DUEL QUIZ - Rebuild Complet             ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

REM === ÉTAPE 1 : Arrêter l'application ===
echo [1/6] Arrêt de l'application en cours...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8443 ^| findstr LISTENING') do (
    echo      - Arrêt du processus PID %%a
    taskkill /F /PID %%a >nul 2>&1
)
timeout /t 2 >nul
echo      ✓ Application arrêtée
echo.

REM === ÉTAPE 2 : Clean complet ===
echo [2/6] Nettoyage complet du projet...
call mvn clean
if %ERRORLEVEL% NEQ 0 (
    echo      ✗ Erreur lors du clean !
    pause
    exit /b 1
)
echo      ✓ Projet nettoyé
echo.

REM === ÉTAPE 3 : Build front-end (CRUCIAL) ===
echo [3/6] Build du front-end Vaadin (index.html, routes, etc.)...
echo      Cette étape peut prendre quelques minutes...
call mvn vaadin:build-frontend
if %ERRORLEVEL% NEQ 0 (
    echo      ✗ Erreur lors du build front-end !
    pause
    exit /b 1
)
echo      ✓ Front-end construit (index.html généré)
echo.

REM === ÉTAPE 4 : Compilation back-end ===
echo [4/6] Compilation du back-end...
call mvn compile -DskipTests
if %ERRORLEVEL% NEQ 0 (
    echo      ✗ Erreur lors de la compilation !
    pause
    exit /b 1
)
echo      ✓ Back-end compilé
echo.

REM === ÉTAPE 5 : Vérifier que le front-end a été généré ===
echo [5/6] Vérification des fichiers générés...
if exist "target\classes\META-INF\VAADIN\webapp\index.html" (
    echo      ✓ index.html trouvé !
) else (
    echo      ✗ index.html MANQUANT ! Le build front-end a échoué.
    pause
    exit /b 1
)
echo.

REM === ÉTAPE 6 : Démarrer l'application ===
echo [6/6] Démarrage de l'application...
echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║  L'application va démarrer...                             ║
echo ║                                                           ║
echo ║  ATTENDEZ le message "Started Application"                ║
echo ║  puis testez le Duel Quiz avec 2 utilisateurs            ║
echo ║                                                           ║
echo ║  Vérifiez qu'il n'y a PLUS d'erreur "index.html"         ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.
pause

call mvn spring-boot:run

