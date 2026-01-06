@echo off
echo ============================================================
echo Test de Demarrage Optimise - Quiz Application
echo ============================================================
echo.

REM Afficher l'heure de debut
echo [%time%] Demarrage de l'application...
echo.

REM Demarrer l'application Spring Boot
cd C:\Users\athom\IdeaProjects\quizz1
call mvn spring-boot:run

echo.
echo [%time%] Application terminee
echo ============================================================

