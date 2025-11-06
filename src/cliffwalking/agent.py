import numpy as np
import random

from iaLib import agent

class AgentSARSA(agent.Agent):
    def __init__(self, alpha, gamma, seed=0):
        super().__init__(long_memoria=0)

        self.__alpha = alpha
        self.__gamma = gamma
        self.q = None

        np.random.seed(seed)
        random.seed(seed)


    def epsilon_greedy(self, eps):
        """ Selects an action using the epsilon-greedy policy.

        TODO

        Returns:

        """
        pass

    def train(self):
        """ Trains the agent using the SARSA algorithm.

        TODO

        Returns:

        """
        pass


    def actua(self, estat):
        """ Selects an action for the given state.

        TODO

        Args:
            estat:

        Returns:

        """
        pass

