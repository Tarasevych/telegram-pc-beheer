# Current acceptance status

Verified on 15 July 2026:

- `@tarasevych_gpt_bot` exists and Bot API `getMe` succeeds;
- Ukrainian description and six Bot API commands are installed;
- long polling is active, webhook URL is empty, and pending updates are zero;
- Windows task `TelegramBeheer` is `Running`, limited, and allowed on battery;
- all six main-menu callback buttons returned the correct live screens;
- the smart-home URL button targets `@tarasevych_Slimme_Woning_bot?start=pcbeheer`;
- an arbitrary `Write-Output` ran only after a fresh confirmation;
- a live Codex invocation returned its control result through Telegram;
- SQLite `PRAGMA integrity_check` returned `ok`, with audit and event rows present;
- GPT-bot tests: 5/5; adjacent Slimme Woning suite: 123/123;
- public GitHub main was verified by SHA and HTTP 200; private runtime configs are absent.

Not yet acceptable without external data:

- a real SSH target requires host/user/port/authorized-key details;
- the reciprocal live button in the home bot has a tested source patch, but its Apps Script deployment is intentionally not mixed with unrelated in-progress provider changes.
