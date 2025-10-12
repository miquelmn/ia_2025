""" Agent Minimax.

Mòdul en el qual es desenvolupa un agent Minimax (sense poda alfa-beta) per resoldre el problema del
Tic-Tac-Toe.

Creat per: Miquel Miró Nicolau (UIB), 2025
"""
from iaLib import agent
from tictac.solucio.estat import Estat



class Agent(agent.Agent):
    def __init__(self):
        super(Agent, self).__init__(long_memoria=1)

    def cerca(self, estat, torn_max=True):
        if estat.es_meta():
            return estat, (1 if not torn_max else -1) # Retornam l'estat i la puntuació

        puntuacio_fills = []

        for fill in estat.genera_fills():
            punt_fill = self.cerca(fill, not torn_max)
            puntuacio_fills.append(punt_fill)

        puntuacio_fills = sorted(puntuacio_fills, key=lambda x: x[1]) # Ordenam pel segon valor guardat a la tupla

        if torn_max:
            return puntuacio_fills[0]
        else:
            return puntuacio_fills[-1]


    def actua(self, percepcio):
        estat_inicial = Estat(percepcio["taulell"], percepcio["torn"])
        res = self.cerca(estat_inicial)

        if isinstance(res, tuple) and res[0].accions_previes is not None and len(res[0].accions_previes) > 0:
            solucio, _ = res
            cami = [solucio.accions_previes[i] for i in range(len(solucio.accions_previes)) if (i % 2 == 0)]

            return "P", cami[0]
        else:
            return "E"
