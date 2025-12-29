@echo off
REM ============================================================
REM   TEST CERTIFICAT LET'S ENCRYPT
REM ============================================================

echo.
echo ============================================================
echo   VERIFICATION INSTALLATION CERTIFICAT LET'S ENCRYPT
echo ============================================================
echo.

cd /d "%~dp0.."

echo [1/5] Verification OpenSSL...
"C:\Program Files\OpenSSL-Win64\bin\openssl.exe" version
if errorlevel 1 (
    echo [ERREUR] OpenSSL non trouve
    pause
    exit /b 1
)
echo [OK] OpenSSL present
echo.

echo [2/5] Verification certificats Let's Encrypt...
if exist "C:\Certbot\archive\apero-quiz.duckdns.org\fullchain1.pem" (
    echo [OK] Certificat fullchain present
) else (
    echo [ERREUR] Certificat fullchain introuvable
    pause
    exit /b 1
)

if exist "C:\Certbot\archive\apero-quiz.duckdns.org\privkey1.pem" (
    echo [OK] Cle privee presente
) else (
    echo [ERREUR] Cle privee introuvable
    pause
    exit /b 1
)
echo.

echo [3/5] Verification keystore application...
if exist "src\main\resources\keystore.p12" (
    echo [OK] Keystore present
    for %%A in (src\main\resources\keystore.p12) do echo     Taille: %%~zA octets
) else (
    echo [ERREUR] Keystore introuvable
    pause
    exit /b 1
)
echo.

echo [4/5] Verification contenu keystore...
keytool -list -keystore src\main\resources\keystore.p12 -storepass quiz-app-2025 -storetype PKCS12 >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Keystore invalide ou mot de passe incorrect
    pause
    exit /b 1
)
echo [OK] Keystore valide
echo.

echo [5/5] Affichage informations certificat...
echo.
keytool -list -v -keystore src\main\resources\keystore.p12 -storepass quiz-app-2025 -storetype PKCS12 | findstr /i "Alias: Owner: Valid from: Valid until:"
echo.

echo ============================================================
echo   VERIFICATION TERMINEE - TOUT EST OK !
echo ============================================================
echo.
echo Certificat Let's Encrypt installe et configure.
echo.
echo PROCHAINES ETAPES:
echo   1. Demarrer l'application: run-app.bat
echo   2. Tester: https://apero-quiz.duckdns.org:8443
echo   3. Verifier: Aucun avertissement de certificat!
echo.

set /p START="Voulez-vous demarrer l'application maintenant? (O/N): "
if /i "%START%"=="O" (
    echo.
    echo Demarrage de l'application...
    start run-app.bat
    timeout /t 5 /nobreak >nul
    echo.
    echo Ouverture du navigateur dans 10 secondes...
    timeout /t 10 /nobreak
    start https://apero-quiz.duckdns.org:8443
)

echo.
pause

