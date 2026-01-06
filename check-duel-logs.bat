@echo off
REM ========================================================
REM Script de Vérification des Logs - Duel Quiz
REM Date: 2026-01-06
REM ========================================================

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║  VÉRIFICATION DES LOGS - Duel Quiz                        ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

set LOG_FILE=logs\application.log

if not exist "%LOG_FILE%" (
    echo ✗ Fichier de log introuvable: %LOG_FILE%
    pause
    exit /b 1
)

echo [1] Vérification de l'erreur index.html...
findstr /C:"Cannot get the 'index.html'" "%LOG_FILE%" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo     ✗ ERREUR: index.html manquant détectée !
    echo     → Solution: Exécuter rebuild-and-run-duel-fix.bat
    set HAS_ERROR=1
) else (
    echo     ✓ Aucune erreur index.html
)
echo.

echo [2] Vérification des accès à DuelQuizView...
findstr /C:"DuelQuizView" "%LOG_FILE%" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo     ✓ DuelQuizView a été accédé
    echo.
    echo     Dernières entrées DuelQuizView:
    findstr /C:"DuelQuizView" "%LOG_FILE%" | powershell -Command "$input | Select-Object -Last 5"
) else (
    echo     ✗ AUCUN accès à DuelQuizView détecté
    echo     → Possible cause: Menu Duel Quiz non cliqué ou route non enregistrée
    set HAS_ERROR=1
)
echo.

echo [3] Vérification de la navigation vers le quiz...
findstr /C:"Navigating to quiz" "%LOG_FILE%" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo     ✓ Navigation vers le quiz détectée
    echo.
    echo     Dernières navigations:
    findstr /C:"Navigating to quiz" "%LOG_FILE%" | powershell -Command "$input | Select-Object -Last 3"
) else (
    echo     ⚠ Aucune navigation vers le quiz détectée
)
echo.

echo [4] Vérification du mode DUEL dans QuizQuestionView...
findstr /C:"DUEL MODE DETECTED" "%LOG_FILE%" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo     ✓ Mode DUEL détecté dans QuizQuestionView
    echo.
    echo     Dernières détections:
    findstr /C:"DUEL MODE DETECTED" "%LOG_FILE%" | powershell -Command "$input | Select-Object -Last 3"
) else (
    echo     ✗ AUCUN mode DUEL détecté dans QuizQuestionView
    echo     → Cause: QuizQuestionView n'est pas instancié après la navigation
    set HAS_ERROR=1
)
echo.

echo [5] Vérification de l'affichage des questions...
findstr /C:"displayQuestion()" "%LOG_FILE%" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo     ✓ Questions affichées
    echo.
    echo     Dernières questions affichées:
    findstr /C:"displayQuestion()" "%LOG_FILE%" | powershell -Command "$input | Select-Object -Last 3"
) else (
    echo     ⚠ Aucune question affichée détectée
)
echo.

echo [6] Vérification des connexions utilisateurs...
findstr /C:"Recorded LOGIN for user" "%LOG_FILE%" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo     ✓ Connexions utilisateurs détectées
    echo.
    echo     Dernières connexions:
    findstr /C:"Recorded LOGIN for user" "%LOG_FILE%" | powershell -Command "$input | Select-Object -Last 5"
) else (
    echo     ⚠ Aucune connexion utilisateur récente
)
echo.

echo ═══════════════════════════════════════════════════════════
echo.
if defined HAS_ERROR (
    echo ❌ DIAGNOSTIC: Problèmes détectés !
    echo.
    echo 📋 PLAN D'ACTION RECOMMANDÉ:
    echo    1. Exécuter: rebuild-and-run-duel-fix.bat
    echo    2. Attendre le message "Started Application"
    echo    3. Tester le Duel Quiz avec 2 utilisateurs
    echo    4. Re-exécuter ce script pour vérifier les corrections
) else (
    echo ✅ Aucun problème majeur détecté
    echo.
    echo    Si vous rencontrez toujours un écran blanc:
    echo    - Vérifiez le cache du navigateur (Ctrl+Shift+Delete)
    echo    - Essayez un autre navigateur
    echo    - Vérifiez les logs en temps réel pendant le test
)
echo.

echo ═══════════════════════════════════════════════════════════
echo.
echo Pour voir les 50 dernières lignes du log en temps réel:
echo    powershell -Command "Get-Content '%LOG_FILE%' -Tail 50"
echo.

pause

