import shutil

file1 = open("copiar.txt","r+")  

result = file1.readlines()

for x in result:
  x = x.strip()
  xF = x.split("/")[-1:][0]
  shutil.copy(x, "InstanciasSAT/" + xF)