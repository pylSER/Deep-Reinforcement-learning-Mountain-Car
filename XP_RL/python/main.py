"""main file of ECE-517 project 2"""

import logging
import pickle
import numpy as np
from RL_SIM import RL_Sim_Env
import matplotlib.pyplot as plt


def river_bomb(width, java_cmd):
    """
    define the river bomb problem
    """

    # states: ( (agent), (bomb) )
    states = []
    for h in range(width):
        for i in range(width):
            for j in range(width):
                for k in range(width):
                    if (h, i) != (j, k):
                        states.append(((h, i), (j, k)))
    # terminal state
    states.append('Delta')

    # actions
    actions = ['E', 'W', 'S', 'N']

    # construct an RL environment
    problem = RL_Sim_Env(
        name='rive_bomb',
        states=states,
        actions=actions,
        java_cmd=java_cmd,
        discount_factor=1.0
    )

    return problem


def plot_canvas(width, state, file):
    """plot canvas with current state"""
    for i in range(width):
        line = ''
        for j in range(width):
            if (i, j) == state[0]:
                line = line + '[&]'
            elif (i, j) == state[1]:
                line = line + '[*]'
            else:
                line = line + '[ ]'
        line = line + '\n'
        file.write(line)
    file.write('\n')
    return


def river_bomb_simulation(name, width, problem, policy, q):
    """
    Simulate a policy, with 'graphic' output.
    """
    print('Simulating...')
    file = open('simulation_{}.txt'.format(name), mode='w+')
    m = problem
    # initialize
    state = np.random.choice(
        m.states, size=1, replace=False,
        p=m.initial_distr
    )[0]
    # state = ((0, 0), (4, 2))
    # iteration
    iter = 0
    while state != 'Delta':
        action = policy[state]
        new_state = m.trans_func(state, action)
        file.write('Iteration {}:\n'.format(iter))
        file.write('q values of taking four actions:\n')
        file.write('E: {}; S: {}; W: {}; N: {}.\n'.format(
            round(q[state, 'E'], 2),
            round(q[state, 'S'], 2),
            round(q[state, 'W'], 2),
            round(q[state, 'N'], 2)
        ))
        file.write('Take action {}.\n'.format(action))
        plot_canvas(width, state, file)
        state = new_state
        iter += 1
        if iter > 50:
            return
    file.close()
    return


def draw_return():
    """
    draw return
    """
    # import return
    returns = pickle.load(open('G.pickle', 'rb'))
    # plot
    fig, ax = plt.subplots(nrows=1, ncols=1)
    ax.plot(
        list(returns.keys()), list(returns.values())
    )
    fig.savefig('G.png', dpi=600)
    return


def plot_G(window):
    """
    plot return using time window
    """
    G = pickle.load(open('G.pickle', 'rb'))
    G_plot = {}
    ind = window
    while ind <= len(G):
        G_plot[ind-1] = np.mean([
            G[i]
            for i in range(ind - window, ind, 1)
        ])
        ind += 1
    fig, ax = plt.subplots(nrows=1, ncols=1)
    ax.plot(list(G_plot.keys())[20:], list(G_plot.values())[20:])
    ax.plot(
        list(G_plot.keys()), [100]*len(list(G_plot.keys())),
        'r-'
    )
    ax.plot(
        list(G_plot.keys()), [0]*len(list(G_plot.keys())),
        'r-'
    )
    fig.savefig('G.png', dpi=600)
    return


def main():
    """main"""

    logging.basicConfig(
        filename='robot_bomb.log',
        filemode='w+',
        format='%(levelname)s - %(message)s',
        level=logging.INFO
    )

    # parameters
    n = 2000
    d = 8
    e = 0.1
    a = 0.1
    java_cmd = [
        '/Library/Java/JavaVirtualMachines/jdk-13.0.1.jdk'
        '/Contents/Home/bin/java',
        '-Dfile.encoding=UTF-8',
        '@/var/folders/gg/1jfz30d15h309vq0rylkp93m0000gp/T'
        '/cp_45t0qy2e04j1eyjrbfxpq5knz.argfile',
        'p.App'
    ]

    # random seed
    # np.random.seed(1)

    # construct problem, change reward here.
    problem = river_bomb(d, java_cmd)

    # run algorithm
    print('Solving...')
    results = problem.Q_Leaning(
        episodes=n,
        b_policy='e-greedy',
        epsilon=e,
        alpha=a
    )
    pickle.dump(results[0], open('policy.pickle', 'wb'))
    pickle.dump(results[2], open('G.pickle', 'wb'))
    plot_G(25)
    '''
    simulation_name = 'Q'
    # after solving, simulates the learned policy.
    river_bomb_simulation(
        name=simulation_name,
        width=d,
        problem=problem,
        policy=results[0],
        q=results[1]
    )
    '''
    return


if __name__ == "__main__":
    main()
