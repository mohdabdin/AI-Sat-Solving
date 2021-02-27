learning_rate = 1e-3  # @param {type:"number"}

from tf_agents.agents.dqn.dqn_agent import DqnAgent
from tf_agents.environments import tf_py_environment
from tf_agents.environments import suite_gym
from tf_agents.networks.sequential import Sequential
from tf_agents.specs import tensor_spec
from tf_agents.utils import common
from tf import Variable
from tf.keras.layers import Dense
from tf.keras.activations import relu
from tf.keras.initializers import VarianceScaling, RandomUniform, Constant
from tf.keras.optimizers import Adam
from Environment import CnfSolverEnv

env = CnfSolverEnv(None); # Ask M about this later
fc_layer_params = (100, 50)
action_tensor_spec = tensor_spec.from_spec(env.action_spec())
num_actions = action_tensor_spec.maximum - action_tensor_spec.minimum + 1
env_name = '[Our Environment Goes Here]'
train_py_env = suite_gym.load(env_name)
train_env = tf_py_environment.TFPyEnvironment(train_py_env)

# Define a helper function to create Dense layers configured with the right
# activation and kernel initializer.
def dense_layer(num_units):
  return Dense(
      num_units,
      activation = relu,
      kernel_initializer = VarianceScaling(
          scale = 2.0, mode = 'fan_in', distribution ='truncated_normal'))

# QNetwork consists of a sequence of Dense layers followed by a dense layer
# with `num_actions` units to generate one q_value per available action as
# it's output.
dense_layers = [dense_layer(num_units) for num_units in fc_layer_params]
q_values_layer = Dense(
    num_actions,
    activation = None,
    kernel_initializer = RandomUniform(minval = -0.03, maxval = 0.03),
    bias_initializer = Constant(-0.2))
q_net = Sequential(dense_layers + [q_values_layer])

optimizer = Adam(learning_rate=learning_rate)

train_step_counter = Variable(0)

agent = DqnAgent(
    train_env.time_step_spec(),
    train_env.action_spec(),
    q_network=q_net,
    optimizer=optimizer,
    td_errors_loss_fn=common.element_wise_squared_loss,
    train_step_counter=train_step_counter)

agent.initialize()
