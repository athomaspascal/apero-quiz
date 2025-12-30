@echo off
echo ============================================================
echo TEST: duckdns.org est-il bloque sur votre ordinateur?
echo ============================================================
echo.

echo 1. TEST DE RESOLUTION DNS
echo ==========================
echo Test de duckdns.org:
nslookup duckdns.org
echo.
echo Test de apero-quiz.duckdns.org:
nslookup apero-quiz.duckdns.org
echo.

echo 2. TEST DE PING
echo ===============
echo Ping vers duckdns.org:
ping duckdns.org -n 2
echo.

echo 3. VERIFICATION DU FICHIER HOSTS
echo =================================
echo Recherche de "duckdns" dans le fichier hosts:
findstr /i "duckdns" C:\Windows\System32\drivers\etc\hosts
if %ERRORLEVEL% NEQ 0 (
    echo [INFO] Aucune entree "duckdns" trouvee dans le fichier hosts
    echo        ^(Cela signifie qu'il n'est pas bloque localement^)
) else (
    echo [ATTENTION] Des entrees "duckdns" existent dans le fichier hosts!
    echo              Verifiez si elles bloquent le domaine.
)
echo.

echo 4. TEST DE CONNECTIVITE HTTPS
echo ==============================
echo Test de connexion au port 443 de duckdns.org:
powershell -Command "try { $result = Test-NetConnection -ComputerName 'duckdns.org' -Port 443 -WarningAction SilentlyContinue; if($result.TcpTestSucceeded) { Write-Host '[OK] Connexion reussie au port 443' -ForegroundColor Green } else { Write-Host '[ERREUR] Impossible de se connecter au port 443' -ForegroundColor Red } } catch { Write-Host '[ERREUR] Test echoue: ' $_.Exception.Message -ForegroundColor Red }"
echo.

echo 5. TEST DE NAVIGATION WEB
echo =========================
echo Tentative d'acces a https://www.duckdns.org:
powershell -Command "try { $response = Invoke-WebRequest -Uri 'https://www.duckdns.org' -TimeoutSec 10 -ErrorAction Stop; Write-Host '[OK] Site accessible - Code HTTP:' $response.StatusCode -ForegroundColor Green } catch { Write-Host '[ERREUR] Site inaccessible:' $_.Exception.Message -ForegroundColor Red }"
echo.

echo 6. VERIFICATION DU PARE-FEU WINDOWS
echo ====================================
echo Recherche de regles de pare-feu mentionnant "duckdns":
netsh advfirewall firewall show rule name=all | findstr /i "duckdns"
if %ERRORLEVEL% NEQ 0 (
    echo [INFO] Aucune regle de pare-feu specifique pour duckdns
    echo        ^(Pas de blocage au niveau du pare-feu Windows^)
) else (
    echo [ATTENTION] Des regles de pare-feu existent pour duckdns!
)
echo.

echo 7. CACHE DNS
echo ============
echo Contenu du cache DNS pour duckdns:
ipconfig /displaydns | findstr /i "duckdns"
if %ERRORLEVEL% NEQ 0 (
    echo [INFO] Aucune entree duckdns dans le cache DNS
)
echo.

echo 8. TEST AVEC VOTRE SOUS-DOMAINE SPECIFIQUE
echo ===========================================
echo Test de apero-quiz.duckdns.org sur le port 8443:
echo.
netstat -ano | findstr ":8443"
if %ERRORLEVEL% EQU 0 (
    echo [INFO] L'application ecoute sur le port 8443
    echo.
    echo Tentative de connexion a https://apero-quiz.duckdns.org:8443:
    powershell -Command "try { $response = Invoke-WebRequest -Uri 'https://apero-quiz.duckdns.org:8443' -SkipCertificateCheck -TimeoutSec 5 -ErrorAction Stop; Write-Host '[OK] Connexion reussie!' -ForegroundColor Green } catch { Write-Host '[ERREUR] Connexion echouee:' $_.Exception.Message -ForegroundColor Red }"
) else (
    echo [ATTENTION] L'application ne semble pas etre lancee sur le port 8443
    echo              Lancez l'application d'abord pour tester completement.
)
echo.

echo ============================================================
echo DIAGNOSTIC COMPLET
echo ============================================================
echo.
echo INTERPRETATION DES RESULTATS:
echo.
echo Si la resolution DNS echoue:
echo   ^> duckdns.org pourrait etre bloque par votre DNS ou FAI
echo.
echo Si le ping echoue mais DNS fonctionne:
echo   ^> Le serveur duckdns ne repond pas au ping (normal)
echo.
echo Si le fichier hosts contient duckdns:
echo   ^> Verifiez si l'entree bloque ou redirige le domaine
echo.
echo Si le port 443 n'est pas accessible:
echo   ^> Votre pare-feu ou antivirus bloque peut-etre duckdns
echo.
echo Si le site web n'est pas accessible:
echo   ^> duckdns.org est vraiment bloque sur votre ordinateur
echo.

echo ============================================================
echo SOLUTIONS POSSIBLES
echo ============================================================
echo.
echo SOLUTION 1: Utilisez localhost a la place
echo    Au lieu de: https://apero-quiz.duckdns.org:8443
echo    Utilisez:   https://localhost:8443
echo.
echo SOLUTION 2: Ajoutez une entree dans le fichier hosts
echo    1. Executez: add-duckdns-to-hosts.bat (en admin)
echo    2. Cela forcera la resolution vers 127.0.0.1
echo.
echo SOLUTION 3: Changez de serveur DNS
echo    1. Utilisez Google DNS: 8.8.8.8
echo    2. Ou Cloudflare DNS: 1.1.1.1
echo.
echo SOLUTION 4: Verifiez votre antivirus
echo    Certains antivirus bloquent les domaines DynDNS
echo    Ajoutez duckdns.org a la liste blanche
echo.
pause

