from __future__ import annotations

import ctypes
import datetime as dt
import html
import json
import os
import platform
import re
import secrets
import shutil
import socket
import sqlite3
import subprocess
import sys
import threading
import time
import traceback
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

import keyring


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "configuratie" / "instellingen.json"
SSH_TARGETS = ROOT / "configuratie" / "ssh-doelen.json"
DATA = ROOT / "gegevens"
AUDIT = DATA / "audit.sqlite3"
EVENTS = DATA / "gebeurtenissen.jsonl"
SERVICE = "TelegramBeheer"
START_ID = secrets.token_hex(8)


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def load_json(path: Path, fallback: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return fallback


def save_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temp.replace(path)


def redact(value: str) -> str:
    value = re.sub(r"\b\d{6,12}:[A-Za-z0-9_-]{30,}\b", "[BOT_TOKEN]", value)
    value = re.sub(r"(?i)(password|passwd|token|secret|api[_-]?key)\s*[:=]\s*\S+", r"\1=[ПРИХОВАНО]", value)
    return value


class AuditLog:
    def __init__(self, path: Path | None = None) -> None:
        path = path or AUDIT
        path.parent.mkdir(parents=True, exist_ok=True)
        self.path = path
        db = sqlite3.connect(path)
        try:
            db.execute("PRAGMA journal_mode=WAL")
            db.execute("CREATE TABLE IF NOT EXISTS audit (id INTEGER PRIMARY KEY, tijd TEXT NOT NULL, actor INTEGER, actie TEXT NOT NULL, status TEXT NOT NULL, detail TEXT NOT NULL)")
            db.commit()
        finally:
            db.close()

    def write(self, actor: int | None, action: str, status: str, detail: str = "") -> None:
        db = sqlite3.connect(self.path)
        try:
            db.execute("INSERT INTO audit(tijd,actor,actie,status,detail) VALUES(?,?,?,?,?)", (now_iso(), actor, action[:80], status[:32], redact(detail)[:2000]))
            db.commit()
        finally:
            db.close()

    def recent(self, limit: int = 10) -> list[tuple]:
        db = sqlite3.connect(self.path)
        try:
            return db.execute("SELECT tijd,actie,status FROM audit ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
        finally:
            db.close()


class TelegramAPI:
    def __init__(self, token: str) -> None:
        self.base = f"https://api.telegram.org/bot{token}/"

    def call(self, method: str, **payload: Any) -> Any:
        clean = {k: json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v for k, v in payload.items() if v is not None}
        request = urllib.request.Request(self.base + method, urllib.parse.urlencode(clean).encode("utf-8"))
        with urllib.request.urlopen(request, timeout=45) as response:
            body = json.loads(response.read().decode("utf-8"))
        if not body.get("ok"):
            raise RuntimeError(f"Telegram {method}: {body.get('description', 'невідома помилка')}")
        return body.get("result")

    def send(self, chat_id: int, text: str, keyboard: dict | None = None) -> Any:
        return self.call("sendMessage", chat_id=chat_id, text=text, parse_mode="HTML", disable_web_page_preview=True, reply_markup=keyboard)


class BeheerBot:
    def __init__(self, api: TelegramAPI, config: dict[str, Any]) -> None:
        self.api = api
        self.config = config
        self.owners = {int(x) for x in config["eigenaar_ids"]}
        self.audit = AuditLog()
        self.pending: dict[str, dict[str, Any]] = {}
        self.wizards: dict[int, dict[str, Any]] = {}
        self.sequence = 0

    def keyboard(self, rows: list[list[tuple[str, str, bool]]]) -> dict:
        output = []
        for row in rows:
            buttons = []
            for label, value, is_url in row:
                buttons.append({"text": label, "url" if is_url else "callback_data": value})
            output.append(buttons)
        return {"inline_keyboard": output}

    def main_keyboard(self) -> dict:
        home = self.config["slimme_woning_bot"]
        return self.keyboard([
            [("💻 Стан ПК", "menu:status", False), ("🧠 Codex GPT", "menu:codex", False)],
            [("🔐 SSH", "menu:ssh", False), ("🧰 Команди", "menu:commands", False)],
            [("🏠 Розумний будинок", f"https://t.me/{home}?start=pcbeheer", True)],
            [("📜 Аудит", "menu:audit", False), ("ℹ️ Довідка", "menu:help", False)],
        ])

    def send(self, chat_id: int, text: str, keyboard: dict | None = None) -> None:
        maximum = int(self.config.get("max_antwoordtekens", 3500))
        safe = redact(text)
        if len(safe) > maximum:
            safe = safe[:maximum - 80] + "\n\n<i>Вивід скорочено; повна версія лишилася локально.</i>"
        self.api.send(chat_id, safe, keyboard)

    def event(self, actor: int, function: str, action: str, target: str, status: str) -> None:
        self.sequence += 1
        record = {"opstart_id": START_ID, "volgnummer": self.sequence, "bericht_id": secrets.token_hex(12), "tijd": now_iso(), "actor": str(actor), "functie": function, "actie": action, "doel": target, "status": status}
        EVENTS.parent.mkdir(parents=True, exist_ok=True)
        with EVENTS.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(record, ensure_ascii=False) + "\n")

    def is_authorized(self, user_id: int, chat: dict[str, Any]) -> bool:
        return user_id in self.owners and chat.get("type") == "private"

    def status_text(self) -> str:
        total, used, free = shutil.disk_usage(Path.home().anchor)
        uptime = "невідомо"
        try:
            raw = subprocess.check_output(["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", "(Get-Date)-(gcim Win32_OperatingSystem).LastBootUpTime | ForEach-Object { '{0} д {1} год {2} хв' -f $_.Days,$_.Hours,$_.Minutes }"], text=True, timeout=15)
            uptime = raw.strip()
        except Exception:
            pass
        return ("<b>💻 Стан цього ПК</b>\n\n"
                f"• Ім’я: <code>{html.escape(socket.gethostname())}</code>\n"
                f"• Система: {html.escape(platform.system() + ' ' + platform.release())}\n"
                f"• Працює: {html.escape(uptime)}\n"
                f"• Диск C: {free / 1024**3:.1f} ГіБ вільно з {total / 1024**3:.1f} ГіБ\n"
                f"• Бот: активний, owner-only\n"
                f"• SSH-клієнт: {'встановлено' if shutil.which('ssh') else 'відсутній'}")

    def help_text(self) -> str:
        return ("<b>ℹ️ Керування</b>\n\n"
                "/start — головне меню\n/status — стан ПК\n/processen — активні процеси\n/netwerk — мережа\n/opslag — диски\n"
                "/ssh — SSH-підключення\n/codex запит — доручити задачу Codex GPT\n"
                "/uitvoeren PowerShell — команда з окремим підтвердженням\n/audit — останні події\n/annuleren — скасувати майстер\n\n"
                "Небезпечні й довільні команди ніколи не виконуються одним повідомленням: потрібна свіжа кнопка підтвердження.")

    def run_powershell(self, chat_id: int, actor: int, command: str) -> None:
        timeout = int(self.config.get("opdracht_timeout_seconden", 90))
        self.audit.write(actor, "powershell", "ontvangen", command)
        self.event(actor, "pc.opdracht", "powershell", socket.gethostname(), "ontvangen")
        try:
            result = subprocess.run(["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", command], capture_output=True, text=True, timeout=timeout, encoding="utf-8", errors="replace")
            output = (result.stdout + ("\n" + result.stderr if result.stderr else "")).strip() or "Команда завершилась без текстового виводу."
            status = "uitgevoerd" if result.returncode == 0 else "mislukt"
            self.audit.write(actor, "powershell", status, f"rc={result.returncode}")
            self.event(actor, "pc.opdracht", "powershell", socket.gethostname(), status)
            self.send(chat_id, f"<b>{'✅ Виконано' if result.returncode == 0 else '⚠️ Помилка'}</b>\n<pre>{html.escape(output)}</pre>", self.main_keyboard())
        except subprocess.TimeoutExpired:
            self.audit.write(actor, "powershell", "verlopen", command)
            self.send(chat_id, "⌛ Час виконання команди вичерпано.", self.main_keyboard())
        except Exception as exc:
            self.audit.write(actor, "powershell", "mislukt", str(exc))
            self.send(chat_id, f"❌ Не вдалося виконати: <code>{html.escape(str(exc))}</code>", self.main_keyboard())

    def find_codex(self) -> str | None:
        base = Path(os.environ.get("LOCALAPPDATA", "")) / "OpenAI" / "Codex" / "bin"
        candidates = sorted(base.glob("*/codex.exe"), key=lambda p: p.stat().st_mtime, reverse=True)
        return str(candidates[0]) if candidates else shutil.which("codex")

    def run_codex(self, chat_id: int, actor: int, prompt: str) -> None:
        executable = self.find_codex()
        if not executable:
            self.send(chat_id, "❌ Локальний Codex CLI не знайдено.", self.main_keyboard()); return
        self.audit.write(actor, "codex", "ontvangen", prompt)
        workspace = str(self.config["werkmap"])
        command = [executable, "-s", "workspace-write", "-a", "never", "-C", workspace, "exec", "--ephemeral", "--skip-git-repo-check", "--color", "never", prompt]
        try:
            result = subprocess.run(command, capture_output=True, text=True, timeout=int(self.config.get("codex_timeout_seconden", 900)), encoding="utf-8", errors="replace")
            output = (result.stdout or result.stderr).strip() or "Codex завершив роботу без текстового підсумку."
            status = "uitgevoerd" if result.returncode == 0 else "mislukt"
            self.audit.write(actor, "codex", status, f"rc={result.returncode}")
            self.send(chat_id, f"<b>🧠 Codex GPT</b>\n\n<pre>{html.escape(output[-12000:])}</pre>", self.main_keyboard())
        except subprocess.TimeoutExpired:
            self.audit.write(actor, "codex", "verlopen", prompt)
            self.send(chat_id, "⌛ Codex не завершив задачу у відведений час.", self.main_keyboard())
        except Exception as exc:
            self.audit.write(actor, "codex", "mislukt", str(exc))
            self.send(chat_id, f"❌ Codex: <code>{html.escape(str(exc))}</code>", self.main_keyboard())

    def ssh_menu(self) -> tuple[str, dict]:
        targets = load_json(SSH_TARGETS, [])
        lines = ["<b>🔐 SSH-підключення з цього ПК</b>", "", "Підключення використовують системний OpenSSH-клієнт і ключі без копіювання секретів у Telegram."]
        rows = []
        for item in targets:
            lines.append(f"• {html.escape(item['naam'])}: <code>{html.escape(item['host'])}</code>:{item['poort']}")
            rows.append([(f"🔎 Перевірити {item['naam']}", f"ssh:test:{item['id']}", False)])
        if not targets:
            lines.append("\nЩе немає збережених віддалених пристроїв.")
        rows.extend([[("➕ Додати SSH", "ssh:add", False)], [("⬅️ Меню", "menu:home", False)]])
        return "\n".join(lines), self.keyboard(rows)

    def ssh_test(self, chat_id: int, actor: int, target_id: str) -> None:
        target = next((x for x in load_json(SSH_TARGETS, []) if x.get("id") == target_id), None)
        if not target:
            self.send(chat_id, "SSH-профіль не знайдено.", self.main_keyboard()); return
        cmd = ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=8", "-p", str(target["poort"])]
        if target.get("sleutelpad"):
            cmd += ["-i", target["sleutelpad"]]
        cmd += [target["host"], "echo TELEGRAM_BEHEER_SSH_OK"]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            ok = result.returncode == 0 and "TELEGRAM_BEHEER_SSH_OK" in result.stdout
            self.audit.write(actor, "ssh.test", "uitgevoerd" if ok else "mislukt", target["naam"])
            self.send(chat_id, ("✅ SSH-підключення і автентифікація працюють." if ok else "❌ SSH не підтверджено. Перевірте host, порт, ключ і authorized_keys."), self.ssh_menu()[1])
        except Exception as exc:
            self.audit.write(actor, "ssh.test", "mislukt", str(exc)); self.send(chat_id, f"❌ SSH: {html.escape(str(exc))}", self.ssh_menu()[1])

    def wizard_message(self, chat_id: int, text: str) -> bool:
        state = self.wizards.get(chat_id)
        if not state:
            return False
        if text == "/annuleren":
            self.wizards.pop(chat_id, None); self.send(chat_id, "Скасовано.", self.main_keyboard()); return True
        step = state["step"]
        if step == "name":
            state.update(name=text[:60], step="host"); self.send(chat_id, "Введіть ім’я хоста у форматі <code>host.com</code> або <code>user@host.com</code>."); return True
        if step == "host":
            if not re.fullmatch(r"(?:[A-Za-z0-9._-]+@)?[A-Za-z0-9._-]+", text):
                self.send(chat_id, "Некоректне ім’я хоста. Спробуйте ще раз або /annuleren."); return True
            state.update(host=text, step="port"); self.send(chat_id, "Введіть SSH-порт (звичайно 22) або надішліть <code>-</code>."); return True
        if step == "port":
            port = 22 if text == "-" else int(text) if text.isdigit() else 0
            if not 1 <= port <= 65535:
                self.send(chat_id, "Порт має бути від 1 до 65535."); return True
            state.update(port=port, step="key"); self.send(chat_id, "Введіть повний шлях до приватного ключа або <code>-</code>, щоб використати ssh-agent/типовий ключ."); return True
        if step == "key":
            key_path = "" if text == "-" else os.path.expandvars(text.strip('"'))
            if key_path and not Path(key_path).is_file():
                self.send(chat_id, "Файл ключа не знайдено. Вкажіть наявний повний шлях або <code>-</code>."); return True
            targets = load_json(SSH_TARGETS, [])
            targets.append({"id": secrets.token_hex(5), "naam": state["name"], "host": state["host"], "poort": state["port"], "sleutelpad": key_path})
            save_json(SSH_TARGETS, targets); self.wizards.pop(chat_id, None)
            self.send(chat_id, "✅ SSH-профіль збережено. Тепер перевірте його кнопкою.", self.ssh_menu()[1]); return True
        return False

    def handle_message(self, message: dict[str, Any]) -> None:
        user_id = int(message.get("from", {}).get("id", 0)); chat = message.get("chat", {}); chat_id = int(chat.get("id", 0)); text = str(message.get("text", "")).strip()
        if not self.is_authorized(user_id, chat):
            self.audit.write(user_id or None, "toegang", "geweigerd", str(chat.get("type"))); return
        if self.wizard_message(chat_id, text): return
        command, _, argument = text.partition(" "); command = command.split("@")[0].lower()
        if command in ("/start", "/menu", "/home"):
            self.send(chat_id, "<b>🤖 Tarasevych GPT — керування ПК</b>\n\nПриватний центр Codex, SSH, діагностики та майбутніх інтеграцій розумного будинку.", self.main_keyboard())
        elif command == "/status": self.send(chat_id, self.status_text(), self.main_keyboard())
        elif command == "/processen":
            out = subprocess.check_output(["powershell.exe", "-NoProfile", "-Command", "Get-Process | Sort-Object CPU -Descending | Select-Object -First 15 ProcessName,Id,CPU | Format-Table -HideTableHeaders"], text=True, timeout=20)
            self.send(chat_id, "<b>⚙️ Активні процеси</b>\n<pre>" + html.escape(out) + "</pre>", self.main_keyboard())
        elif command == "/netwerk":
            out = subprocess.check_output(["powershell.exe", "-NoProfile", "-Command", "Get-NetIPConfiguration | Where-Object IPv4Address | ForEach-Object { $_.InterfaceAlias + ': ' + $_.IPv4Address.IPAddress }"], text=True, timeout=20)
            self.send(chat_id, "<b>🌐 Мережа</b>\n<pre>" + html.escape(out) + "</pre>", self.main_keyboard())
        elif command == "/opslag":
            out = subprocess.check_output(["powershell.exe", "-NoProfile", "-Command", "Get-Volume | Where-Object DriveLetter | Select DriveLetter,FileSystemLabel,@{n='FreeGB';e={[math]::Round($_.SizeRemaining/1GB,1)}},@{n='SizeGB';e={[math]::Round($_.Size/1GB,1)}} | Format-Table -HideTableHeaders"], text=True, timeout=20)
            self.send(chat_id, "<b>💾 Накопичувачі</b>\n<pre>" + html.escape(out) + "</pre>", self.main_keyboard())
        elif command == "/ssh": self.send(chat_id, *self.ssh_menu())
        elif command == "/codex":
            if not argument: self.send(chat_id, "Надішліть: <code>/codex що саме треба зробити</code>", self.main_keyboard())
            else: self.send(chat_id, "🧠 Codex прийняв задачу. Результат надійде окремим повідомленням."); threading.Thread(target=self.run_codex, args=(chat_id, user_id, argument), daemon=True).start()
        elif command == "/uitvoeren":
            if not argument: self.send(chat_id, "Надішліть PowerShell-команду після <code>/uitvoeren</code>.", self.main_keyboard()); return
            if not self.config.get("volledig_beheer"): self.send(chat_id, "Повне керування вимкнено локально.", self.main_keyboard()); return
            nonce = secrets.token_urlsafe(8); self.pending[nonce] = {"actor": user_id, "chat": chat_id, "command": argument, "expires": time.time() + 120}
            keys = self.keyboard([[("✅ Виконати", f"confirm:{nonce}:yes", False), ("❌ Скасувати", f"confirm:{nonce}:no", False)]])
            self.send(chat_id, f"<b>Підтвердіть локальну команду</b>\n<pre>{html.escape(argument)}</pre>\nКнопка дійсна 2 хвилини.", keys)
        elif command == "/audit":
            rows = self.audit.recent(); body = "\n".join(f"• {r[0][11:19]} — {html.escape(r[1])}: {html.escape(r[2])}" for r in rows) or "Подій немає."
            self.send(chat_id, "<b>📜 Останній аудит</b>\n" + body, self.main_keyboard())
        else: self.send(chat_id, self.help_text(), self.main_keyboard())

    def handle_callback(self, query: dict[str, Any]) -> None:
        user_id = int(query.get("from", {}).get("id", 0)); message = query.get("message", {}); chat = message.get("chat", {}); chat_id = int(chat.get("id", 0)); data = str(query.get("data", ""))
        try: self.api.call("answerCallbackQuery", callback_query_id=query.get("id"), text="Готово")
        except Exception: pass
        if not self.is_authorized(user_id, chat): self.audit.write(user_id, "callback", "geweigerd", data); return
        if data in ("menu:home",): self.send(chat_id, "Головне меню", self.main_keyboard())
        elif data == "menu:status": self.send(chat_id, self.status_text(), self.main_keyboard())
        elif data == "menu:codex": self.send(chat_id, "<b>🧠 Codex GPT</b>\n\nНадішліть <code>/codex ваш запит</code>. Codex працює у вибраній робочій папці та повертає підсумок сюди.", self.main_keyboard())
        elif data == "menu:ssh": self.send(chat_id, *self.ssh_menu())
        elif data == "menu:commands": self.send(chat_id, self.help_text(), self.main_keyboard())
        elif data == "menu:help": self.send(chat_id, self.help_text(), self.main_keyboard())
        elif data == "menu:audit":
            rows = self.audit.recent(); self.send(chat_id, "<b>📜 Аудит</b>\n" + ("\n".join(f"• {r[0][11:19]} — {html.escape(r[1])}: {html.escape(r[2])}" for r in rows) or "Подій немає."), self.main_keyboard())
        elif data == "ssh:add": self.wizards[chat_id] = {"step": "name"}; self.send(chat_id, "Введіть відображувану назву SSH-підключення. Для скасування: /annuleren")
        elif data.startswith("ssh:test:"): threading.Thread(target=self.ssh_test, args=(chat_id, user_id, data.split(":", 2)[2]), daemon=True).start()
        elif data.startswith("confirm:"):
            _, nonce, answer = data.split(":", 2); pending = self.pending.pop(nonce, None)
            if not pending or pending["actor"] != user_id or pending["expires"] < time.time(): self.send(chat_id, "⌛ Підтвердження недійсне або застаріло.", self.main_keyboard()); return
            if answer != "yes": self.audit.write(user_id, "powershell", "geweigerd", "скасовано власником"); self.send(chat_id, "Команду скасовано.", self.main_keyboard()); return
            self.send(chat_id, "⏳ Виконую підтверджену команду…"); threading.Thread(target=self.run_powershell, args=(chat_id, user_id, pending["command"]), daemon=True).start()

    def process_update(self, update: dict[str, Any]) -> None:
        if "message" in update: self.handle_message(update["message"])
        elif "callback_query" in update: self.handle_callback(update["callback_query"])


def acquire_mutex() -> Any:
    handle = ctypes.windll.kernel32.CreateMutexW(None, False, "Local\\TarasevychTelegramBeheer")
    if not handle or ctypes.windll.kernel32.GetLastError() == 183:
        raise SystemExit("TelegramBeheer вже запущено.")
    return handle


def configure_profile(api: TelegramAPI) -> None:
    commands = [
        {"command": "start", "description": "Головне меню"}, {"command": "status", "description": "Стан цього ПК"},
        {"command": "ssh", "description": "SSH-підключення"}, {"command": "codex", "description": "Задача для Codex GPT"},
        {"command": "uitvoeren", "description": "PowerShell із підтвердженням"}, {"command": "audit", "description": "Журнал безпеки"},
    ]
    api.call("setMyCommands", commands=commands, language_code="uk")
    api.call("setMyDescription", description="Приватний україномовний центр віддаленого керування ПК: Codex GPT, SSH, діагностика, аудит і міст до Tarasevych Slimme Woning.", language_code="uk")
    api.call("setMyShortDescription", short_description="Codex GPT, SSH і безпечне керування вашим ПК", language_code="uk")


def main() -> None:
    mutex = acquire_mutex()
    config = load_json(CONFIG, {})
    token = keyring.get_password(SERVICE, "bot_token")
    if not token: raise SystemExit("У Windows Credential Manager немає TelegramBeheer/bot_token")
    api = TelegramAPI(token); bot = BeheerBot(api, config)
    api.call("deleteWebhook", drop_pending_updates=False)
    configure_profile(api)
    offset = 0; bot.audit.write(None, "dienst", "opgestart", START_ID)
    while True:
        try:
            updates = api.call("getUpdates", offset=offset, timeout=30, allowed_updates=["message", "callback_query"])
            for update in updates:
                offset = max(offset, int(update["update_id"]) + 1)
                try: bot.process_update(update)
                except Exception as exc: bot.audit.write(None, "update", "mislukt", f"{exc}\n{traceback.format_exc()}")
        except KeyboardInterrupt: break
        except Exception as exc:
            bot.audit.write(None, "polling", "mislukt", str(exc)); time.sleep(5)
    ctypes.windll.kernel32.CloseHandle(mutex)


if __name__ == "__main__":
    main()
