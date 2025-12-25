@echo off
echo Enabling Windows Firewall for all profiles...
netsh advfirewall set allprofiles state on
echo.
echo Firewall has been enabled.
pause

