import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


MODULE = Path(__file__).parents[1] / "bron" / "beheer_bot.py"
SPEC = importlib.util.spec_from_file_location("beheer_bot", MODULE)
bot = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(bot)


class FakeAPI:
    def __init__(self): self.calls = []
    def send(self, chat_id, text, keyboard=None): self.calls.append((chat_id, text, keyboard)); return True
    def call(self, method, **payload): self.calls.append((method, payload)); return True


class BotTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        bot.AUDIT = Path(self.temp.name) / "audit.sqlite3"
        self.api = FakeAPI()
        self.owner = 123456789
        self.service = bot.BeheerBot(self.api, {"eigenaar_ids": [self.owner], "werkmap": self.temp.name, "slimme_woning_bot": "voorbeeld_Slimme_Woning_bot", "volledig_beheer": True, "codex_actief": True, "max_antwoordtekens": 3500})
    def tearDown(self): self.temp.cleanup()

    def test_only_owner_private_chat(self):
        self.assertTrue(self.service.is_authorized(self.owner, {"type": "private"}))
        self.assertFalse(self.service.is_authorized(1, {"type": "private"}))
        self.assertFalse(self.service.is_authorized(self.owner, {"type": "group"}))

    def test_main_menu_contains_all_surfaces(self):
        data = json.dumps(self.service.main_keyboard(), ensure_ascii=False)
        for expected in ("Стан ПК", "Codex GPT", "SSH", "Розумний будинок", "Аудит"):
            self.assertIn(expected, data)

    def test_arbitrary_command_requires_confirmation(self):
        self.service.handle_message({"from": {"id": self.owner}, "chat": {"id": self.owner, "type": "private"}, "text": "/uitvoeren Get-Date"})
        self.assertEqual(1, len(self.service.pending))
        markup = self.api.calls[-1][2]
        self.assertIn("confirm:", json.dumps(markup))

    def test_redacts_bot_tokens(self):
        token = "1234567:" + "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghi"
        self.assertNotIn(token, bot.redact(token))

    def test_ssh_host_validation_pattern(self):
        self.service.wizards[self.owner] = {"step": "host", "name": "Server"}
        self.assertTrue(self.service.wizard_message(self.owner, "user@host.example"))
        self.assertEqual("port", self.service.wizards[self.owner]["step"])


if __name__ == "__main__": unittest.main()
