# -*- coding: utf-8 -*-

import time
import math
import sys
import os
import shutil
from os import walk
from multiprocessing import Pool
from multiprocessing import freeze_support
from multiprocessing import cpu_count
from functools import partial
from wrapt_timeout_decorator import *
from helper import *
from solvers import *

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

def main(sat, solver, timeout_time):
    start_time = time.time()

    files = []
    for (dirpath, dirnames, filenames) in walk("./InstanciasSAT"):
        files.extend(filenames)
        break

    '''
    set up parameters required by the task
    '''
    n_processors = cpu_count()
    x_ls = list(files)

    '''
    pass the task function, followed by the parameters to processors
    '''
    run_multiprocessing(control_proccess_sat_file, x_ls, sat, solver, timeout_time, n_processors)

    elapsed_time = time.time() - start_time
    print("Tiempo transcurrido: %.10f segundos." % elapsed_time)

if __name__ == "__main__":
    if len(sys.argv) < 2 and sys.argv[1].strip() != "":
        print("Ingrese un numero entre 3 y 10.")
        exit()

    sat = int(sys.argv[1].strip())
    if sat < 3 or sat > 10:
        print("Ingrese un numero entre 3 y 10.")
        exit()

    timeout_time = 240
    if len(sys.argv) >= 3 and sys.argv[2].strip() != "":
        temp_timeout_time = int(sys.argv[2].strip())
        if temp_timeout_time > 0:
            timeout_time = temp_timeout_time
    
    solver = "glucose4"
    if len(sys.argv) >= 4 and sys.argv[3].strip() != "":
        temp_solver = sys.argv[3].strip()
        if is_solver_avaliable(temp_solver):
            solver = temp_solver

    if os.path.exists('./X-SAT'):
        shutil.rmtree('./X-SAT', ignore_errors=True)
    
    os.makedirs('./X-SAT')

    freeze_support()   # required to use multiprocessing
    main(sat, solver, timeout_time)