# Beveiliging en bescherming van privégegevens

**Taal:** Nederlands | [Українська (Oekraïens)](../uk/безпека.md) | [Beveiligingsbeleid (BEVEILIGING.nl.md)](../../BEVEILIGING.nl.md) | [Hoofdpagina (README.md)](../../README.md)

## Overzicht van privégegevens en openbare bestanden

| Gegevenstype | Besloten opslaglocatie | Inhoud in openbare opslagplaats |
|---|---|---|
| Toegangssleutel van de bot | Windows-referentiebeheer | Enkel de naam van de dienst en sleutelvermelding |
| Telegram-identificatienummer van eigenaar | Lokaal bestand `instellingen.json` | Fictief voorbeeldgetal |
| SSH-adres, gebruiker, poort en sleutelpad | Lokaal bestand `ssh-doelen.json` | Leeg sjabloon `[]` |
| Privésleutel voor SSH | Standaard lokale sleutelmap van de gebruiker | Nooit opgenomen |
| MTProto-sessie en toepassingsgegevens | Afzonderlijk besloten Telegram-project | Nooit opgenomen |
| Logboek en gebeurtenissen | Lokale map `gegevens/` | Uitsluitend het veldschema |
| Toegangssleutels en apparaatnummers van slimme woning | Besloten opslag van de betreffende koppeling | Nooit opgenomen |

## Dreigingsmodel en tegenmaatregelen

- **Overname van het Telegram-account van de eigenaar:** een aanvaller zou in theorie namens de eigenaar kunnen handelen. Bescherming bestaat uit tweestapsverificatie in Telegram, regelmatige controle van aangemelde apparaten, kortstondig geldige bevestigingsknoppen, lokale logboekregistratie en de noodstopopdracht.
- **Uitlekken van de toegangssleutel van de bot:** trek de sleutel onmiddellijk in via `@BotFather`, werk de waarde in het Windows-referentiebeheer bij en herstart de taak `TelegramBeheer`.
- **Opdrachtinjectie in Codex of de opdrachtregel:** vrije PowerShell-opdrachten vereisen handmatige bevestiging; Codex is beperkt tot de ingestelde werkmap; veelvoorkomende patronen van geheime sleutels worden automatisch uit de tekstuitvoer weggefilterd.
- **Vervalsing van een SSH-doelcomputer:** de systeemcontrole van `known_hosts` blijft strikt ingeschakeld; schakel `StrictHostKeyChecking` nooit uit.
- **Herhaald gebruik van een bevestigingsknop:** elke bevestigingscode is eenmalig bruikbaar, gekoppeld aan het identificatienummer van de eigenaar en verloopt na 120 seconden.

## Noodstop

```powershell
Stop-ScheduledTask -TaskName TelegramBeheer
```

Controleer na een beveiligingsincident altijd de aangemelde apparaten in Telegram, de sleutel bij `@BotFather`, het Windows-referentiebeheer, de bestanden `authorized_keys` op externe systemen en het lokale SQLite-logboek.

## Overige documentatie

- [Architectuur en systeemgrenzen](architectuur.md)
- [Installatie en configuratie](installatie.md)
- [SSH-verbindingen en externe apparaten](ssh.md)
- [Codex GPT](codex.md)
- [Koppeling met Slimme Woning](slimme-woning.md)
- [Herstel en controle](herstel.md)
- [Huidige acceptatiestatus](status.md)
