from ast import While
from genericpath import isfile
import certpars
import createcert
import rootcertmaker
import json

u = True
if not isfile("root_cert.pem"): #verifies if root certificate has already been created 
    rootcertmaker.makeroo() #if not launches the script to create it
    print("root and registration authority created succesfully...")
    number = {"nb" : 1}
else:
    print("root and registration authority already exist, continuing to next step...")
    with open('num.json', 'r') as z :
        number = json.load(z)
while u :
    t= input("do you want to make certificates?(y/n)\n")
    if t.casefold() == "y".casefold():
        u = False
        o = True
    elif t.casefold() == "n".casefold():
        u = False
        o = False
    else:
        print("please pick a valid option")
if o:
    number['nb'] = createcert.them(number['nb'])
with open("num.json", 'w') as g:
    json.dump(number,g)
print("beginning parsing...")
certpars.parser()