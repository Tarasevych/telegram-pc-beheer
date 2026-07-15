# Codex GPT

`/codex prompt` starts the locally installed official Codex CLI as an ephemeral session. The bot discovers the current local `codex.exe`, passes the configured workspace, and returns the final textual result to Telegram.

Current policy:

- sandbox: `workspace-write`;
- approval: `never`, so a headless run fails instead of waiting for an invisible dialog;
- no `danger-full-access`;
- no web search by default;
- configurable timeout;
- long output is truncated before Telegram delivery.

This provides substantial file and code management but is not a pixel-for-pixel duplicate of every Codex Desktop feature. Official `codex remote-control` can remain an independent backup channel and must not share the Telegram bot token.

