@echo off
echo ============================================================
echo   CONFIGURATION HOSTS FILE POUR apero-quiz.com
echo ============================================================
echo.
echo ATTENTION: Ce script doit etre execute en tant qu'Administrateur
echo.
echo Ce script va ajouter l'entree DNS locale:
echo   192.168.1.90    apero-quiz.com
echo.
pause

set HOSTS_FILE=C:\Windows\System32\drivers\etc\hosts
set DOMAIN=apero-quiz.com
set IP=192.168.1.90

echo.
echo [1] Verification des droits Administrateur...
net session >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Ce script doit etre execute en tant qu'Administrateur!
    echo.
    echo Faites un clic droit sur ce fichier et selectionnez:
    echo "Executer en tant qu'administrateur"
    echo.
    pause
    exit /b 1
)
echo [OK] Droits Administrateur confirmes
echo.

echo [2] Backup du fichier hosts...
copy %HOSTS_FILE% %HOSTS_FILE%.backup.%date:~-4%%date:~-7,2%%date:~-10,2%
echo [OK] Backup cree: %HOSTS_FILE%.backup.%date:~-4%%date:~-7,2%%date:~-10,2%
echo.

echo [3] Verification si l'entree existe deja...
findstr /C:"%DOMAIN%" %HOSTS_FILE% >nul 2>&1
if not errorlevel 1 (
    echo [INFO] L'entree pour %DOMAIN% existe deja
    echo.
    echo Contenu actuel:
    findstr /C:"%DOMAIN%" %HOSTS_FILE%
    echo.
    set /p REPLACE="Voulez-vous la remplacer? (O/N): "
    if /i not "%REPLACE%"=="O" (
        echo Operation annulee
        pause
        exit /b 0
    )

    echo [INFO] Suppression ancienne entree...
    powershell -Command "(Get-Content '%HOSTS_FILE%') | Where-Object { $_ -notmatch '%DOMAIN%' } | Set-Content '%HOSTS_FILE%'"
)
echo.

echo [4] Ajout de la nouvelle entree DNS...
echo # Quiz Application - apero-quiz.com >> %HOSTS_FILE%
echo %IP%    %DOMAIN% >> %HOSTS_FILE%
echo %IP%    www.%DOMAIN% >> %HOSTS_FILE%
echo.
echo [OK] Entrees ajoutees

echo.
echo [5] Verification du fichier hosts...
echo.
echo Dernieres lignes du fichier hosts:
echo ----------------------------------------
type %HOSTS_FILE% | findstr /V "^#" | findstr /V "^$" | find /V "" | more +10
echo ----------------------------------------
echo.

echo [6] Flush DNS cache...
ipconfig /flushdns
echo [OK] Cache DNS vide
echo.

echo [7] Test de resolution DNS...
ping -n 1 %DOMAIN% | findstr "192.168.1.90"
if errorlevel 1 (
    echo [ATTENTION] Le domaine ne resout pas encore vers 192.168.1.90
    echo Attendez quelques secondes et reessayez
) else (
    echo [OK] Le domaine resout correctement vers 192.168.1.90
)
echo.

echo ============================================================
echo [SUCCESS] Configuration hosts terminee!
echo ============================================================
echo.
echo Entrees DNS ajoutees:
echo   %IP%    %DOMAIN%
echo   %IP%    www.%DOMAIN%
echo.
echo Vous pouvez maintenant acceder a l'application via:
echo   - HTTP:  http://%DOMAIN%:8089
echo   - HTTPS: https://%DOMAIN%:8443
echo.
echo IMPORTANT: Si vous avez plusieurs PC, executez ce script
echo            sur chaque PC qui doit acceder au quiz.
echo.
pause

