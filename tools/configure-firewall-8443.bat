@echo off
echo ============================================================
echo   CONFIGURATION PARE-FEU POUR HTTPS
echo   Port 8443 (HTTPS)
echo ============================================================
echo.
echo ATTENTION: Ce script doit etre execute en tant qu'Administrateur
echo.
echo Faites un clic droit sur ce fichier et selectionnez
echo "Executer en tant qu'administrateur"
echo.
pause

echo.
echo [1] Suppression des anciennes regles...
netsh advfirewall firewall delete rule name="Quiz App - HTTPS 8443" >nul 2>&1
netsh advfirewall firewall delete rule name="Quiz App - HTTPS 8443 Out" >nul 2>&1
echo [OK] Anciennes regles supprimees

echo.
echo [2] Creation regle HTTPS entrant (port 8443)...
netsh advfirewall firewall add rule name="Quiz App - HTTPS 8443" dir=in action=allow protocol=TCP localport=8443 profile=any
if errorlevel 1 (
    echo [ERREUR] Impossible de creer la regle entrante
    echo Verifiez que vous executez en tant qu'Administrateur
    pause
    exit /b 1
)
echo [OK] Regle entrante creee

echo.
echo [3] Creation regle HTTPS sortant (port 8443)...
netsh advfirewall firewall add rule name="Quiz App - HTTPS 8443 Out" dir=out action=allow protocol=TCP localport=8443 profile=any
if errorlevel 1 (
    echo [ERREUR] Impossible de creer la regle sortante
) else (
    echo [OK] Regle sortante creee
)

echo.
echo [4] Verification des regles creees...
netsh advfirewall firewall show rule name="Quiz App - HTTPS 8443"

echo.
echo ============================================================
echo [SUCCESS] Pare-feu configure pour HTTPS!
echo ============================================================
echo.
echo Port 8443 autorise pour:
echo   - Connexions entrantes (IN)
echo   - Connexions sortantes (OUT)
echo   - Tous les profils (Domaine, Prive, Public)
echo.
echo URL d'acces:
echo   - HTTPS: https://192.168.1.90:8443
echo   - Local: https://localhost:8443
echo.
echo Prochaine etape:
echo   - Demarrer l'application: start_clean.bat
echo   - Acceder via: https://192.168.1.90:8443
echo.
pause

