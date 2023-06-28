import requests
import json
from Utils.config import api_key
from Utils.log import setup_logger

# URL samt nøgle til API.
baseURL = 'https://fm-api.dalux.com/api/v1'
headers = {
    'X-API-KEY':api_key
}

# Opretter en log.
peek_log = setup_logger("peek_log", "peek.log")

def get_workorder(w_id):
    return requests.request("Get", baseURL+'/workorders/'+str(w_id), headers=headers)

# Grundet små spring i ID numre bliver der smukigget på de næste 5. Skulle der findes et
# returneres dette og programmet kører videre derfra. Starter på 0 da det har vist sig at
# hvis 2 eller flere workorders bliver oprettet inden for kort tid af hinanden (1-2 sekunder)
# vil den vi leder efter blive sprunget over.
def peek(w_id):
    for i in range (0, 6):
        response = get_workorder(w_id + i)
        if response.status_code == 200:
            if (i != 0):
                peek_log.info("Short peeked " + str(i+1) + " from " + str(w_id-1) + " to " + str(w_id+i))
            return w_id + i
    return w_id

# Grundet større spring (op mod 1000) i ID numre er `peek()` ikke tilstrækkelig. Derfor
# bliver alle workorders fundet, sorteret og sammelignet med det ID hoved programmet er
# nået til.
def peek_long(w_id):
    all = requests.request("Get", baseURL + "/workorders", headers=headers)
    allJSON = json.loads(all.content)

    IDs = []
    for i in range(0, 100):
       IDs.append(allJSON['items'][i]['data']['ID'])

    IDs.sort()
    s = w_id
    for i in range(0, 100):
        if IDs[i] > w_id:
            s = IDs[i]
            break

    for i in range(w_id, s):
        r = get_workorder(i)
        if r.status_code == 200:
            peek_log.info("Long peeked " + str(i-w_id) + " from " + str(w_id) + " to " + str(i))
            return i

    return w_id