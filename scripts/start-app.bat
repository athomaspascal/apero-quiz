@echo off
REM Script pour démarrer l'application avec le JDK embarqué d'IntelliJ

echo Configuration du JDK...
set JAVA_HOME=C:\Users\athom\.jdks\azul-23.0.2
set PATH=%JAVA_HOME%\bin;%PATH%

echo Vérification de la version Java...
java -version

echo.
echo Démarrage de l'application Spring Boot...
echo.

cd /d "%~dp0"
call mvnw.cmd spring-boot:run

pause

