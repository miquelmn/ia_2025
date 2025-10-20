"""
Tasca a fer:
    - Implementa la funció `generate_episode` per generar un episodi seguint una política
        epsilon-greedy.
    - Completa el bucle principal a `main` per actualitzar els valors Q utilitzant l'algorisme de
        Monte Carlo amb política epsilon-greedy.
"""
from gridworld import joc
import numpy as np
import random


def generate_episode(env, state, policy, epsilon):
    # TODO
    pass


def main():
    y = 0.9 # Gamma
    episodis = 2000

    Q = np.zeros((5, 5, 4), dtype=float)
    env = joc.GridWorld((0, 0), (5, 5))
    returns = dict()

    for ep in range(episodis):
        initial_state = random.randint(0, 4), random.randint(0, 4)
        # TODO


if __name__ == "__main__":
    main()
