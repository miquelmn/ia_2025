import copy
from tictac import victoria

class Estat:

    def __init__(self, taulell, fitxa: str, accions_previes=None):
        self.taulell = taulell

        if accions_previes is None:
            accions_previes = []

        self.accions_previes = accions_previes
        self.fitxa = fitxa

        self.__es_meta = None

    def __hash__(self):
        return hash(str(self.taulell) + "," + self.fitxa)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __repr__(self):
        return str(self.taulell)

    def es_ple(self):
        ocupats = 0

        for row in self.taulell:
            for casella in row:
                ocupats += int(casella != " ")

        return ocupats == len(self.taulell[0]) * len(self.taulell[1])

    def guanyador(self):
        if self.__es_meta is None:
            for pos in [(0, 0), (1, 1), (2, 2)]:
                meta = victoria.victoria(self.taulell, pos)
                if meta:
                    break

            self.__es_meta = meta

        return self.__es_meta

    def es_meta(self) -> bool:
        ple = self.es_ple()
        guanyador = self.guanyador()

        return guanyador or ple


    def accions_possibles(self):
        accions = []
        for pos_x in range(len(self.taulell)):
            for pos_y in range(len(self.taulell[0])):
                casella = self.taulell[pos_x][pos_y]
                if casella == " ":
                    accions.append((pos_x, pos_y))

        return accions

    @property
    def fitxa_contrari(self):
        if self.fitxa == "0":
            return "X"
        else:
            return "0"

    def transicio(self, pos):
        nou_estat = copy.deepcopy(self)
        x, y = pos

        nou_estat.taulell[x][y] = self.fitxa
        nou_estat.fitxa = self.fitxa_contrari
        nou_estat.accions_previes.append((x, y))
        nou_estat.__es_meta = None # Optimització

        return nou_estat

    def genera_fills(self):
        fills = []

        for acc in self.accions_possibles():
            fills.append(self.transicio(acc))


        return fills
