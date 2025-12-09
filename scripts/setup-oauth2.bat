@echo off
REM OAuth2 Setup Helper Script
REM This script helps you configure OAuth2 authentication

echo ========================================
echo OAuth2 Setup Helper
echo ========================================
echo.

REM Check Java version first
echo [1/4] Checking Java version...
java -version 2>&1 | findstr /i "version" > temp_version.txt
for /f "tokens=3" %%a in ('java -version 2^>^&1 ^| findstr /i "version"') do set JAVA_VER=%%a
set JAVA_VER=%JAVA_VER:"=%
for /f "tokens=1 delims=." %%a in ("%JAVA_VER%") do set MAJOR_VER=%%a

if %MAJOR_VER% LSS 17 (
    echo [ERROR] Java version is too old: %JAVA_VER%
    echo.
    echo OAuth2 requires Java 17 or higher.
    echo Please install Java 21 first.
    echo.
    echo Run: check-java.bat
    echo.
    pause
    exit /b 1
)

echo [OK] Java version: %JAVA_VER%
echo.

REM Step 2: Create VaadinSecurityConfig
echo [2/4] Creating VaadinSecurityConfig...
if exist "VaadinSecurityConfig.java.template" (
    if not exist "src\main\java\com\quizz\examplefeature\security\VaadinSecurityConfig.java" (
        copy "VaadinSecurityConfig.java.template" "src\main\java\com\quizz\examplefeature\security\VaadinSecurityConfig.java" >nul 2>&1
        echo [OK] VaadinSecurityConfig.java created
    ) else (
        echo [SKIP] VaadinSecurityConfig.java already exists
    )
) else (
    echo [WARNING] Template file not found
)
echo.

REM Step 3: Check application.properties
echo [3/4] Checking application.properties...
findstr /C:"YOUR_GOOGLE_CLIENT_ID" "src\main\resources\application.properties" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [WARNING] OAuth2 credentials not configured yet
    echo.
    echo Please edit src\main\resources\application.properties
    echo and replace:
    echo   - YOUR_GOOGLE_CLIENT_ID
    echo   - YOUR_GOOGLE_CLIENT_SECRET
    echo   - YOUR_FACEBOOK_CLIENT_ID
    echo   - YOUR_FACEBOOK_CLIENT_SECRET
    echo   - YOUR_LINKEDIN_CLIENT_ID
    echo   - YOUR_LINKEDIN_CLIENT_SECRET
    echo.
    echo See OAUTH2_QUICK_START.md for instructions.
    echo.
) else (
    echo [OK] OAuth2 credentials appear to be configured
)
echo.

REM Step 4: Try to compile
echo [4/4] Testing compilation...
echo This may take a few minutes...
echo.

mvn clean compile -q -DskipTests >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] Project compiled successfully!
    echo.
    echo ========================================
    echo Setup Complete!
    echo ========================================
    echo.
    echo Next steps:
    echo 1. Configure OAuth2 credentials in application.properties
    echo 2. Run: mvn spring-boot:run
    echo 3. Open: http://localhost:8080
    echo.
    echo For detailed instructions, see:
    echo   - NEXT_STEPS.md
    echo   - OAUTH2_QUICK_START.md
    echo.
) else (
    echo [ERROR] Compilation failed
    echo.
    echo Please check:
    echo 1. Java version (must be 17+)
    echo 2. Maven is installed
    echo 3. No syntax errors in code
    echo.
    echo Run: mvn clean install
    echo to see detailed error messages.
    echo.
)

pause

