@echo off
:: Ce script doit etre execute en tant qu'administrateur
:: Clic droit -> Executer en tant qu'administrateur

echo ============================================================
echo AJOUT DE apero-quiz.duckdns.org DANS LE FICHIER HOSTS
echo ============================================================
echo.

:: Verification des droits admin
net session >nul 2>&1
if %errorLevel% NEQ 0 (
    echo [ERREUR] Ce script doit etre execute en tant qu'administrateur!
    echo.
    echo Clic droit sur le fichier -^> Executer en tant qu'administrateur
    echo.
    pause
    exit /b 1
)

echo [OK] Execution en tant qu'administrateur
echo.

:: Etape 1: Vider le cache DNS
echo 1. Vidage du cache DNS...
ipconfig /flushdns >nul 2>&1
echo [OK] Cache DNS vide
echo.

:: Etape 2: Verifier si l'entree existe deja
echo 2. Verification du fichier hosts...
findstr /C:"apero-quiz.duckdns.org" C:\Windows\System32\drivers\etc\hosts >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [INFO] Une entree existe deja pour apero-quiz.duckdns.org
    echo.
    echo Contenu actuel:
    findstr /C:"apero-quiz.duckdns.org" C:\Windows\System32\drivers\etc\hosts
    echo.
    set /p REPLACE="Voulez-vous la remplacer? (O/N): "
    if /I "!REPLACE!"=="O" (
        echo.
        echo Suppression de l'ancienne entree...
        findstr /V /C:"apero-quiz.duckdns.org" C:\Windows\System32\drivers\etc\hosts > C:\Windows\System32\drivers\etc\hosts.tmp
        move /Y C:\Windows\System32\drivers\etc\hosts.tmp C:\Windows\System32\drivers\etc\hosts >nul 2>&1
        echo [OK] Ancienne entree supprimee
    ) else (
        echo.
        echo [INFO] Conservation de l'entree existante
        echo.
        goto :end
    )
)

:: Etape 3: Ajouter la nouvelle entree
echo 3. Ajout de la nouvelle entree...
echo. >> C:\Windows\System32\drivers\etc\hosts
echo # Ajout pour Quiz App - %date% %time% >> C:\Windows\System32\drivers\etc\hosts
echo 127.0.0.1 apero-quiz.duckdns.org >> C:\Windows\System32\drivers\etc\hosts

if %ERRORLEVEL% EQU 0 (
    echo [OK] Entree ajoutee avec succes!
    echo.
    echo Dernières lignes du fichier hosts:
    powershell -Command "Get-Content 'C:\Windows\System32\drivers\etc\hosts' | Select-Object -Last 5"
) else (
    echo [ERREUR] Impossible d'ajouter l'entree
    goto :error
)
echo.

:: Etape 4: Test de resolution
echo 4. Test de resolution DNS...
ping apero-quiz.duckdns.org -n 1 | findstr /C:"127.0.0.1"
if %ERRORLEVEL% EQU 0 (
    echo [OK] Le domaine est maintenant resolu vers 127.0.0.1
) else (
    echo [ATTENTION] La resolution DNS pourrait prendre quelques secondes
)
echo.

:end
echo ============================================================
echo CONFIGURATION TERMINEE!
echo ============================================================
echo.
echo Vous pouvez maintenant acceder a l'application via:
echo.
echo   https://apero-quiz.duckdns.org:8443
echo   OU
echo   https://localhost:8443
echo.
echo Si vous voyez une erreur de certificat dans le navigateur:
echo   - Chrome: Tapez 'thisisunsafe' sur la page d'erreur
echo   - Edge: Cliquez 'Avance' puis 'Continuer'
echo.
pause
exit /b 0

:error
echo.
echo ============================================================
echo ERREUR
echo ============================================================
echo.
echo Une erreur s'est produite lors de la modification du fichier hosts.
echo.
echo Vous pouvez le faire manuellement:
echo.
echo 1. Ouvrez Notepad en tant qu'administrateur
echo 2. Ouvrez: C:\Windows\System32\drivers\etc\hosts
echo 3. Ajoutez cette ligne a la fin:
echo.
echo    127.0.0.1 apero-quiz.duckdns.org
echo.
echo 4. Sauvegardez (Ctrl+S)
echo.
pause
exit /b 1

