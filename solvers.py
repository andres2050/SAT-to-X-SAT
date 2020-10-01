import pysat.solvers as solvers

solvers_avaliable = {
  "lingeling": solvers.Lingeling,
  "glucose3": solvers.Glucose3,
  "glucose4": solvers.Glucose4,
  "cadical": solvers.Cadical,
  "maplechrono": solvers.MapleChrono,
  "maplecm": solvers.MapleCM,
  "maplesat": solvers.Maplesat,
  "minicard": solvers.Minicard,
  "minisat22": solvers.Minisat22,
  "minisatgh": solvers.MinisatGH,
}

'''
solve_clauses: Solves clauses with the specified SAT solver.
'''
def solve_clauses(clauses, solver="gloucose4"):
  solution = False

  with solvers_avaliable[solver](bootstrap_with=clauses) as m:
      solution = m.solve()

  return solution

'''
is_solver_avaliable: By means of a key see if the SAT solution is available.
'''
def is_solver_avaliable(solver):
  return solvers_avaliable.get(solver) != None