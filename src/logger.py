from datetime import date

dato = date.today()
f = open("../Logs/" + str(dato) + ".txt", "w+")

def init_log(start, slut):
    f.write("---" + str(dato) + "---\nOpgave ID fra " + str(start) + " til " + str(slut) + ".")

def log(s):
    2+2 
    #print(s)
    #f.write(s)
