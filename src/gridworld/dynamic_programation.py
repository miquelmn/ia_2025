""" Implementació de l'algorisme de programació dinàmica per resoldre el Gridworld.

Autor: Gabriel Moyà Alcover i Miquel Miró Nicolau (UIB), 2025
"""
import numpy as np
from gridworld import joc

key_2_action = {0: "N", 1: "S", 2: "O", 3: "E"}

def dibuixar_matriu(m, decimals=2):
    """ Mostra la matriu m arrodonida al nombre de decimals indicat per paràmetre.

    Args:
        m: Matriu a mostrar
        decimals: Enter que indica el nombre de decimals a mostrar
    """
    grid = np.round(m, decimals)
    for i in range(5):
        for j in range(5):
            print(str(grid[j, i]).rjust(5, " "), end=": ")
        print()

def draw_q(estat_accions):
    """ Mostra les accions òptimes per a cada estat segons els valors Q donats.

    Args:
        estat_accions: Matriu amb els valors Q per a cada estat i acció
    """
    grid = np.round(estat_accions, 2)

    for i in range(5):  # all the rows
        for j in range(5):  # all the columns
            max_q = max(grid[j, i, :])
            direc = np.argwhere(grid[j, i, :] == max_q)
            string = ""
            for s in range(len(direc)):
                string += key_2_action[direc[s][0]]
            print(string.rjust(5, " "), end=" ")
            print(":", end="")
        print(" ")


def main():
    q = np.zeros((5, 5, 4), dtype=float)  # 0 nord, 1 sud, 2 est, 3 oest
    valors = np.zeros((5, 5), dtype=float)

    estat = (0, 0)
    env = joc.GridWorld(estat, (5, 5))

    tol = 1e-3
    Y = 0.9  # discount value
    iterations = 0

    convergence = False
    valors_accio = np.ndarray(4, float)
    while not convergence:
        n_valors = np.zeros_like(valors)
        for i in range(5):  # files
            for j in range(5):  # columnes
                valors_accio[:] = 0
                for idx, accio in enumerate(env.actions):
                    env.reset((i, j))
                    nou_estat, recompensa = env.step(accio)
                    g = recompensa + (Y * valors[nou_estat[0], nou_estat[1]])
                    valors_accio[idx] = g
                n_valors[i, j] = np.max(valors_accio)
                q[i, j, :] = valors_accio

        if np.sum(np.abs(n_valors - valors)) < tol:
            convergence = True

        valors = np.copy(n_valors)
        iterations += 1

    print("===========================================")
    draw_q(q)
    dibuixar_matriu(np.max(q, axis=2))
    print(f" Han estat necessaries {iterations} iteracions")


if __name__ == '__main__':
    main()