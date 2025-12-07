@echo off
setlocal

echo ==============================================
echo Configuration Java 21 pour Quizz Application
echo ==============================================
echo.

REM Set JAVA_HOME to Azul Java 21
set "JAVA_HOME=C:\Users\athom\.jdks\azul-21.0.9"
set "PATH=%JAVA_HOME%\bin;%PATH%"

echo JAVA_HOME: %JAVA_HOME%
echo PATH: %PATH%
echo.

REM Verify Java version
echo Verification de la version Java...
"%JAVA_HOME%\bin\java.exe" -version
if errorlevel 1 (
    echo ERREUR: Java 21 n'est pas accessible
    pause
    exit /b 1
)
echo.

echo ==============================================
echo Compilation et demarrage de l'application...
echo ==============================================
echo.

REM Clean and start the application using Maven wrapper
call "%~dp0mvnw.cmd" clean spring-boot:run

if errorlevel 1 (
    echo.
    echo ERREUR: Le build a echoue
    pause
    exit /b 1
)

endlocal
pause

