@echo off
REM ============================================================
REM   DEMARRAGE APPLICATION AVEC CERTIFICAT LET'S ENCRYPT
REM ============================================================

echo.
echo ============================================================
echo   DEMARRAGE QUIZ APPLICATION
echo   Certificat SSL: Let's Encrypt
echo   Domaine: apero-quiz.duckdns.org
echo ============================================================
echo.

cd /d "%~dp0"

echo [INFO] Verification rapide...
echo.

REM Vérifier le keystore
if not exist "src\main\resources\keystore.p12" (
    echo [ERREUR] Keystore introuvable!
    echo Executez: tools\install-letsencrypt-cert-auto.bat
    pause
    exit /b 1
)

echo [OK] Keystore Let's Encrypt present
echo.

echo [INFO] Demarrage de l'application Spring Boot...
echo.
echo L'application sera accessible sur:
echo   - Local: https://localhost:8443
echo   - Domaine: https://apero-quiz.duckdns.org:8443
echo.
echo Veuillez patienter pendant le demarrage...
echo.

REM Démarrer l'application
call mvnw.cmd spring-boot:run

if errorlevel 1 (
    echo.
    echo [ERREUR] Echec du demarrage de l'application!
    echo.
    echo Verifiez les logs dans: logs\application.log
    pause
    exit /b 1
)

pause

