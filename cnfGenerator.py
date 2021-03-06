import numpy as np
import random
from pysat.solvers import Solver

class cnfGenerator:
    def __init__(self, n_variables=2, clause_range = (2,3), cnf_size=6, sat_bias=0.5):
       self.n_variables = n_variables
       self.clause_range = clause_range
       self.cnf_size = cnf_size
       self.sat_bias = sat_bias

    def generateCnf(self):
        bias = random.random()
        if(bias >= self.sat_bias):
            desiredSat = True
        else:
            desiredSat = False
            
        done = False
        while not done:
            cnf = []
            i = 0
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
                
            if desiredSat==self.solveCnf(cnf):
                done=True
                
        #cnf = self.forceSatOrUnsat(cnf, desiredSat)
        return cnf

    def solveCnf(self, cnf):
        with Solver(bootstrap_with=cnf) as s:
            return s.solve()
    
    def getLabelledCnf(self):
        cnf = self.generateCnf()
        label = self.solveCnf(cnf)
        return {"cnf": cnf,
                "label": label}
    
    
