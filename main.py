# -*- coding: utf-8 -*-

import time
import math
import sys
import os
import shutil
import argparse
from os import walk
from multiprocessing import Pool, freeze_support, cpu_count
from functools import partial
from wrapt_timeout_decorator import *
from helper import *
from solvers import *
from argparse import RawTextHelpFormatter

'''Define function to run mutiple processors and pool the results together'''
def run_multiprocessing(func, i, sat, solver, timeout_time, n_processors):
  with Pool(processes=n_processors) as pool:
    return pool.map(partial(func, sat=sat, solver=solver, timeout_time=timeout_time), i)

'''Define task function'''
def control_proccess_sat_file(filename, sat, solver, timeout_time):
  try:
    timeout(timeout_time)(proccess_sat_file)(filename, sat, solver)
  except TimeoutError:
    print("Archivo", filename, "|| Excedió el tiempo de ejecución de", timeout_time, "segundos || Solucionador de sat:", solver)

'''Define main function'''
def main(sat, solver, timeout_time, n_processors):
  start_time = time.time()

  files = []
  for (dirpath, dirnames, filenames) in walk("./InstanciasSAT"):
      files.extend(filenames)
      break

  '''
  set up parameters required by the task
  '''
  x_ls = list(files)

  '''
  pass the task function, followed by the parameters to processors
  '''
  run_multiprocessing(control_proccess_sat_file, x_ls, sat, solver, timeout_time, n_processors)

  elapsed_time = time.time() - start_time
  print("Tiempo transcurrido: {:.10f} segundos.".format(elapsed_time))

if __name__ == "__main__":
  '''
  set up default values used in arguments
  '''
  n_processors = cpu_count()
  default_timeout = 240
  default_solver = "glucose4"

  '''
  get arguments value and set up help test
  '''
  parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
  parser.add_argument("--x_sat", "-x",
                      type=int,
                      help="Establece X-SAT de los archivos de salida.\n"
                          "Se aceptan valores entre 3 y 10.")
  parser.add_argument("--timeout", "-t",
                      default=default_timeout,
                      type=int,
                      help="Establece tiempo máximo en segundos para la ejecución de cada archivo (default: %(default)s).\n"
                          "Se aceptan valores positivos, en caso de ser cero o negativo se utilizara el valor por defecto.")
  parser.add_argument("--solver", "-s",
                      default=default_solver, 
                      type=str, 
                      help="Establece el solucionador de SAT utilizado (default: %(default)s).\n"
                          "En caso de ingresar un valor no disponible se utilizara el valor por defecto.\n"
                          "Disponibles: lingeling, glucose3, glucose4, cadical, maplechrono, maplecm, maplesat, minicard, minisat22 y minisatgh.")
  parser.add_argument("--processes", "-p",
                      default=n_processors,
                      type=int,
                      help="Establece la cantidad de hilos utilizados (default: %(default)s).\n"
                          "Se aceptan valores entre 1 y %(default)s.\n"
                          "En caso de ingresar un valor invalido se utilizara el valor por defecto.")
  parser.add_argument("--about", "-a",
                      action="version",
                      version="Elaborado por:\n"
                            "Andres Felipe Herrera Moreno\n"
                            "Donald Marcelo Catañeda\n"
                            "Jose Alexander Muñoz\n",
                      help="Ver desarrolladores del proyecto.")

  args = parser.parse_args()

  '''
  verify required and optional arguments
  '''

  x_sat = args.x_sat
  if x_sat == None:
    print("Parametro -x o --x_sat requerido, se aceptan valores entre 3 y 10.")
    exit()
  if x_sat < 3 or x_sat > 10:
    print("Parametro -x o --x_sat solo acepta valores entre 3 y 10.")
    exit()
  sat = x_sat

  solver_value = args.solver
  if solver_value == None or not is_solver_avaliable(solver_value):
    solver_value = default_solver
  solver = solver_value

  timeout_value = args.timeout
  if timeout_value == None or timeout_value < 1:
    timeout_value = default_timeout
  timeout_time = timeout_value

  processes_value = args.processes
  if processes_value == None or processes_value < 1 or processes_value > n_processors:
    processes_value = n_processors
  n_processors = processes_value

  '''
  Delete old results and create required folder
  '''
  if os.path.exists('./X-SAT'):
    shutil.rmtree('./X-SAT', ignore_errors=True)
  os.makedirs('./X-SAT')

  '''
  Start program
  '''
  freeze_support()   # required to use multiprocessing
  main(sat, solver, timeout_time, n_processors)