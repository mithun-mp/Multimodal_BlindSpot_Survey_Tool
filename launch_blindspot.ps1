# BlindSpot Workstation PowerShell Launcher
# Double-click or run from PowerShell prompt

$ErrorActionPreference = "Continue"
$host.UI.RawUI.WindowTitle = "BlindSpot Workstation"

Set-Location $PSScriptRoot
$env:PYTHONPATH = "$PSScriptRoot;$env:PYTHONPATH"

try {
    & python -m blindspot.launcher $args
    if ($LASTEXITCODE -ne 0) {
        Write-Host "`n[ERROR] BlindSpot exited with code $LASTEXITCODE." -ForegroundColor Red
        Read-Host "Press Enter to exit..."
    }
}
catch {
    Write-Host "`n[ERROR] Failed to execute Python launcher: $_" -ForegroundColor Red
    Read-Host "Press Enter to exit..."
}

# SIG # Begin signature block
# MIIFlAYJKoZIhvcNAQcCoIIFhTCCBYECAQExCzAJBgUrDgMCGgUAMGkGCisGAQQB
# gjcCAQSgWzBZMDQGCisGAQQBgjcCAR4wJgIDAQAABBAfzDtgWUsITrck0sYpfvNR
# AgEAAgEAAgEAAgEAAgEAMCEwCQYFKw4DAhoFAAQUtR+UlqG6OAaOWDZhuso4bJFU
# 6SigggMiMIIDHjCCAgagAwIBAgIQQktp3ibdrJpCuOwJF3XjtjANBgkqhkiG9w0B
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
# MQ4wDAYKKwYBBAGCNwIBFTAjBgkqhkiG9w0BCQQxFgQUG+PFurXreYnknXpwvYqH
# tXzrOnQwDQYJKoZIhvcNAQEBBQAEggEAfepPWeL9KOSdO2gcWqP/X8npZcW+Tne5
# uv2OqpMtyJ8Ow5ZTLuTHdW2bNd/GMKJhW76dDOJTRsKhFQ2DX98BLLQyWp6s2a8R
# gE4zjxjJL9sSqI4eyS5tNBweLIC6VL9cxH0KJ25VPH3K6O5LZ8DjcQxSGxiN+J4x
# m0fJV2yxkUM+z7QH/lOQwKZ7odaBAe4crRk9uradeir+gQjzuYl6PzUgbVAXX7as
# ibx5Yc1ui1rF+VtUIhhONAXVkPhcleDxudxyyE3RJ2f2wBRd/2f32tbrl5lF2j/M
# obzaLZZ2S+3P6Hkx9kNiB1Aws+OPQnA8BuyNwxZBPD5bEiOYlY1CJw==
# SIG # End signature block
