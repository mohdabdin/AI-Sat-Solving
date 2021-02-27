import tensorflow as tf
import numpy as np

from tf_agents.environments import py_environment
from tf_agents.specs import array_spec

from tf_agents.trajectories import time_step as ts


from cnfGenerator import cnfGenerator

tf.compat.v1.enable_v2_behavior()

class CnfSolverEnv(py_environment.PyEnvironment):
  def __init__(self):
    self._action_spec = array_spec.BoundedArraySpec(
        shape=(), dtype=np.int32, minimum=0, maximum=40, name='action')
    self._observation_spec = array_spec.BoundedArraySpec(
        shape=(1,), dtype=np.int32, minimum=0, name='observation')
    self.generator = cnfGenerator(n_variables = 10, clause_range=(1,3), cnf_size=40)
    self.cnf = self.generator.generateCnf()
    self.initial_label = self.generator.solveCnf(self.cnf)
    self._state = self.cnf
    self._episode_ended = False

  def action_spec(self):
    return self._action_spec

  def observation_spec(self):
    return self._observation_spec

  def _reset(self):
    self.cnf = self.generator.generateCnf()
    self._state = self.cnf
    self._episode_ended = False
    return ts.restart(self._state)

  def simplify(self, lit):
    c=0
    while c<len(self.cnf):
      if -lit in self.cnf[c]:
        self.cnf[c].remove(-lit)
      if not self.cnf[c] or lit in self.cnf[c]:
        self.cnf.remove(self.cnf[c])
      c+=1
    return self.cnf
  
  def _step(self, action):
    reward = 0
    
    if action==0:
        #agent predicts unsatifiable
        if self.initial_label == True:
            reward = -1 #negative reward for false prediction
            print("Agent predicted unsatisfiable incorrectly")
        else:
            reward = 1 #positive reward for correct prediction
            print("Agent predicted unsatisfiable correctly")
            
        self._episode_ended = True
        return ts.termination(self._state, reward)
    
    elif action==99:
        #agent predicts satisfiable
        if self.initial_label == False:
            reward = -1 #negative reward for false prediction
            print("Agent predicted satisfiable incorrectly")
        else:
            reward = 1 #positive reward for correct prediction
            print("Agent predicted satisfiable correctly")
            
        self._episode_ended = True
        return ts.termination(self._state, reward)
    
    else:
        #agent chosen a literal to simplify the formula
        updated_cnf = self.simplify(action)   
        if self.generator.solveCnf(updated_cnf) != self.initial_label:
            #if the agent's implification made it unsatifiable when it was satisfiable
            self._episode_ended = True
            reward = -1
            return ts.termination(self._state, reward)

    self._state = updated_cnf
    return ts.transition(self._state, reward, discount=1.0)
    

  def current_time_step(self):
    return self._current_time_step

  def render(self):
    print(self._state)













