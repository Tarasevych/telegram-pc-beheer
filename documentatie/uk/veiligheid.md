# Безпека і приватні дані

## Що є приватним

| Дані | Приватне місце | Публічний репозиторій |
|---|---|---|
| Bot token | Windows Credential Manager | лише назва service/username |
| Telegram owner ID | локальний `instellingen.json` | фіктивний приклад |
| SSH host/user/port/key path | локальний `ssh-doelen.json` | порожній шаблон |
| Приватний SSH-ключ | стандартна локальна тека ключів | ніколи |
| MTProto session/API hash | окремий приватний Telegram-проєкт | ніколи |
| Аудит і події | `gegevens/` | лише схема |
| Smart-home токени/provider IDs | сховище відповідного адаптера | ніколи |

## Модель загроз

- Викрадення Telegram-облікового запису власника: зловмисник теоретично отримає owner-контекст. Захист — Telegram 2FA, список Devices, короткі підтвердження, локальний аудит і аварійне зупинення задачі.
- Викрадення bot token: токен треба відкликати через BotFather, оновити Credential Manager і перезапустити задачу.
- Ін’єкція в Codex або shell: довільний PowerShell потребує підтвердження; Codex обмежений робочою текою; вивід проходить редагування типових секретів.
- Підміна SSH-host: використовується системна перевірка `known_hosts`; не вимикайте `StrictHostKeyChecking`.
- Повтор callback: nonce одноразовий, прив’язаний до owner ID і має TTL 120 секунд.

Аварійна зупинка:

```powershell
Stop-ScheduledTask -TaskName TelegramBeheer
```

Після інциденту перевірте Telegram Devices, BotFather token, Windows Credential Manager, SSH `authorized_keys` на віддалених хостах і локальний SQLite-аудит.

