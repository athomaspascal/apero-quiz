@echo off
REM ============================================================
REM   RESUME - Installation certificat Let's Encrypt
REM ============================================================

echo.
echo ============================================================
echo   INSTALLATION CERTIFICAT LET'S ENCRYPT
echo   Etat actuel et prochaines etapes
echo ============================================================
echo.

echo [ETAT] Certificats Let's Encrypt telecharges
echo   Emplacement: C:\Certbot\live\apero-quiz.duckdns.org
echo   - fullchain.pem [OK]
echo   - privkey.pem [OK]
echo.

echo [ATTENTE] Installation OpenSSL
echo.

where openssl >nul 2>&1
if errorlevel 1 (
    echo   [X] OpenSSL n'est pas encore installe
    echo.
    echo   PROCHAINES ETAPES:
    echo   1. Le telechargement d'OpenSSL est en cours dans votre navigateur
    echo   2. Executez Win64OpenSSL-3_0_13.exe une fois telecharge
    echo   3. Installez dans: C:\Program Files\OpenSSL-Win64
    echo   4. Fermez et rouvrez le terminal
    echo   5. Relancez ce script pour continuer
    echo.
    echo   OU executez: tools\install-openssl.bat
    echo.
    pause
    exit /b 0
) else (
    echo   [OK] OpenSSL est installe!
    openssl version
    echo.
)

echo [ETAPE SUIVANTE] Installation du certificat dans l'application
echo.
echo   Script: tools\install-letsencrypt-cert-auto.bat
echo.

set /p CONTINUE="Voulez-vous installer le certificat maintenant? (O/N): "

if /i not "%CONTINUE%"=="O" (
    echo.
    echo Installation annulee.
    echo Executez: tools\install-letsencrypt-cert-auto.bat quand vous serez pret
    pause
    exit /b 0
)

echo.
echo Lancement de l'installation...
echo.

call "%~dp0install-letsencrypt-cert-auto.bat"

if errorlevel 1 (
    echo.
    echo [ERREUR] Installation echouee
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   INSTALLATION COMPLETE !
echo ============================================================
echo.
echo Prochaines etapes:
echo   1. Redemarrez l'application: run-app.bat
echo   2. Testez: https://apero-quiz.duckdns.org:8443
echo   3. Le certificat devrait etre accepte sans avertissement!
echo.

set /p START_APP="Voulez-vous demarrer l'application maintenant? (O/N): "

if /i "%START_APP%"=="O" (
    echo.
    echo Demarrage de l'application...
    cd /d "%~dp0.."
    start run-app.bat
    timeout /t 3 /nobreak >nul
    start https://apero-quiz.duckdns.org:8443
)

echo.
pause

