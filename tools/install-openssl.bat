@echo off
REM ============================================================
REM   INSTALLATION OPENSSL
REM ============================================================

echo.
echo ============================================================
echo   INSTALLATION OPENSSL
echo ============================================================
echo.

REM Vérifier si OpenSSL est déjà installé
where openssl >nul 2>&1
if not errorlevel 1 (
    echo [OK] OpenSSL est deja installe!
    openssl version
    pause
    exit /b 0
)

echo OpenSSL n'est pas installe.
echo.
echo Choisissez la methode d'installation:
echo.
echo   1. Telecharger et installer automatiquement (RECOMMANDE)
echo   2. Telecharger manuellement depuis le site officiel
echo   3. Installer Git for Windows (inclut OpenSSL)
echo.
set /p CHOICE="Votre choix (1-3): "

if "%CHOICE%"=="1" goto AUTO_INSTALL
if "%CHOICE%"=="2" goto MANUAL
if "%CHOICE%"=="3" goto GIT

echo Choix invalide
pause
exit /b 1

:AUTO_INSTALL
echo.
echo [METHODE 1] Installation automatique
echo.

set OPENSSL_VERSION=3.0.13
set DOWNLOAD_URL=https://slproweb.com/download/Win64OpenSSL-3_0_13.exe
set INSTALLER_PATH=%TEMP%\OpenSSL-Installer.exe

echo Telechargement d'OpenSSL %OPENSSL_VERSION%...
echo URL: %DOWNLOAD_URL%
echo.

powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri '%DOWNLOAD_URL%' -OutFile '%INSTALLER_PATH%'}"

if errorlevel 1 (
    echo [ERREUR] Telechargement echoue
    echo.
    echo Telechargez manuellement depuis:
    echo https://slproweb.com/products/Win32OpenSSL.html
    echo.
    echo Choisissez: Win64 OpenSSL v3.x Light
    pause
    exit /b 1
)

echo [OK] Telechargement termine
echo.
echo Lancement de l'installateur...
echo.
echo IMPORTANT:
echo   - Acceptez les termes de la licence
echo   - Installez dans: C:\Program Files\OpenSSL-Win64
echo   - Cochez "Add to system PATH" si propose
echo.

start /wait "" "%INSTALLER_PATH%"

REM Supprimer l'installateur
del "%INSTALLER_PATH%" >nul 2>&1

echo.
echo Ajout d'OpenSSL au PATH...
echo.

set OPENSSL_DIR=C:\Program Files\OpenSSL-Win64\bin

REM Vérifier si OpenSSL a été installé
if not exist "%OPENSSL_DIR%\openssl.exe" (
    echo [ERREUR] OpenSSL introuvable dans: %OPENSSL_DIR%
    echo.
    echo Verifiez l'installation et ajoutez manuellement le chemin au PATH
    pause
    exit /b 1
)

REM Ajouter au PATH utilisateur
setx PATH "%PATH%;%OPENSSL_DIR%"

echo.
echo [OK] OpenSSL ajoute au PATH
echo.
echo IMPORTANT: Fermez et rouvrez ce terminal pour que le PATH soit mis a jour
echo.

REM Tester dans une nouvelle session
start cmd /k "openssl version && echo. && echo [OK] OpenSSL fonctionne! && pause"

goto END

:MANUAL
echo.
echo [METHODE 2] Installation manuelle
echo.
echo 1. Ouvrez votre navigateur et allez sur:
echo    https://slproweb.com/products/Win32OpenSSL.html
echo.
echo 2. Telechargez: Win64 OpenSSL v3.x Light
echo.
echo 3. Executez l'installateur
echo.
echo 4. Installez dans: C:\Program Files\OpenSSL-Win64
echo.
echo 5. Ajoutez au PATH:
echo    - Panneau de configuration ^> Systeme ^> Parametres systeme avances
echo    - Variables d'environnement
echo    - PATH ^> Modifier
echo    - Ajouter: C:\Program Files\OpenSSL-Win64\bin
echo.
echo 6. Redemarrez le terminal
echo.

start https://slproweb.com/products/Win32OpenSSL.html

pause
goto END

:GIT
echo.
echo [METHODE 3] Installation de Git for Windows
echo.
echo Git for Windows inclut OpenSSL.
echo.
echo 1. Ouvrez votre navigateur et allez sur:
echo    https://git-scm.com/download/win
echo.
echo 2. Telechargez l'installateur
echo.
echo 3. Executez l'installateur (installation par defaut)
echo.
echo 4. OpenSSL sera disponible via Git Bash
echo.

start https://git-scm.com/download/win

pause
goto END

:END
echo.
echo ============================================================
echo   INSTALLATION TERMINEE
echo ============================================================
echo.
echo Apres installation:
echo   1. Fermez TOUS les terminaux ouverts
echo   2. Rouvrez un nouveau terminal
echo   3. Testez: openssl version
echo   4. Relancez: tools\install-letsencrypt-cert.bat
echo.
pause

