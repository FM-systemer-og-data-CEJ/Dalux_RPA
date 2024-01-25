from Utils.parserS import parser, find_ean_indmelding, find_psp_indmelding
from Utils.log import setup_logger
from Utils.patch import patch_ean_psp, patch_ean, patch_psp

# Opretter en log.
EAN_PSP_log = setup_logger("main", "EAN_PSP.log")


def EAN_PSP_RPA(w_id, json):
    ean_skal_opdateres = True
    psp_skal_opdateres = True
    for match in parser.parse("data[*].history[*].lines[?(@.title=='EAN/GLN')]").find(
        json
    ):
        ean_skal_opdateres = False
    for match in parser.parse(
        "data[*].history[*].lines[?(@.title=='Omk.sted / PSP')]"
    ).find(json):
        psp_skal_opdateres = False

    ean = None
    psp = None
    if ean_skal_opdateres:
        ean = find_ean_indmelding(json)
    if psp_skal_opdateres:
        psp = find_psp_indmelding(json)

    if ean is None and psp is None:
        EAN_PSP_log.info("\tWorkorder: " + str(w_id) + ", har intet i indmeldninger.")
    elif ean is None:
        patch_psp(w_id, psp)
        EAN_PSP_log.info("\tWorkorder: " + str(w_id) + ", patched PSP.")
    elif psp is None:
        patch_ean(w_id, ean)
        EAN_PSP_log.info("\tWorkorder: " + str(w_id) + ", patched EAN.")
    else:
        patch_ean_psp(w_id, ean, psp)
        EAN_PSP_log.info("\tWorkorder: " + str(w_id) + ", patched EAN & PSP.")
