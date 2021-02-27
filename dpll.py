import itertools
import cnfGenerator as g
import numpy as np

gen = g.cnfGenerator()
cnf = gen.generateCnf()


def dpll(cnf):
    if len(cnf)==0:
        return 'satisfiable'

    c = 0
    while any(c for c in cnf if len(c)==1):
        if len(cnf[c])==1:
            pure_lit=cnf[c][0]
            for c_ in cnf:
                if len(c_)==1 and c_[0]==-pure_lit:
                    return 'unsatisfiable'
            cnf = Simplify(cnf, pure_lit)
            c = -1
        c+=1
        
    if not cnf:
        return 'satisfiable'

    lit = cnf[0][0]
    if dpll(Simplify(cnf, lit))=='satisfiable':
        return('satisfiable')
    else:
        return(dpll(Simplify(cnf, -lit)))

                     
def Simplify(cnf,l):
    c=0
    while c<len(cnf):
        if -l in cnf[c]:
            cnf[c].remove(-l)
        if not cnf[c]:
            cnf.remove(cnf[c])
        if l in cnf[c]:
            cnf.remove(cnf[c])
            c-=1
        c+=1
    return cnf

print(gen.solveCnf(cnf))
print(dpll(cnf))


#truth denotation = 41
#false denotation = 42
'''
def step(cnf, action):
    lit = action[1]
    bool_ = action[0]
    while j<len(cnf):
        while i<len(c):
            if cnf[j][i]==lit:
                if (bool_==True and lit>0) or (bool_==False and lit<0):
                    cnf[j][i] = 41
                else if bool_==False and lit>0:
                    cnf[j][i] = 42

'''  
                    
