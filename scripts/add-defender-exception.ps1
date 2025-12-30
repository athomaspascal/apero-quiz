# Script PowerShell pour ajouter apero-quiz.duckdns.org aux exceptions Windows Defender
# Doit être exécuté en tant qu'administrateur

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "AJOUT D'EXCEPTIONS DANS WINDOWS DEFENDER" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Vérification des droits administrateur
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "[ERREUR] Ce script doit être exécuté en tant qu'administrateur!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Faites un clic droit sur PowerShell -> Exécuter en tant qu'administrateur" -ForegroundColor Yellow
    Write-Host ""
    pause
    exit
}

Write-Host "[OK] Exécution en tant qu'administrateur" -ForegroundColor Green
Write-Host ""

# Vérifier si Windows Defender est actif
try {
    $defenderStatus = Get-MpComputerStatus -ErrorAction Stop
    Write-Host "[INFO] Windows Defender est actif" -ForegroundColor Green
    Write-Host "      Protection en temps réel: $($defenderStatus.RealTimeProtectionEnabled)" -ForegroundColor Cyan
    Write-Host ""
} catch {
    Write-Host "[ERREUR] Impossible de vérifier l'état de Windows Defender" -ForegroundColor Red
    Write-Host "        $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    pause
    exit
}

# Afficher les exclusions actuelles
Write-Host "1. Exclusions actuelles:" -ForegroundColor Yellow
Write-Host "-----------------------" -ForegroundColor Yellow
try {
    $currentExclusions = Get-MpPreference | Select-Object -ExpandProperty ExclusionPath
    if ($currentExclusions) {
        foreach ($exclusion in $currentExclusions) {
            Write-Host "   - $exclusion" -ForegroundColor Cyan
        }
    } else {
        Write-Host "   Aucune exclusion configurée" -ForegroundColor Gray
    }
} catch {
    Write-Host "   Impossible de lire les exclusions" -ForegroundColor Red
}
Write-Host ""

# Ajouter le dossier du projet en exclusion
Write-Host "2. Ajout du dossier du projet en exclusion..." -ForegroundColor Yellow
Write-Host "----------------------------------------------" -ForegroundColor Yellow
$projectPath = "C:\Users\athom\IdeaProjects\quizz1"
try {
    Add-MpPreference -ExclusionPath $projectPath -ErrorAction Stop
    Write-Host "[OK] Dossier ajouté: $projectPath" -ForegroundColor Green
} catch {
    Write-Host "[INFO] Le dossier est peut-être déjà en exclusion" -ForegroundColor Yellow
    Write-Host "       $($_.Exception.Message)" -ForegroundColor Gray
}
Write-Host ""

# Note: Windows Defender ne permet pas d'ajouter directement des domaines/URLs en exclusion
# Il faut utiliser d'autres méthodes

Write-Host "3. Configuration avancée nécessaire..." -ForegroundColor Yellow
Write-Host "--------------------------------------" -ForegroundColor Yellow
Write-Host ""
Write-Host "[INFO] Windows Defender ne permet pas d'ajouter directement des domaines" -ForegroundColor Cyan
Write-Host "       comme duckdns.org en exclusion via PowerShell." -ForegroundColor Cyan
Write-Host ""
Write-Host "SOLUTIONS ALTERNATIVES:" -ForegroundColor Yellow
Write-Host ""

Write-Host "SOLUTION 1 (RECOMMANDÉE): Utilisez localhost" -ForegroundColor Green
Write-Host "   Au lieu de: https://apero-quiz.duckdns.org:8443" -ForegroundColor Gray
Write-Host "   Utilisez:   https://localhost:8443" -ForegroundColor Cyan
Write-Host ""

Write-Host "SOLUTION 2 (ALTERNATIVE): Modifiez le fichier hosts" -ForegroundColor Green
Write-Host "   Exécutez: add-duckdns-to-hosts.bat (en administrateur)" -ForegroundColor Cyan
Write-Host "   Cela forcera la résolution vers 127.0.0.1" -ForegroundColor Gray
Write-Host "   Windows Defender ne bloquera pas car c'est une connexion locale" -ForegroundColor Gray
Write-Host ""

Write-Host "SOLUTION 3 (MANUELLE): Via l'interface Windows Defender" -ForegroundColor Green
Write-Host "   1. Ouvrez 'Sécurité Windows'" -ForegroundColor Cyan
Write-Host "   2. 'Protection contre les virus et menaces'" -ForegroundColor Cyan
Write-Host "   3. 'Gérer les paramètres'" -ForegroundColor Cyan
Write-Host "   4. 'Exclusions' -> 'Ajouter ou supprimer des exclusions'" -ForegroundColor Cyan
Write-Host "   5. Ajoutez le dossier du projet ou désactivez temporairement" -ForegroundColor Cyan
Write-Host ""

# Proposer de désactiver temporairement la protection réseau
Write-Host "4. Options avancées (ATTENTION):" -ForegroundColor Yellow
Write-Host "--------------------------------" -ForegroundColor Yellow
Write-Host ""
$response = Read-Host "Voulez-vous désactiver temporairement la protection réseau? (O/N)"

if ($response -eq "O" -or $response -eq "o") {
    Write-Host ""
    Write-Host "[ATTENTION] Vous allez désactiver temporairement la protection!" -ForegroundColor Red
    Write-Host "[ATTENTION] N'oubliez pas de la réactiver après vos tests!" -ForegroundColor Red
    Write-Host ""

    $confirm = Read-Host "Êtes-vous sûr? (O/N)"

    if ($confirm -eq "O" -or $confirm -eq "o") {
        try {
            # Désactiver la protection en temps réel
            Set-MpPreference -DisableRealtimeMonitoring $true -ErrorAction Stop
            Write-Host "[OK] Protection en temps réel désactivée temporairement" -ForegroundColor Yellow
            Write-Host ""
            Write-Host "IMPORTANT: Pour la réactiver, exécutez:" -ForegroundColor Red
            Write-Host "Set-MpPreference -DisableRealtimeMonitoring `$false" -ForegroundColor Cyan
            Write-Host ""
        } catch {
            Write-Host "[ERREUR] Impossible de désactiver la protection" -ForegroundColor Red
            Write-Host "        $($_.Exception.Message)" -ForegroundColor Red
        }
    }
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "RÉSUMÉ DES ACTIONS" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "[OK] Dossier du projet ajouté en exclusion" -ForegroundColor Green
Write-Host "     $projectPath" -ForegroundColor Gray
Write-Host ""
Write-Host "PROCHAINES ÉTAPES:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. TESTEZ avec localhost (RECOMMANDÉ):" -ForegroundColor White
Write-Host "   https://localhost:8443" -ForegroundColor Cyan
Write-Host ""
Write-Host "2. OU configurez le fichier hosts:" -ForegroundColor White
Write-Host "   Exécutez: add-duckdns-to-hosts.bat (en admin)" -ForegroundColor Cyan
Write-Host ""
Write-Host "3. Si nécessaire, configurez manuellement Defender:" -ForegroundColor White
Write-Host "   Sécurité Windows -> Protection -> Exclusions" -ForegroundColor Cyan
Write-Host ""

# Afficher les nouvelles exclusions
Write-Host "5. Exclusions actuelles (après modifications):" -ForegroundColor Yellow
Write-Host "----------------------------------------------" -ForegroundColor Yellow
try {
    $newExclusions = Get-MpPreference | Select-Object -ExpandProperty ExclusionPath
    if ($newExclusions) {
        foreach ($exclusion in $newExclusions) {
            Write-Host "   - $exclusion" -ForegroundColor Cyan
        }
    }
} catch {
    Write-Host "   Impossible de lire les exclusions" -ForegroundColor Red
}
Write-Host ""

Write-Host "============================================================" -ForegroundColor Cyan
pause

