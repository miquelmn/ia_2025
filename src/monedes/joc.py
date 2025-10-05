import random

import pygame
from importlib.resources import files

from iaLib import agent, joc


class Moneda(joc.Joc):
    def __init__(self, agents: list[agent.Agent], random_order: bool = False):
        super(Moneda, self).__init__(agents, (800, 512), title="Casa")

        monedes = "CXCX "

        if random_order:
            monedes = ''.join(random.sample(monedes, len(monedes)))

        print(f"Monedes {monedes}")

        self.__monedes = monedes

    @staticmethod
    def __gira(caract: str):
        if caract == "C":
            return "X"
        elif caract == "X":
            return "C"
        else:
            return caract

    def __empty_pos(self) -> int:
        return self.__monedes.find(" ")

    def _aplica(self, accio, params=None, agent_actual=None) -> None:
        id_moneda = params
        monedes_aux = list(self.__monedes)
        if accio == "D": # Desplaçar
            if (self.__empty_pos() != (id_moneda - 1)) and (
                    self.__empty_pos() != (id_moneda + 1)
            ):
                raise joc.HasPerdut("Moneda una damunt l'altra")
            monedes_aux[id_moneda] = " "
            monedes_aux[self.__empty_pos()] = self.__monedes[id_moneda]
        elif accio == "B": # Botar
            if (self.__empty_pos() != (id_moneda - 2)) and (
                    self.__empty_pos() != (id_moneda + 2)
            ):
                raise joc.HasPerdut("Moneda una damunt l'altra")
            monedes_aux[id_moneda] = " "
            monedes_aux[self.__empty_pos()] = self.__gira(self.__monedes[id_moneda])
        elif accio == "G": # Girar
            monedes_aux[id_moneda] = self.__gira(self.__monedes[id_moneda])
        elif not accio == "R": # Res
            raise Exception(f"Acció no existent en aquest joc: {accio}")

        self.__monedes = "".join(monedes_aux)

    def _draw(self) -> None:
        super(Moneda, self)._draw()
        window = self._game_window
        window.fill(pygame.Color(0, 255, 189))

        img_path = files("monedes.images") / "cara.png"
        cara = pygame.image.load(img_path)
        cara = pygame.transform.scale(cara, (150, 150))

        img_path = files("monedes.images") / "creu.png"
        creu = pygame.image.load(img_path)
        creu = pygame.transform.scale(creu, (150, 150))

        for i, c in enumerate(self.__monedes):
            if c == 'X':
                window.blit(creu, (20 + (i * 150), 181))
            elif c == 'C':
                window.blit(cara, (20 + (i * 150), 181))

    def percepcio(self) -> dict:
        return {"Monedes": self.__monedes}
