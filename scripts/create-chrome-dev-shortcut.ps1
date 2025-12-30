# Script PowerShell pour créer un raccourci Chrome de développement
# Doit être exécuté en tant qu'administrateur

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "CREATION D'UN RACCOURCI CHROME POUR DEVELOPPEMENT" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Chemin de Chrome
$chromePath = ""
if (Test-Path "C:\Program Files\Google\Chrome\Application\chrome.exe") {
    $chromePath = "C:\Program Files\Google\Chrome\Application\chrome.exe"
} elseif (Test-Path "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe") {
    $chromePath = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
} else {
    Write-Host "[ERREUR] Chrome n'est pas installé!" -ForegroundColor Red
    pause
    exit
}

Write-Host "[OK] Chrome trouvé: $chromePath" -ForegroundColor Green
Write-Host ""

# Créer le raccourci sur le Bureau
$desktopPath = [Environment]::GetFolderPath("Desktop")
$shortcutPath = "$desktopPath\Chrome DEV - Quiz App.lnk"

Write-Host "Création du raccourci..." -ForegroundColor Yellow

$WScriptShell = New-Object -ComObject WScript.Shell
$Shortcut = $WScriptShell.CreateShortcut($shortcutPath)
$Shortcut.TargetPath = $chromePath
$Shortcut.Arguments = "--ignore-certificate-errors --ignore-urlfetcher-cert-requests --allow-insecure-localhost https://apero-quiz.duckdns.org:8443"
$Shortcut.WorkingDirectory = "C:\Program Files\Google\Chrome\Application"
$Shortcut.Description = "Chrome en mode développement pour Quiz App (accepte certificats auto-signés)"
$Shortcut.Save()

Write-Host "[OK] Raccourci créé sur le Bureau!" -ForegroundColor Green
Write-Host ""
Write-Host "Nom du raccourci: Chrome DEV - Quiz App.lnk" -ForegroundColor Cyan
Write-Host ""

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "UTILISATION" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Double-cliquez sur le raccourci 'Chrome DEV - Quiz App'" -ForegroundColor White
Write-Host "   sur votre Bureau" -ForegroundColor White
Write-Host ""
Write-Host "2. Chrome s'ouvrira directement sur:" -ForegroundColor White
Write-Host "   https://apero-quiz.duckdns.org:8443" -ForegroundColor Cyan
Write-Host ""
Write-Host "3. Si vous voyez une erreur de certificat:" -ForegroundColor White
Write-Host "   Tapez 'thisisunsafe' sur la page" -ForegroundColor Yellow
Write-Host ""
Write-Host "ATTENTION:" -ForegroundColor Red
Write-Host "Ce mode désactive certaines protections de sécurité." -ForegroundColor Red
Write-Host "Utilisez-le UNIQUEMENT pour le développement local!" -ForegroundColor Red
Write-Host ""

pause

