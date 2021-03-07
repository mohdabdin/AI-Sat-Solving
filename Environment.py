import tensorflow as tf
import numpy as np

from tf_agents.environments import py_environment
from tf_agents.specs import array_spec

from tf_agents.trajectories import time_step as ts


from cnfGenerator import cnfGenerator

tf.compat.v1.enable_v2_behavior()

CLAUSE_LENGTH = 2
N_VARIABLES = 10
CNF_SIZE = 40

class CnfSolverEnv(py_environment.PyEnvironment):
  def __init__(self):
    self._action_spec = array_spec.BoundedArraySpec(
        shape=(), dtype=np.int32, minimum=0, maximum=(N_VARIABLES*2)+1, name='action')
    self._observation_spec = array_spec.BoundedArraySpec(
        shape=(40,), dtype=np.int32, minimum=[-N_VARIABLES for _ in range(CNF_SIZE)], maximum=[N_VARIABLES for _ in range(CNF_SIZE)], name='observation')
    self.generator = cnfGenerator(n_variables = N_VARIABLES, clause_range=(2,3), cnf_size=40)
    self.cnf = self.generator.generateCnf()
    self.initial_label = self.generator.solveCnf(self.cnf)
    self._state = np.array(self.cnf)
    self._episode_ended = False

  def action_spec(self):
    return self._action_spec

  def observation_spec(self):
    return self._observation_spec

  def _reset(self):
    self.cnf = self.generator.generateCnf()
    self._state = np.array(self.cnf)
    self._episode_ended = False
    return ts.restart(self._state.flatten())

  def simplify(self, cnf, lit):
    c=0
    while c<len(cnf):
      l=0
      while l<len(cnf[c]):
        if -lit==cnf[c][l]:
          cnf[c][l] = 0
        l+=1
      if lit in cnf[c]:
        cnf[c] = [0 for _ in range(CLAUSE_LENGTH)]
      c+=1

    return cnf

  def minisat_reformat(self, cnf):
    #removes the zeros from the cnf to be understood by the minisat solver
    cnf = cnf.tolist()
    for clause in cnf:
        i=0
        while i<len(clause):
            if clause[i]==0:
                clause.remove(0)
                i-=1
            i+=1
    return [x for x in cnf if len(x)>0]
  
      
  
  def _step(self, action):
    reward = 0
    action = action-N_VARIABLES
    if action==0:
        #agent predicts unsatifiable
        if self.initial_label == True:
            reward = -1 #negative reward for false prediction
            print("episode ended: Agent predicted unsatisfiable incorrectly")
        else:
            reward = 1 #positive reward for correct prediction
            print("episode ended: Agent predicted unsatisfiable correctly")
            
        self._episode_ended = True
        return ts.termination(self._state.flatten(), reward)
    
    elif action==N_VARIABLES+1:
        #agent predicts satisfiable
        if self.initial_label == False:
            reward = -1 #negative reward for false prediction
            print("episode ended: Agent predicted satisfiable incorrectly")
        else:
            reward = 1 #positive reward for correct prediction
            print("episode ended: Agent predicted satisfiable correctly")
            
        self._episode_ended = True
        return ts.termination(self._state.flatten(), reward)
    
    elif action not in self._state or -action not in self._state:
        #if literal in not present in formula
        reward = -1
        print("agent chose a literal not found in cnf")
        
        self._episode_ended = True
        return ts.termination(self._state.flatten(), reward)
    
    else:
        #agent chose a literal to simplify the formula
        self._state = self.simplify(self._state, action)   
        minisat_updated_cnf = self.minisat_reformat(self._state)
        
        if self.generator.solveCnf(minisat_updated_cnf) != self.initial_label:
            print("episode ended: Agent simplified the cnf making it unsatisfiable when it was satisfiable")
            #if the agent's implification made it unsatifiable when it was satisfiable
            self._episode_ended = True
            reward = -1
            return ts.termination(self._state.flatten(), reward)

    return ts.transition(self._state.flatten(), reward, discount=1.0)
    

  def current_time_step(self):
    return self._current_time_step

  def render(self):
    print(self._state)
