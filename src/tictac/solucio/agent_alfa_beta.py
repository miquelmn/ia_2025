""" Agent Minimax amb poda alfa-beta.

Mòdul en el qual es desenvolupa un agent Minimax amb poda alfa-beta per resoldre el problema del
Tic Tac Toe.

Creat per: Miquel Miró Nicolau (UIB), 2025
"""
from iaLib import agent
from tictac.solucio.estat import Estat

class Agent(agent.Agent):
    def __init__(self, poda = False):
        super(Agent, self).__init__(long_memoria=1)
        self.__cami_exit = None
        self.__poda = poda

    def cerca(self, estat: Estat, alpha, beta, torn_max=True):
        if estat.es_meta():
            res = 0
            if estat.guanyador():
                res = (1 if not torn_max else -1)
            return estat, res

        puntuacio_fills = []

        for fill in estat.genera_fills():
            punt_fill = self.cerca(fill, alpha, beta, not torn_max)

            if torn_max:
                alpha = max(alpha, punt_fill[1])
            else:
                beta = min(beta, punt_fill[1])

            puntuacio_fills.append(punt_fill)

            if alpha >= beta:
                break


        puntuacio_fills = sorted(puntuacio_fills, key=lambda x: x[1])
        if torn_max:
            return puntuacio_fills[-1]
        else:
            return puntuacio_fills[0]

    def pinta(self, display):
        pass

    def actua(self, percepcio):
        estat_inicial = Estat(percepcio["taulell"], percepcio["torn"])
        res = self.cerca(estat_inicial, alpha=-float('inf'), beta=float('inf'))

        if isinstance(res, tuple) and res[0].accions_previes is not None and len(res[0].accions_previes) > 0:
            solucio, _ = res
            cami = [solucio.accions_previes[i] for i in range(len(solucio.accions_previes)) if (i % 2 == 0)]

            return "P", cami[0]
        else:
            return "E"

