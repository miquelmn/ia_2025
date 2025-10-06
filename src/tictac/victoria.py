""" Mòdul per determinar si hi ha una victòria en un joc de tauler com el Tic-Tac-Toe.

Creat per: Miquel Miró Nicolau (UIB), 2025
"""

def victoria(taulell, posicio, dificultat=3):
    """ Determina si hi ha una victòria en el taulell donada una posició i dificultat.

    Args:
        taulell: Llista de llistes representant el taulell.
        posicio: Tupla (x, y) representant la posició a comprovar.
        dificultat: Enter representant la dificultat (nombre de fitxes en línia necessàries per guanyar).

    Returns:
        Boolean: True si hi ha una victòria, False en cas contrari.
    """
    horizontal_check = __linear_check(taulell, posicio, dificultat=dificultat)
    vertical_check = __linear_check(taulell, posicio, dificultat=dificultat, vertical=True)

    diagonal_check_tl = __diagonal_check(taulell, posicio, (+1, -1), dificultat=dificultat)
    diagonal_check_tr = __diagonal_check(taulell, posicio, (+1, +1), dificultat=dificultat)

    return (
            horizontal_check or vertical_check or diagonal_check_tl or diagonal_check_tr
    )


def __diagonal_check(taulell, posicio, desp, dificultat):
    """ Comprova si hi ha una línia diagonal de fitxes iguals en el taulell.

    Mètode auxiliar per a la funció `victoria`.

    Args:
        taulell: Llista de llistes representant el taulell.
        posicio: Tupla (x, y) representant la posició a comprovar.
        desp: Tupla (dx, dy) representant la direcció de la diagonal.
        dificultat: Enter representant la dificultat (nombre de fitxes en línia necessàries per guanyar).

    Returns:
        Boolean: True si hi ha una línia diagonal de fitxes iguals, False en cas contrari.
    """
    continu = False
    count = 0
    best_lineal = 0

    fitxa = None

    for i, j in zip(
            range(
                posicio[0] - (dificultat * desp[0]), posicio[0] + (dificultat * desp[0]), desp[0]
            ),
            range(
                posicio[1] - (dificultat * desp[1]), posicio[1] + (dificultat * desp[1]), desp[1]
            ),
    ):
        if not (0 <= i < len(taulell) and 0 <= j < len(taulell[0])):
            continue

        if fitxa is None and taulell[i][j] in ("X", "0"):
            fitxa = taulell[i][j]

        if taulell[i][j] == fitxa:
            if not continu:
                continu = True
            count += 1
        else:
            continu = False
            if count > best_lineal:
                best_lineal = count
            count = 0

    if count > best_lineal:
        best_lineal = count

    return best_lineal >= dificultat


def __linear_check(taulell, posicio, dificultat, vertical=False):
    """ Comprova si hi ha una línia horitzontal o vertical de fitxes iguals en el taulell.

    Funció auxiliar per a la funció `victoria`.

    Args:
        taulell: Llista de llistes representant el taulell.
        posicio: Tupla (x, y) representant la posició a comprovar.
        dificultat: Tuple (dx, dy) representant la direcció de la diagonal.
        vertical: Boolean indicant si es comprova en vertical (True) o horitzontal (False).

    Returns:
        Boolean: True si hi ha una línia horitzontal o vertical de fitxes iguals, False en cas contrari.
    """
    continu = False
    count = 0
    best_lineal = 0

    fitxa = None

    pos_1, pos_2 = posicio
    for x in range(
            max(pos_1 - dificultat, 0),
            min(pos_1 + dificultat, len(taulell)),
            1,
    ):
        i, j = x, pos_2
        if vertical:
            i, j = j, i

        if fitxa is None and taulell[i][j] in ("X", "0"):
            fitxa = taulell[i][j]

        if taulell[i][j] == fitxa:
            if not continu:
                continu = True
            count += 1
        else:
            continu = False
            if count > best_lineal:
                best_lineal = count
            count = 0

    if count > best_lineal:
        best_lineal = count

    return best_lineal >= dificultat
