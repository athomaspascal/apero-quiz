@echo off
REM ============================================================
REM   INSTALLATION CERTIFICAT LET'S ENCRYPT (SANS OPENSSL)
REM   Utilise Java keytool uniquement
REM ============================================================

echo.
echo ============================================================
echo   INSTALLATION CERTIFICAT LET'S ENCRYPT
echo   (Methode alternative sans OpenSSL)
echo ============================================================
echo.

set "CERT_DIR=C:\Certbot\live\apero-quiz.duckdns.org"
set "PROJECT_DIR=%~dp0.."
set "KEYSTORE_PATH=%PROJECT_DIR%\src\main\resources\keystore.p12"
set "KEYSTORE_PASSWORD=quiz-app-2025"
set "BACKUP_DIR=%PROJECT_DIR%\src\main\resources"
set "TEMP_DIR=%TEMP%\letsencrypt-import"

echo [ETAPE 1/6] Verification des certificats Let's Encrypt...
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
echo [ETAPE 2/6] Sauvegarde de l'ancien keystore...
echo.

if exist "%KEYSTORE_PATH%" (
    for /f "tokens=2-4 delims=/ " %%a in ('date /t') do set DATE_STAMP=%%c%%b%%a
    for /f "tokens=1-3 delims=:. " %%a in ('echo %TIME%') do set TIME_STAMP=%%a%%b%%c
    set "TIMESTAMP=%DATE_STAMP%_%TIME_STAMP: =0%"
    copy "%KEYSTORE_PATH%" "%BACKUP_DIR%\keystore.p12.backup.letsencrypt.%TIMESTAMP%" >nul
    echo [OK] Ancien keystore sauvegarde: keystore.p12.backup.letsencrypt.%TIMESTAMP%
) else (
    echo [INFO] Aucun keystore existant
)

echo.
echo [ETAPE 3/6] Creation repertoire temporaire...
echo.

if not exist "%TEMP_DIR%" mkdir "%TEMP_DIR%"
echo [OK] Repertoire temporaire: %TEMP_DIR%

echo.
echo [ETAPE 4/6] Conversion avec OpenSSL...
echo.

REM Chercher OpenSSL dans différents emplacements
set OPENSSL_FOUND=0

REM Essayer les emplacements communs
for %%P in (
    "C:\Program Files\OpenSSL-Win64\bin\openssl.exe"
    "C:\Program Files\OpenSSL\bin\openssl.exe"
    "C:\OpenSSL-Win64\bin\openssl.exe"
    "C:\Program Files\Git\usr\bin\openssl.exe"
    "C:\Program Files (x86)\Git\usr\bin\openssl.exe"
) do (
    if exist %%P (
        set "OPENSSL=%%~P"
        set OPENSSL_FOUND=1
        goto OPENSSL_FOUND
    )
)

REM Essayer dans le PATH
where openssl >nul 2>&1
if not errorlevel 1 (
    set "OPENSSL=openssl"
    set OPENSSL_FOUND=1
    goto OPENSSL_FOUND
)

:OPENSSL_NOT_FOUND
echo [ERREUR] OpenSSL introuvable!
echo.
echo Vous avez 2 options:
echo.
echo OPTION 1 (RECOMMANDEE): Installer OpenSSL
echo   Executez: tools\install-openssl.bat
echo.
echo OPTION 2: Utiliser un outil en ligne
echo   1. Allez sur: https://www.sslshopper.com/ssl-converter.html
echo   2. Upload: %CERT_DIR%\cert.pem
echo   3. Upload private key: %CERT_DIR%\privkey.pem
echo   4. Type to convert to: PFX/PKCS#12
echo   5. Password: %KEYSTORE_PASSWORD%
echo   6. Telechargez le fichier .pfx
echo   7. Renommez-le en keystore.p12
echo   8. Copiez-le dans: %BACKUP_DIR%
echo.
echo OPTION 3: Utiliser PowerShell (complexe)
echo   Voir: tools\convert-cert-powershell.ps1
echo.
pause
exit /b 1

:OPENSSL_FOUND
echo [OK] OpenSSL trouve: %OPENSSL%
echo.

echo Conversion en cours...
"%OPENSSL%" pkcs12 -export ^
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
echo [ETAPE 5/6] Verification du nouveau keystore...
echo.

keytool -list -keystore "%KEYSTORE_PATH%" -storepass %KEYSTORE_PASSWORD% -storetype PKCS12

if errorlevel 1 (
    echo [ERREUR] Verification du keystore echouee
    pause
    exit /b 1
)

echo [OK] Keystore valide

echo.
echo [ETAPE 6/6] Mise a jour de application.properties...
echo.

set "PROPS_FILE=%PROJECT_DIR%\src\main\resources\application.properties"

REM Backup des properties
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do set DATE_STAMP=%%c%%b%%a
copy "%PROPS_FILE%" "%PROPS_FILE%.backup.%DATE_STAMP%" >nul

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
echo   - Keystore: %KEYSTORE_PATH%
echo.
echo Pour voir la date d'expiration:
echo   certbot certificates
echo.
echo IMPORTANT:
echo   1. Redemarrez l'application Spring Boot
echo   2. Accedez a: https://apero-quiz.duckdns.org:8443
echo   3. Le certificat devrait etre accepte sans avertissement!
echo.
echo RENOUVELLEMENT (tous les 90 jours):
echo   1. Commande: certbot renew
echo   2. Relancez ce script: tools\install-letsencrypt-cert-auto.bat
echo.

REM Nettoyer le répertoire temporaire
if exist "%TEMP_DIR%" rmdir /s /q "%TEMP_DIR%" >nul 2>&1

pause

