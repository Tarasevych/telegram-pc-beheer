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
    owner = input("Telegram owner ID: ").strip()
    if not owner.isdigit():
        raise SystemExit("Owner ID must contain digits only.")
    token = getpass.getpass("Telegram bot token (hidden): ").strip()
    if not re.fullmatch(r"\d{6,12}:[A-Za-z0-9_-]{30,}", token):
        raise SystemExit("The bot token format is invalid.")
    workspace = input(f"Workspace [{settings['werkmap']}]: ").strip() or settings["werkmap"]
    home_bot = input(f"Smart-home bot [{settings['slimme_woning_bot']}]: ").strip() or settings["slimme_woning_bot"]
    settings.update(eigenaar_ids=[int(owner)], werkmap=workspace, slimme_woning_bot=home_bot)
    TARGET.write_text(json.dumps(settings, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    keyring.set_password("TelegramBeheer", "bot_token", token)
    keyring.set_password("TelegramBeheer", "owner_id", owner)
    print("Configuration saved locally. The token is in Windows Credential Manager.")


if __name__ == "__main__":
    main()

