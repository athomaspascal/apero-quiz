@echo off
echo ============================================================
echo Diagnostic de connexion navigateur pour Quiz App
echo ============================================================
echo.

echo 1. Verification si l'application est en cours d'execution:
echo ----------------------------------------------------------
netstat -ano | findstr ":8443"
if %ERRORLEVEL% EQU 0 (
    echo [OK] L'application ecoute sur le port 8443
) else (
    echo [ERREUR] L'application n'ecoute PAS sur le port 8443
    echo Veuillez demarrer l'application d'abord!
)
echo.

echo 2. Test de connexion locale (localhost):
echo ----------------------------------------
echo Tentative de connexion a https://localhost:8443
curl -k -I https://localhost:8443 2>&1 | findstr /C:"HTTP" /C:"SSL"
echo.

echo 3. Adresses IP de la machine:
echo ------------------------------
ipconfig | findstr /C:"IPv4"
echo.

echo 4. Verification du certificat SSL:
echo ----------------------------------
echo Verification du keystore...
if exist "%~dp0..\src\main\resources\keystore.p12" (
    echo [OK] Keystore trouve: src\main\resources\keystore.p12
) else (
    echo [ERREUR] Keystore NON trouve!
)
echo.

echo 5. Verification du certificat dans le navigateur:
echo -------------------------------------------------
echo PROBLEMES POSSIBLES:
echo.
echo A) Certificat auto-signe bloque par le navigateur:
echo    - Chrome/Edge affiche "Votre connexion n'est pas privee"
echo    - Solution 1: Cliquez sur "Avance" puis "Continuer vers localhost (dangereux)"
echo    - Solution 2: Tapez "thisisunsafe" directement dans la page d'erreur
echo    - Solution 3: Importez le certificat dans le magasin de certificats Windows
echo.
echo B) Le navigateur redirige vers HTTP au lieu de HTTPS:
echo    - Verifiez que vous utilisez HTTPS:// et non HTTP://
echo    - URL correcte: https://localhost:8443
echo.
echo C) Cache du navigateur:
echo    - Videz le cache du navigateur (Ctrl+Shift+Del)
echo    - Essayez en mode navigation privee (Ctrl+Shift+N)
echo.
echo D) Parametre de securite Windows:
echo    - Verifiez les parametres de securite Internet dans le Panneau de configuration
echo.

echo 6. URLs a tester dans votre navigateur:
echo ---------------------------------------
echo URL 1 (Localhost): https://localhost:8443
echo URL 2 (Nom d'hote): https://%COMPUTERNAME%:8443
echo URL 3 (Adresse IP locale): https://192.168.x.x:8443
echo URL 4 (Domaine DuckDNS): https://apero-quiz.duckdns.org:8443
echo.

echo 7. Test de resolution DNS pour DuckDNS:
echo ---------------------------------------
nslookup apero-quiz.duckdns.org
echo.

echo 8. Instructions pour accepter le certificat dans Chrome/Edge:
echo ------------------------------------------------------------
echo 1. Ouvrez: https://localhost:8443
echo 2. Vous verrez une erreur de certificat
echo 3. Cliquez sur "Avance" ou "Advanced"
echo 4. Cliquez sur "Continuer vers localhost (dangereux)" ou "Proceed to localhost"
echo.
echo OU tapez simplement "thisisunsafe" directement sur la page d'erreur!
echo.

echo ============================================================
echo Diagnostic termine
echo ============================================================
echo.
echo Pour importer le certificat dans Windows:
echo 1. Allez dans src\main\resources\
echo 2. Double-cliquez sur keystore.p12
echo 3. Importez-le dans "Autorites de certification racines de confiance"
echo 4. Mot de passe: quiz-app-2025
echo.
pause

