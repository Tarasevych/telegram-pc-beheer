# Tarasevych GPT — Telegram PC control

This project is a private control plane for the owner's Windows PC through Telegram. User-facing text is Ukrainian. Technical paths and identifiers use Dutch where Cyrillic is unsuitable.

## Implemented capabilities

- owner-only access for exact Telegram user IDs in private chats;
- PC status, process, network, storage, SSH, Codex, audit, and smart-home menus;
- arbitrary PowerShell only after a fresh confirmation that expires after two minutes;
- the local Codex CLI in a configured workspace with `workspace-write` isolation;
- an SSH wizard for display name, `user@host`, port, and private-key path;
- bot token storage in Windows Credential Manager only;
- SQLite audit log, output redaction, and a single-instance mutex;
- Windows Scheduled Task autostart, restart-on-failure, and battery operation;
- mutual menu links and a vendor-neutral event contract for a separate smart-home bot.

## Documentation

- [Architecture and boundaries](documentatie/en/architectuur.md)
- [Installation and configuration](documentatie/en/installatie.md)
- [Security and private data](documentatie/en/veiligheid.md)
- [SSH and remote devices](documentatie/en/ssh.md)
- [Codex GPT](documentatie/en/codex.md)
- [Smart-home integration](documentatie/en/slimme-woning.md)
- [Recovery and verification](documentatie/en/herstel.md)

## Quick local verification

```powershell
& '..\.venv\Scripts\python.exe' -m unittest discover -s tests -v
& '.\installeren.ps1'
Get-ScheduledTask -TaskName TelegramBeheer
```

A real SSH acceptance test requires the remote host, user, port, and an authorized key. Those values intentionally never appear in this repository.

