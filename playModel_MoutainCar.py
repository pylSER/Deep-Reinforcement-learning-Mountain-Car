import gym
import numpy as np

env = gym.make("MountainCar-v0")
env = env.unwrapped

env.reset()

print(env.observation_space.high) # position and velocity # [0.6  0.07]
print(env.observation_space.low) # [-1.2  -0.07]
print(env.action_space.n) # 3

DISCRETE_OS_SIZE = [20] * len(env.observation_space.high)
DISCRETE_OS_WIN_SIZE = (env.observation_space.high - env.observation_space.low) / DISCRETE_OS_SIZE

print(DISCRETE_OS_SIZE) # [20, 20]
print(DISCRETE_OS_WIN_SIZE) # [0.09  0.007]

q_table = np.random.uniform(low=-2, high=0, size=(DISCRETE_OS_SIZE) + [env.action_space.n])
#
# 
print(q_table.shape)

def get_discrete_state(state):
    discrete_state = (state - env.observation_space.low) / DISCRETE_OS_WIN_SIZE
    return tuple(discrete_state.astype(np.int))

num_states = (env.observation_space.high - env.observation_space.low)*\
                    np.array([10, 100])
num_states = np.round(num_states, 0).astype(int) + 1
print(num_states)