@echo off
echo Applying database migration: add selected_question_ids to duel_match table...

REM Path to H2 jar (adjust if needed)
set H2_JAR=C:\Users\%USERNAME%\.m2\repository\com\h2database\h2\2.2.224\h2-2.2.224.jar

REM Database URL (adjust if needed)
set DB_URL=jdbc:h2:tcp://localhost:9092/./data/quizdb

REM Username and password (adjust if needed)
set DB_USER=sa
set DB_PASSWORD=

REM Apply migration
java -cp "%H2_JAR%" org.h2.tools.RunScript -url "%DB_URL%" -user "%DB_USER%" -password "%DB_PASSWORD%" -script "add-selected-questions-to-duel.sql"

if %ERRORLEVEL% EQU 0 (
    echo Migration applied successfully!
) else (
    echo Error applying migration. Error code: %ERRORLEVEL%
)

pause

