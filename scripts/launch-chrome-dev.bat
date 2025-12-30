@echo off
echo ============================================================
echo LANCEMENT DE CHROME EN MODE DEVELOPPEMENT
echo ============================================================
echo.
echo Ce script lance Chrome avec des parametres de securite
echo assouplis pour accepter les certificats auto-signes.
echo.
echo ATTENTION: Utilisez ceci uniquement pour le developpement!
echo.
echo Les parametres actives:
echo   - Accepter les certificats invalides
echo   - Accepter localhost non securise
echo   - Ignorer les erreurs SSL
echo.
pause

echo.
echo Lancement de Chrome...
echo.

:: Verifier si Chrome est installe
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --ignore-certificate-errors --ignore-urlfetcher-cert-requests --allow-insecure-localhost https://apero-quiz.duckdns.org:8443
    echo [OK] Chrome lance avec succes
) else if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" (
    start "" "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --ignore-certificate-errors --ignore-urlfetcher-cert-requests --allow-insecure-localhost https://apero-quiz.duckdns.org:8443
    echo [OK] Chrome lance avec succes
) else (
    echo [ERREUR] Chrome n'est pas installe dans les emplacements standards!
    echo.
    echo Veuillez lancer Chrome manuellement avec ces parametres:
    echo chrome.exe --ignore-certificate-errors --ignore-urlfetcher-cert-requests --allow-insecure-localhost
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo Chrome est maintenant ouvert en mode developpement
echo ============================================================
echo.
echo Si vous voyez encore une erreur de certificat:
echo   - Tapez "thisisunsafe" sur la page d'erreur
echo.
echo IMPORTANT: Fermez Chrome completement quand vous avez termine
echo            pour revenir au mode de securite normal.
echo.

