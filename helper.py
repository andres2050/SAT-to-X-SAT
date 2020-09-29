from pysat.formula import CNF
from pysat.solvers import Glucose4

def divide_list(listInput, length):
  result = [listInput[:length]]
  residue = listInput[length:]

  while len(residue) != 0:
    result.append(residue[:length])
    residue = residue[length:]

  return result

def sat_a_3sat(clauses, nv):
  i = 0
  while i < len(clauses):
    len_current = len(clauses[i])

    if len_current == 1:
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
    elif len_current == 2:
      nv += 1
      temp = clauses[i][:]

      clauses[i].append(nv)
      temp.append(-nv)
      clauses.append(temp[:])
    elif len_current == 4:
      nv += 1
      division = divide_list(clauses[i][:], 2)
      
      division[0].append(nv)
      division[1].append(-nv)
      clauses[i] = division[0][:]
      clauses.append(division[1][:])
    elif len_current > 4:
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

      temp.extend(last)
      clauses.append(temp[:])
    else:
      i += 1

  return clauses, nv

def reducir_a_xsat(clauses, nv):
  tamaño = len(clauses)
  for i in range(tamaño):
    nv += 1
    temp = clauses[i][:]
    clauses[i].append(nv)
    temp.append(-nv)
    clauses.append(temp[:])

  return clauses, nv

def proccess_sat_file(sat, filename):
  formula = CNF(from_file="./InstanciasSAT/" + filename)
  solucion_original = False

  with Glucose4(bootstrap_with=formula.clauses[:]) as m:
    solucion_original = m.solve()

  clauses = formula.clauses[:]
  nv = formula.nv

  clauses, nv = sat_a_3sat(clauses, nv)
  if sat > 3:
    x_sat = 3
    while x_sat < sat:
      clauses, nv = reducir_a_xsat(clauses, nv)
      x_sat += 1

  solucion_xsat = False

  with Glucose4(bootstrap_with=clauses) as m:
    solucion_xsat = m.solve()

  print("Archivo", filename, "|| solucion original:", solucion_original, "|| solucion " + str(sat) + "-SAT:", solucion_xsat, "|| coinciden:", solucion_original == solucion_xsat)

  formula.clauses = clauses
  formula.nv = nv
  formula.to_file("./X-SAT/" + filename)