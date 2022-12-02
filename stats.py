from tabulate import tabulate
from datetime import datetime, timedelta

with open('workorder.log') as f:
    lines = f.readlines()

def string2date(s):
    return datetime.strptime(s, '%Y-%m-%d %H:%M:%S')

def since_hours(h):
    nu = datetime.now()
    date = string2date(lines[len(lines)-1][0:19])
    sum = 0
    l = len(lines)-1
    while ((nu - date) < timedelta(hours=h) and (l-sum) >= 0):
        sum += 1
        date = string2date(lines[l-sum][0:19])
    return sum

data = [["Total workorders:", len(lines)],
        ["Sidste time:", since_hours(1)],
        ["Sidste døgn:", since_hours(24)]
]    
print(tabulate(data, tablefmt="fancy_grid"))
