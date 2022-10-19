import sys
import requests
import json
from parser import *
from patch import *
from config import api_key

# Får workorder som argument.
workorder_id = int(sys.argv[1])

# URL samt nøgle til API.
baseURL = 'https://fm-api.dalux.com/api/v1'
headers = {
    'X-API-KEY':api_key
}

# TODO: Find condition til at stoppe loop.
while True:
    response = requests.request("Get", baseURL+'/workorders/'+str(workorder_id), headers=headers)
    responseJSON = json.loads(response.content)

    if response.status_code == 200:
        print("\nWorkorder " + str(workorder_id) + " blev fundet.")

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
        print("\nWorkorder " + str(workorder_id) + " blev ikke fundet")

    workorder_id += 1