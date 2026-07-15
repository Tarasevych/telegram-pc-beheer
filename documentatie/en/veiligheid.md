# Security and private data

## Private-data inventory

| Data | Private location | Public repository |
|---|---|---|
| Bot token | Windows Credential Manager | service/username label only |
| Telegram owner ID | local `instellingen.json` | synthetic example |
| SSH host/user/port/key path | local `ssh-doelen.json` | empty template |
| SSH private key | normal local key directory | never |
| MTProto session/API hash | separate private Telegram project | never |
| Audit and events | `gegevens/` | schema only |
| Smart-home tokens/provider IDs | each adapter's private store | never |

## Threat model

- Stolen owner Telegram account: an attacker could gain owner context. Mitigate with Telegram 2FA, regular Devices review, short-lived confirmations, local audit, and the emergency stop.
- Stolen bot token: revoke it through BotFather, update Credential Manager, and restart the task.
- Codex or shell injection: arbitrary PowerShell requires confirmation; Codex is workspace-scoped; common secret patterns are redacted from output.
- SSH host substitution: the system `known_hosts` check remains enabled. Do not disable `StrictHostKeyChecking`.
- Callback replay: each nonce is single-use, owner-bound, and expires after 120 seconds.

Emergency stop:

```powershell
Stop-ScheduledTask -TaskName TelegramBeheer
```

After an incident, review Telegram Devices, the BotFather token, Windows Credential Manager, remote `authorized_keys`, and the local SQLite audit log.

