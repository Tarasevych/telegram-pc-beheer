$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Python = Join-Path (Split-Path -Parent $Root) '.venv\Scripts\pythonw.exe'
if (-not (Test-Path -LiteralPath $Python)) { throw "Python-omgeving niet gevonden: $Python" }
$Script = Join-Path $Root 'bron\beheer_bot.py'
$Action = New-ScheduledTaskAction -Execute $Python -Argument ('"{0}"' -f $Script) -WorkingDirectory $Root
$Identity = [Security.Principal.WindowsIdentity]::GetCurrent()
$Trigger = New-ScheduledTaskTrigger -AtLogOn -User $Identity.Name
$Settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -RestartCount 5 -RestartInterval (New-TimeSpan -Minutes 1) -ExecutionTimeLimit ([TimeSpan]::Zero) -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
$Principal = New-ScheduledTaskPrincipal -UserId $Identity.User.Value -LogonType Interactive -RunLevel Limited -Id 'Author'
$Task = New-ScheduledTask -Action $Action -Trigger $Trigger -Settings $Settings -Principal $Principal -Description 'Tarasevych GPT Telegram-beheer voor Codex, SSH en pc-diagnostiek.'
$Xml = $Task | Export-ScheduledTask
# Windows 11 zet bij objectregistratie soms een lege Actions-context en een
# korte lokale gebruikersnaam in het XML. Task Scheduler weigert die combinatie.
$Xml = $Xml -replace '<SecurityDescriptor></SecurityDescriptor>\s*', ''
$Xml = $Xml -replace '<Principal id="Author">\s*<UserId>[^<]+</UserId>', ('<Principal id="Author"><UserId>' + $Identity.User.Value + '</UserId>')
$Xml = $Xml -replace '<Actions>', '<Actions Context="Author">'
Register-ScheduledTask -TaskName 'TelegramBeheer' -Xml $Xml -Force -ErrorAction Stop | Out-Null
Start-ScheduledTask -TaskName 'TelegramBeheer' -ErrorAction Stop
Write-Host 'TelegramBeheer is geïnstalleerd en gestart.'
