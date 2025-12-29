@echo off
REM ============================================================
REM   SCRIPT DE RENOUVELLEMENT AUTOMATIQUE
REM   Certificat Let's Encrypt
REM ============================================================
REM
REM Ce script doit etre execute tous les 2 mois via
REM le Planificateur de taches Windows
REM
REM ============================================================

echo.
echo ============================================================
echo   RENOUVELLEMENT CERTIFICAT LET'S ENCRYPT
echo ============================================================
echo.
echo Date: %DATE% %TIME%
echo.

REM Dossier du projet
cd /d "C:\Users\athom\IdeaProjects\quizz1"

echo [ETAPE 1/5] Renouvellement du certificat...
echo.

REM Renouveler le certificat avec Certbot
certbot renew --quiet --no-random-sleep-on-renew

if errorlevel 1 (
    echo [ERREUR] Echec du renouvellement
    echo Consultez les logs de Certbot
    goto ERROR
)

echo [OK] Certificat renouvele
echo.

echo [ETAPE 2/5] Attente de la propagation...
timeout /t 5 /nobreak >nul
echo.

echo [ETAPE 3/5] Conversion et installation du nouveau certificat...
echo.

REM Convertir et installer le nouveau certificat
call tools\install-letsencrypt-cert-auto.bat

if errorlevel 1 (
    echo [ERREUR] Echec de l'installation du certificat
    goto ERROR
)

echo [OK] Certificat installe
echo.

echo [ETAPE 4/5] Arret de l'application...
echo.

REM Arrêter l'application Java
taskkill /IM java.exe /F >nul 2>&1
timeout /t 5 /nobreak >nul

echo [OK] Application arretee
echo.

echo [ETAPE 5/5] Redemarrage de l'application...
echo.

REM Redémarrer l'application
start "" "%~dp0run-app.bat"

timeout /t 10 /nobreak >nul

echo [OK] Application redemarree
echo.

echo ============================================================
echo   RENOUVELLEMENT TERMINE AVEC SUCCES !
echo ============================================================
echo.
echo Le nouveau certificat est actif.
echo.
echo URL: https://apero-quiz.duckdns.org:8443
echo.

REM Log du succès
echo [%DATE% %TIME%] Renouvellement reussi >> logs\cert-renewal.log

exit /b 0

:ERROR
echo.
echo ============================================================
echo   ERREUR LORS DU RENOUVELLEMENT
echo ============================================================
echo.
echo Consultez:
echo   - Logs Certbot: C:\Certbot\logs
echo   - Logs application: logs\application.log
echo.

REM Log de l'erreur
echo [%DATE% %TIME%] Renouvellement echoue >> logs\cert-renewal.log

exit /b 1

