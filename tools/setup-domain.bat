@echo off
echo ============================================================
echo   CONFIGURATION COMPLETE apero-quiz.com
echo ============================================================
echo.
echo Ce script va configurer votre application pour utiliser:
echo   https://apero-quiz.com:8443
echo.
echo Au lieu de:
echo   https://192.168.1.90:8443
echo.
echo Etapes:
echo   1. Generer certificat SSL pour apero-quiz.com
echo   2. Configurer le fichier hosts (DNS local)
echo   3. Configurer le pare-feu pour HTTPS
echo   4. Mettre a jour application.properties
echo.
pause

echo.
echo ============================================================
echo ETAPE 1/4 : Generation certificat SSL pour apero-quiz.com
echo ============================================================
echo.
call generate-ssl-cert-domain.bat
if errorlevel 1 (
    echo [ERREUR] Echec generation certificat
    pause
    exit /b 1
)

echo.
echo ============================================================
echo ETAPE 2/4 : Configuration DNS local (hosts file)
echo ============================================================
echo.
echo IMPORTANT: L'etape suivante necessite des droits Administrateur
echo.
echo Faites un clic droit sur configure-hosts-domain.bat
echo et selectionnez "Executer en tant qu'administrateur"
echo.
echo Ou appuyez sur une touche pour essayer maintenant...
pause
echo.
call configure-hosts-domain.bat
if errorlevel 1 (
    echo [ATTENTION] Configuration hosts file echouee
    echo Executez manuellement configure-hosts-domain.bat en tant qu'Admin
    pause
)

echo.
echo ============================================================
echo ETAPE 3/4 : Configuration pare-feu HTTPS
echo ============================================================
echo.
echo Verification si le port 8443 est deja autorise...
netsh advfirewall firewall show rule name="Quiz App - HTTPS 8443" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Port 8443 non configure
    echo.
    echo Faites un clic droit sur configure-firewall-8443.bat
    echo et selectionnez "Executer en tant qu'administrateur"
    echo.
    pause
) else (
    echo [OK] Port 8443 deja autorise dans le pare-feu
)

echo.
echo ============================================================
echo ETAPE 4/4 : Configuration application.properties
echo ============================================================
echo.
echo Mise a jour de server.address pour accepter toutes les connexions...
python -c "import fileinput; [print(line.replace('server.address=192.168.1.90', 'server.address=0.0.0.0') if 'server.address' in line and not line.strip().startswith('#') else line, end='') for line in open('src/main/resources/application.properties', 'r', encoding='utf-8')]; exit(0)" > temp.properties 2>nul
if exist temp.properties (
    move /Y temp.properties src\main\resources\application.properties >nul
    echo [OK] application.properties mis a jour
) else (
    echo [INFO] Mise a jour manuelle requise
    echo Modifiez src\main\resources\application.properties:
    echo   Changez: server.address=192.168.1.90
    echo   En:      server.address=0.0.0.0
)
echo.

echo.
echo ============================================================
echo [SUCCESS] Configuration apero-quiz.com terminee!
echo ============================================================
echo.
echo Recapitulatif:
echo   - Domaine: apero-quiz.com
echo   - Certificat SSL: src\main\resources\keystore.p12
echo   - DNS local: 192.168.1.90 ^-^> apero-quiz.com
echo   - Port HTTPS: 8443
echo   - Protocoles: TLSv1.2, TLSv1.3
echo.
echo URLS d'acces:
echo   - Principal: https://apero-quiz.com:8443
echo   - Alternatif: https://www.apero-quiz.com:8443
echo   - IP locale:  https://192.168.1.90:8443
echo.
echo Prochaines etapes:
echo   1. Demarrer l'application: start_clean.bat
echo   2. Ouvrir le navigateur: https://apero-quiz.com:8443
echo   3. Accepter le certificat auto-signe (clic sur "Avance")
echo.
echo Pour les autres PC du reseau:
echo   - Executez configure-hosts-domain.bat en Admin sur chaque PC
echo   - Ou configurez le DNS dans votre routeur
echo.
echo NOTE: Le certificat est auto-signe, le navigateur affichera
echo       un avertissement de securite. C'est normal.
echo.
echo Pour un certificat valide (production):
echo   - Achetez le domaine apero-quiz.com (~10 euros/an)
echo   - Utilisez Let's Encrypt (certificat gratuit)
echo   - Voir: MD\DOMAIN_CONFIGURATION.md
echo.
pause

