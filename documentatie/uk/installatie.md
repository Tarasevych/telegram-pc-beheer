# Встановлення і налаштування

## Передумови

- Windows 11, Python 3.13 або сумісний Python;
- пакет `keyring`;
- системний OpenSSH Client;
- локально встановлений та авторизований Codex CLI;
- власний Telegram-бот, створений через `@BotFather`.

## Секрети та конфігурація

1. Скопіюйте `configuratie/instellingen.voorbeeld.json` у `configuratie/instellingen.json`.
2. Встановіть правильний Telegram owner ID і робочу теку.
3. Запустіть `gereedschap/configureren.py`. Токен вводиться приховано й потрапляє до Windows Credential Manager під service `TelegramBeheer`, username `bot_token`.
4. Не додавайте `instellingen.json` або `ssh-doelen.json` у Git.

Профіль бота, опис і команди українською встановлюються автоматично під час старту сервісу.

## Автозапуск

`installeren.ps1` створює задачу `TelegramBeheer` для поточного SID користувача. Вона працює з обмеженим рівнем прав, не зупиняється при переході на батарею, ігнорує паралельний дубль та перезапускається після збою.

```powershell
& '.\installeren.ps1'
Get-ScheduledTask -TaskName TelegramBeheer
Get-ScheduledTaskInfo -TaskName TelegramBeheer
```

## BotFather

Рекомендовано встановити українську відображувану назву, опис і команди. Username мусить бути латиницею та завершуватися на `bot`. Токен після створення треба негайно передати в Credential Manager і не зберігати в нотатках, чатах, `.env` або репозиторії.

