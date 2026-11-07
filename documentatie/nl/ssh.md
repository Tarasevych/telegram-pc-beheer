# SSH-verbindingen en externe apparaten

**Taal:** Nederlands | [Українська (Oekraïens)](../uk/захищене-зєднання-ssh.md) | [Nederlands overzicht (LEESMIJ.nl.md)](../../LEESMIJ.nl.md) | [Hoofdpagina (README.md)](../../README.md)

Op de computer is uitsluitend de standaard OpenSSH-client van Windows vereist. De bot installeert of opent geen enkele SSH-server voor inkomende verbindingen.

## Een nieuw SSH-doel toevoegen

De stapsgewijze hulpfunctie `SSH → Додати SSH` vraagt achtereenvolgens om:

1. de weergavenaam;
2. het adres in de vorm `host.com` of `user@host.com`;
3. het poortnummer, of `-` voor standaardpoort 22;
4. het volledige pad naar de privésleutel, of `-` om de standaard sleutelagent te gebruiken.

## Werking van de verbindingstest

De controle voert een niet-interactieve `ssh`-opdracht uit met `BatchMode=yes` en `ConnectTimeout=8`. Een geslaagde test bewijst dat de TCP-verbinding tot stand komt, de serversleutel volgens het lokale beveiligingsbeleid wordt geaccepteerd en aanmelding met de publieke sleutel is toegestaan in `authorized_keys` op het externe apparaat.

Verstuur nooit een privésleutel via Telegram. Maak voor de eerste acceptatie van een nieuwe serversleutel lokaal verbinding via een vertrouwd netwerk, controleer de vingerafdruk van de sleutel buiten Telegram om en sla pas daarna de vermelding op in `known_hosts`.

## Overige documentatie

- [Architectuur en systeemgrenzen](architectuur.md)
- [Installatie en configuratie](installatie.md)
- [Beveiliging en privégegevens](veiligheid.md)
- [Codex GPT](codex.md)
- [Koppeling met Slimme Woning](slimme-woning.md)
- [Herstel en controle](herstel.md)
- [Huidige acceptatiestatus](status.md)
