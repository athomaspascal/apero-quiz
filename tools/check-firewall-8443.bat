@echo off
chcp 65001 >nul
echo ============================================================
echo   VERIFICATION PARE-FEU - PORT 8443 (HTTPS)
echo ============================================================
echo.

echo Vérification des règles du pare-feu pour le port 8443...
echo.

netsh advfirewall firewall show rule name=all | findstr /C:"8443" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Des règles existent pour le port 8443
    echo.
    echo Détails des règles:
    echo -------------------
    netsh advfirewall firewall show rule name=all | findstr /C:"8443"
    echo.
) else (
    echo ✗ Aucune règle trouvée pour le port 8443
    echo.
    echo Voulez-vous ajouter une règle maintenant ? (O/N)
    set /p CHOICE="> "
    if /i "%CHOICE%"=="O" (
        echo.
        echo Ajout de la règle...
        netsh advfirewall firewall add rule name="Quiz App HTTPS" dir=in action=allow protocol=TCP localport=8443
        echo ✓ Règle ajoutée avec succès
    )
)

echo.
echo Test de connexion sur le port 8443...
netstat -an | findstr ":8443" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ L'application écoute sur le port 8443
    netstat -an | findstr ":8443"
) else (
    echo ✗ Aucune application n'écoute sur le port 8443
    echo   → L'application n'est peut-être pas démarrée
)

echo.
echo ============================================================
pause

