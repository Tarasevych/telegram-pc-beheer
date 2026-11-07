# Koppeling met Tarasevych Slimme Woning

**Taal:** Nederlands | [Українська (Oekraïens)](../uk/розумний-дім.md) | [Nederlands overzicht (LEESMIJ.nl.md)](../../LEESMIJ.nl.md) | [Hoofdpagina (README.md)](../../README.md)

De twee bots behouden bewust gescheiden identiteiten bij `@BotFather`, afzonderlijke toegangssleutels, eigen uitvoeringsomgevingen en strikt gescheiden bevoegdheden. De woningbot bedient uitsluitend goedgekeurde apparaatroutes en deelt nooit leveranciersgeheimen met de pc-beheerbot.

## Integratielagen

1. De pc-beheerbot beschikt over een werkende snelkoppelingsknop naar de woningbot. De omgekeerde knop is al opgenomen in het lokale bestand `Code.gs` en heeft alle 123 eenheidstests doorstaan, maar wordt pas geactiveerd bij de reguliere uitrol van het Apps Script-project.
2. Gedeelde statusbetekenissen en een lokale gebeurtenissenstroom in JSONL-formaat.
3. Een toekomstige koppeling naar het lokale kernsysteem via MQTT of ondertekend HTTPS.
4. Het onafhankelijke besturingskanaal van de woning (Telegram / Apps Script / Tuya) blijft volledig doorwerken wanneer de pc-bot uitgeschakeld is.

De Telegram Bot-interface stuurt nooit berichten van de ene bot door naar een andere bot. Een gezamenlijke groepschat kan daarom niet als reserveverbinding dienen. Een deugdelijke reserveverbinding maakt gebruik van een onafhankelijk geauthenticeerde koppeling, ontdubbeling op basis van `bericht_id`, volgordecontrole via `opstart_id + volgnummer` en een verse teruglezing van de daadwerkelijke fysieke apparaatstatus.

## Overige documentatie

- [Architectuur en systeemgrenzen](architectuur.md)
- [Installatie en configuratie](installatie.md)
- [Beveiliging en privégegevens](veiligheid.md)
- [SSH-verbindingen en externe apparaten](ssh.md)
- [Codex GPT](codex.md)
- [Herstel en controle](herstel.md)
- [Huidige acceptatiestatus](status.md)
