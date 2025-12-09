@echo off
echo ========================================
echo Verification du Pare-feu Windows
echo Pour l'application Quiz
echo ========================================
echo.

echo 1. Etat du pare-feu:
echo --------------------
netsh advfirewall show currentprofile state
echo.

echo 2. Regles pour le port 8089:
echo -----------------------------
netsh advfirewall firewall show rule name=all | findstr /i "8089"
echo.

echo 3. Regles pour l'application Quiz:
echo -----------------------------------
netsh advfirewall firewall show rule name="Quiz Application - Port 8089"
echo.
netsh advfirewall firewall show rule name="Quiz Application - Java"
echo.

echo 4. Ports en ecoute:
echo -------------------
netstat -an | findstr "8089"
echo.

echo 5. Test de connexion locale:
echo ----------------------------
echo Tentative de connexion a http://192.168.38.1:8089
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://192.168.38.1:8089' -TimeoutSec 5 -UseBasicParsing; Write-Host '[OK] Le serveur repond - Code:' $response.StatusCode } catch { Write-Host '[ERREUR] Impossible de se connecter:' $_.Exception.Message }"
echo.

echo ========================================
echo Verification terminee
echo ========================================
pause

