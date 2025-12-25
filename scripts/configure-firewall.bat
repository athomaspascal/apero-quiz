@echo off
echo Adding firewall rule to allow incoming connections on port 8089...
netsh advfirewall firewall add rule name="Quizz App Inbound" dir=in action=allow protocol=TCP localport=8089
if %errorlevel% equ 0 (
    echo Firewall rule added successfully.
) else (
    echo Failed to add firewall rule. Please make sure you are running this script as an administrator.
)
pause

