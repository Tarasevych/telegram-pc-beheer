# Installation and configuration

## Prerequisites

- Windows 11 with Python 3.13 or a compatible Python;
- the `keyring` package;
- Windows OpenSSH Client;
- a locally installed and authenticated Codex CLI;
- a personal Telegram bot created through `@BotFather`.

## Secrets and configuration

1. Copy `configuratie/instellingen.voorbeeld.json` to `configuratie/instellingen.json`.
2. Set the exact Telegram owner ID and workspace.
3. Run `gereedschap/configureren.py`. The token is entered with hidden input and stored in Windows Credential Manager under service `TelegramBeheer`, username `bot_token`.
4. Never commit `instellingen.json` or `ssh-doelen.json`.

The bot's Ukrainian description and command menu are configured automatically at service startup.

## Autostart

`installeren.ps1` creates the `TelegramBeheer` task for the current user's SID. It runs with limited privileges, continues on battery, ignores parallel duplicates, and restarts after failure.

```powershell
& '.\installeren.ps1'
Get-ScheduledTask -TaskName TelegramBeheer
Get-ScheduledTaskInfo -TaskName TelegramBeheer
```

## BotFather

Use a Ukrainian display name, description, and command text. Telegram usernames must use Latin characters and end in `bot`. Move the token directly to Credential Manager; never retain it in notes, chat history, `.env`, or source control.

