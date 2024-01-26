from jsonpath_ng.ext import parser


def find_ean_indmelding(json) -> str | None:
    """
    Retunere det sidst tilføjet EAN-nummer i historiken, hvis der findes et.
    Arguments:
    - json
    """
    eans: list[str] = []
    for match in parser.parse(
        "data[*].history[*].lines[?(@.title=='EAN-nummer')]"
    ).find(json):
        eans.append(match.value["value"])

    if len(eans) >= 1:
        return eans[0]
    else:
        return None


def find_psp_indmelding(json) -> int | None:
    """
    Retunere det sidst tilføjet PSP-nummer i historiken, hvis der findes et.
    Arguments:
    - json
    """
    psps: list[str] = []
    for match in parser.parse(
        "data[*].history[*].lines[?(@.title=='Omkostningssted eller PSP-nummer')]"
    ).find(json):
        psps.append(match.value["value"])

    if len(psps) >= 1:
        return psps[0]
    else:
        return None
