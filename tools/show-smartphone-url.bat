@echo off
chcp 65001 >nul
cls
echo ============================================================
echo   INFORMATIONS D'ACCES SMARTPHONE
echo ============================================================
echo.

echo Récupération de la configuration...
echo.

REM Trouver l'adresse IP WiFi
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /C:"Adresse IPv4" ^| findstr /V "192.168"') do (
    set IP=%%a
)
set IP=%IP:~1%

REM Vérifier si SSL est activé
findstr /C:"server.ssl.enabled=true" src\main\resources\application.properties >nul 2>&1
if %errorlevel% equ 0 (
    set PROTOCOL=https
    set PORT=8443
    set SSL_STATUS=ACTIVÉ
) else (
    set PROTOCOL=http
    findstr /C:"server.port=8089" src\main\resources\application.properties >nul 2>&1
    if %errorlevel% equ 0 (
        set PORT=8089
    ) else (
        set PORT=8080
    )
    set SSL_STATUS=DÉSACTIVÉ
)

echo ┌──────────────────────────────────────────────────────────┐
echo │  CONFIGURATION ACTUELLE                                  │
echo └──────────────────────────────────────────────────────────┘
echo.
echo   Adresse IP du PC : %IP%
echo   Protocole        : %PROTOCOL%
echo   Port             : %PORT%
echo   SSL/HTTPS        : %SSL_STATUS%
echo.
echo ┌──────────────────────────────────────────────────────────┐
echo │  URL D'ACCES DEPUIS LE SMARTPHONE                        │
echo └──────────────────────────────────────────────────────────┘
echo.
echo.
echo              %PROTOCOL%://%IP%:%PORT%
echo.
echo.
echo ┌──────────────────────────────────────────────────────────┐
echo │  INSTRUCTIONS                                            │
echo └──────────────────────────────────────────────────────────┘
echo.
echo 1. Assurez-vous que le PC est connecté au hotspot du smartphone
echo 2. Vérifiez que l'application est lancée (run-app.bat)
echo 3. Ouvrez le navigateur sur le smartphone
echo 4. Tapez l'URL ci-dessus
echo.

if "%PROTOCOL%"=="https" (
    echo ⚠️  ATTENTION: Avec HTTPS, vous devrez accepter
    echo    l'avertissement de certificat sur le smartphone
    echo.
)

echo ┌──────────────────────────────────────────────────────────┐
echo │  SCRIPTS UTILES                                          │
echo └──────────────────────────────────────────────────────────┘
echo.
echo   configure-http-smartphone.bat  → Passer en HTTP (sans SSL)
echo   restore-https.bat              → Restaurer HTTPS
echo   check-firewall-8089.bat        → Vérifier pare-feu HTTP
echo   check-firewall-8443.bat        → Vérifier pare-feu HTTPS
echo.
echo ============================================================
echo.
pause

