# -*- coding: utf-8 -*-

import time
from pysat.formula import CNF
from solvers import *
from wrapt_timeout_decorator import *

'''
split_list: Based on a length it divides an array and creates an array of arrays.
'''
def split_list(list_input, length):
  if len(list_input) == 0:
    return []

  result = [list_input[:length]]
  residue = list_input[length:]

  while len(residue) != 0:
    result.append(residue[:length])
    residue = residue[length:]

  return result

'''
sat_to_3_sat: Complete and divide the clauses in order to bring them to 3-sat
'''
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

    elif clause_length > 3:
      nv += 1
      first = clauses[i][:2]
      last = clauses[i][-2:]

      residue = clauses[i][2:-2]
      division = split_list(residue, 1)
      division_length = len(division)
      if division_length == 0:
        clause = [-nv]

      first.append(nv)
      clauses[i] = first

      for j in range(division_length):
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

'''
reduce_to_x_sat: It takes clauses on 3-SATs and brings them to a given X-SAT.
'''
def reduce_to_x_sat(clauses, nv):
  size = len(clauses)
  for i in range(size):
    nv += 1
    clause = clauses[i][:]

    clauses[i].append(nv)
    clause.append(-nv)
    clauses.append(clause[:])

  return clauses, nv

'''
proccess_sat_file: It obtains the file, reduces it to X-SAT, obtains the solution for both the original and the reduced, 
                  stores the reduced and delivers the result of the whole process.
'''
def proccess_sat_file(filename, sat, solver):
  start_time = time.time()

  result = "{} || solver {} ".format(filename, solver)
  formula = CNF(from_file="./InstanciasSAT/" + filename)
  clauses = formula.clauses[:]
  nv = formula.nv

  original_time = time.time()
  original_solution = solve_clauses(clauses, solver)
  result += "|| original: {} || Tiempo: {:.10f} segundos ".format(original_solution, time.time() - original_time)

  clauses, nv = sat_to_3_sat(clauses, nv)
  if sat > 3:
    x_sat = 3
    while x_sat < sat:
      clauses, nv = reduce_to_x_sat(clauses, nv)
      x_sat += 1

  x_sat_time = time.time()
  x_sat_solution = solve_clauses(clauses, solver)
  result += "|| {}-SAT: {} || Tiempo: {:.10f} segundos ".format(sat, x_sat_solution, time.time() - x_sat_time)

  formula.clauses = clauses
  formula.nv = nv
  formula.to_file("./X-SAT/" + filename)

  result += "|| Tiempo total: {:.10f} segundos".format(time.time() - start_time)
  print(result)

