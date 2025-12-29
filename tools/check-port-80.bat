@echo off
REM ============================================================
REM   VERIFICATION PORT 80 - Let's Encrypt
REM ============================================================

echo.
echo ============================================================
echo   VERIFICATION PORT 80 POUR LET'S ENCRYPT
echo ============================================================
echo.

echo [ETAPE 1] Verification pare-feu Windows pour port 80...
echo.

netsh advfirewall firewall show rule name="HTTP Port 80" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Regle pare-feu pour port 80 non trouvee
    echo [ACTION] Creation de la regle...
    netsh advfirewall firewall add rule name="HTTP Port 80" dir=in action=allow protocol=TCP localport=80
    if errorlevel 1 (
        echo [ERREUR] Impossible de creer la regle. Executez en tant qu'administrateur!
        pause
        exit /b 1
    )
    echo [OK] Regle pare-feu creee pour port 80
) else (
    echo [OK] Regle pare-feu existante pour port 80
)

echo.
echo [ETAPE 2] Test d'ecoute sur port 80...
echo.

netstat -an | findstr ":80 " | findstr "LISTENING"
if errorlevel 1 (
    echo [INFO] Aucun service n'ecoute sur le port 80
    echo [OK] Port 80 disponible pour Certbot
) else (
    echo [ATTENTION] Un service ecoute deja sur le port 80!
    echo.
    netstat -ano | findstr ":80 " | findstr "LISTENING"
    echo.
    echo [ACTION] Vous devez arreter ce service avant d'executer Certbot
    echo          OU utiliser le mode --webroot au lieu de --standalone
)

echo.
echo [ETAPE 3] Verification IP publique et DuckDNS...
echo.

echo Votre IP publique :
curl -s https://api.ipify.org
echo.
echo.

echo Resolution DNS de apero-quiz.duckdns.org :
nslookup apero-quiz.duckdns.org
echo.

echo [ETAPE 4] Instructions pour configurer votre routeur...
echo.
echo IMPORTANT : Vous devez configurer votre routeur/box Internet
echo.
echo 1. Connectez-vous a votre routeur (ex: 192.168.1.1)
echo 2. Cherchez "Redirection de port" ou "Port Forwarding"
echo 3. Ajoutez une regle :
echo    - Port externe : 80
echo    - Port interne : 80
echo    - IP locale : 192.168.x.x (votre PC)
echo    - Protocole : TCP
echo.
echo 4. Activez la regle et sauvegardez
echo.

echo [ETAPE 5] Test depuis Internet...
echo.
echo Une fois le port 80 ouvert sur le routeur, testez depuis :
echo https://www.yougetsignal.com/tools/open-ports/
echo.
echo Port a tester : 80
echo IP : Votre IP publique affichee ci-dessus
echo.

pause

