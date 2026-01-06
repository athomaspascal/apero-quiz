@echo off
echo ================================================
echo Test Duel Matchmaking - Analyse des logs
echo ================================================
echo.

set LOG_FILE=C:\Users\athom\IdeaProjects\quizz1\logs\application.log

echo Recherche des logs de Marie Curie...
echo ====================================
findstr /C:"Marie Curie" /C:"DUEL_POLLING" /C:"startPolling" /C:"startSearching" "%LOG_FILE%" > marie_curie_logs.txt
type marie_curie_logs.txt
echo.

echo Recherche des logs d'Isaac Newton...
echo =====================================
findstr /C:"Isaac Newton" /C:"DUEL_POLLING" /C:"startPolling" /C:"startSearching" "%LOG_FILE%" > isaac_newton_logs.txt
type isaac_newton_logs.txt
echo.

echo Recherche des changements de statut de duel...
echo ===============================================
findstr /C:"Duel status changed" /C:"Match found" /C:"creating new searching duel" "%LOG_FILE%" > duel_status_changes.txt
type duel_status_changes.txt
echo.

echo Recherche des logs de polling...
echo =================================
findstr /C:"startPolling() CALLED" /C:"Polling task started" /C:"DUEL_POLLING" "%LOG_FILE%" > polling_logs.txt
type polling_logs.txt
echo.

echo Recherche des erreurs...
echo ========================
findstr /C:"ERROR" /C:"EXECUTOR IS NULL" /C:"Exception" "%LOG_FILE%" > error_logs.txt
type error_logs.txt
echo.

echo ================================================
echo Analyse terminee. Fichiers generes:
echo - marie_curie_logs.txt
echo - isaac_newton_logs.txt
echo - duel_status_changes.txt
echo - polling_logs.txt
echo - error_logs.txt
echo ================================================
pause

