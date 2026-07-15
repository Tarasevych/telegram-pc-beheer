# Tarasevych Slimme Woning integration

The two bots intentionally keep separate BotFather identities, tokens, runtimes, and permissions. The home bot controls only accepted capability routes and never shares provider secrets with the GPT bot.

Integration layers:

1. The GPT bot has a live URL button to the home bot. The reciprocal button is present in local `Code.gs` and passed the 123/123 suite, but still requires the normal Apps Script release together with the current provider work; it is not claimed as live.
2. Shared status semantics and a local JSONL event stream.
3. A future adapter to the local core over MQTT or signed HTTPS.
4. The independent Telegram/Apps Script/Tuya home channel continues when the PC bot is unavailable.

Bots API does not deliver one bot's messages to another bot. A shared chat is therefore not a failover transport. Proper failover uses an independently authenticated adapter, `bericht_id` deduplication, `opstart_id + volgnummer` ordering, and fresh physical readback.
