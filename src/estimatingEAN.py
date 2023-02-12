import json
from fetch import *
from parser import *
from jsonpath_ng import *

# Make json into a dictionary.
db = json.loads(open("../EAN_DB.json").read())

# test id that i know have no ean.
w_id = 500000

# Get the json data from a workorder.
response = get_workorder(w_id)
responseJSON = json.loads(response.content)

# Finding the building and room number from a workorder.
b_id = responseJSON['data']['buildingID']
r_id = responseJSON['data']['roomID']
ean = None

# Find an EAN that match the room number.
for b in db['buildings']:
    if b['buildingID'] == b_id:
        for r in b['rooms']:
            if r['roomID'] == r_id:
                ean = r['EAN']

print(ean)

# TODO: Insert in recommended EAN.
