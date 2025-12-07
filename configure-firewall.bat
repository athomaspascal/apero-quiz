@echo off
echo ========================================
echo Configuration du Pare-feu Windows
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

echo Ajout de la regle pour le port 8089 (TCP)...
netsh advfirewall firewall delete rule name="Quiz Application - Port 8089" >nul 2>&1
netsh advfirewall firewall add rule name="Quiz Application - Port 8089" dir=in action=allow protocol=TCP localport=8089

if %errorLevel% equ 0 (
    echo [OK] Regle TCP ajoutee avec succes
) else (
    echo [ERREUR] Echec de l'ajout de la regle TCP
)

echo.
echo Ajout de la regle pour Java (programme)...
netsh advfirewall firewall delete rule name="Quiz Application - Java" >nul 2>&1
netsh advfirewall firewall add rule name="Quiz Application - Java" dir=in action=allow program="%JAVA_HOME%\bin\java.exe" enable=yes

if %errorLevel% equ 0 (
    echo [OK] Regle Java ajoutee avec succes
) else (
    echo [ATTENTION] Echec de l'ajout de la regle Java (verifiez JAVA_HOME)
)

echo.
echo Ajout de la regle pour le profil de reseau...
netsh advfirewall firewall delete rule name="Quiz Application - Network Profile" >nul 2>&1
netsh advfirewall firewall add rule name="Quiz Application - Network Profile" dir=in action=allow protocol=TCP localport=8089 profile=private,public

if %errorLevel% equ 0 (
    echo [OK] Regle pour profil reseau ajoutee avec succes
) else (
    echo [ERREUR] Echec de l'ajout de la regle pour profil reseau
)

echo.
echo ========================================
echo Configuration terminee!
echo ========================================
echo.
echo Les regles suivantes ont ete ajoutees:
netsh advfirewall firewall show rule name="Quiz Application - Port 8089"
echo.
echo Vous pouvez maintenant acceder a l'application via:
echo http://192.168.38.1:8089
echo.
echo Pour verifier les connexions, utilisez:
echo netstat -an ^| findstr "8089"
echo.
pause

