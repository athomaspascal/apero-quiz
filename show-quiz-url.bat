@echo off
chcp 65001 >nul
cls
color 0A
echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║     URL DE CONNEXION - APPLICATION QUIZ                ║
echo ╚════════════════════════════════════════════════════════╝
echo.
echo.

echo 📱 Depuis CET ordinateur :
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo    http://localhost:8080
echo.
echo.

echo 🌐 Depuis d'autres appareils (même réseau Wi-Fi) :
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /C:"Adresse IPv4"') do (
    set ip=%%a
    setlocal enabledelayedexpansion
    echo    http:!ip!:8080
    endlocal
)
echo.
echo.

echo 💡 ASTUCE :
echo    - Partagez cette URL avec les participants
echo    - Ils doivent être sur le même réseau Wi-Fi
echo    - Le serveur doit être démarré (port 8080)
echo.

echo ╔════════════════════════════════════════════════════════╗
echo ║  Appuyez sur une touche pour fermer...                ║
echo ╚════════════════════════════════════════════════════════╝
pause >nul

