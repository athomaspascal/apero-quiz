@echo off
setlocal
set PY=C:\Users\athom\AppData\Local\Programs\Python\Python312\python.exe

if not exist "%PY%" (
  echo Python introuvable: %PY%
  exit /b 1
)

echo Installation des dependances Python pour parser l'infobox Wikipedia...
"%PY%" -m pip install -r tools\requirements-wikipedia.txt

echo OK
endlocal

