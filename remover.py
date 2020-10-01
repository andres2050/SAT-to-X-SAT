import os

file1 = open("eliminar.txt","r+")  

result = file1.readlines()

for x in result:
    os.remove("InstanciasSAT/" + x.strip())