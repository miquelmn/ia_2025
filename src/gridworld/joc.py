""" GridWorld environment module.

This module implements a simple GridWorld environment where an agent can move in four directions
(North, South, East, West) within a grid. The agent receives rewards or penalties based on its
actions and the specific cells it visits.
"""
from iaLib import joc


class GridWorld(joc.JocNoGrafic):
    """
    A maze with walls. An agent is placed at the start cell and must find the exit cell by moving
    through the maze.
    """

    actions = ["N", "S", "O", "E"]  # all possible actions

    penalty_move = (
        -1
    )

    def __init__(
            self,
            start_cell,
            size=None
    ):
        """Create a gridworld environment
        """
        if size is None:
            size = (5, 5)
        super().__init__([])

        self.__size = size
        self.__start_cell = self.__previous_cell = self.__current_cell = start_cell

    @property
    def size(self):
        return self.__size

    def _aplica(self, accio, params=None, agent_actual=None):
        """ Move the agent according to 'action' and return the new state, reward and game status.

        Args:
            accio: the agent will move in this direction
            params:
            agent_actual:

        Returns:
            state, reward, status
        """

        reward = self.__execute(accio)
        state = self.__current_cell

        return state, reward

    def step(self, *args, **kwargs):
        return self._aplica(*args, **kwargs)

    def reset(self, start_cell=(0, 0)):
        """ Reset the environment to the initial state.

        Args:
            start_cell: Tuple with the initial cell position of the agent.

        Returns:
            None
        """
        self.__previous_cell = self.__current_cell = self.__start_cell = start_cell

        return self.__current_cell

    @property
    def current_cell(self):
        return self.__current_cell

    def __execute(self, action):
        """Execute action and collect the reward or penalty.

        Args:
            action: direction in which the agent will move (N, S, E, O)

        Returns:
            Float: reward or penalty which results from the action
        """
        possible_actions = self.__possible_actions(self.current_cell)

        reward = 0.0
        x, y = self.__current_cell
        if (x == 1) and (y == 0):
            self.__previous_cell = self.__current_cell
            self.__current_cell = (1, 4)
            reward = 10.0
        elif x == 3 and y == 0:
            self.__previous_cell = self.__current_cell
            self.__current_cell = (3, 2)
            reward = 5.0
        elif action in possible_actions:
            if action == 'O':
                x = max(x - 1, 0)
            elif action == 'E':
                x = min(x + 1, self.size[0] - 1)
            elif action == 'N':
                y = max(y - 1, 0)
            elif action == 'S':
                y = min(y + 1, self.size[0] - 1)

            self.__previous_cell = self.__current_cell
            self.__current_cell = x, y
        else:
            self.__previous_cell = self.__current_cell
            reward = -1.0

        return reward

    def __possible_actions(self, cell):
        """Create a list with all possible actions from 'cell', avoiding the maze's edges and
        walls.

        Args:
            cell (tuple): location of the agent

        Returns:
            list: all possible actions
        """
        row, col = cell

        possible_actions = GridWorld.actions.copy()  # initially allow all

        # now restrict the initial list by removing impossible actions
        nrows, ncols = self.size
        if row == 0:
            possible_actions.remove("O")
        if row == (nrows - 1):
            possible_actions.remove("E")
        if col == 0:
            possible_actions.remove("N")
        if col == (ncols - 1):
            possible_actions.remove("S")

        return possible_actions

    def percepcio(self):
        """Return the state of the maze: the agent current location

        Returns:
            {'POS': numpy.array [1][2]: agents current location}
        """

        pos = self.__current_cell
        return {"POS": pos}

    def _draw(self):
        pass

    def __str__(self):
        return str(self.__current_cell)

    def __repr__(self):
        return self.__str__()