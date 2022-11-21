## Kotankt
svante.geisshirt@regionh.dk

## Motivation
Dette python program opdatere opgaver's EAN/GLN og Omkostningssted (PSP) i 
dalux med det som findes i indmeldinger med tilsvarende ID.

## Kørsel
### config.py
Programmet skal konfigurers og her skal din API nøgle samt brugernavnet til din computer indtastes.

Du kan nu køre programmet med følgende kommando:
`python3 src/main.py [id]`

hvor `id` er det ID du ønsker programmet starter fra.

Alternativt kan programmet køres i baggrunden på maskinen med:
`./run.sh`

## Log
En log fil med navnet `workorder.log` genereres og her gemmes der dato med tidsstempel på hvornår en given opgave er blevet behandlet.
