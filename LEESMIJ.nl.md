# Tarasevych GPT — pc-beheer via Telegram

**Taal:** Nederlands | [Українська (Oekraïens)](ОГЛЯД.uk.md) | [Tweetalig overzicht (README.md)](README.md) | [Beveiligingsbeleid (BEVEILIGING.nl.md)](BEVEILIGING.nl.md)

Dit project vormt een persoonlijk besturingscentrum voor de Windows-pc van de eigenaar via Telegram. De gebruikersteksten zijn in het Oekraïens opgesteld; technische bestandspaden en interne aanduidingen gebruiken het Nederlands waar Cyrillische tekens ongeschikt zijn.

## Geïmplementeerde mogelijkheden

- toegang uitsluitend voor de eigenaar op basis van exacte Telegram-identificatienummers in privégesprekken;
- keuzemenu's voor pc-status, actieve processen, netwerk, opslag, SSH, Codex, logboekcontrole en de slimme woning;
- uitvoering van vrije PowerShell-opdrachten uitsluitend na een verse drukknopbevestiging die na twee minuten verloopt;
- aansturing van de lokale Codex-opdrachtregel binnen een afgebakende werkmap met `workspace-write`-afscherming;
- een stapsgewijze SSH-hulpfunctie voor weergavenaam, `user@host`, poortnummer en het pad naar de privésleutel;
- opslag van de toegangssleutel van de bot uitsluitend in het Windows-referentiebeheer;
- SQLite-logboekregistratie, automatische maskering van geheimen in uitvoerteksten en een vergrendeling tegen dubbele procesinstanties;
- automatisch opstarten via Windows Taakplanner, herstart bij storingen en ononderbroken werking op batterijvoeding;
- een directe snelkoppeling naar de afzonderlijke bot voor de slimme woning, een voorbereide terugkoppeling in de lokale broncode daarvan en een leveranciersonafhankelijk gebeurteniscontract.

## Documentatie

- [Architectuur en systeemgrenzen](documentatie/nl/architectuur.md)
- [Installatie en configuratie](documentatie/nl/installatie.md)
- [Beveiliging en bescherming van privégegevens](documentatie/nl/veiligheid.md)
- [SSH-verbindingen en externe apparaten](documentatie/nl/ssh.md)
- [Codex GPT](documentatie/nl/codex.md)
- [Koppeling met Slimme Woning](documentatie/nl/slimme-woning.md)
- [Herstel en controle](documentatie/nl/herstel.md)
- [Huidige acceptatiestatus](documentatie/nl/status.md)
- [Beveiligingsbeleid](BEVEILIGING.nl.md)

## Snelle lokale verificatie

```powershell
& '..\.venv\Scripts\python.exe' -m unittest discover -s tests -v
& '.\installeren.ps1'
Get-ScheduledTask -TaskName TelegramBeheer
```

Een daadwerkelijke acceptatietest voor SSH vereist het externe adres, de gebruikersnaam, het poortnummer en een geautoriseerde sleutel. Deze gegevens worden bewust nooit in deze opslagplaats opgenomen.
