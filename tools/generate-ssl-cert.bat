@echo off
echo ============================================================
echo   GENERATION CERTIFICAT SSL AUTO-SIGNE
echo   Application Quiz - 192.168.1.90:8443
echo ============================================================
echo.

set KEYSTORE_PATH=src\main\resources\keystore.p12
set KEYSTORE_PASSWORD=quiz-app-2025
set KEYSTORE_ALIAS=quiz-app
set VALIDITY_DAYS=365

echo [1] Verification de Java...
java -version
if errorlevel 1 (
    echo [ERREUR] Java non trouve!
    pause
    exit /b 1
)
echo [OK] Java trouve
echo.

echo [2] Suppression ancien certificat (si existant)...
if exist %KEYSTORE_PATH% (
    del %KEYSTORE_PATH%
    echo [OK] Ancien certificat supprime
) else (
    echo [INFO] Aucun ancien certificat
)
echo.

echo [3] Generation du certificat SSL...
echo     Keystore: %KEYSTORE_PATH%
echo     Alias: %KEYSTORE_ALIAS%
echo     Validite: %VALIDITY_DAYS% jours
echo     IP/DNS: 192.168.1.90, localhost
echo.

keytool -genkeypair -alias %KEYSTORE_ALIAS% -keyalg RSA -keysize 2048 -storetype PKCS12 -keystore %KEYSTORE_PATH% -validity %VALIDITY_DAYS% -storepass %KEYSTORE_PASSWORD% -keypass %KEYSTORE_PASSWORD% -dname "CN=192.168.1.90, OU=Quiz Application, O=Quiz App, L=Paris, ST=IDF, C=FR" -ext "SAN=dns:192.168.1.90,dns:localhost,ip:192.168.1.90"

if errorlevel 1 (
    echo [ERREUR] Echec de generation du certificat
    pause
    exit /b 1
)

echo.
echo [4] Verification du certificat...
keytool -list -v -keystore %KEYSTORE_PATH% -storepass %KEYSTORE_PASSWORD% -alias %KEYSTORE_ALIAS%

echo.
echo ============================================================
echo [SUCCESS] Certificat SSL genere avec succes!
echo ============================================================
echo.
echo Fichier: %KEYSTORE_PATH%
echo Mot de passe: %KEYSTORE_PASSWORD%
echo Alias: %KEYSTORE_ALIAS%
echo Validite: %VALIDITY_DAYS% jours
echo.
echo INFORMATIONS IMPORTANTES:
echo   - Ce certificat est AUTO-SIGNE
echo   - Le navigateur affichera un avertissement
echo   - Cliquez sur "Avancé" puis "Continuer"
echo   - Normal pour un environnement de developpement
echo.
echo Prochaine etape:
echo   1. Executer: configure-ssl-properties.bat
echo   2. Executer en Admin: configure-firewall-8443.bat
echo   3. Demarrer l'app: start_clean.bat
echo.
pause

