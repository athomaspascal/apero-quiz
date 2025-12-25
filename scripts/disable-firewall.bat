@echo off
echo Disabling Windows Firewall for all profiles...
netsh advfirewall set allprofiles state off
echo.
echo Firewall has been disabled.
echo IMPORTANT: Remember to re-enable it after your test.
pause

