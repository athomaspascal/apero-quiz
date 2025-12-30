@echo off
setlocal enabledelayedexpansion

echo ============================================================
echo DIAGNOSTIC: "n'autorise pas la connexion"
echo ============================================================
echo.
echo Ce message signifie que Chrome ne peut pas se connecter
echo au serveur. Voici les verifications:
echo.

echo 1. VERIFICATION: L'application est-elle lancee?
echo ================================================
netstat -ano | findstr ":8443" > nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] L'application est EN COURS D'EXECUTION sur le port 8443
    echo.
    netstat -ano | findstr ":8443"
    echo.
    goto :check_firewall
) else (
    echo [ERREUR] L'APPLICATION N'EST PAS LANCEE!
    echo.
    echo ============================================================
    echo SOLUTION: Demarrez l'application
    echo ============================================================
    echo.
    echo Option 1: Via votre IDE (IntelliJ IDEA)
    echo    - Ouvrez le projet dans IntelliJ
    echo    - Executez la classe Application.java
    echo.
    echo Option 2: Via Maven
    echo    1. Ouvrez un terminal dans le projet
    echo    2. Tapez: mvn spring-boot:run
    echo.
    echo Une fois l'application demarree, vous verrez:
    echo    "Tomcat started on port(s): 8443 (https)"
    echo.
    echo Ensuite, retestez dans Chrome:
    echo    https://localhost:8443
    echo    OU
    echo    https://apero-quiz.duckdns.org:8443
    echo.
    goto :end
)

:check_firewall
echo 2. VERIFICATION: Configuration du pare-feu
echo ===========================================
netsh advfirewall firewall show rule name=all | findstr /C:"8443" > nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [INFO] Des regles de pare-feu existent pour le port 8443
) else (
    echo [ATTENTION] Aucune regle de pare-feu trouvee pour le port 8443
)
echo.

echo 3. VERIFICATION: Resolution DNS de apero-quiz.duckdns.org
echo ==========================================================
nslookup apero-quiz.duckdns.org > temp_dns.txt 2>&1
findstr /C:"127.0.0.1" temp_dns.txt > nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] Le domaine est resolu vers 127.0.0.1 (localhost)
) else (
    findstr /C:"Adresse" temp_dns.txt
    echo.
    echo [ATTENTION] Le domaine ne pointe pas vers localhost!
    echo.
    echo SOLUTION: Executez le script add-duckdns-to-hosts.bat
    echo           en tant qu'administrateur
)
del temp_dns.txt > nul 2>&1
echo.

echo 4. VERIFICATION: Fichier hosts
echo ===============================
findstr /C:"apero-quiz.duckdns.org" C:\Windows\System32\drivers\etc\hosts > nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] Entree trouvee dans le fichier hosts:
    findstr /C:"apero-quiz.duckdns.org" C:\Windows\System32\drivers\etc\hosts
) else (
    echo [ATTENTION] Aucune entree pour apero-quiz.duckdns.org dans hosts
    echo.
    echo RECOMMANDATION: Ajoutez cette ligne dans le fichier hosts:
    echo    127.0.0.1 apero-quiz.duckdns.org
    echo.
    echo Ou executez: add-duckdns-to-hosts.bat (en admin)
)
echo.

echo 5. TEST DE CONNEXION
echo ====================
echo Test de connexion a localhost:8443...
powershell -Command "try { $response = Invoke-WebRequest -Uri 'https://localhost:8443' -SkipCertificateCheck -TimeoutSec 5 -ErrorAction Stop; Write-Host '[OK] Connexion reussie!' -ForegroundColor Green } catch { Write-Host '[ERREUR] Connexion echouee: ' $_.Exception.Message -ForegroundColor Red }"
echo.

:end
echo ============================================================
echo RESUME
echo ============================================================
echo.
echo Si l'application n'est pas lancee:
echo   ^>^>^> DEMARREZ L'APPLICATION D'ABORD
echo.
echo Si l'application est lancee mais Chrome bloque:
echo   1. Utilisez: https://localhost:8443
echo   2. Si erreur de certificat: tapez 'thisisunsafe'
echo.
echo Pour utiliser apero-quiz.duckdns.org:
echo   1. Executez: add-duckdns-to-hosts.bat (en admin)
echo   2. Puis testez: https://apero-quiz.duckdns.org:8443
echo.
pause

