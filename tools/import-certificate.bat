@echo off
REM ============================================================
REM   LANCEUR - Import certificat (Mode Administrateur)
REM ============================================================

echo.
echo ============================================================
echo   IMPORTATION CERTIFICAT SSL
echo ============================================================
echo.
echo Ce script va importer le certificat SSL dans Windows
echo pour eviter les avertissements du navigateur.
echo.
echo ATTENTION : Necessite les droits ADMINISTRATEUR
echo.
pause

REM Lancer PowerShell en tant qu'administrateur
PowerShell -NoProfile -ExecutionPolicy Bypass -Command "& {Start-Process PowerShell -ArgumentList '-NoProfile -ExecutionPolicy Bypass -File \"%~dp0import-certificate-windows.ps1\"' -Verb RunAs}"

echo.
echo Si une fenetre UAC apparait, cliquez sur OUI pour autoriser.
echo.
pause

