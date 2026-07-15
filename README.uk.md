# Tarasevych GPT — керування ПК через Telegram

Це приватний центр віддаленого керування власним Windows ПК через Telegram. Інтерфейс користувача — український; технічні шляхи й назви, де кирилиця недоречна, — нідерландські.

## Що реалізовано

- owner-only доступ лише з точного Telegram ID у приватному чаті;
- кнопки стану ПК, процесів, мережі, дисків, SSH, Codex, аудиту й розумного будинку;
- довільний PowerShell тільки після свіжого підтвердження, яке діє 2 хвилини;
- локальний Codex CLI у контрольованій робочій папці та режимі `workspace-write`;
- майстер SSH із полями: відображувана назва, `user@host`, порт і шлях до ключа;
- токен лише у Windows Credential Manager;
- SQLite-аудит, редагування секретів у виводі, single-instance mutex;
- Windows Scheduled Task із автозапуском, повторним запуском і роботою від батареї;
- взаємні кнопки з окремим ботом розумного будинку й нейтральний контракт подій.

## Навігація

- [Архітектура та межі](documentatie/uk/architectuur.md)
- [Встановлення і налаштування](documentatie/uk/installatie.md)
- [Безпека і приватні дані](documentatie/uk/veiligheid.md)
- [SSH і віддалені пристрої](documentatie/uk/ssh.md)
- [Codex GPT](documentatie/uk/codex.md)
- [Інтеграція з розумним будинком](documentatie/uk/slimme-woning.md)
- [Відновлення й перевірка](documentatie/uk/herstel.md)

## Швидка локальна перевірка

```powershell
& '..\.venv\Scripts\python.exe' -m unittest discover -s tests -v
& '.\installeren.ps1'
Get-ScheduledTask -TaskName TelegramBeheer
```

Для реального SSH-тесту потрібні дані зовнішнього пристрою: host, користувач, порт і дозволений ключ. Вони навмисно не зберігаються в GitHub.

