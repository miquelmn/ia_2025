from queue import PriorityQueue
from monedes.solucio.estat import Estat

from iaLib import agent

SOLUCIO = " XXXC"


class AgentMoneda(agent.Agent):
    def __init__(self):
        super().__init__(long_memoria=0)
        self.__frontera = None
        self.__tancats = None
        self.__accions = None

    def pinta(self, display):
        print(self._posicio_pintar)

    def cerca(self, estat_inicial):
        self.__frontera = PriorityQueue()
        self.__tancats = set()

        self.__frontera.put((estat_inicial.calc_heuristica(), estat_inicial))

        actual = None
        while not self.__frontera.empty():
            _, actual = self.__frontera.get()
            if actual in self.__tancats:
                continue

            if actual.es_meta():
                break

            estats_fills = actual.genera_fills()

            for estat_f in estats_fills:
                self.__frontera.put((estat_f.calc_heuristica(), estat_f))

            self.__tancats.add(actual)

        if actual.es_meta():
            self.__accions = actual.accions_previes

    def actua(self, percepcio):
        estat_inicial = Estat(list(percepcio["Monedes"]), 0)

        if self.__accions is None:
            self.cerca(estat_inicial)

        if self.__accions:
            acc = self.__accions.pop(0)

            return acc[0], acc[1]
        else:
            return "R"
