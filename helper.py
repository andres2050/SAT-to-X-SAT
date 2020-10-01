# -*- coding: utf-8 -*-

import time
from pysat.formula import CNF
from solvers import *

def split_list(list_input, length):
  result = [list_input[:length]]
  residue = list_input[length:]

  while len(residue) != 0:
    result.append(residue[:length])
    residue = residue[length:]

  return result

def sat_to_3_sat(clauses, nv):
  i = 0
  while i < len(clauses):
    clause_length = len(clauses[i])

    if clause_length == 1:
      nv += 1
      clause1 = clauses[i][:]
      clause2 = clauses[i][:]
      clause1.append(nv)
      clause2.append(-nv)

      nv += 1
      clause3 = clause1[:]
      clause4 = clause2[:]

      clause1.append(nv)
      clause2.append(nv)
      clause3.append(-nv)
      clause4.append(-nv)

      clauses[i] = clause1[:]
      clauses.append(clause2[:])
      clauses.append(clause3[:])
      clauses.append(clause4[:])

    elif clause_length == 2:
      nv += 1
      clause = clauses[i][:]

      clauses[i].append(nv)
      clause.append(-nv)
      clauses.append(clause[:])

    elif clause_length == 4:
      nv += 1
      division = split_list(clauses[i][:], 2)
      
      division[0].append(nv)
      division[1].append(-nv)
      clauses[i] = division[0][:]
      clauses.append(division[1][:])

    elif clause_length > 4:
      nv += 1
      first = clauses[i][:2]
      last = clauses[i][-2:]

      residue = clauses[i][2:-2]
      division = split_list(residue, 1)

      first.append(nv)
      clauses[i] = first

      for j in range(len(division)):
        clause = [-nv]
        clause.append(division[j][0])

        nv += 1
        clause.append(nv)
        clauses.append(clause[:])

      clause.extend(last)
      clauses.append(clause[:])

    else:
      i += 1

  return clauses, nv

def reduce_to_x_sat(clauses, nv):
  size = len(clauses)
  for i in range(size):
    nv += 1
    clause = clauses[i][:]

    clauses[i].append(nv)
    clause.append(-nv)
    clauses.append(clause[:])

  return clauses, nv

def proccess_sat_file(filename, sat, solver):
  start_time = time.time()

  formula = CNF(from_file="./InstanciasSAT/" + filename)
  clauses = formula.clauses[:]
  nv = formula.nv
  original_solution = solve_clauses(clauses, solver)

  clauses, nv = sat_to_3_sat(clauses, nv)
  if sat > 3:
    x_sat = 3
    while x_sat < sat:
      clauses, nv = reduce_to_x_sat(clauses, nv)
      x_sat += 1

  x_sat_solution = solve_clauses(clauses, solver)
  formula.clauses = clauses
  formula.nv = nv
  formula.to_file("./X-SAT/" + filename)

  elapsed_time = time.time() - start_time
  match = original_solution == x_sat_solution

  print("Archivo {} || solucionador de sat {} || solucion original: {} || solucion {}-SAT: {} || coinciden: {} || Tiempo ejecución: {}".format(filename, solver, original_solution, sat, x_sat_solution, match, elapsed_time))
