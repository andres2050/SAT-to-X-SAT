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

'''Define function to run mutiple processors and pool the results together'''
def run_multiprocessing(func, i, sat, timeout_time, n_processors):
    with Pool(processes=n_processors) as pool:
        return pool.map(partial(func, sat=sat, timeout_time=timeout_time), i)

'''Define task function'''
def control_proccess_sat_file(filename, sat, timeout_time):
    try:
        timeout(timeoutTime)(proccess_sat_file)(sat, filename)
        return True
    except TimeoutError:
        print(filename)
        return True


def main(sat, timeout_time):
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
    run_multiprocessing(control_proccess_sat_file, x_ls, sat, timeout_time, n_processors)

    elapsed_time = time.time() - start_time
    print("Tiempo transcurrido: %.10f segundos." % elapsed_time)

if __name__ == "__main__":
    if len(sys.argv) < 2 and sys.argv[1].strip() != "":
        print("Ingrese un numero entre 3 y 10.")
        exit()

    SAT = int(sys.argv[1].strip())
    if SAT < 3 or SAT > 10:
        print("Ingrese un numero entre 3 y 10.")
        exit()

    timeoutTime = 30

    if os.path.exists('./X-SAT'):
        shutil.rmtree('./X-SAT', ignore_errors=True)
    
    os.makedirs('./X-SAT')

    freeze_support()   # required to use multiprocessing
    main(SAT, timeoutTime)