""" Joc del Tic, tac, toe

Fitxer que implementa un joc de n en línia. La dificultat es paramètrica.

Creat per: Miquel Miró Nicolau (UIB), 2025
"""

import pygame
from iaLib import joc

from tictac import victoria


class Casella:
    def __init__(
        self,
        tipus=" ",
    ):
        self.tipus = tipus

    def draw(self, window, x, y, width=100, height=100):
        pygame.draw.rect(
            window,
            pygame.Color(0, 0, 0),
            pygame.Rect(x * width, y * height, width, height),
            2,
        )

        if self.tipus == "X":
            Casella.drawX(window, (x * 100) + 50, (y * 100) + 50)
        if self.tipus == "0":
            pygame.draw.circle(
                window, (0, 0, 255), ((x * 100) + 50, (y * 100) + 50), 40, width=5
            )

    def posa(self, tipus):
        if self.tipus != " ":
            raise Exception("Has fet trampes: aquesta casella ja està ocupada")
        self.tipus = tipus

    def __str__(self):
        return self.tipus


    @staticmethod
    def drawX(window, x, y):
        pygame.draw.lines(
            window, (255, 0, 0), True, [(x - 45, y - 45), (x + 45, y + 45)], 5
        )
        pygame.draw.lines(
            window, (255, 0, 0), True, [(x - 45, y + 45), (x + 50, y - 45)], 5
        )


class Taulell(joc.Joc):
    def __init__(
        self,
        agents,
        mida_taulell = (8, 8),
        dificultat = 4,
    ):
        super(Taulell, self).__init__(
            agents, (mida_taulell[0] * 100, mida_taulell[1] * 100), title="Minimax"
        )

        self.__caselles = []
        self.__mida_taulell = mida_taulell

        for x in range(mida_taulell[0]):
            caselles_col = []
            for y in range(mida_taulell[1]):
                tipus = " "
                caselles_col.append(Casella(tipus))
            self.__caselles.append(caselles_col)

        self.agents_fitxes = {a.nom: f for a, f in zip(agents, ["0", "X"])}

        if not isinstance(agents, list):
            agents = [agents]

        self._agents = agents
        self.torn = 0
        self.acabat = False
        self.dificultat = dificultat

    def _aplica(
        self, accio, params=None, agent_actual = None
    ) -> None:
        if not self.acabat:
            if accio not in ("E", "P"):
                raise ValueError(f"Acció no existent en aquest joc: {accio}")

            if accio != "E" and not isinstance(params, tuple):
                raise ValueError(f"Paràmetres {params} per acció {accio} són incorrectes")

            if accio == "P":
                pos_x, pos_y = params
                if not (
                    0 <= pos_x < len(self.__caselles)
                    and 0 <= pos_y < len(self.__caselles[0])
                ):
                    raise ValueError(f"Posició {params} fora dels límits")

                self.__caselles[pos_x][pos_y].posa(self.agents_fitxes[agent_actual])
                self.acabat = victoria.victoria(self.__taulell_str(), (pos_x, pos_y))

            if self.acabat:
                print(f"Agent {agent_actual} ha guanyat")
            self.torn += 1

    def _draw(self) -> None:
        super(Taulell, self)._draw()
        window = self._game_window
        window.fill(pygame.Color(255, 255, 255))

        for x in range(len(self.__caselles)):
            for y in range(len(self.__caselles[0])):
                self.__caselles[x][y].draw(window, x, y)

    def __taulell_str(self):
        return [[c.tipus for c in row] for row in self.__caselles]

    def percepcio(self) -> dict:
        return {
            "taulell": self.__taulell_str(),
            "mida": self.__mida_taulell,
            "torn": ("0" if self.torn % 2 == 0 else "X"),
        }
