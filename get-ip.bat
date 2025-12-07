@echo off
echo ========================================
echo     INFORMATIONS ADRESSE IP
echo ========================================
echo.

echo [1] Adresse IP locale (interne) :
echo ----------------------------------------
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /C:"IPv4"') do echo %%a
echo.

echo [2] Toutes les informations réseau :
echo ----------------------------------------
ipconfig | findstr /C:"IPv4" /C:"Masque" /C:"Passerelle"
echo.

echo [3] Adresse IP publique (externe) :
echo ----------------------------------------
curl -s ifconfig.me
echo.
echo.

echo [4] Détails complets de la configuration réseau :
echo ----------------------------------------
ipconfig /all | findstr /C:"IPv4" /C:"Carte" /C:"DNS"
echo.

pause

