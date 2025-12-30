@echo off
echo ============================================================
echo CORRECTION DE L'ACCES A apero-quiz.duckdns.org
echo ============================================================
echo.

echo 1. DIAGNOSTIC DU PROBLEME
echo --------------------------
echo.

echo A) Test de resolution DNS:
echo --------------------------
nslookup apero-quiz.duckdns.org
echo.

echo B) Test de ping:
echo ----------------
ping apero-quiz.duckdns.org -n 2
echo.

echo C) Verification du fichier hosts:
echo ----------------------------------
findstr /C:"apero-quiz" C:\Windows\System32\drivers\etc\hosts
if %ERRORLEVEL% NEQ 0 (
    echo Aucune entree pour apero-quiz dans le fichier hosts
) else (
    echo Entree trouvee dans le fichier hosts
)
echo.

echo 2. SOLUTION 1: Vider le cache DNS
echo ----------------------------------
echo Vidage du cache DNS...
ipconfig /flushdns
echo.

echo 3. SOLUTION 2: Ajouter une entree dans le fichier hosts
echo --------------------------------------------------------
echo.
echo Pour forcer la resolution locale de apero-quiz.duckdns.org,
echo nous devons ajouter une entree dans le fichier hosts.
echo.
echo ATTENTION: Ceci necessite les droits administrateur!
echo.
echo Voulez-vous ajouter l'entree dans le fichier hosts? (O/N)
set /p RESPONSE=Votre choix:
if /I "%RESPONSE%"=="O" (
    echo.
    echo Ajout de l'entree dans le fichier hosts...
    echo 127.0.0.1 apero-quiz.duckdns.org >> C:\Windows\System32\drivers\etc\hosts
    if %ERRORLEVEL% EQU 0 (
        echo [OK] Entree ajoutee avec succes!
        echo.
        echo Le fichier hosts contient maintenant:
        type C:\Windows\System32\drivers\etc\hosts | findstr /C:"apero-quiz"
    ) else (
        echo [ERREUR] Impossible d'ajouter l'entree.
        echo Veuillez executer ce script en tant qu'administrateur!
        echo.
        echo OU ajoutez manuellement cette ligne dans:
        echo C:\Windows\System32\drivers\etc\hosts
        echo.
        echo 127.0.0.1 apero-quiz.duckdns.org
    )
) else (
    echo.
    echo Operation annulee.
    echo.
    echo Pour ajouter manuellement, editez le fichier:
    echo C:\Windows\System32\drivers\etc\hosts
    echo.
    echo Et ajoutez cette ligne:
    echo 127.0.0.1 apero-quiz.duckdns.org
)
echo.

echo 4. SOLUTION 3: Utiliser localhost a la place
echo ---------------------------------------------
echo.
echo Au lieu de: https://apero-quiz.duckdns.org:8443
echo Utilisez:   https://localhost:8443
echo.
echo Ces deux URLs pointent vers votre ordinateur local.
echo.

echo 5. VERIFICATION DES REGLES DE PARE-FEU
echo ---------------------------------------
echo.
echo Verification des regles de pare-feu Windows pour le port 8443...
netsh advfirewall firewall show rule name=all | findstr /C:"8443"
echo.

echo 6. TEST DE CONNEXION
echo --------------------
echo Test de connexion au port 8443...
netstat -ano | findstr ":8443"
if %ERRORLEVEL% EQU 0 (
    echo [OK] L'application ecoute sur le port 8443
) else (
    echo [ATTENTION] L'application ne semble pas etre en cours d'execution!
)
echo.

echo 7. PROBLEMES POSSIBLES ET SOLUTIONS
echo ------------------------------------
echo.
echo PROBLEME 1: Le domaine DuckDNS pointe vers une IP externe
echo Solution: Ajoutez 127.0.0.1 apero-quiz.duckdns.org dans le fichier hosts
echo.
echo PROBLEME 2: Le pare-feu Windows bloque le domaine
echo Solution: Ajoutez une exception dans le pare-feu Windows
echo.
echo PROBLEME 3: Le navigateur a mis en cache une erreur
echo Solution: Videz le cache du navigateur (Ctrl+Shift+Del)
echo           Ou utilisez le mode navigation privee (Ctrl+Shift+N)
echo.
echo PROBLEME 4: Le certificat SSL est pour "localhost" et non pour le domaine
echo Solution: Utilisez https://localhost:8443 a la place
echo.

echo ============================================================
echo RESUME DES URLS A TESTER
echo ============================================================
echo.
echo 1. https://localhost:8443               (RECOMMANDE)
echo 2. https://127.0.0.1:8443               (Alternative)
echo 3. https://apero-quiz.duckdns.org:8443  (Si hosts configure)
echo.

echo ============================================================
echo FIN DU DIAGNOSTIC
echo ============================================================
echo.
pause

