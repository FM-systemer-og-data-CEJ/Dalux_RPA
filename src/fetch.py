import requests
from config import *
import logging

# URL samt nøgle til API.
baseURL = 'https://fm-api.dalux.com/api/v1'
headers = {
    'X-API-KEY':api_key
}

def get_workorder(w_id):
    # Det lader til at dalux time-out'er eller sender noget ulæseligt. Efter 3 forsøg lukkes programmet.
    i = 1
    while (i <= 3):
        try:
            return requests.request("Get", baseURL+'/workorders/'+str(w_id), headers=headers)
        except:
            print(i + " mislykket forsøg på at få fat på " + str(w_id))
    i += 1
    logging.info("Kunne ikke få fat på ID: " + str(w_id) + "efter 3 forsøg.")
    exit()

def peek(w_id):
    for i in range (1, 6):
        response = get_workorder(w_id + i)
        if response.status_code == 200:
            return w_id + i
        
    return w_id
