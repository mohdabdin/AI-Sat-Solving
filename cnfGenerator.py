import numpy as np
import random

from pysat.solvers import Minisat22

class cnfGenerator:
    def __init__(self, n_variables=40, clause_range = (1,4), cnf_size=120):
       self.n_variables = n_variables
       self.clause_range = clause_range
       self.cnf_size = cnf_size

    def generateCnf(self):
        i = 0
        cnf = []
        while i<self.cnf_size:
            clause = [] 
            #random number of literals in each clause
            n_clause = random.randrange(self.clause_range[0], self.clause_range[1])
            for _ in range(n_clause):
                lit_state = random.randint(1,2)
                lit = random.randint(1,self.n_variables)
                if lit_state==1: #positive literal
                    clause.append(lit)
                else: #negated literal
                    clause.append(-lit)
                i+=1
            cnf.append(clause)
        return np.array(cnf)

    def solveCnf(self, cnf):
        m = Minisat22()
        for clause in cnf:
            m.add_clause(clause)
        return m.solve()
    
    def getLabelledCnf(self):
        cnf = self.generateCnf()
        label = self.solveCnf(cnf)
        return {"cnf": cnf,
                "label": label}
    
