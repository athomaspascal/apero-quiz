@echo off
chcp 65001 >nul
echo ============================================================
echo   CONFIGURATION HTTP POUR ACCES SMARTPHONE
echo ============================================================
echo.

echo 1. Sauvegarde de la configuration actuelle...
copy /Y src\main\resources\application.properties src\main\resources\application.properties.backup.%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
echo    ✓ Backup créé
echo.

echo 2. Configuration du port HTTP 8089...
powershell -Command "(Get-Content src\main\resources\application.properties) -replace '^server.port=8443', '#server.port=8443' | Set-Content src\main\resources\application.properties"
powershell -Command "(Get-Content src\main\resources\application.properties) -replace '^#server.port=8089', 'server.port=8089' | Set-Content src\main\resources\application.properties"
echo    ✓ Port 8089 activé
echo.

echo 3. Désactivation SSL...
powershell -Command "(Get-Content src\main\resources\application.properties) -replace '^server.ssl.enabled=true', 'server.ssl.enabled=false' | Set-Content src\main\resources\application.properties"
echo    ✓ SSL désactivé
echo.

echo 4. Configuration du pare-feu...
netsh advfirewall firewall delete rule name="Quiz App HTTP" >nul 2>&1
netsh advfirewall firewall add rule name="Quiz App HTTP" dir=in action=allow protocol=TCP localport=8089
echo    ✓ Pare-feu configuré pour le port 8089
echo.

echo 5. Récupération de l'adresse IP...
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
echo    http://%IP%:8089
echo.
echo ============================================================
echo.
echo Appuyez sur une touche pour lancer l'application...
pause >nul

echo.
echo Lancement de l'application...
call mvnw spring-boot:run

