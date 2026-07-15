# Recovery and verification

After a reboot or interruption:

1. Check `Get-ScheduledTask -TaskName TelegramBeheer`.
2. Verify that the token exists in Credential Manager, not a file.
3. Send `/status` and open SSH/help buttons.
4. Run a harmless confirmed `Write-Output` command.
5. Run a short Codex prompt and verify the final text.
6. Perform a key-based test for every SSH profile.
7. Review `/audit` and run SQLite integrity checking locally.

Release checks:

```powershell
& '..\.venv\Scripts\python.exe' -m py_compile '.\bron\beheer_bot.py'
& '..\.venv\Scripts\python.exe' -m unittest discover -s tests -v
rg -n "\b[0-9]{7,12}:[A-Za-z0-9_-]{30,}\b" .
```

The public release is accepted only after the GitHub URL, bilingual links, secret scan, and remote commit SHA are verified against local HEAD.

