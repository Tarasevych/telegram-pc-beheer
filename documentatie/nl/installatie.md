# Installatie en configuratie

**Taal:** Nederlands | [Українська (Oekraïens)](../uk/встановлення.md) | [Nederlands overzicht (LEESMIJ.nl.md)](../../LEESMIJ.nl.md) | [Hoofdpagina (README.md)](../../README.md)

## Vereisten

- Windows 11 met Python 3.13 of een compatibele versie van Python;
- het Python-pakket `keyring`;
- de ingebouwde OpenSSH-client van Windows;
- een lokaal geïnstalleerde en aangemelde Codex-opdrachtregel;
- een persoonlijke Telegram-bot, aangemaakt via `@BotFather`.

## Geheimen en instellingen

1. Kopieer `configuratie/instellingen.voorbeeld.json` naar `configuratie/instellingen.json`.
2. Vul het juiste numerieke Telegram-identificatienummer van de eigenaar en de gewenste werkmap in.
3. Voer `gereedschap/configureren.py` uit. De toegangssleutel van de bot wordt onzichtbaar ingevoerd en opgeslagen in het Windows-referentiebeheer onder de dienstnaam `TelegramBeheer` en gebruikersnaam `bot_token`.
4. Neem `instellingen.json` of `ssh-doelen.json` nooit op in versiebeheer.

De Oekraïense beschrijving en het opdrachtenmenu van de bot worden automatisch ingesteld bij het opstarten van de achtergronddienst.

## Automatisch opstarten

Het script `installeren.ps1` maakt de geplande taak `TelegramBeheer` aan voor de huidige Windows-gebruiker. Deze taak draait met beperkte rechten, blijft actief op batterijvoeding, negeert dubbele gelijktijdige processen en start zichzelf automatisch opnieuw op na een storing.

```powershell
& '.\installeren.ps1'
Get-ScheduledTask -TaskName TelegramBeheer
Get-ScheduledTaskInfo -TaskName TelegramBeheer
```

## Instellingen bij BotFather

Gebruik een Oekraïense weergavenaam, beschrijving en opdrachtenlijst. De technische gebruikersnaam in Telegram moet uit Latijnse tekens bestaan en eindigen op `bot`. Breng de toegangssleutel na aanmaak direct over naar het Windows-referentiebeheer en bewaar deze nooit in notities, chatgeschiedenis, `.env`-bestanden of broncodebeheer.

## Overige documentatie

- [Architectuur en systeemgrenzen](architectuur.md)
- [Beveiliging en privégegevens](veiligheid.md)
- [SSH-verbindingen en externe apparaten](ssh.md)
- [Codex GPT](codex.md)
- [Koppeling met Slimme Woning](slimme-woning.md)
- [Herstel en controle](herstel.md)
- [Huidige acceptatiestatus](status.md)
