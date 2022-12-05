import sys
import json
import time
from parser import *
from patch import *
from fetch import *
import logging

# Sætter log'en.
logging.basicConfig(filename='workorder.log', level=logging.INFO, format='%(asctime)s %(message)s')

# Får workorder som argument.
workorder_id = int(sys.argv[1])

total_sleep = 0
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
    
        if ean_skal_opdateres:
            ean = find_ean_indmelding(responseJSON)
        if psp_skal_opdateres:
            psp = find_psp_indmelding(responseJSON)
            
        if ean == None and psp == None:
            print("Der findes intet ean eller psp i indmeldninger.")
            logging.info("\tWorkorder: " + str(workorder_id) + ", har intet i indmeldninger.")
        elif ean == None:
            print("Der findes intet ean i indmeldninger.")
            patch_psp(baseURL, headers, workorder_id, psp)
            logging.info("\tWorkorder: " + str(workorder_id) + ", patched PSP.")
        elif psp == None:
            print("Der findes intet psp i indmeldninger.")
            patch_ean(baseURL, headers, workorder_id, ean)
            logging.info("\tWorkorder: " + str(workorder_id) + ", patched EAN.")
        else:
            patch_ean_psp(baseURL, headers, workorder_id, ean, psp)
            logging.info("\tWorkorder: " + str(workorder_id) + ", patched EAN & PSP.")
            
        workorder_id += 1
    else:
        print("Sleeping for 10 seconds. Total sleep time: " + str(total_sleep) + " seconds.") 
        time.sleep(10)
        total_sleep += 10
        if (total_sleep % 60 == 0):
            print("Peeking...")
            workorder_id = peek(workorder_id)
            print("Continuing at: " + str(workorder_id))
            
