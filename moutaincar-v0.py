# '''
# https://gym.openai.com/docs/
# '''
import gym
import numpy as np

env = gym.make("MountainCar-v0")
env = env.unwrapped

# env.reset()

LEARNING_RATE = 0.1
DISCOUNT = 0.95
EPISODES = 1000

EPSILON = 0.50
START_EPISILON_DECAYING = 1
END_EPISOLON_DECAYING = EPISODES // 2

epsilon_decay_value = EPSILON / (END_EPISOLON_DECAYING - START_EPISILON_DECAYING)

# print(env.observation_space.high)
# print(env.observation_space.low)
# print(env.action_space.n)

SHOW_EVERY = 20 

DISCRETE_OS_SIZE = [20] * len(env.observation_space.high)
DISCRETE_OS_WIN_SIZE = (env.observation_space.high - env.observation_space.low) / DISCRETE_OS_SIZE

# print(DISCRETE_OS_SIZE)
# print(DISCRETE_OS_WIN_SIZE)

q_table = np.random.uniform(low=-2, high=0, size=(DISCRETE_OS_SIZE) + [env.action_space.n])

# print(q_table.shape)

def get_discrete_state(state):
    discrete_state = (state - env.observation_space.low) / DISCRETE_OS_WIN_SIZE
    return tuple(discrete_state.astype(np.int))

for episode in range(EPISODES):
    if episode % SHOW_EVERY == 0:
        print(episode)
        render = True        
    else:
        render = False

    discrete_state = get_discrete_state(env.reset())
    done = False
    while not done:
        if np.random.random() > EPSILON:
            action = np.argmax(q_table[discrete_state])
        else:
            action = np.random.randint(0, env.action_space.n)

        new_state, reward, done, _ =  env.step(action)
        new_discrete_state = get_discrete_state(new_state)
        # print(reward, new_state)

        if (render):
            env.render()
        if not done:
            max_future_q = np.max(q_table[discrete_state])
            current_q = q_table[discrete_state + (action,)]

            new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)
            q_table[discrete_state + (action, )] = new_q
        elif new_state[0] >= env.goal_position:
            print(f"We made it on episode {episode}")
            q_table[discrete_state + (action,)] = 0
            break

        discrete_state = new_discrete_state

    if END_EPISOLON_DECAYING >= episode >= START_EPISILON_DECAYING:
        EPSILON -= epsilon_decay_value
        
env.close()
