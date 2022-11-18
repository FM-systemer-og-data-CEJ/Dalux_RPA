import datetime

f = open("../log.txt", "a")

def log(s):
    dato = datetime.datetime.now()
    f.write("Kigget paa workorder " + s + " d.: " + str(dato) + "\n") 