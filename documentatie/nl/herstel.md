# Herstel en controle

**Taal:** Nederlands | [Українська (Oekraïens)](../uk/відновлення.md) | [Nederlands overzicht (LEESMIJ.nl.md)](../../LEESMIJ.nl.md) | [Hoofdpagina (README.md)](../../README.md)

## Stappenplan na herstart of storing

1. Controleer de geplande taak in Windows met `Get-ScheduledTask -TaskName TelegramBeheer`.
2. Verifieer dat de toegangssleutel van de bot in het Windows-referentiebeheer staat en niet in een tekstbestand.
3. Stuur `/status` in Telegram en open de knoppen voor SSH en hulp.
4. Voer een onschadelijke bevestigde `Write-Output`-opdracht uit.
5. Start een korte `/codex`-opdracht en controleer het teruggezonden tekstresultaat.
6. Voer voor elk opgeslagen SSH-profiel een verbindingstest op basis van sleutels uit.
7. Bekijk `/audit` en voer lokaal een integriteitscontrole uit op de SQLite-gegevensbank.

## Controles vóór vrijgave

```powershell
& '..\.venv\Scripts\python.exe' -m py_compile '.\bron\beheer_bot.py'
& '..\.venv\Scripts\python.exe' -m unittest discover -s tests -v
rg -n "\b[0-9]{7,12}:[A-Za-z0-9_-]{30,}\b" .
```

De openbare uitgave wordt pas goedgekeurd nadat het GitHub-adres, alle tweetalige verwijzingen (Oekraïens en Nederlands), de controle op afwezigheid van geheimen en de revisiecode ten opzichte van de lokale hoofdversie volledig zijn geverifieerd.

## Overige documentatie

- [Architectuur en systeemgrenzen](architectuur.md)
- [Installatie en configuratie](installatie.md)
- [Beveiliging en privégegevens](veiligheid.md)
- [SSH-verbindingen en externe apparaten](ssh.md)
- [Codex GPT](codex.md)
- [Koppeling met Slimme Woning](slimme-woning.md)
- [Huidige acceptatiestatus](status.md)
