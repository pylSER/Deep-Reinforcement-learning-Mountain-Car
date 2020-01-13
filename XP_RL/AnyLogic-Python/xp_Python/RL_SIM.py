"""
Reinforcement learning.
"""

# import
import re
import json
import logging
import subprocess
import numpy as np


class RL_Sim_Env:
    """
    Reinforcement learning class, using ANYLOGIC to simulate;
    - java_cmd: java command to run the model;
    - no transition function;
    """

    def __init__(
        self, name, states, actions, java_cmd, discount_factor
    ):
        self.name = name
        self.states = states
        self.actions = actions
        self.java_cmd = java_cmd
        self.discount_factor = discount_factor

    def __prepare_q(self, q):
        """
        prepare q values to transfer to java.
        """
        q_str = {}
        for key in q.keys():
            if key[0] == 'Delta':
                s = 'Delta-{}'.format(
                    key[1]
                )
            else:
                s = '{}-{}-{}-{}-{}'.format(
                    key[0][0][0], key[0][0][1], key[0][1][0],
                    key[0][1][1], key[1]
                )
            q_str[s] = q[key]
        byte_q = json.dumps(q_str).encode('utf-8')
        return byte_q

    def __execute_java(self, java_cmd, q):
        """
        run java file.
        """
        proc = subprocess.Popen(
            java_cmd, stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        stdout, stderr = proc.communicate(q)
        return stdout.decode("utf-8")

    def __extract_sim_output(self, output):
        """
        extract states, actions and returns
        """
        # get data
        matched = re.findall(r".*?\[(.*)].*", output)
        # states
        states_text = re.findall(r'[+-]?\d+(?:\.\d+)?', matched[0]) ## first part of the output is states; ended with a ]. 
        states = []
        ind = 0
        s = [[0, 0], [0, 0]]
        for i in states_text:
            if ind > 1:
                s[1][ind - 2] = int(i)
            else:
                s[0][ind] = int(i)
            if (ind + 1) % 4 == 0:
                # check if it's Delta
                if s[1][0] < 0 or s[1][0] > 7 or\
                   s[1][1] < 0 or s[1][1] > 7:
                    states.append('Delta')
                else:
                    states.append(
                        (tuple(s[0]), tuple(s[1]))
                    )
                s = [[0, 0], [0, 0]]
                ind = 0
                continue
            ind += 1
        # actions
        actions = []
        for i in matched[1]:
            if i != ' ' and i != ',': # actions are a single char
                actions.append(i)
        # returns
        returns_text = re.findall(r'[+-]?\d+(?:\.\d+)?', matched[2]) # signed/unsigned single float number
        returns = [
            float(i)
            for i in returns_text
        ]
        return states, actions, returns

    def __Q_update(self, q, b_policy, epsilon, alpha):
        """one episode of Q-learning"""
        # make q values byte-like objects
        byte_q = self.__prepare_q(q)
        # run a simulation
        output = self.__execute_java(self.java_cmd, byte_q)
        # print(output)
        # inteprete results
        sim_states, sim_actions, sim_returns = self.__extract_sim_output(
            output
        )
        # averaged return
        G = 0
        # start iteration to update q value
        for iter in range(len(sim_returns)):
            # state
            state = sim_states[iter]
            # termination condition
            if state == 'Delta':
                break
            # take action
            action = sim_actions[iter]
            # get reward
            R = sim_returns[iter]
            # observe reward and new_state
            new_state = sim_states[iter + 1]
            # update q
            G = G + self.discount_factor * R
            q[state, action] = q[state, action] + alpha * (
                R + self.discount_factor * np.max([
                    q[new_state, a]
                    for a in self.actions
                ]) - q[state, action]
            )
        return q, G

    def Q_Leaning(self, episodes, b_policy, epsilon, alpha):
        """
        Q_learning.
        - b_policy: behavior policy. 'e-greedy' or 'random';
        - ternimal state is denoted by 'Delta';
        - alpha: step size;
        - function return: 'policy', 'q', 'G'.
        """
        # initialization
        q = {}
        for s in self.states:
            for a in self.actions:
                q[s, a] = 0
        G = {}
        # loop for episodes
        for iter in range(episodes):
            logging.info("Iteration {}".format(iter))
            q, G[iter] = self.__Q_update(q, b_policy, epsilon, alpha)
            logging.info("G {}".format(G[iter]))

        # find the learned policy
        policy = {}
        for s in self.states:
            policy[s] = self.actions[np.argmax([
                q[s, a]
                for a in self.actions
            ])]

        return policy, q, G

    def simulation(self, q):
        """
        simulation
        """
        byte_q = self.__prepare_q(q)
        output = self.__execute_java(self.java_cmd, byte_q)
        return output
