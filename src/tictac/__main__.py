from tictac import joc
from tictac.solucio import agent as agent


def main():
    quatre = joc.Taulell(
        [agent.Agent(), agent.Agent()],
        mida_taulell=(3, 3),
        dificultat=3,
    )
    quatre.comencar()


if __name__ == "__main__":
    main()
