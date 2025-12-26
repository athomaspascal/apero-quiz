@echo off
echo ============================================================
echo   GENERATION CERTIFICAT SSL POUR apero-quiz.com
echo ============================================================
echo.

set KEYSTORE_PATH=src\main\resources\keystore.p12
set KEYSTORE_PASSWORD=quiz-app-2025
set KEYSTORE_ALIAS=quiz-app
set VALIDITY_DAYS=365
set DOMAIN=apero-quiz.com

echo Configuration:
echo   - Domaine principal: %DOMAIN%
echo   - Alias: www.%DOMAIN%
echo   - IP locale: 192.168.1.90
echo   - Validite: %VALIDITY_DAYS% jours
echo.
pause

echo.
echo [1] Verification de Java...
java -version
if errorlevel 1 (
    echo [ERREUR] Java non trouve!
    pause
    exit /b 1
)
echo [OK] Java trouve
echo.

echo [2] Backup ancien certificat (si existant)...
if exist %KEYSTORE_PATH% (
    ren %KEYSTORE_PATH% keystore.p12.backup.%date:~-4%%date:~-7,2%%date:~-10,2%_%time:~0,2%%time:~3,2%%time:~6,2%
    echo [OK] Ancien certificat sauvegarde
) else (
    echo [INFO] Aucun ancien certificat
)
echo.

echo [3] Generation du nouveau certificat SSL pour %DOMAIN%...
echo.

keytool -genkeypair ^
    -alias %KEYSTORE_ALIAS% ^
    -keyalg RSA ^
    -keysize 2048 ^
    -storetype PKCS12 ^
    -keystore %KEYSTORE_PATH% ^
    -validity %VALIDITY_DAYS% ^
    -storepass %KEYSTORE_PASSWORD% ^
    -keypass %KEYSTORE_PASSWORD% ^
    -dname "CN=%DOMAIN%, OU=Quiz Application, O=Apero Quiz, L=Paris, ST=Ile-de-France, C=FR" ^
    -ext "SAN=dns:%DOMAIN%,dns:www.%DOMAIN%,dns:192.168.1.90,dns:localhost,ip:192.168.1.90"

if errorlevel 1 (
    echo [ERREUR] Echec generation certificat
    pause
    exit /b 1
)

echo.
echo [4] Verification du certificat...
keytool -list -v -keystore %KEYSTORE_PATH% -storepass %KEYSTORE_PASSWORD% -alias %KEYSTORE_ALIAS%

echo.
echo ============================================================
echo [SUCCESS] Certificat SSL genere pour %DOMAIN%!
echo ============================================================
echo.
echo Informations:
echo   - Fichier: %KEYSTORE_PATH%
echo   - Domaine principal: %DOMAIN%
echo   - Domaine secondaire: www.%DOMAIN%
echo   - IP locale: 192.168.1.90
echo   - Validite: %VALIDITY_DAYS% jours
echo.
echo IMPORTANT - Configuration DNS requise:
echo.
echo Option 1 - Hosts file (chaque PC):
echo   Windows: C:\Windows\System32\drivers\etc\hosts
echo   Ajouter: 192.168.1.90    %DOMAIN%
echo.
echo Option 2 - DNS routeur:
echo   Interface admin routeur ^> DNS Local
echo   Ajouter: %DOMAIN% ^-^> 192.168.1.90
echo.
echo Option 3 - Domaine public:
echo   Acheter %DOMAIN% chez un registrar
echo   Configurer DNS: A record ^-^> Votre IP publique
echo.
echo Prochaines etapes:
echo   1. Configurer DNS (voir ci-dessus)
echo   2. Demarrer l'application: start_clean.bat
echo   3. Acceder via: https://%DOMAIN%:8443
echo.
echo NOTE: Le navigateur affichera un avertissement car
echo       le certificat est auto-signe.
echo.
pause

