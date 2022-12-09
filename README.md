## Kontakt
svante.geisshirt@regionh.dk

## Motivation
Dette python program opdatere opgaver's EAN/GLN og Omkostningssted (PSP) i dalux med det som findes i indmeldinger med tilsvarende ID.

## Kørsel
Programmet skal konfigurers flere steder:
* i `src/config.py` skal din REST API nøgle indtastes. 
* i `setup/emails.txt` skal alle email-adresser som du ønsker skal modtage en email hvis robotten genstartes indtastes.
* i `setup/indmeldelse.service` samt `setup/run` skal stien til dette repository indtastes.

Programmet skal dernæst sættes op ved at kopiere `setup/indmeldelse.service` til `/etc/systemd/system/indmeldelse.service`. De følgende 3 kommandoer bruges til starte, stoppe og tjekke dets status:
* `systemctl start indmeldelse.service`
* `systemctl stop indmeldelse.service`
* `systemctl status indmeldelse.service`

## Log
Programmet genere to log-filer.
* `workorder.log` som indeholder de workorders, der bliver behandlet samt evt. opdateringer og et tidsstempel.
* `run.log` som indeholder en komplet log.