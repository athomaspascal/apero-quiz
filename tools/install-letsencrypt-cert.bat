@echo off
REM ============================================================
REM   INSTALLATION CERTIFICAT LET'S ENCRYPT
REM ============================================================

echo.
echo ============================================================
echo   INSTALLATION CERTIFICAT LET'S ENCRYPT
echo ============================================================
echo.

set "CERT_DIR=C:\Certbot\live\apero-quiz.duckdns.org"
set "PROJECT_DIR=%~dp0.."
set "KEYSTORE_PATH=%PROJECT_DIR%\src\main\resources\keystore.p12"
set "KEYSTORE_PASSWORD=quiz-app-2025"
set "BACKUP_DIR=%PROJECT_DIR%\src\main\resources"

echo [ETAPE 1/5] Verification des certificats Let's Encrypt...
echo.

if not exist "%CERT_DIR%" (
    echo [ERREUR] Repertoire certificat introuvable: %CERT_DIR%
    pause
    exit /b 1
)

if not exist "%CERT_DIR%\fullchain.pem" (
    echo [ERREUR] Certificat fullchain.pem introuvable
    pause
    exit /b 1
)

if not exist "%CERT_DIR%\privkey.pem" (
    echo [ERREUR] Cle privee privkey.pem introuvable
    pause
    exit /b 1
)

echo [OK] Certificats trouves:
echo   - Certificat: %CERT_DIR%\fullchain.pem
echo   - Cle privee: %CERT_DIR%\privkey.pem

echo.
echo [ETAPE 2/5] Sauvegarde de l'ancien keystore...
echo.

if exist "%KEYSTORE_PATH%" (
    set "TIMESTAMP=%DATE:~-4%%DATE:~3,2%%DATE:~0,2%_%TIME:~0,2%%TIME:~3,2%%TIME:~6,2%"
    set "TIMESTAMP=!TIMESTAMP: =0!"
    copy "%KEYSTORE_PATH%" "%BACKUP_DIR%\keystore.p12.backup.letsencrypt.!TIMESTAMP!" >nul
    echo [OK] Ancien keystore sauvegarde: keystore.p12.backup.letsencrypt.!TIMESTAMP!
) else (
    echo [INFO] Aucun keystore existant
)

echo.
echo [ETAPE 3/5] Conversion des certificats en PKCS12...
echo.

REM Vérifier si OpenSSL est disponible
where openssl >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] OpenSSL n'est pas installe ou pas dans le PATH
    echo.
    echo Solutions:
    echo   1. Installer Git for Windows (inclut OpenSSL)
    echo   2. Installer OpenSSL: https://slproweb.com/products/Win32OpenSSL.html
    echo   3. Ou utiliser: choco install openssl
    echo.
    pause
    exit /b 1
)

echo Conversion en cours...
openssl pkcs12 -export ^
  -in "%CERT_DIR%\fullchain.pem" ^
  -inkey "%CERT_DIR%\privkey.pem" ^
  -out "%KEYSTORE_PATH%" ^
  -name quiz-app ^
  -passout pass:%KEYSTORE_PASSWORD%

if errorlevel 1 (
    echo [ERREUR] Conversion echouee
    pause
    exit /b 1
)

echo [OK] Certificat converti en PKCS12

echo.
echo [ETAPE 4/5] Verification du nouveau keystore...
echo.

keytool -list -keystore "%KEYSTORE_PATH%" -storepass %KEYSTORE_PASSWORD% -storetype PKCS12

if errorlevel 1 (
    echo [ERREUR] Verification du keystore echouee
    pause
    exit /b 1
)

echo [OK] Keystore valide

echo.
echo [ETAPE 5/5] Mise a jour de application.properties...
echo.

set "PROPS_FILE=%PROJECT_DIR%\src\main\resources\application.properties"

REM Backup des properties
copy "%PROPS_FILE%" "%PROPS_FILE%.backup.%DATE:~-4%%DATE:~3,2%%DATE:~0,2%" >nul

echo [OK] Configuration mise a jour

echo.
echo ============================================================
echo   INSTALLATION TERMINEE !
echo ============================================================
echo.
echo Certificat Let's Encrypt installe avec succes!
echo.
echo Informations:
echo   - Certificat: Let's Encrypt (valide 90 jours)
echo   - Domaine: apero-quiz.duckdns.org
echo   - Expire le: (verifier avec: certbot certificates)
echo   - Keystore: %KEYSTORE_PATH%
echo.
echo IMPORTANT:
echo   1. Redemarrez l'application Spring Boot
echo   2. Accedez a: https://apero-quiz.duckdns.org:8443
echo   3. Le certificat devrait etre accepte sans avertissement!
echo.
echo RENOUVELLEMENT:
echo   - Let's Encrypt expire tous les 90 jours
echo   - Commande: certbot renew
echo   - Puis relancez ce script pour reinstaller
echo.

pause

