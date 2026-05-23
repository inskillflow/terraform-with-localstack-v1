# Script de push rapide pour ce depot.
# Usage:
#   .\scripts1.ps1
#   .\scripts1.ps1 "message de commit"

param(
    [string]$Message = "mise a jour du cours"
)

$ErrorActionPreference = "Stop"

Write-Host "Depot courant :" (Get-Location)
Write-Host ""

if (-not (Test-Path ".git")) {
    Write-Error "Ce dossier ne contient pas de depot .git local. Arret pour eviter de pousser le mauvais dossier."
}

$gitDir = git rev-parse --git-dir
if ($gitDir -ne ".git") {
    Write-Error "Le depot actif n'est pas le .git local du projet ($gitDir). Arret."
}

Write-Host "Statut avant commit :"
git status --short
Write-Host ""

git add -A

$changes = git status --short
if (-not $changes) {
    Write-Host "Aucun changement a commiter."
}
else {
    git commit -m $Message
}

Write-Host ""
Write-Host "Push vers origin/main..."
git push

Write-Host ""
Write-Host "Termine."
