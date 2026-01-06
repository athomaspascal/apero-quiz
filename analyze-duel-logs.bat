@echo off
echo ========================================
echo ANALYSE DES LOGS - Duel Quiz
echo ========================================
echo.

cd /d C:\Users\athom\IdeaProjects\quizz1\logs

REM Chercher les logs de navigation
echo [1] Logs de navigation vers le quiz duel:
echo ========================================
powershell "Get-Content application.log | Select-String 'NAVIGATING TO DUEL QUIZ'"
echo.

REM Chercher les logs de beforeEnter
echo [2] Logs de beforeEnter (QuizQuestionView):
echo ========================================
powershell "Get-Content application.log | Select-String 'QuizQuestionView.beforeEnter'"
echo.

REM Chercher les logs de Darwin
echo [3] Logs de Charles Darwin:
echo ========================================
powershell "Get-Content application.log | Select-String 'Darwin'"
echo.

REM Chercher les logs de Mandela
echo [4] Logs de Nelson Mandela:
echo ========================================
powershell "Get-Content application.log | Select-String 'Mandela'"
echo.

REM Chercher les logs de duel
echo [5] Logs de creation/match de duel:
echo ========================================
powershell "Get-Content application.log | Select-String 'DUEL MODE|duel.*match|Starting countdown'"
echo.

REM Chercher les erreurs
echo [6] Erreurs detectees:
echo ========================================
powershell "Get-Content application.log | Select-String 'ERROR|Exception' -Context 2"
echo.

echo ========================================
echo Analyse terminee
echo ========================================
echo.
echo Fichier log complet: %cd%\application.log
echo.
pause

