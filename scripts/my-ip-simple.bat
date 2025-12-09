@echo off
:: Script simple pour obtenir votre adresse IP

echo.
echo === ADRESSE IP LOCALE ===
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /C:"Adresse IPv4"') do echo Adresse IP locale:%%a
echo.

echo === ADRESSE IP PUBLIQUE ===
powershell -Command "(Invoke-WebRequest -Uri 'https://api.ipify.org' -UseBasicParsing).Content"
echo.

pause

