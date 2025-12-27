@echo off
chcp 65001 >nul
echo ============================================================
echo   RESTAURATION CONFIGURATION HTTPS
echo ============================================================
echo.

echo 1. Configuration du port HTTPS 8443...
powershell -Command "(Get-Content src\main\resources\application.properties) -replace '^#server.port=8443', 'server.port=8443' | Set-Content src\main\resources\application.properties"
powershell -Command "(Get-Content src\main\resources\application.properties) -replace '^server.port=8089', '#server.port=8089' | Set-Content src\main\resources\application.properties"
echo    ✓ Port 8443 activé
echo.

echo 2. Activation SSL...
powershell -Command "(Get-Content src\main\resources\application.properties) -replace '^server.ssl.enabled=false', 'server.ssl.enabled=true' | Set-Content src\main\resources\application.properties"
echo    ✓ SSL activé
echo.

echo 3. Configuration du pare-feu...
netsh advfirewall firewall delete rule name="Quiz App HTTPS" >nul 2>&1
netsh advfirewall firewall add rule name="Quiz App HTTPS" dir=in action=allow protocol=TCP localport=8443
echo    ✓ Pare-feu configuré pour le port 8443
echo.

echo 4. Récupération de l'adresse IP...
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /C:"Adresse IPv4" ^| findstr /V "192.168"') do (
    set IP=%%a
)
set IP=%IP:~1%
echo    ✓ Adresse IP: %IP%
echo.

echo ============================================================
echo   CONFIGURATION TERMINÉE
echo ============================================================
echo.
echo URL d'accès depuis le smartphone:
echo.
echo    https://%IP%:8443
echo.
echo ATTENTION: Vous devrez accepter l'avertissement de certificat
echo           sur le smartphone.
echo.
echo ============================================================
echo.
pause

