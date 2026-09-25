# ==============================================================================
# BlindSpot: Behavioral and Explainable-AI Framework for Auditing Text Classifiers
# PowerShell Execution Launcher Script (run.ps1)
# ==============================================================================

[CmdletBinding()]
param(
    [Parameter(Position=0)]
    [ValidateSet("cli", "dashboard", "test", "docs", "help")]
    [string]$Mode = "cli",

    [Parameter(Position=1)]
    [string]$Sentence = "This is awesome.",

    [Parameter(Position=2)]
    [string]$Model = "distilbert-base-uncased-finetuned-sst-2-english",

    [Parameter()]
    [string]$Explainer = "lime",

    [Parameter()]
    [string]$OutputDir = "audit_reports"
)

$ErrorActionPreference = "Stop"
$WorkspaceDir = $PSScriptRoot

Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host " BlindSpot: Text Classifier Auditing Framework Launcher " -ForegroundColor Yellow
Write-Host "========================================================================" -ForegroundColor Cyan

# Ensure script runs from project root
Set-Location -Path $WorkspaceDir

switch ($Mode.ToLower()) {
    "cli" {
        Write-Host "[+] Running Audit Pipeline via CLI..." -ForegroundColor Green
        Write-Host "  - Target Model: $Model" -ForegroundColor Gray
        Write-Host "  - Sentence:     '$Sentence'" -ForegroundColor Gray
        Write-Host "  - Explainer:    $Explainer" -ForegroundColor Gray
        Write-Host "  - Output Dir:   $OutputDir" -ForegroundColor Gray
        Write-Host "------------------------------------------------------------------------" -ForegroundColor Cyan
        
        python -m blindspot.cli --model $Model --sentence $Sentence --explainer $Explainer --output-dir $OutputDir
    }

    "dashboard" {
        Write-Host "[+] Launching Streamlit Interactive Web Dashboard..." -ForegroundColor Green
        Write-Host "  - Local URL: http://localhost:8501" -ForegroundColor Gray
        Write-Host "------------------------------------------------------------------------" -ForegroundColor Cyan
        
        python -m streamlit run blindspot/app.py
    }

    "test" {
        Write-Host "[!] Test suite files have been cleaned from the project." -ForegroundColor Yellow
    }

    "docs" {
        Write-Host "[+] Serving MkDocs Technical Documentation..." -ForegroundColor Green
        Write-Host "  - Local Docs Server: http://127.0.0.1:8000" -ForegroundColor Gray
        Write-Host "------------------------------------------------------------------------" -ForegroundColor Cyan
        
        python -m mkdocs serve
    }

    "help" {
        Write-Host "Usage Guidelines for run.ps1:" -ForegroundColor Yellow
        Write-Host "  .\run.ps1 cli -Sentence 'The food was great.'     Run CLI audit on a sentence" -ForegroundColor White
        Write-Host "  .\run.ps1 dashboard                               Launch Streamlit web dashboard" -ForegroundColor White
        Write-Host "  .\run.ps1 test                                    Run unit test suite" -ForegroundColor White
        Write-Host "  .\run.ps1 docs                                    Serve MkDocs documentation" -ForegroundColor White
    }
}

# SIG # Begin signature block
# MIIFlAYJKoZIhvcNAQcCoIIFhTCCBYECAQExCzAJBgUrDgMCGgUAMGkGCisGAQQB
# gjcCAQSgWzBZMDQGCisGAQQBgjcCAR4wJgIDAQAABBAfzDtgWUsITrck0sYpfvNR
# AgEAAgEAAgEAAgEAAgEAMCEwCQYFKw4DAhoFAAQUkFudlmMKMhXgf6nABMJKpwcz
# fRegggMiMIIDHjCCAgagAwIBAgIQQktp3ibdrJpCuOwJF3XjtjANBgkqhkiG9w0B
# AQsFADAnMSUwIwYDVQQDDBxCbGluZFNwb3QgTG9jYWwgQ29kZSBTaWduaW5nMB4X
# DTI2MDkyMzAzNDkxMFoXDTI3MDkyMzA0MDkxMFowJzElMCMGA1UEAwwcQmxpbmRT
# cG90IExvY2FsIENvZGUgU2lnbmluZzCCASIwDQYJKoZIhvcNAQEBBQADggEPADCC
# AQoCggEBAKopYMjD78DcPRZr0zkDXw53lh7wKfUA6RDb3Uy8xzB6EqOvDCML/7YN
# aGTbKwauRiDAqzGGfxXsEDSr/D4wKnvIgw37SH6LRjLOXzrrclYnK6TvlKruVhGg
# xbw8EYZuGfRJiIF44mlUJDTcfCJ0ezVox2apPht+iU1XNHUHH9x9udlZSM4LYueT
# cD1Uzd5cOgJ2Kr3WFkuFxU8cBy3dlZAp1JifdlM72EdCcVyrFWosR0q3PzP957I6
# SCur0JMpbGszFDuTDUHWVucNb/vHmwdH0WSyiw8wq59wMAuRE5Bd+rzJE1am3z6W
# QLQywpWIu8C50ILyaCPYLk+4DnDG4PUCAwEAAaNGMEQwDgYDVR0PAQH/BAQDAgeA
# MBMGA1UdJQQMMAoGCCsGAQUFBwMDMB0GA1UdDgQWBBTo9sSWBuSEWB8G4qmL4Z2m
# Q5DFyzANBgkqhkiG9w0BAQsFAAOCAQEAnl6lIBlq7/lTXuZkfUHCiRJ/jaBspnvC
# O4vagEaNEPTbTCoc82T67R8eYDNIHDHXX2HeaaxWs3Iq/AgO1B1miqQGUzs/mnPS
# TKx+EhZTCv51pBCpGjczCkNFOh6oxBeadsmriHtzPXprIDHI2hYf5S8ADqRTbFqD
# cligxAAvpw5D54Ynor6GIRf4sLoJXPfuZwZiBpxcxZtepiU6avftcEFVTtTOzJBz
# OIKmhpngrsrXCEBMJvmHZE5MlfspDRIZ6+rRd1uT4eT7I+UZIhRSZp0+7EBacvlo
# kPlO4Z2jxsFlsO2ZKE9uZSnjpKmcVkDfKgO9SaTrXFs89THZCNSKcDGCAdwwggHY
# AgEBMDswJzElMCMGA1UEAwwcQmxpbmRTcG90IExvY2FsIENvZGUgU2lnbmluZwIQ
# Qktp3ibdrJpCuOwJF3XjtjAJBgUrDgMCGgUAoHgwGAYKKwYBBAGCNwIBDDEKMAig
# AoAAoQKAADAZBgkqhkiG9w0BCQMxDAYKKwYBBAGCNwIBBDAcBgorBgEEAYI3AgEL
# MQ4wDAYKKwYBBAGCNwIBFTAjBgkqhkiG9w0BCQQxFgQUqYY7m1R09qGkczZdvrd4
# LccS1S0wDQYJKoZIhvcNAQEBBQAEggEAO7lDvCa+0nv1e4yiSjAI1b3rtpgnec1T
# D15IzxEYI2h3VrEG/5L6i/fsSRgxFK4gwqOr8JZUxw0nFooislk2n4lSZqKfwXP5
# rKSEGcz6AKXI6TTY85vg9hyZBiTZ5/j3sv+rIT54nRuVsHIgleNJxMoimxH1NtIX
# DhsAGYOhb0/nq03y7it0IoycupNygC7c3l2V6MUMzFRm/eoNsnra4KhXLdoJTH6K
# 9HaPVbZ7Rk0WDZeWf0faxhcrVjOvqHLYcy4C3uujHodVstlRk1whWnLV04qhCcMc
# bKpZ7PF5wBBAXnDW6w1W7j3BB9pf+bf8lNMVAafy+33TieyX3X0rqQ==
# SIG # End signature block
