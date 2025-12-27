# ============================================================
# Script PowerShell - Importation automatique du certificat
# ============================================================
# ATTENTION : Ce script doit être exécuté en tant qu'ADMINISTRATEUR
# ============================================================

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  IMPORTATION AUTOMATIQUE DU CERTIFICAT SSL" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Chemins
$projectRoot = Split-Path -Parent $PSScriptRoot
$keystorePath = Join-Path $projectRoot "src\main\resources\keystore.p12"
$certPath = Join-Path $projectRoot "src\main\resources\quiz-app-cert.crt"
$keystorePassword = "quiz-app-2025"

# Vérifier si le script est exécuté en tant qu'administrateur
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "[ERREUR] Ce script doit etre execute en tant qu'ADMINISTRATEUR" -ForegroundColor Red
    Write-Host ""
    Write-Host "Clic droit sur PowerShell > Executer en tant qu'administrateur" -ForegroundColor Yellow
    Write-Host ""
    pause
    exit 1
}

Write-Host "[ETAPE 1/4] Verification du keystore..." -ForegroundColor Green
if (-not (Test-Path $keystorePath)) {
    Write-Host "[ERREUR] Keystore introuvable : $keystorePath" -ForegroundColor Red
    pause
    exit 1
}
Write-Host "[OK] Keystore trouve" -ForegroundColor Green
Write-Host ""

Write-Host "[ETAPE 2/4] Export du certificat depuis le keystore..." -ForegroundColor Green

# Supprimer l'ancien certificat s'il existe
if (Test-Path $certPath) {
    Remove-Item $certPath -Force
}

# Exporter le certificat avec keytool
$keytoolCmd = "keytool -exportcert -alias quiz-app -keystore `"$keystorePath`" -storepass $keystorePassword -file `"$certPath`" -rfc"
Invoke-Expression $keytoolCmd

if (-not (Test-Path $certPath)) {
    Write-Host "[ERREUR] Impossible d'exporter le certificat" -ForegroundColor Red
    pause
    exit 1
}
Write-Host "[OK] Certificat exporte : $certPath" -ForegroundColor Green
Write-Host ""

Write-Host "[ETAPE 3/4] Importation dans le magasin de certificats Windows..." -ForegroundColor Green

try {
    # Charger le certificat
    $cert = New-Object System.Security.Cryptography.X509Certificates.X509Certificate2($certPath)

    Write-Host "  - Emetteur : $($cert.Issuer)" -ForegroundColor Gray
    Write-Host "  - Sujet : $($cert.Subject)" -ForegroundColor Gray
    Write-Host "  - Valide du : $($cert.NotBefore) au $($cert.NotAfter)" -ForegroundColor Gray
    Write-Host ""

    # Ouvrir le magasin de certificats "Autorités de certification racines de confiance" pour l'ordinateur local
    $store = New-Object System.Security.Cryptography.X509Certificates.X509Store("Root", "LocalMachine")
    $store.Open("ReadWrite")

    # Vérifier si le certificat existe déjà
    $existingCerts = $store.Certificates | Where-Object { $_.Thumbprint -eq $cert.Thumbprint }

    if ($existingCerts) {
        Write-Host "[INFO] Le certificat existe deja dans le magasin" -ForegroundColor Yellow
        Write-Host "  Suppression de l'ancien certificat..." -ForegroundColor Yellow
        $store.Remove($existingCerts[0])
    }

    # Ajouter le certificat
    $store.Add($cert)
    $store.Close()

    Write-Host "[OK] Certificat importe avec succes!" -ForegroundColor Green

} catch {
    Write-Host "[ERREUR] Impossible d'importer le certificat : $_" -ForegroundColor Red
    pause
    exit 1
}

Write-Host ""
Write-Host "[ETAPE 4/4] Verification..." -ForegroundColor Green

# Vérifier que le certificat est bien installé
$store = New-Object System.Security.Cryptography.X509Certificates.X509Store("Root", "LocalMachine")
$store.Open("ReadOnly")
$installedCert = $store.Certificates | Where-Object { $_.Thumbprint -eq $cert.Thumbprint }
$store.Close()

if ($installedCert) {
    Write-Host "[OK] Certificat bien installe dans le magasin Windows" -ForegroundColor Green
} else {
    Write-Host "[AVERTISSEMENT] Impossible de verifier l'installation" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  IMPORTATION TERMINEE !" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "IMPORTANT : " -ForegroundColor Yellow
Write-Host "  1. Redemarrez TOUS vos navigateurs web" -ForegroundColor White
Write-Host "  2. Videz le cache du navigateur (Ctrl+Shift+Suppr)" -ForegroundColor White
Write-Host "  3. Relancez l'application Spring Boot" -ForegroundColor White
Write-Host ""
Write-Host "Ensuite, accedez a : https://apero-quiz.com:8443" -ForegroundColor Cyan
Write-Host ""
Write-Host "Le certificat devrait maintenant etre accepte sans avertissement!" -ForegroundColor Green
Write-Host ""

# Proposer d'ouvrir le gestionnaire de certificats
Write-Host "Voulez-vous ouvrir le gestionnaire de certificats Windows ? (O/N)" -ForegroundColor Yellow
$response = Read-Host "> "

if ($response -eq "O" -or $response -eq "o") {
    Start-Process "certmgr.msc"
    Write-Host ""
    Write-Host "Naviguez vers : Autorites de certification racines de confiance > Certificats" -ForegroundColor Cyan
    Write-Host "Vous devriez voir : CN=apero-quiz.com" -ForegroundColor Cyan
}

Write-Host ""
pause

