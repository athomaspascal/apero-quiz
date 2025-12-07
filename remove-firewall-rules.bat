@echo off
echo ========================================
echo Suppression des regles de Pare-feu
echo Pour l'application Quiz
echo ========================================
echo.

REM Vérifier les privilèges administrateur
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERREUR: Ce script doit etre execute en tant qu'administrateur!
    echo.
    echo Faites un clic droit sur le fichier et selectionnez
    echo "Executer en tant qu'administrateur"
    echo.
    pause
    exit /b 1
)

echo Suppression de la regle pour le port 8089...
netsh advfirewall firewall delete rule name="Quiz Application - Port 8089"

if %errorLevel% equ 0 (
    echo [OK] Regle pour le port 8089 supprimee
) else (
    echo [INFO] Aucune regle trouvee pour le port 8089
)

echo.
echo Suppression de la regle pour Java...
netsh advfirewall firewall delete rule name="Quiz Application - Java"

if %errorLevel% equ 0 (
    echo [OK] Regle pour Java supprimee
) else (
    echo [INFO] Aucune regle trouvee pour Java
)

echo.
echo Suppression de la regle pour le profil reseau...
netsh advfirewall firewall delete rule name="Quiz Application - Network Profile"

if %errorLevel% equ 0 (
    echo [OK] Regle pour profil reseau supprimee
) else (
    echo [INFO] Aucune regle trouvee pour profil reseau
)

echo.
echo ========================================
echo Suppression terminee!
echo ========================================
pause

