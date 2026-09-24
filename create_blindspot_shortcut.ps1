# Create Desktop Shortcut for BlindSpot Workstation
# Does NOT require administrator privileges.

$WshShell = New-Object -ComObject WScript.Shell
$DesktopPath = [System.Environment]::GetFolderPath([System.Environment+SpecialFolder]::Desktop)
$ShortcutPath = Join-Path $DesktopPath "BlindSpot Workstation.lnk"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$TargetPath = Join-Path $ScriptDir "launch_blindspot.bat"

if (-not (Test-Path $TargetPath)) {
    Write-Host "[ERROR] Target launcher '$TargetPath' not found." -ForegroundColor Red
    exit 1
}

$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $TargetPath
$Shortcut.WorkingDirectory = $ScriptDir
$Shortcut.Description = "BlindSpot Multimodel AI Auditing Workstation"
$Shortcut.Save()

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host " BLINDSPOT DESKTOP SHORTCUT CREATED                     " -ForegroundColor Green
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "Location : $ShortcutPath"
Write-Host "Target   : $TargetPath"
Write-Host "`nYou can now double-click the desktop icon to launch BlindSpot."

# SIG # Begin signature block
# MIIFlAYJKoZIhvcNAQcCoIIFhTCCBYECAQExCzAJBgUrDgMCGgUAMGkGCisGAQQB
# gjcCAQSgWzBZMDQGCisGAQQBgjcCAR4wJgIDAQAABBAfzDtgWUsITrck0sYpfvNR
# AgEAAgEAAgEAAgEAAgEAMCEwCQYFKw4DAhoFAAQUyyNfyma+xqwP2mCylVWnD4PF
# 7uCgggMiMIIDHjCCAgagAwIBAgIQQktp3ibdrJpCuOwJF3XjtjANBgkqhkiG9w0B
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
# MQ4wDAYKKwYBBAGCNwIBFTAjBgkqhkiG9w0BCQQxFgQUhBfji2EQBIy6HSsP9tht
# d3OEr+cwDQYJKoZIhvcNAQEBBQAEggEAgbzrnR/poLSTqUqlO9D4Yd4EP4juqAPD
# dR2nVL5m2sCxRcVRpOS41Wx4SDwoIanrbM/M58vo2mzF310aqxEEDZ6dIblLNyht
# kg5Mcj4cRi3dl3HL48vLZ5cXR+UygVihhI88227k9VVo5WLUkTH7TYaqKxszwg+S
# c/PyDfkYhuks3iQhKYhvFjcnafF9Hn42FtPsxrUzFHkAUJ6j2TDCi9KQkJl+ppvU
# jpUtIfwNtwNe8uxi4fnPFmEUTJb+s/jPrmXVeiXxvCZdnup0S0dgxvP3f8ssNuWK
# MMhSHPo2Ym+qsQ2E7fUZv3W0FgN8Rq40Q+TBETEIG2Pu7vngNJ+w+g==
# SIG # End signature block
