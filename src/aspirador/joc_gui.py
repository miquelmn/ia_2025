""" Joc de l'aspirador.

Autor: Miquel Miró Niclau (UIB), 2024

"""
import random
import enum

import pygame
from iaLib import joc


class AspiradorRomput(Exception):
    """Excepció aixecada quan l'aspirador es romp."""

    def __init__(self):
        self.message = "L'aspirador ha caigut i s'ha romput"
        super().__init__(self.message)


class Aspirador(joc.Joc):
    """
    Accions disponibles:
        - "A": Aspira
        - "D": Dreta
        - "E": Esquerra
        - "S": Atura
    """

    def __init__(self, agents):
        super(Aspirador, self).__init__(agents, mida_pantalla=(512, 512), title="Casa")

        self.__habitacions = [
            bool(random.randint(0, 1)),
            bool(random.randint(0, 1))
        ]  # True -> Net

        self.__loc = bool(random.randint(0, 1))

    def _aplica(self, accio, params=None, agent_actual=None) -> None:
        if accio == "A":
            self.__habitacions[self.__loc] = True
        elif accio == "D":
            if self.__loc == 1:
                raise AspiradorRomput
            self.__loc = 1
        elif accio == "E":
            if self.__loc is 0:
                raise AspiradorRomput
            self.__loc = 0
        elif accio == "S":
            pass
        else:
            raise Exception(f"Acció no existent en aquest joc: {accio}")

    def _draw(self) -> None:
        super(Aspirador, self)._draw()
        window = self._game_window
        window.fill(pygame.Color(255, 255, 255))
        pygame.draw.line(
            window,
            pygame.Color(0, 0, 0),
            (self._mida_pantalla[0] // 2, 0),
            (self._mida_pantalla[0] // 2, self._mida_pantalla[1]),
            2,
        )

        for i, hab in enumerate(self.__habitacions):
            if not hab:
                pygame.draw.rect(
                    window,
                    pygame.Color(0, 0, 0),
                    pygame.Rect((i * self._mida_pantalla[0] // 2) + 50, 50, 20, 20),
                )

        for a in self._agents:
            if self.__loc == 0:
                a.set_posicio((50, self._mida_pantalla[1] // 2))
            else:
                a.set_posicio(
                    ((self._mida_pantalla[0] // 2) + 50, self._mida_pantalla[1] // 2)
                )
            a.pinta(window)

    def percepcio(self) -> dict:
        return {"Loc": self.__loc, "Net": self.__habitacions[self.__loc]}
