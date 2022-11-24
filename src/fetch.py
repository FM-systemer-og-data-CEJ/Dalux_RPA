import requests
from config import *
import json

# URL samt nøgle til API.
baseURL = 'https://fm-api.dalux.com/api/v1'
headers = {
    'X-API-KEY':api_key
}

def get_workorder(w_id):
    return requests.request("Get", baseURL+'/workorders/'+str(w_id), headers=headers)


def peek(w_id):
    for i in range (0, 6):
        response = get_workorder(w_id + i)
        if response.status_code == 200:
            return w_id + i
        
    return w_id
