@echo off
echo ============================================================
echo Verification du pare-feu pour l'application Quiz (Port 8443)
echo ============================================================
echo.

echo 1. Etat du pare-feu Windows:
echo ----------------------------
netsh advfirewall show allprofiles state
echo.

echo 2. Regle de pare-feu pour le port 8443:
echo ---------------------------------------
netsh advfirewall firewall show rule name="Quiz App - HTTPS 8443" verbose
echo.

echo 3. Test d'ecoute sur le port 8443:
echo ----------------------------------
netstat -an | findstr ":8443"
echo.

echo 4. Adresses IP de la machine:
echo ----------------------------
ipconfig | findstr /C:"IPv4"
echo.

echo 5. Status du pare-feu - Resume:
echo -------------------------------
for /f "tokens=1,2 delims=:" %%a in ('netsh advfirewall show allprofiles ^| findstr /C:"tat"') do (
    echo %%a: %%b
)
echo.

echo 6. Verification de la connectivite externe:
echo ------------------------------------------
echo Pour tester depuis l'exterieur, utilisez:
echo   https://apero-quiz.duckdns.org:8443
echo   ou depuis votre smartphone connecte au meme reseau:
echo   https://[VOTRE_IP]:8443
echo.

echo ============================================================
echo Verification terminee
echo ============================================================
pause

