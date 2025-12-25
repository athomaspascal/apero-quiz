@echo off
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| find "IPv4"') do (
    for /f "tokens=*" %%b in ("%%a") do echo Your IP address is: %%b
)
pause

