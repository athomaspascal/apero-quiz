@echo off
REM ============================================================
REM   INSTALLATION CLOUDFLARED
REM ============================================================

echo.
echo ============================================================
echo   INSTALLATION CLOUDFLARED
echo ============================================================
echo.

REM Vérifier si déjà installé
where cloudflared >nul 2>&1
if not errorlevel 1 (
    echo [OK] cloudflared est deja installe!
    cloudflared --version
    echo.
    echo Voulez-vous le reinstaller? (O/N)
    set /p REINSTALL="> "
    if /i not "%REINSTALL%"=="O" (
        echo Installation annulee
        pause
        exit /b 0
    )
)

echo.
echo Choisissez la methode d'installation:
echo.
echo   1. Telecharger manuellement (recommande)
echo   2. Installer avec Chocolatey (si installe)
echo   3. Installer avec Scoop (si installe)
echo.
set /p CHOICE="Votre choix (1-3): "

if "%CHOICE%"=="1" goto MANUAL
if "%CHOICE%"=="2" goto CHOCO
if "%CHOICE%"=="3" goto SCOOP

echo Choix invalide
pause
exit /b 1

:MANUAL
echo.
echo [METHODE 1] Installation manuelle
echo.
echo 1. Telechargement de cloudflared...
echo.

set DOWNLOAD_URL=https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe
set INSTALL_DIR=%ProgramFiles%\cloudflared
set INSTALL_PATH=%INSTALL_DIR%\cloudflared.exe

echo URL: %DOWNLOAD_URL%
echo Destination: %INSTALL_PATH%
echo.

REM Créer le répertoire
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

REM Télécharger avec PowerShell
echo Telechargement en cours...
powershell -Command "& {Invoke-WebRequest -Uri '%DOWNLOAD_URL%' -OutFile '%INSTALL_PATH%'}"

if errorlevel 1 (
    echo [ERREUR] Telechargement echoue
    echo.
    echo Telechargez manuellement depuis:
    echo https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/
    echo.
    echo Puis:
    echo   1. Renommez le fichier en cloudflared.exe
    echo   2. Placez-le dans: %INSTALL_DIR%
    echo   3. Ajoutez %INSTALL_DIR% au PATH
    pause
    exit /b 1
)

echo [OK] Fichier telecharge

echo.
echo 2. Ajout au PATH...
echo.

REM Ajouter au PATH système (nécessite admin)
setx /M PATH "%PATH%;%INSTALL_DIR%" >nul 2>&1

if errorlevel 1 (
    echo [INFO] Impossible d'ajouter au PATH systeme (necessaire admin)
    echo [INFO] Ajout au PATH utilisateur...
    setx PATH "%PATH%;%INSTALL_DIR%"
)

echo [OK] cloudflared ajoute au PATH

echo.
echo 3. Verification...
echo.

REM Rafraîchir le PATH pour cette session
set PATH=%PATH%;%INSTALL_DIR%

cloudflared --version

if errorlevel 1 (
    echo [ATTENTION] Redemarrez le terminal ou le PC pour utiliser cloudflared
) else (
    echo [OK] Installation reussie!
)

goto END

:CHOCO
echo.
echo [METHODE 2] Installation avec Chocolatey
echo.

where choco >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Chocolatey n'est pas installe
    echo.
    echo Installez Chocolatey depuis: https://chocolatey.org/install
    echo Ou utilisez la methode manuelle (choix 1)
    pause
    exit /b 1
)

echo Installation en cours...
choco install cloudflared -y

if errorlevel 1 (
    echo [ERREUR] Installation echouee
    pause
    exit /b 1
)

echo [OK] Installation reussie!
cloudflared --version

goto END

:SCOOP
echo.
echo [METHODE 3] Installation avec Scoop
echo.

where scoop >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Scoop n'est pas installe
    echo.
    echo Installez Scoop depuis: https://scoop.sh/
    echo Ou utilisez la methode manuelle (choix 1)
    pause
    exit /b 1
)

echo Installation en cours...
scoop install cloudflared

if errorlevel 1 (
    echo [ERREUR] Installation echouee
    pause
    exit /b 1
)

echo [OK] Installation reussie!
cloudflared --version

goto END

:END
echo.
echo ============================================================
echo   INSTALLATION TERMINEE
echo ============================================================
echo.
echo Prochaine etape: Configurez le tunnel avec
echo   tools\setup-cloudflare-tunnel.bat
echo.
pause

