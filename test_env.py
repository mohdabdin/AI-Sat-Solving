import numpy as np
import Environment as env
import random
import time

cnfEnv = env.CnfSolverEnv()
action_array = [0,1,2,3,4,5,6,7,8,9,10,99]

cnfEnv.reset()
for _ in range(100):
    action = random.choice(action_array)
    cnfEnv.step(action)
    time.sleep(0.5)
