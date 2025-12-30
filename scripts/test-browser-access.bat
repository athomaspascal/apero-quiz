@echo off
setlocal enabledelayedexpansion

echo ============================================================
echo TEST DE CONNEXION NAVIGATEUR - QUIZ APP
echo ============================================================
echo.

echo 1. VERIFICATION DE L'APPLICATION
echo ---------------------------------
echo Recherche de l'application sur le port 8443...
netstat -ano | findstr ":8443" > nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] L'application est en cours d'execution sur le port 8443
    netstat -ano | findstr ":8443"
) else (
    echo [ERREUR] L'application n'est PAS en cours d'execution!
    echo.
    echo SOLUTION: Demarrez l'application d'abord avec Maven ou votre IDE
    echo.
    goto :end
)
echo.

echo 2. ADRESSE IP DE VOTRE PC
echo -------------------------
ipconfig | findstr /C:"IPv4"
echo.

echo 3. TEST DE CONNEXION
echo --------------------
echo Test de connexion a https://localhost:8443...
curl -k -s -o nul -w "HTTP Status: %%{http_code}\n" https://localhost:8443 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [INFO] curl n'est pas disponible, test ignore
)
echo.

echo 4. SOLUTION POUR CHROME
echo ------------------------
echo Si Chrome affiche "Votre connexion n'est pas privee":
echo.
echo ^>^>^> TAPEZ SIMPLEMENT: thisisunsafe
echo     (tapez directement ces lettres sur la page d'erreur)
echo.
echo Ou cliquez sur "Avance" puis "Continuer vers localhost"
echo.

echo 5. SOLUTION POUR EDGE
echo ---------------------
echo Si Edge affiche une erreur de certificat:
echo.
echo 1. Cliquez sur "Avance"
echo 2. Cliquez sur "Continuer vers localhost (non securise)"
echo.

echo 6. URLS A TESTER
echo -----------------
echo Testez ces URLs dans votre navigateur:
echo.
echo   https://localhost:8443
echo   https://127.0.0.1:8443
echo.

:end
echo ============================================================
echo FIN DU TEST
echo ============================================================
pause

