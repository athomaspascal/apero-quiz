@echo off
echo ============================================================
echo   VERIFICATION PARE-FEU - Port 8089 et IP 192.168.1.90
echo ============================================================
echo.

echo [1] Configuration dans application.properties:
echo ------------------------------------------------------------
echo Adresse serveur: 192.168.1.90
echo Port serveur: 8089
echo.

echo [2] Etat du pare-feu Windows:
echo ------------------------------------------------------------
netsh advfirewall show currentprofile state
echo.

echo [3] Verification si le port 8089 est en ecoute:
echo ------------------------------------------------------------
netstat -ano | findstr :8089
if errorlevel 1 (
    echo [INFO] Port 8089 NON utilise - Application non demarree
) else (
    echo [OK] Port 8089 ACTIF - Application en cours d'execution
)
echo.

echo [4] Recherche de regles existantes pour le port 8089:
echo ------------------------------------------------------------
netsh advfirewall firewall show rule name=all | findstr /C:"LocalPort" | findstr "8089" >nul 2>&1
if errorlevel 1 (
    echo [!] Aucune regle trouvee pour le port 8089
    echo.
    echo RECOMMANDATION: Creer une regle de pare-feu
    echo Executez en tant qu'Administrateur:
    echo   configure-firewall-8089.bat
) else (
    echo [OK] Des regles existent pour le port 8089
    echo.
    echo Details des regles contenant le port 8089:
    netsh advfirewall firewall show rule name=all | findstr /B /C:"Rule Name" /C:"Enabled" /C:"Direction" /C:"Protocol" /C:"LocalPort" | findstr /B /A:5 "8089"
)
echo.

echo [5] Test de connectivite locale:
echo ------------------------------------------------------------
echo Test de connexion sur localhost:8089...
powershell -Command "$result = Test-NetConnection -ComputerName localhost -Port 8089 -WarningAction SilentlyContinue; if($result.TcpTestSucceeded) { Write-Host '[OK] Port 8089 accessible localement' -ForegroundColor Green } else { Write-Host '[ECHEC] Port 8089 non accessible' -ForegroundColor Red }"
echo.

echo [6] Test de connectivite reseau:
echo ------------------------------------------------------------
echo Test de connexion sur 192.168.1.90:8089...
powershell -Command "$result = Test-NetConnection -ComputerName 192.168.1.90 -Port 8089 -WarningAction SilentlyContinue; if($result.TcpTestSucceeded) { Write-Host '[OK] Port 8089 accessible sur le reseau' -ForegroundColor Green } else { Write-Host '[ECHEC] Port 8089 non accessible sur le reseau' -ForegroundColor Red }"
echo.

echo ============================================================
echo RESUME:
echo ============================================================
echo.
echo Pour autoriser le port 8089 dans le pare-feu:
echo   1. Clic droit sur configure-firewall-8089.bat
echo   2. "Executer en tant qu'administrateur"
echo.
echo Pour demarrer l'application:
echo   start_clean.bat
echo.
echo Pour acceder a l'application:
echo   - Local: http://localhost:8089
echo   - Reseau: http://192.168.1.90:8089
echo.
pause

