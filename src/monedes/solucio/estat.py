import copy

SOLUCIO = " XXXC"

class Estat:

    def __init__(self, info, pes: int, accions_previes: list = None):
        if accions_previes is None:
            accions_previes = []

        self.pes = pes
        self.accions_previes = accions_previes

        self.__info = info

    @property
    def accions_possibles(self):
        acc_possibles = []
        pos_blanc = self.__pos_lliure()

        # Girar
        for pos in range(0, 5):
            if pos != pos_blanc:
                acc_possibles.append(("G", pos))

        # Desplaçar
        for desp in (1, -1):
            if 0 <= (pos_blanc + desp) < 5:
                acc_possibles.append(("D", desp))

        # Botar
        for desp in (2, -2):
            if 0 <= (pos_blanc + desp) < 5:
                acc_possibles.append(("B", desp))

        return acc_possibles

    def __pos_lliure(self):
        return self.__info.index(" ")


    def __hash__(self):
        return hash(tuple(self.__info))

    @property
    def info(self):
        return self.__info

    @info.setter
    def info(self, value):
        self.__info = value


    def __eq__(self, other):
        """Overrides the default implementation"""
        return self.__info == other.info

    def es_meta(self) -> bool:
        return self.__info == SOLUCIO

    def transicio(self, acc):
        nou_estat = copy.deepcopy(self)
        acc, pos = acc
        pes = 0

        if acc == "G":
            nou_estat.info[pos] = Estat.gira(nou_estat.info[pos])
            pes = 1
        elif acc == "D" or acc == "B":
            moneda = nou_estat.info[pos]
            if acc == "B":
                moneda = self.gira(moneda)

            nou_estat.info[self.__pos_lliure()] = moneda
            nou_estat.info[pos] = " "
            pes = 2

        return nou_estat, pes


    def genera_fills(self):
        fills = []

        for acc in self.accions_possibles:
            estat_fill, pes = self.transicio(acc)
            estat_fill.accions_previes.append(acc)
            estat_fill.pes += pes

            fills.append(estat_fill)

        return fills

    def calc_heuristica(self):
        pos = self.__pos_lliure()
        heuristica = 0
        for lletra_es, lletra_sol in zip(self.__info, SOLUCIO):
            if lletra_sol != " ":
                heuristica += int(lletra_es != lletra_sol)

        heuristica += pos

        return heuristica + self.pes

    def __str__(self):
        return str(self.__info)

    def __lt__(self, other):
        return False

    @staticmethod
    def gira(moneda):
        if moneda == "C":
            return "X"
        elif moneda == "X":
            return "C"
        else:
            return " "

