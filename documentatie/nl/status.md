# Huidige acceptatiestatus

**Taal:** Nederlands | [Українська (Oekraïens)](../uk/стан.md) | [Nederlands overzicht (LEESMIJ.nl.md)](../../LEESMIJ.nl.md) | [Hoofdpagina (README.md)](../../README.md)

## Gecontroleerd op 15 juli 2026

- `@tarasevych_gpt_bot` is aangemaakt en de aanroep `getMe` via de Telegram Bot-interface slaagt;
- de Oekraïense profielbeschrijving en zes Bot-opdrachten zijn actief ingesteld;
- langdurige opvraging is actief, het terugroep-adres is leeg en er staan nul onverwerkte berichten in de wachtrij;
- de geplande Windows-taak `TelegramBeheer` heeft de status `Running`, draait met beperkte rechten en blijft werken op batterijvoeding;
- alle zes interactieve knoppen van het hoofdmenu gaven direct de juiste antwoorden;
- de snelkoppelingsknop voor de slimme woning verwijst naar `@tarasevych_Slimme_Woning_bot?start=pcbeheer`;
- een vrije `Write-Output`-opdracht werd pas uitgevoerd na een verse bevestiging via een drukknop;
- een directe Codex-aanroep stuurde het verwachte controleresultaat terug via Telegram;
- de integriteitscontrole van SQLite (`PRAGMA integrity_check`) gaf `ok` terug en het logboek en het gebeurtenissenbestand bevatten geldige registraties;
- lokale eenheidstests van de pc-bot: 5 van 5 geslaagd; aangrenzende testreeks van Slimme Woning: 123 van 123 geslaagd;
- de openbare hoofdvertakking op GitHub is gecontroleerd op revisiecode en HTTP 200; persoonlijke uitvoeringsinstellingen ontbreken volledig.

## Nog afhankelijk van externe gegevens

- Een daadwerkelijk extern SSH-doel vereist echte gegevens voor adres, gebruiker, poort en geautoriseerde sleutel;
- de omgekeerde snelkoppelingsknop in de woningbot is in de lokale broncode getest, maar de uitrol naar Apps Script wordt bewust gescheiden gehouden van lopende leverancierswijzigingen.

## Overige documentatie

- [Architectuur en systeemgrenzen](architectuur.md)
- [Installatie en configuratie](installatie.md)
- [Beveiliging en privégegevens](veiligheid.md)
- [SSH-verbindingen en externe apparaten](ssh.md)
- [Codex GPT](codex.md)
- [Koppeling met Slimme Woning](slimme-woning.md)
- [Herstel en controle](herstel.md)
