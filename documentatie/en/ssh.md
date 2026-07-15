# SSH connections

Only Windows OpenSSH Client is required. The bot neither installs nor exposes an SSH Server.

The `SSH → Add SSH` wizard asks for:

1. display name;
2. `host.com` or `user@host.com`;
3. port, or `-` for 22;
4. full private-key path, or `-` for ssh-agent/default key discovery.

The test runs non-interactive `ssh` with `BatchMode=yes` and `ConnectTimeout=8`. Success proves TCP connectivity, host-key acceptance under the local policy, and public-key authorization in the remote host's `authorized_keys`.

Never send a private key through Telegram. For first-time host-key acceptance, connect locally over a trusted network, verify the fingerprint out of band, and only then retain the `known_hosts` entry.

