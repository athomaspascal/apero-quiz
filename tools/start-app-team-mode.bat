@echo off
REM Script de démarrage de l'application Quiz avec Mode Équipe

echo ========================================
echo   Application Quiz - Mode Equipe
echo ========================================
echo.

cd /d C:\Users\athom\IdeaProjects\quizz1

echo [1/3] Compilation du projet...
call mvn clean compile
if %ERRORLEVEL% NEQ 0 (
    echo ERREUR : La compilation a echoue !
    pause
    exit /b 1
)
echo.

echo [2/3] Build du frontend Vaadin...
call mvn vaadin:build-frontend
if %ERRORLEVEL% NEQ 0 (
    echo ERREUR : Le build frontend a echoue !
    pause
    exit /b 1
)
echo.

echo [3/3] Demarrage de l'application...
echo.
echo L'application sera disponible sur :
echo   - https://localhost:8089
echo   - https://apero-quiz.duckdns.org:8089
echo.
echo Pour tester le mode equipe :
echo   1. Creer une session de quiz
echo   2. Cocher "Activer le mode equipe"
echo   3. Selectionner les equipes (Stark, Lannister, Targaryen, etc.)
echo   4. Inviter des joueurs avec le code de session
echo   5. Demarrer pour tout le monde
echo   6. Chaque joueur selectionne son equipe
echo   7. Voir le classement par equipe a la fin
echo.
echo Appuyez sur Ctrl+C pour arreter l'application
echo.

call mvn spring-boot:run

pause

