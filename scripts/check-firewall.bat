@echo off
echo Checking firewall rule "Quizz App Inbound"...
netsh advfirewall firewall show rule name="Quizz App Inbound"
echo.
echo If the rule is enabled, you should see 'Enabled: Yes' in the output above.
echo Make sure the application is running and listening on port 8089.
pause

