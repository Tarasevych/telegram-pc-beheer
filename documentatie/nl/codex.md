# Codex GPT

**Taal:** Nederlands | [Українська (Oekraïens)](../uk/кодекс-ші.md) | [Nederlands overzicht (LEESMIJ.nl.md)](../../LEESMIJ.nl.md) | [Hoofdpagina (README.md)](../../README.md)

De opdracht `/codex verzoek` start de lokaal geïnstalleerde officiële Codex-opdrachtregel als een eenmalige sessie. De bot zoekt automatisch het actuele programmabestand `codex.exe` in de lokale programmamap, geeft de ingestelde werkmap door en stuurt het uiteindelijke tekstresultaat terug naar Telegram.

## Huidig uitvoeringsbeleid

- **Afscherming:** `workspace-write` (schrijven is uitsluitend toegestaan binnen de ingestelde werkmap);
- **Goedkeuring:** `never` (zodat een achtergrondproces niet blijft wachten op een onzichtbaar dialoogvenster);
- **Geen volledige systeemtoegang:** `danger-full-access` wordt nooit ingeschakeld;
- **Geen internetzoekopdrachten:** standaard uitgeschakeld (geen `--search`);
- **Tijdslimiet:** instelbaar via het lokale configuratiebestand;
- **Ingekorte uitvoer:** te lange antwoorden worden netjes ingekort vóór verzending naar Telegram, terwijl de volledige uitvoer lokaal behouden blijft.

Dit biedt uitgebreide mogelijkheden voor bestands- en codebeheer op afstand, zonder elke grafische functie van de bureaubladtoepassing na te bouwen. De officiële functie `codex remote-control` kan als zelfstandig reservekanaal dienen en mag nooit de toegangssleutel van de Telegram-bot delen.

## Overige documentatie

- [Architectuur en systeemgrenzen](architectuur.md)
- [Installatie en configuratie](installatie.md)
- [Beveiliging en privégegevens](veiligheid.md)
- [SSH-verbindingen en externe apparaten](ssh.md)
- [Koppeling met Slimme Woning](slimme-woning.md)
- [Herstel en controle](herstel.md)
- [Huidige acceptatiestatus](status.md)
