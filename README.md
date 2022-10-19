## Kotankt
svante.geisshirt@regionh.dk

## Motivering
Dette python program opdatere opgaver's EAN/GLN og Omkostningssted (PSP) i 
dalux med det som findes i indmeldinger med tilsvarende ID. Programmet 
iterer fra det givet ID til der ikke findes flere gyldige ID'er.

## Kørsel
For at køre dette program lokalt på din maskine skal du sørge for at have
følgende installeret (evt. med pip):
* requests
* jsonpath_ng

### config.py
Her skal din api nøgle samt brugernavnet til din computer indtastes.

Du kan nu køre programmet med følgende kommando:
`python3 src/main.py [id]`

hvor `id` er det ID du ønsker programmet starter fra.

## TODO
keep a log - maybe generate a json.