import requests
from Utils.fetch import baseURL, headers

# Patch metode til ean.
def patch_ean(id, ean):
    payload = {
        'data': {
            'userDefinedFields':
                [
                    {'name':'EAN/GLN', 'value':ean}
                ]
        }
    }
    requests.patch(baseURL+'/workorders/'+str(id), headers=headers, json=payload)

# Patch metode til psp.
def patch_psp(id, psp):
    payload = {
        'data': {
            'userDefinedFields':
                [
                    {'name':'Omk.sted / PSP', 'value':psp}
                ]
        }
    }
    requests.patch(baseURL+'/workorders/'+str(id), headers=headers, json=payload)

# Patch metode til både til både ean og psp.
def patch_ean_psp(id, ean, psp):
    payload = {
        'data': {
            'userDefinedFields':
                [
                    {'name':'EAN/GLN',        'value':ean},
                    {'name':'Omk.sted / PSP', 'value':psp}
                ]
        }
    }
    requests.patch(baseURL+'/workorders/'+str(id), headers=headers, json=payload)

def patch_workorder_with_room(w_id, field):
    payload = {
        'data': {
            'description': field
        }
    }
    requests.patch(baseURL + '/workorders/' + str(w_id), headers=headers, json=payload)