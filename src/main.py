import sys
import requests
import json
import time
from parser import *
from patch import *
from config import api_key
from logger import *

# Får workorder som argument.
workorder_id = int(sys.argv[1])

# URL samt nøgle til API.
baseURL = 'https://fm-api.dalux.com/api/v1'
headers = {
    'X-API-KEY':api_key
}

while 1:
    response = requests.request("Get", baseURL+'/workorders/'+str(workorder_id), headers=headers)
    responseJSON = json.loads(response.content)

    if response.status_code == 200:
        print("\nWorkorder " + str(workorder_id) + " blev fundet.")
        log(str(workorder_id))

        # Find ud af om ean eller psp allerede er sat.
        skal_opdateres = True;
        for match in parser.parse("data[*].history[*].lines[?(@.title=='EAN/GLN')]").find(responseJSON):
            skal_opdateres = False
        for match in parser.parse("data[*].history[*].lines[?(@.title=='Omk.sted / PSP')]").find(responseJSON):
            skal_opdateres = False
    
        if skal_opdateres:
            ean = find_ean_indmelding(responseJSON)
            psp = find_psp_indmelding(responseJSON)

            if ean == None and psp == None:
                print("Der findes intet ean eller psp i indmeldninger.")
            elif ean == None:
                print("Der findes intet ean i indmeldninger.")
                patch_psp(baseURL, headers, workorder_id, psp)
            elif psp == None:
                print("Der findes intet psp i indmeldninger.")
                patch_ean(baseURL, headers, workorder_id, ean)
            else:
                patch_ean_psp(baseURL, headers, workorder_id, ean, psp)
        else:
            print("Der findes allerede et ean og/eller psp nummer på denne opgave.")

        workorder_id += 1
    else:
        print("Venter i 10 sekunder og tjekker om der er kommet en ny indmelding.") 
        time.sleep(10)