@echo off
echo ============================================================
echo   CONFIGURATION COMPLETE SSL/HTTPS
echo   Application Quiz
echo ============================================================
echo.
echo Ce script va:
echo   1. Generer un certificat SSL auto-signe
echo   2. Configurer application.properties pour HTTPS
echo   3. Vous guider pour la configuration du pare-feu
echo.
pause

echo.
echo ============================================================
echo ETAPE 1/3 : Generation du certificat SSL
echo ============================================================
echo.
call generate-ssl-cert.bat
if errorlevel 1 (
    echo [ERREUR] Echec generation certificat
    pause
    exit /b 1
)

echo.
echo ============================================================
echo ETAPE 2/3 : Configuration application.properties
echo ============================================================
echo.
python configure-ssl-properties.py
if errorlevel 1 (
    echo [ERREUR] Echec configuration properties
    pause
    exit /b 1
)

echo.
echo ============================================================
echo ETAPE 3/3 : Configuration du pare-feu
echo ============================================================
echo.
echo IMPORTANT: Cette etape necessite des droits Administrateur
echo.
echo Ouvrez une nouvelle fenetre en tant qu'Administrateur et executez:
echo   configure-firewall-8443.bat
echo.
echo Ou faites un clic droit sur configure-firewall-8443.bat
echo et selectionnez "Executer en tant qu'administrateur"
echo.
pause

echo.
echo ============================================================
echo [SUCCESS] Configuration SSL terminee!
echo ============================================================
echo.
echo Recapitulatif:
echo   - Certificat SSL: src\main\resources\keystore.p12
echo   - Mot de passe: quiz-app-2025
echo   - Port HTTPS: 8443
echo   - Protocoles: TLSv1.2, TLSv1.3
echo.
echo N'OUBLIEZ PAS:
echo   1. Executer configure-firewall-8443.bat en Administrateur
echo   2. Demarrer l'application: start_clean.bat
echo   3. Acceder via: https://192.168.1.90:8443
echo.
echo NOTE: Le navigateur affichera un avertissement car le certificat
echo       est auto-signe. Cliquez sur "Avance" puis "Continuer".
echo.
pause

