import sys
import json
import time
from parser import *
from patch import *
from fetch import *
from log import setup_logger

# Opretter en log.
main_log = setup_logger("main", "workorder.log")

# Får workorder som argument.
workorder_id = int(sys.argv[1])

total_sleep = 0
peek_counter = 0
while 1:
    try:
        response = get_workorder(workorder_id)
        responseJSON = json.loads(response.content)
    except:
        continue

    if response.status_code == 200:
        total_sleep = 0
        print("\nWorkorder " + str(workorder_id) + " blev fundet.")

        # Workorder skal ikke opdateres hvis der allerede findes et EAN / PSP i historikken.
        ean_skal_opdateres = True
        psp_skal_opdateres = True
        for match in parser.parse("data[*].history[*].lines[?(@.title=='EAN/GLN')]").find(responseJSON):
            ean_skal_opdateres = False
        for match in parser.parse("data[*].history[*].lines[?(@.title=='Omk.sted / PSP')]").find(responseJSON):
            psp_skal_opdateres = False

        ean = None
        psp = None
        if ean_skal_opdateres:
            ean = find_ean_indmelding(responseJSON)
        if psp_skal_opdateres:
            psp = find_psp_indmelding(responseJSON)

        if ean == None and psp == None:
            print("Der findes intet EAN eller PSP i indmeldninger.")
            main_log.info("\tWorkorder: " + str(workorder_id) + ", har intet i indmeldninger.")
        elif ean == None:
            print("Der findes intet EAN i indmeldninger.")
            patch_psp(baseURL, headers, workorder_id, psp)
            main_log.info("\tWorkorder: " + str(workorder_id) + ", patched PSP.")
        elif psp == None:
            print("Der findes intet PSP i indmeldninger.")
            patch_ean(baseURL, headers, workorder_id, ean)
            main_log.info("\tWorkorder: " + str(workorder_id) + ", patched EAN.")
        else:
            patch_ean_psp(baseURL, headers, workorder_id, ean, psp)
            main_log.info("\tWorkorder: " + str(workorder_id) + ", patched EAN & PSP.")

        workorder_id += 1
    else:
        print("Sleeping for 30 seconds. Total sleep time: " + str(total_sleep) + " seconds.")
        time.sleep(30)
        total_sleep += 30
        if (total_sleep % 300 == 0):
            print("Peeking - PC: " + str(peek_counter))
            if (peek_counter >= 20):
                workorder_id = peek_long(workorder_id)
                peek_counter = 0
            else:
                old_w = workorder_id
                workorder_id = peek(workorder_id)
                if (old_w == workorder_id):
                    peek_counter += 1

            print("Continuing at: " + str(workorder_id))

