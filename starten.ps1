$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Python = Join-Path (Split-Path -Parent $Root) '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $Python)) { throw "Python-omgeving niet gevonden: $Python" }
& $Python (Join-Path $Root 'bron\beheer_bot.py')

