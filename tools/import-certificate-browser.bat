@echo off
REM ============================================================
REM   IMPORTATION CERTIFICAT SSL DANS LE NAVIGATEUR
REM ============================================================

echo.
echo ============================================================
echo   IMPORTATION CERTIFICAT SSL
echo ============================================================
echo.

set "KEYSTORE_PATH=%~dp0..\src\main\resources\keystore.p12"
set "CERT_PATH=%~dp0..\src\main\resources\quiz-app-cert.crt"
set "KEYSTORE_PASSWORD=quiz-app-2025"

echo [ETAPE 1/3] Export du certificat depuis le keystore...
echo.

REM Export du certificat au format CRT
keytool -exportcert -alias quiz-app -keystore "%KEYSTORE_PATH%" -storepass %KEYSTORE_PASSWORD% -file "%CERT_PATH%" -rfc

if errorlevel 1 (
    echo [ERREUR] Impossible d'exporter le certificat
    pause
    exit /b 1
)

echo [SUCCESS] Certificat exporte: %CERT_PATH%
echo.

echo [ETAPE 2/3] Instructions d'importation manuelle
echo.
echo Le certificat a ete exporte. Veuillez suivre ces etapes :
echo.
echo === POUR CHROME / EDGE ===
echo 1. Ouvrir Chrome/Edge
echo 2. Parametres ^> Confidentialite et securite ^> Securite
echo 3. Gerer les certificats
echo 4. Onglet "Autorites de certification racines de confiance"
echo 5. Cliquer "Importer..."
echo 6. Selectionner le fichier: %CERT_PATH%
echo 7. Cocher "Faire confiance a ce certificat..."
echo 8. Terminer
echo.
echo === POUR FIREFOX ===
echo 1. Ouvrir Firefox
echo 2. Parametres ^> Vie privee et securite
echo 3. Certificats ^> Afficher les certificats
echo 4. Onglet "Autorites"
echo 5. Importer... ^> Selectionner: %CERT_PATH%
echo 6. Cocher "Faire confiance pour identifier les sites web"
echo 7. OK
echo.

echo [ETAPE 3/3] Ouverture automatique du fichier certificat...
echo.
echo Voulez-vous ouvrir le certificat maintenant ? (O/N)
set /p OPEN_CERT="> "

if /i "%OPEN_CERT%"=="O" (
    start "" "%CERT_PATH%"
    echo.
    echo [INFO] Double-cliquez sur le certificat pour l'installer
    echo [INFO] Choisir "Ordinateur local" puis "Autorites de certification racines de confiance"
)

echo.
echo ============================================================
echo [INFO] REDEMARREZ VOTRE NAVIGATEUR apres l'importation
echo ============================================================
echo.
pause

