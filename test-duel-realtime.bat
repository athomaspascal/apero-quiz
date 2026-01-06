@echo off
REM ========================================================
REM Script de Test Duel Quiz avec Logs en Temps Réel
REM Date: 2026-01-06
REM ========================================================

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║  TEST DUEL QUIZ - Surveillance des Logs                  ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

set LOG_FILE=logs\application.log

echo Instructions pour le test:
echo.
echo 1. Ouvrir 2 navigateurs (ou 2 appareils)
echo 2. Connecter 2 utilisateurs différents (ex: Charles Darwin + Nelson Mandela)
echo 3. Les deux cliquent sur "Duel Quiz" dans le menu
echo 4. Observer les logs ci-dessous
echo.
echo ═══════════════════════════════════════════════════════════
echo LOGS EN TEMPS RÉEL (Ctrl+C pour arrêter)
echo ═══════════════════════════════════════════════════════════
echo.

REM Afficher les dernières lignes et suivre les nouvelles
powershell -Command "Get-Content '%LOG_FILE%' -Wait -Tail 20 | Where-Object { $_ -match 'Duel|duel|Quiz|NAVIGATING|beforeEnter|displayQuestion' }"

