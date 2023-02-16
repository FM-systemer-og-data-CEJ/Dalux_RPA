import json
from fetch import *
from parser import *
from jsonpath_ng import *

# Make json into a dictionary.
db = json.loads(open("../EAN_DB.json").read())

def patch_recommended_ean(w_id):
    # Get the json data from a workorder.
    response = get_workorder(w_id)
    responseJSON = json.loads(response.content)

    # Finding the building and room number from a workorder.
    b_id = responseJSON['data']['buildingID']
    r_id = responseJSON['data']['roomID']
    rec_ean = None

    # Find an EAN in the local database that match the room number.
    for b in db['buildings']:
        if b['buildingID'] == b_id:
            for r in b['rooms']:
                if r['roomID'] == r_id:
                    rec_ean = r['EAN']
                    break

    # TODO: patch in dalux.
    if rec_ean != None:
        payload = {
            'data': {
                'userDefinedfields':
                [
                    {
                     'name':'Forslået EAN/GLN',
                     'value':rec_ean
                    }
                ]
            }
        }

        print(payload)

# test id that i know have no ean.
w_id = 500000
patch_recommended_ean(w_id)
