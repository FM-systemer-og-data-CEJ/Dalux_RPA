## Kotankt
svante.geisshirt@regionh.dk

## Motivation
Dette python program opdatere opgaver's EAN/GLN og Omkostningssted (PSP) i 
dalux med det som findes i indmeldinger med tilsvarende ID.

## Kørsel
Programmet skal konfigurers i filen `config.py` og her skal din API nøgle indtastes. Derudover kan du indtaste de email-adresser
som skal modtage en email hvis robotten crasher i emails.txt. 

Programmet køres i baggrunden på maskinen med `./run.sh [id]` hvor `id` er det ID du ønsker programmet starter fra.

Programmet kan tilsvarende lukkes igen med `./stop.sh`. NB: du vil modtage en email.

## Log
En log fil med navnet `workorder.log` genereres og her gemmes der dato med tidsstempel på hvornår en given opgave er blevet behandlet.
