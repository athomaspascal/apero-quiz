@echo off
chcp 65001 >nul
cls
echo ========================================
echo     MES ADRESSES IP
echo ========================================
echo.

echo 🌐 Adresse IP locale (Wi-Fi) :
echo -----------------------------------
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /C:"Adresse IPv4"') do (
    set ip=%%a
    setlocal enabledelayedexpansion
    echo !ip!
    endlocal
)
echo.

echo 🌍 Adresse IP publique (Internet) :
echo -----------------------------------
powershell -Command "try { (Invoke-WebRequest -Uri 'https://api.ipify.org' -UseBasicParsing -TimeoutSec 5).Content } catch { Write-Host 'Erreur de connexion' }"
echo.

echo 📋 Résumé des connexions réseau :
echo -----------------------------------
ipconfig | findstr /C:"Carte" /C:"Adresse IPv4"
echo.

echo ========================================
echo.
pause

