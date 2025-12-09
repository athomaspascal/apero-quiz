@echo off
setlocal

echo ==============================================
echo Compilation avec Java 21
echo ==============================================
echo.

REM Set JAVA_HOME to Azul Java 21
set "JAVA_HOME=C:\Users\athom\.jdks\azul-21.0.9"
set "PATH=%JAVA_HOME%\bin;%PATH%"

echo JAVA_HOME: %JAVA_HOME%
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
echo Compilation du projet...
echo ==============================================
echo.

REM Compile the project
call "%~dp0mvnw.cmd" clean compile -DskipTests

if errorlevel 1 (
    echo.
    echo ERREUR: La compilation a echoue
    pause
    exit /b 1
) else (
    echo.
    echo SUCCESS: Compilation reussie!
)

endlocal
pause

