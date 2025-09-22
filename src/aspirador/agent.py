""" Fitxer que conté els diferents agents aspiradors.

Percepcions:
    "Loc": [0]
    "Net": [1]

Accions:
    AccionsAspirador.DRETA
    AccionsAspirador.ESQUERRA
    AccionsAspirador.ATURA
    AccionsAspirador.ASPIRA

Autor: Miquel Miró Nicolau (UIB), 2022
"""
import abc
from importlib.resources import files

import pygame

from iaLib import agent


class Aspirador(agent.Agent):
    def __init__(self):
        super().__init__(long_memoria=1)

    def pinta(self, display):
        img_path = files("aspirador.images") / "sprite.png"

        img = pygame.image.load(img_path)
        img = pygame.transform.scale(img, (100, 100))
        display.blit(img, self._posicio_pintar)

    @abc.abstractmethod
    def actua(self, percepcio):
        pass


class AspiradorTaula(Aspirador):
    TAULA = {
        (0, True): "D",
        (0, False): "A",
        (1, True): "E",
        (1, False): "S",
    }

    def actua(self, percepcio: dict):
        return AspiradorTaula.TAULA[
            (percepcio["Loc"], percepcio["Net"])
        ]


class AspiradorReflex(Aspirador):
    def actua(self, percepcio: dict):
        """ TODO """


class AspiradorMemoria(Aspirador):
    def actua(self, percepcio: dict):
        """ TODO """

