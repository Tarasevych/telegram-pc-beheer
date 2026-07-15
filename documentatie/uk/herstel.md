# Відновлення й перевірка

Після перезавантаження або збою:

1. Перевірте `Get-ScheduledTask -TaskName TelegramBeheer`.
2. Переконайтеся, що bot token є в Credential Manager, не в файлі.
3. Надішліть `/status` і натисніть SSH/довідку.
4. Виконайте нешкідливу підтверджену команду `Write-Output`.
5. Запустіть короткий Codex-запит і перевірте фінальний текст.
6. Для кожного SSH-профілю проведіть key-based тест.
7. Перегляньте `/audit` і локальну SQLite integrity check.

Перевірка релізу:

```powershell
& '..\.venv\Scripts\python.exe' -m py_compile '.\bron\beheer_bot.py'
& '..\.venv\Scripts\python.exe' -m unittest discover -s tests -v
rg -n "\b[0-9]{7,12}:[A-Za-z0-9_-]{30,}\b" .
```

Публічна версія вважається прийнятою лише після перевірки GitHub URL, двомовних посилань, відсутності секретів і збігу commit SHA з локальним HEAD.

