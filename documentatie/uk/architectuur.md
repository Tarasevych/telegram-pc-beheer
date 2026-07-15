# Архітектура

```mermaid
flowchart LR
  U[Власник у Telegram] --> B[tarasevych_gpt_bot]
  B --> A[Owner allowlist і підтвердження]
  A --> P[Діагностика та PowerShell]
  A --> S[Системний SSH-клієнт]
  A --> C[Локальний Codex CLI]
  B --> L[SQLite-аудит і JSONL-події]
  B --> D[Live deep-link]
  D --> H[Окремий бот Slimme Woning]
  H -. підготовлено до deployment .-> B
  L -. майбутній адаптер .-> M[MQTT або підписаний HTTPS]
```

Бот використовує Telegram Bot API через long polling і не відкриває вхідний мережевий порт. Всі операції виконуються в інтерактивному Windows-сеансі власника, тому доступні його Credential Manager, SSH-ключі та Codex-авторизація.

Ключові межі:

1. Авторизація відбувається до маршрутизації команди.
2. Групові чати відхиляються, навіть якщо повідомлення надіслав власник.
3. Довільна локальна команда відділена від діагностичних read-only маршрутів і потребує callback-підтвердження.
4. Codex не отримує `danger-full-access`; типовий режим — `workspace-write`, approvals `never` означає fail-closed замість очікування недоступного діалогу.
5. SSH — вихідний клієнт із `BatchMode=yes`, а не публічний SSH-сервер цього ПК.
6. Боти Telegram не отримують повідомлень від інших ботів. Взаємодія з розумним будинком відбувається через deep-link та окремий подієвий контракт.

Подієвий контракт містить `opstart_id`, монотонний `volgnummer`, випадковий `bericht_id`, час, актора, функцію, дію, ціль і статус. Статуси узгоджені з ядром будинку: `ontvangen`, `aanvaard`, `uitgevoerd`, `geweigerd`, `mislukt`, `verlopen`, `onzeker`.
