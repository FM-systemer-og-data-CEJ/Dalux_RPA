import requests

# Patch metode til ean.
def patch_ean(url, headers, id, ean):
    payload = {
        'data': {
            'userDefinedFields':
                [
                    {'name':'EAN/GLN', 'value':ean}
                ]
        }
    }
    response = requests.patch(url+'/workorders/'+str(id), headers=headers, json=payload)

# Patch metode til psp.
def patch_psp(url, headers, id, psp):
    payload = {
        'data': {
            'userDefinedFields':
                [
                    {'name':'Omk.sted / PSP', 'value':psp}
                ]
        }
    }
    response = requests.patch(url+'/workorders/'+str(id), headers=headers, json=payload)

# Patch metode til både til både ean og psp.
def patch_ean_psp(url, headers, id, ean, psp):
    payload = {
        'data': {
            'userDefinedFields':
                [
                    {'name':'EAN/GLN',        'value':ean},
                    {'name':'Omk.sted / PSP', 'value':psp}
                ]
        }
    }
    response = requests.patch(url+'/workorders/'+str(id), headers=headers, json=payload)