from logging import Logger
from typing import Optional
from utils.parserS import parser, find_ean_indmelding, find_psp_indmelding
from utils.log import setup_logger
from utils.patch import patch_ean_psp, patch_ean, patch_psp

# Opretter en log.
EAN_PSP_log: Logger = setup_logger("main", "EAN_PSP.log")


def EAN_PSP_RPA(w_id, json) -> None:
    ean_skal_opdateres: bool = True
    psp_skal_opdateres: bool = True

    for match in parser.parse("data[*].history[*].lines[?(@.title=='EAN/GLN')]").find(
        json
    ):
        ean_skal_opdateres = False
    for match in parser.parse(
        "data[*].history[*].lines[?(@.title=='Omk.sted / PSP')]"
    ).find(json):
        psp_skal_opdateres = False

    ean: Optional[int] = None
    psp: Optional[int] = None

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
