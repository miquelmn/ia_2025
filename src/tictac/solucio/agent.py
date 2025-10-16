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

    def cerca(self, estat, torn_max=True, iter=0):
        if estat.es_meta():
            res = 0
            if estat.guanyador():
                res = (1 if not torn_max else -1)
            return estat, res

        puntuacio_fills = []
        fills = estat.genera_fills()

        for fill in fills:
            punt_fill = self.cerca(fill, not torn_max, iter + 1)
            puntuacio_fills.append(punt_fill)

        idx = Agent.arg_max(puntuacio_fills, not torn_max)

        return puntuacio_fills[idx]

    @staticmethod
    def arg_max(estats, reverse=False):
        """ Troba l'índex de l'estat amb la puntuació més alta, o més baixa si reverse és True.

        Args:
            estats: Llista de tuples (Estat, puntuació).
            reverse: Si és True, busca la puntuació més baixa.

        Returns:
            Enter, índex de l'estat amb la puntuació més alta o més baixa.
        """
        major_idx = 0
        major_puntuacio = estats[0][1]

        if reverse:
            major_puntuacio *= -1

        for i, estat in enumerate(estats):
            puntuacio_estat = estat[1]
            if reverse:
                puntuacio_estat *= -1

            if puntuacio_estat > major_puntuacio:
                major_idx = i
                major_puntuacio = puntuacio_estat

        return major_idx

    def actua(self, percepcio):
        estat_inicial = Estat(percepcio["taulell"], percepcio["torn"])
        res = self.cerca(estat_inicial)

        if isinstance(res, tuple) and res[0].accions_previes is not None and len(res[0].accions_previes) > 0:
            solucio, _ = res
            cami = [solucio.accions_previes[i] for i in range(len(solucio.accions_previes)) if (i % 2 == 0)]

            return "P", cami[0]
        else:
            return "E"
