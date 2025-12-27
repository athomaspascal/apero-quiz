@echo off
echo ========================================
echo Recompiling Quiz Application
echo ========================================
echo.

echo Step 1: Maven Clean...
call mvn clean
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Maven clean failed!
    pause
    exit /b 1
)
echo.

echo Step 2: Building Vaadin Frontend...
call mvn vaadin:build-frontend
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Vaadin build-frontend failed!
    pause
    exit /b 1
)
echo.

echo Step 3: Compiling...
call mvn compile
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Maven compile failed!
    pause
    exit /b 1
)
echo.

echo ========================================
echo Build completed successfully!
echo You can now run the application with:
echo   mvn spring-boot:run
echo Or use: run-app.bat
echo ========================================
pause

