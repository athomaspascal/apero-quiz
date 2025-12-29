@echo off
REM ============================================================
REM   SETUP CLOUDFLARE TUNNEL - Solution SSL Automatique
REM ============================================================

echo.
echo ============================================================
echo   CLOUDFLARE TUNNEL SETUP
echo ============================================================
echo.
echo Cette solution vous permet d'avoir un certificat SSL valide
echo SANS ouvrir de ports sur votre routeur!
echo.
echo Avantages:
echo   - Certificat SSL automatique et GRATUIT
echo   - Fonctionne derriere n'importe quel firewall
echo   - Protection DDoS gratuite
echo   - Pas besoin d'IP publique
echo.
pause

echo.
echo [ETAPE 1/7] Verification de cloudflared...
echo.

where cloudflared >nul 2>&1
if errorlevel 1 (
    echo [INFO] cloudflared n'est pas installe
    echo.
    echo Telechargez cloudflared depuis:
    echo https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/
    echo.
    echo Ou avec chocolatey:
    echo   choco install cloudflared
    echo.
    echo Apres installation, relancez ce script.
    pause
    exit /b 1
)

echo [OK] cloudflared est installe
cloudflared --version

echo.
echo [ETAPE 2/7] Authentification Cloudflare...
echo.
echo Une page web va s'ouvrir pour vous connecter a Cloudflare.
echo Si vous n'avez pas de compte, creez-en un (gratuit).
echo.
pause

cloudflared tunnel login

if errorlevel 1 (
    echo [ERREUR] Authentification echouee
    pause
    exit /b 1
)

echo [OK] Authentification reussie

echo.
echo [ETAPE 3/7] Creation du tunnel...
echo.

set TUNNEL_NAME=quiz-app-%RANDOM%

echo Creation du tunnel: %TUNNEL_NAME%
cloudflared tunnel create %TUNNEL_NAME%

if errorlevel 1 (
    echo [ERREUR] Impossible de creer le tunnel
    pause
    exit /b 1
)

echo [OK] Tunnel cree

echo.
echo [ETAPE 4/7] Recuperation de l'ID du tunnel...
echo.

for /f "tokens=1" %%i in ('cloudflared tunnel list ^| findstr "%TUNNEL_NAME%"') do set TUNNEL_ID=%%i

if "%TUNNEL_ID%"=="" (
    echo [ERREUR] Impossible de recuperer l'ID du tunnel
    echo Executez: cloudflared tunnel list
    pause
    exit /b 1
)

echo [OK] Tunnel ID: %TUNNEL_ID%

echo.
echo [ETAPE 5/7] Configuration du tunnel...
echo.

set CONFIG_FILE=%USERPROFILE%\.cloudflared\config.yml
set CREDENTIALS_FILE=%USERPROFILE%\.cloudflared\%TUNNEL_ID%.json

echo Configuration:
echo   Fichier: %CONFIG_FILE%
echo   Credentials: %CREDENTIALS_FILE%
echo.

REM Créer le fichier de configuration
(
echo tunnel: %TUNNEL_ID%
echo credentials-file: %CREDENTIALS_FILE%
echo.
echo ingress:
echo   - hostname: apero-quiz.duckdns.org
echo     service: https://localhost:8443
echo     originRequest:
echo       noTLSVerify: true
echo   - service: http_status:404
) > "%CONFIG_FILE%"

echo [OK] Configuration creee: %CONFIG_FILE%

echo.
echo [ETAPE 6/7] Configuration DNS...
echo.
echo Ajout de l'enregistrement DNS pour apero-quiz.duckdns.org
echo.

cloudflared tunnel route dns %TUNNEL_NAME% apero-quiz.duckdns.org

if errorlevel 1 (
    echo [ATTENTION] Configuration DNS echouee
    echo Vous devrez peut-etre configurer manuellement le DNS sur Cloudflare
    pause
)

echo [OK] DNS configure

echo.
echo [ETAPE 7/7] Test du tunnel...
echo.
echo Demarrage du tunnel en arriere-plan...
echo.

start "Cloudflare Tunnel" cloudflared tunnel run %TUNNEL_NAME%

timeout /t 5 /nobreak >nul

echo [OK] Tunnel demarre

echo.
echo ============================================================
echo   CONFIGURATION TERMINEE !
echo ============================================================
echo.
echo Votre application est maintenant accessible via:
echo.
echo   https://apero-quiz.duckdns.org
echo.
echo Le certificat SSL est gere automatiquement par Cloudflare!
echo.
echo IMPORTANT:
echo   1. Assurez-vous que votre application Spring Boot tourne sur le port 8443
echo   2. Le tunnel tourne en arriere-plan
echo   3. Pour arreter le tunnel: fermez la fenetre "Cloudflare Tunnel"
echo.
echo Pour demarrer le tunnel automatiquement au demarrage du PC,
echo executez: tools\install-cloudflare-service.bat
echo.

echo Voulez-vous ouvrir l'application maintenant? (O/N)
set /p OPEN_APP="> "

if /i "%OPEN_APP%"=="O" (
    start https://apero-quiz.duckdns.org
)

echo.
echo Script termine!
pause

