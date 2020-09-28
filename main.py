# -*- coding: utf-8 -*-

from pysat.formula import CNF
from pysat.solvers import Glucose4
from time import time
import glob
from os import walk
import shutil
import os
import sys
import traceback
import signal

def divide_list(listInput, length):
  result = [listInput[:length]]
  residue = listInput[length:]

  while len(residue) != 0:
    result.append(residue[:length])
    residue = residue[length:]

  return result

def SAT_a_3SAT(clauses, nv):
  i = 0
  while i < len(clauses):
    if len(clauses[i]) == 1:
      nv += 1
      temp1 = clauses[i][:]
      temp2 = clauses[i][:]
      temp1.append(nv)
      temp2.append(-nv)

      nv += 1
      temp3 = temp1[:]
      temp4 = temp2[:]

      temp1.append(nv)
      temp2.append(nv)
      temp3.append(-nv)
      temp4.append(-nv)

      clauses[i] = temp1[:]
      clauses.append(temp2[:])
      clauses.append(temp3[:])
      clauses.append(temp4[:])
    if len(clauses[i]) == 2:
      nv += 1
      temp = clauses[i][:]
      clauses[i].append(nv)
      temp.append(-nv)
      clauses.append(temp[:])
    elif len(clauses[i]) == 4:
      nv += 1
      division = divide_list(clauses[i][:], 2)
      
      division[0].append(nv)
      division[1].append(-nv)
      clauses[i] = division[0][:]
      clauses.append(division[1][:])
    elif len(clauses[i]) > 4:
      nv += 1
      first = clauses[i][:2]
      last = clauses[i][-2:]
      residue = clauses[i][2:-2]
      division = divide_list(residue, 1)

      first.append(nv)
      clauses[i] = first
      for j in range(len(division)):
        temp = [-nv]
        temp.append(division[j][0])
        nv += 1
        temp.append(nv)
        clauses.append(temp[:])
      
      temp = [-nv]
      temp.extend(last)
      clauses.append(temp[:])
    else:
      i += 1

  return clauses, nv


def reducir_a_XSAT(clauses, nv):
  tamaño = len(clauses)
  for i in range(tamaño):
    nv += 1
    temp = clauses[i][:]
    clauses[i].append(nv)
    temp.append(-nv)
    clauses.append(temp[:])

  return clauses, nv

def proccessSATFile(SAT, fileName):
  formula = CNF(from_file="./InstanciasSAT/" + fileName)
  solucionOriginal = False

  with Glucose4(bootstrap_with=formula.clauses[:]) as m:
    solucionOriginal = m.solve()

  clauses = formula.clauses[:]
  nv = formula.nv

  clauses, nv = SAT_a_3SAT(clauses, nv)
  if SAT > 3:
    x_sat = 3
    while x_sat < SAT:
      clauses, nv = reducir_a_XSAT(clauses, nv)
      x_sat += 1

  solucionXSAT = False

  with Glucose4(bootstrap_with=clauses) as m:
    solucionXSAT = m.solve()

  print("Solucion", fileName, "|| solucion original:", solucionOriginal, "|| solucion " + str(SAT) + "-SAT:", solucionXSAT, "|| coinciden:", solucionOriginal == solucionXSAT)

  formula.clauses = clauses
  formula.nv = nv
  formula.to_file("./X-SAT/" + fileName)

# START PROGRAM
start_time = time()
if len(sys.argv) < 2 and sys.argv[1].strip() != "":
  print("Ingrese un numero entre 3 y 10.")
  exit()

SAT = int(sys.argv[1].strip())
if SAT < 3 or SAT > 10:
  print("Ingrese un numero entre 3 y 10.")
  exit()


if os.path.exists('./X-SAT'):
  shutil.rmtree('./X-SAT', ignore_errors=True)
    
os.makedirs('./X-SAT')

class TimeoutError (RuntimeError):
    pass

def handler (signum, frame):
    raise TimeoutError()

#signal.signal (signal.SIGALRM, handler)

files = []
for (dirpath, dirnames, filenames) in walk("./InstanciasSAT"):
    files.extend(filenames)
    break

for fl in files:
  try:
    signal.alarm (5)
    proccessSATFile(SAT, fl)
  except TimeoutError as ex:
    print("filename:", fl)

elapsed_time = time() - start_time
print("Tiempo transcurrido: %.10f segundos." % elapsed_time)

