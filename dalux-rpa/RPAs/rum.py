from Utils.log import setup_logger
from Utils.fetch import get_room
from Utils.parserS import *
from Utils.patch import patch_workorder_desc

rum_log = setup_logger("rum", "rum.log")

def rum_RPA(w_id, json):
    roomID = json['data']['roomID']

    if roomID == None:
        return
    else:
        room = get_room(roomID)
        roomJSON = json.loads(room.content)

        p = None
        for match in parser.parse("data[*].userDefinedFields[?(@.name=='Kritisk rum:')]").find(roomJSON):
            p = match.value['value']

        if p == None:
            return
        else:
            patch_string = p['name'] + " " + p['value']
            rum_log.info("\tRum: " + str(roomID) + " er kritisk og tilføjes på workorder: " + str(w_id))
            patch_workorder_desc(w_id, patch_string)
