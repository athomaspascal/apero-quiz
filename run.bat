@echo off
echo ========================================
echo Demarrage de l'application Quiz
echo ========================================
echo.

REM Configuration du JDK
set "JAVA_HOME=C:\Users\athom\.jdks\azul-23.0.2"
set "PATH=%JAVA_HOME%\bin;%PATH%"

REM Verification Java
echo Verification de Java...
"%JAVA_HOME%\bin\java.exe" -version
if errorlevel 1 (
    echo ERREUR: Java non trouve!
    pause
    exit /b 1
)

echo.
echo Demarrage de l'application...
echo L'application sera accessible sur http://localhost:8080
echo.
echo Veuillez patienter pendant le demarrage...
echo.

REM Demarrage de l'application
"%~dp0mvnw.cmd" spring-boot:run

if errorlevel 1 (
    echo.
    echo ERREUR lors du demarrage de l'application!
    pause
)

