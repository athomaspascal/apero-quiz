@echo off
echo ========================================
echo   Redemarrage de l'application Quiz
echo   avec migration automatique des pays
echo ========================================
echo.
echo IMPORTANT: La migration UserCountryMigration va s'executer
echo Elle va lier automatiquement les utilisateurs aux pays
echo.
echo Appuyez sur une touche pour continuer...
pause >nul
echo.
echo Demarrage de l'application...
echo.

cd /d "%~dp0"
call mvn spring-boot:run

pause

