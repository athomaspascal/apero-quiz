@echo off
echo ========================================
echo Starting Quiz Application
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

echo Step 3: Starting Spring Boot Application...
call mvn spring-boot:run

