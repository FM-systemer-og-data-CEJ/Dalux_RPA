import sys
import json
import time
from Utils.fetch import get_workorder, peek, peek_long
from RPAs.EAN_PSP import EAN_PSP_RPA

# Command line inputs.
workorder_id = int(sys.argv[1])
flags = sys.argv[2:]

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
        for f in flags:
            match f:
                case '-E':
                    EAN_PSP_RPA(workorder_id, responseJSON)

            ############################
            #        More RPA's        #
            ############################

        workorder_id += 1
    else:
        time.sleep(30)
        total_sleep += 30
        if (total_sleep % 300 == 0):
            if (peek_counter >= 20):
                workorder_id = peek_long(workorder_id)
                peek_counter = 0
            else:
                old_w = workorder_id
                workorder_id = peek(workorder_id)
                if (old_w == workorder_id):
                    peek_counter += 1
