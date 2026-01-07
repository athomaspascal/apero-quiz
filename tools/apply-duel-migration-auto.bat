@echo off
echo ================================================
echo Application de la migration SQL pour duel_match
echo ================================================
echo.
echo Cette migration ajoute le champ cancelled_by_user_id
echo pour tracker qui a quitte un duel.
echo.

REM Verifier si le serveur H2 est demarre
echo Tentative de connexion a la base de donnees H2...
echo.

REM Construire le classpath avec les JARs H2
set H2_JAR=%USERPROFILE%\.m2\repository\com\h2database\h2\2.3.232\h2-2.3.232.jar
if not exist "%H2_JAR%" (
    echo ERREUR: Le JAR H2 n'a pas ete trouve !
    echo Chemin attendu: %H2_JAR%
    echo.
    echo Veuillez compiler le projet d'abord avec: mvn compile
    exit /b 1
)

echo JAR H2 trouve: %H2_JAR%
echo.

REM Executer le script SQL
echo Execution du script SQL...
java -cp "%H2_JAR%" org.h2.tools.RunScript -url "jdbc:h2:file:./data/quizdb" -user "sa" -password "" -script "SQL/add_cancelled_by_to_duel_match.sql" -showResults

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ================================================
    echo Migration appliquee avec succes !
    echo ================================================
    echo.
    echo Vous pouvez maintenant demarrer l'application.
    echo.
) else (
    echo.
    echo ================================================
    echo ERREUR lors de l'application de la migration
    echo ================================================
    echo.
    echo Verifiez que :
    echo 1. La base de donnees n'est pas verrouillee
    echo 2. L'application n'est pas en cours d'execution
    echo 3. Le fichier SQL est correct
    echo.
)

exit /b %ERRORLEVEL%

