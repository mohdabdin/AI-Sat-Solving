from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import abc
import tensorflow as tf
import numpy as np

from tf_agents.environments import py_environment
from tf_agents.environments import tf_environment
from tf_agents.environments import tf_py_environment
from tf_agents.environments import utils
from tf_agents.specs import array_spec
from tf_agents.environments import wrappers
from tf_agents.environments import suite_gym
from tf_agents.trajectories import time_step as ts

from pysat.solvers import Minisat22

import cnfGenerator as gen


tf.compat.v1.enable_v2_behavior()

class CnfSolverEnv(py_environment.PyEnvironment):
  def __init__(self):
    self._action_spec = array_spec.BoundedArraySpec(
        shape=(1), dtype=np.int32, minimum=0, maximum=40, name='action')
    self._observation_spec = array_spec.BoundedArraySpec(
        shape=(1,), dtype=np.int32, minimum=0, name='observation')
    self.generator = gen(n_variables = 10, clause_range=(1,3), cnf_size=40)
    self._state = np.zeros(self.cnf.shape)
    self._episode_ended = False

  def action_spec(self):
    return self._action_spec

  def observation_spec(self):
    return self._observation_spec

  def _reset(self):
    self.cnf = self.generator.generateCnf()
    self._state = np.zeros(self.cnf.shape)
    self._episode_ended = False
    return ts.restart(np.array([self._state], dtype=np.int32))

  def _step(self, action):
    reward = 0
    return ts.transition(np.array([self._state], dtype=np.int32), reward, discount=1.0)

  def render(self):
    print(self.observation_spec())






