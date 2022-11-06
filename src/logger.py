from datetime import date

dato = date.today()
f = open("../" + str(dato) + ".txt", "w+")

def init_log():
    f.write("---" + str(dato) + "---")

def log(s):
    print(s)
    f.write(s)