# Script PowerShell pour corriger l'acces a apero-quiz.duckdns.org
# Doit etre execute en tant qu'administrateur

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "CORRECTION DE L'ACCES A apero-quiz.duckdns.org" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Verification des droits administrateur
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "[ERREUR] Ce script doit etre execute en tant qu'administrateur!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Clic droit sur PowerShell -> Executer en tant qu'administrateur" -ForegroundColor Yellow
    Write-Host ""
    pause
    exit
}

Write-Host "[OK] Execution en tant qu'administrateur" -ForegroundColor Green
Write-Host ""

# Etape 1: Vider le cache DNS
Write-Host "1. Vidage du cache DNS..." -ForegroundColor Yellow
ipconfig /flushdns | Out-Null
Write-Host "[OK] Cache DNS vide" -ForegroundColor Green
Write-Host ""

# Etape 2: Verifier le fichier hosts
$hostsPath = "C:\Windows\System32\drivers\etc\hosts"
Write-Host "2. Verification du fichier hosts..." -ForegroundColor Yellow

$hostsContent = Get-Content $hostsPath -ErrorAction SilentlyContinue
$hasEntry = $hostsContent | Select-String -Pattern "apero-quiz.duckdns.org"

if ($hasEntry) {
    Write-Host "[INFO] Une entree existe deja pour apero-quiz.duckdns.org:" -ForegroundColor Yellow
    Write-Host $hasEntry -ForegroundColor Cyan
    Write-Host ""
    $response = Read-Host "Voulez-vous la remplacer? (O/N)"

    if ($response -eq "O" -or $response -eq "o") {
        # Supprimer l'ancienne entree
        $newContent = $hostsContent | Where-Object { $_ -notmatch "apero-quiz.duckdns.org" }
        Set-Content -Path $hostsPath -Value $newContent
        Write-Host "[OK] Ancienne entree supprimee" -ForegroundColor Green
    } else {
        Write-Host "[INFO] Conservation de l'entree existante" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "SOLUTION ALTERNATIVE:" -ForegroundColor Cyan
        Write-Host "Utilisez https://localhost:8443 a la place" -ForegroundColor Cyan
        Write-Host ""
        pause
        exit
    }
}

# Etape 3: Ajouter l'entree dans hosts
Write-Host "3. Ajout de l'entree dans le fichier hosts..." -ForegroundColor Yellow

$newEntry = "`n# Ajout pour Quiz App - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
$newEntry += "`n127.0.0.1 apero-quiz.duckdns.org"

Add-Content -Path $hostsPath -Value $newEntry
Write-Host "[OK] Entree ajoutee avec succes!" -ForegroundColor Green
Write-Host ""

# Etape 4: Afficher le contenu du fichier hosts
Write-Host "4. Contenu du fichier hosts (dernières lignes):" -ForegroundColor Yellow
Get-Content $hostsPath | Select-Object -Last 10
Write-Host ""

# Etape 5: Tester la resolution DNS
Write-Host "5. Test de resolution DNS..." -ForegroundColor Yellow
try {
    $dnsResult = Resolve-DnsName -Name "apero-quiz.duckdns.org" -ErrorAction Stop
    Write-Host "[OK] Resolution DNS reussie:" -ForegroundColor Green
    Write-Host "    IP: $($dnsResult.IPAddress)" -ForegroundColor Cyan
} catch {
    Write-Host "[ATTENTION] La resolution DNS a echoue, mais le fichier hosts forcera l'utilisation de 127.0.0.1" -ForegroundColor Yellow
}
Write-Host ""

# Etape 6: Verifier si l'application est en cours d'execution
Write-Host "6. Verification de l'application..." -ForegroundColor Yellow
$listening = netstat -ano | Select-String ":8443"
if ($listening) {
    Write-Host "[OK] L'application ecoute sur le port 8443" -ForegroundColor Green
} else {
    Write-Host "[ATTENTION] L'application ne semble pas etre en cours d'execution!" -ForegroundColor Red
    Write-Host "Veuillez demarrer l'application avant de tester." -ForegroundColor Yellow
}
Write-Host ""

# Etape 7: Instructions finales
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "CONFIGURATION TERMINEE!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "PROCHAINES ETAPES:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Ouvrez votre navigateur (Chrome ou Edge)" -ForegroundColor White
Write-Host ""
Write-Host "2. Allez sur: https://apero-quiz.duckdns.org:8443" -ForegroundColor Cyan
Write-Host "   OU sur:    https://localhost:8443" -ForegroundColor Cyan
Write-Host ""
Write-Host "3. Si vous voyez une erreur de certificat:" -ForegroundColor White
Write-Host "   - Chrome: Tapez 'thisisunsafe' sur la page d'erreur" -ForegroundColor Yellow
Write-Host "   - Edge: Cliquez 'Avance' puis 'Continuer vers le site'" -ForegroundColor Yellow
Write-Host ""
Write-Host "4. Profitez de votre application! " -ForegroundColor Green
Write-Host ""

Write-Host "============================================================" -ForegroundColor Cyan
pause

