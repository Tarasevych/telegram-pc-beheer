$task = Get-ScheduledTask -TaskName 'TelegramBeheer' -ErrorAction SilentlyContinue
if ($task) { Unregister-ScheduledTask -TaskName 'TelegramBeheer' -Confirm:$false }
Write-Host 'TelegramBeheer-autostart is verwijderd. Geheimen zijn niet verwijderd.'

