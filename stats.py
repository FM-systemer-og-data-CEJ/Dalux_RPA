import sys
sys.path.append('C:\\Users\\sgei0004\\AppData\\Roaming\\Python\\Python310\\site-packages')
from tabulate import tabulate
from datetime import datetime, timedelta

with open('workorder.log') as f:
    lines = f.readlines()

def string2date(s):
    return datetime.strptime(s, '%Y-%m-%d %H:%M:%S')

def since_hours(h):
    r_arr = []
    nu = datetime.now()
    date = string2date(lines[len(lines)-1][0:19])
    w_sum = 0
    e_sum = 0
    p_sum = 0
    l = len(lines)-1
    while ((nu - date) < timedelta(hours=h) and (l-w_sum) >= 0):
        w_sum += 1
        split = (lines[l-w_sum]).split(",")
        
        if (len(split) == 3):
            if (split[2][1:13] == 'patched EAN.'):
                e_sum += 1
            elif(split[2][1:13] == 'patched PSP.'):
                p_sum += 1
            elif(split[2][18] == 'patched EAN & PSP.'):
                e_sum += 1
                p_sum += 1
        
        date = string2date(lines[l-w_sum][0:19])
    r_arr.append(w_sum)
    r_arr.append(e_sum)
    r_arr.append(p_sum)
    return r_arr

col_names = ["", "Seneste time", "Seneste døgn", "Seneste uge"]

# 0: sum af workorders der kigget på
# 1: sum af workorders kun opdateret ean
# 2: sum af workorders kun opdateret psp
# 3: sum af workorders opdateret med både ean og psp
data = [
        ["Workorders scannet", since_hours(1)[0], since_hours(24)[0], since_hours(168)[0]],
        ["Opdateret EAN", since_hours(1)[1], since_hours(24)[1], since_hours(168)[1]],
        ["Opdateret PSP", since_hours(1)[2], since_hours(24)[2], since_hours(168)[2]] 
       ]

print(tabulate(data, headers=col_names, tablefmt="fancy_grid"))
