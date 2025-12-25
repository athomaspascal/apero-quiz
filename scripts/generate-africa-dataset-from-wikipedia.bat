@echo off
setlocal
set PY=C:\Users\athom\AppData\Local\Programs\Python\Python312\python.exe

if not exist "%PY%" (
  echo Python introuvable: %PY%
  exit /b 1
)

set EXTRACTED=tools\extracted\enwiki
if not exist "%EXTRACTED%" (
  echo Dossier d'extraction introuvable: %EXTRACTED%
  echo Lancez d'abord WikiExtractor pour generer ce dossier.
  exit /b 1
)

echo Generation du dataset Afrique depuis dump Wikipedia (offline)...
"%PY%" tools\generate_africa_dataset_from_wikipedia_dump.py --extracted "%EXTRACTED%" --out tools\datasets\africa_countries_wikipedia.json --mode infobox

echo Termine.
endlocal

