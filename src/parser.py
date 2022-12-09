from jsonpath_ng.ext import parser

# Retunere det sidst tilføjet EAN-nummer i historiken, hvis der findes et.
def find_ean_indmelding(json):
    eans = []
    for match in parser.parse("data[*].history[*].lines[?(@.title=='EAN-nummer')]").find(json):
        eans.append(match.value['value'])
    
    if len(eans) >= 1:
        return eans[0]
    else:
        return None

# Retunere det sidst tilføjet PSP-nummer i historiken, hvis der findes et.
def find_psp_indmelding(json):
    psps = []
    for match in parser.parse("data[*].history[*].lines[?(@.title=='Omkostningssted eller PSP-nummer')]").find(json):
        psps.append(match.value['value'])
    
    if len(psps) >= 1:
        return psps[0]
    else:
        return None
