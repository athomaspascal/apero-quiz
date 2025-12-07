@echo off
REM Check Java version and provide instructions

echo ================================
echo Java Version Check
echo ================================
echo.

java -version 2>&1 | findstr /i "version" > temp_java_version.txt
set /p JAVA_VERSION_LINE=<temp_java_version.txt
del temp_java_version.txt

echo Current Java version:
java -version
echo.

REM Extract major version number
for /f "tokens=3" %%a in ('java -version 2^>^&1 ^| findstr /i "version"') do (
    set JAVA_VER=%%a
)

REM Remove quotes
set JAVA_VER=%JAVA_VER:"=%

REM Get major version (first number)
for /f "tokens=1 delims=." %%a in ("%JAVA_VER%") do set MAJOR_VER=%%a

echo.
echo ================================
echo Required: Java 17 or higher
echo ================================
echo.

if %MAJOR_VER% GEQ 17 (
    echo [OK] Java version is compatible!
    echo You can proceed with running the application.
    echo.
    echo To start the application, run:
    echo   mvn clean install
    echo   mvn spring-boot:run
) else (
    echo [WARNING] Java version is too old!
    echo.
    echo This project requires Java 17 or higher.
    echo Current version: %JAVA_VER%
    echo.
    echo ================================
    echo Installation Instructions
    echo ================================
    echo.
    echo 1. Download Java 21 from:
    echo    https://www.oracle.com/java/technologies/downloads/#java21
    echo    or
    echo    https://adoptium.net/temurin/releases/?version=21
    echo.
    echo 2. Install Java 21
    echo.
    echo 3. Set JAVA_HOME environment variable:
    echo    setx JAVA_HOME "C:\Program Files\Java\jdk-21"
    echo.
    echo 4. Update PATH:
    echo    setx PATH "%%JAVA_HOME%%\bin;%%PATH%%"
    echo.
    echo 5. Restart your terminal and IDE
    echo.
    echo 6. Verify installation:
    echo    java -version
)

echo.
echo Press any key to exit...
pause >nul

