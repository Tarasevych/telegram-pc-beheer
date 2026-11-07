from __future__ import annotations

import getpass
import json
import re
from pathlib import Path

import keyring


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "configuratie" / "instellingen.voorbeeld.json"
TARGET = ROOT / "configuratie" / "instellingen.json"


def main() -> None:
    settings = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    owner = input("Числовий ідентифікатор власника в Telegram: ").strip()
    if not owner.isdigit():
        raise SystemExit("Ідентифікатор власника має містити лише цифри.")
    token = getpass.getpass("Ключ доступу бота Telegram (введення приховано): ").strip()
    if not re.fullmatch(r"\d{6,12}:[A-Za-z0-9_-]{30,}", token):
        raise SystemExit("Некоректний формат ключа доступу бота.")
    workspace = input(f"Робоча тека [{settings['werkmap']}]: ").strip() or settings["werkmap"]
    home_bot = input(f"Бот розумного дому [{settings['slimme_woning_bot']}]: ").strip() or settings["slimme_woning_bot"]
    settings.update(eigenaar_ids=[int(owner)], werkmap=workspace, slimme_woning_bot=home_bot)
    TARGET.write_text(json.dumps(settings, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    keyring.set_password("TelegramBeheer", "bot_token", token)
    keyring.set_password("TelegramBeheer", "owner_id", owner)
    print("Налаштування збережено локально. Ключ доступу записано до сховища облікових даних Windows.")


if __name__ == "__main__":
    main()
