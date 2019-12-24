import numpy as np
import matplotlib.pyplot as plt

def getStateToRC(state):
    r = state // 6
    c = state % 6
    return r, c

def getRCToState(r, c):
    return int(r*6 + c)

def xp_step(state, action):
    r, c = getStateToRC(state)
    if (r>0 and action == 0):
        r-=1
    if (r<3 and action == 1):
        r+=1
    if (c>1 and action == 2):
        c-=1
    if (c<5 and action == 3):
        c+=1

    state2 = getRCToState(r, c)
    done = False
    reward = -10
    if (state2 == 13):
        done = True
        reward = 100
    return state2, reward, done

env = []

# Define Q-learning function
def QLearning(env, learning, discount, epsilon, min_eps, episodes):
    # Determine size of discretized state space
    num_states = 24
    
    # Initialize Q table
    Q = np.random.uniform(low = -1, high = 1, 
                          size = (24, 4))
    
    # Initialize variables to track rewards
    reward_list = []
    ave_reward_list = []
    
    # Calculate episodic reduction in epsilon
    reduction = (epsilon - min_eps)/episodes
    
    # Run Q learning algorithm
    for i in range(episodes):
        # Initialize parameters
        done = False
        tot_reward, reward = 0,0
        state = np.random.randint(0, 23)
    
        while done != True:                  
            # Determine next action - epsilon greedy strategy
            if np.random.random() < 1 - epsilon:
                action = np.argmax(Q[state]) 
            else:
                action = np.random.randint(0, 3)
                
            # Get next state and reward
            state2, reward, done = xp_step(state, action) 
 
            #Allow for terminal states
            if done:
                Q[state, action] = reward
                
            # Adjust Q value for current state
            else:
                delta = learning * (reward + discount * np.max(Q[state2]) - Q[state, action])
                Q[state, action] += delta
                                     
            # Update variables
            tot_reward += reward
            state = state2
        
        # Decay epsilon
        if epsilon > min_eps:
            epsilon -= reduction
        
        # Track rewards
        reward_list.append(tot_reward)
        
        if (i+1) % 100 == 0:
            ave_reward = np.mean(reward_list)
            ave_reward_list.append(ave_reward)
            reward_list = []
            
        if (i+1) % 100 == 0:    
            print('Episode {} Average Reward: {}'.format(i+1, ave_reward))
            
    # env.close()
    
    return ave_reward_list

# Run Q-learning algorithm
rewards = QLearning(env, 0.2, 0.9, 0.8, 0, 5000)

# Plot Rewards
plt.plot(100*(np.arange(len(rewards)) + 1), rewards)
plt.xlabel('Episodes')
plt.ylabel('Average Reward')
plt.title('Average Reward vs Episodes')
# plt.savefig('rewards.jpg')     
# plt.close()  