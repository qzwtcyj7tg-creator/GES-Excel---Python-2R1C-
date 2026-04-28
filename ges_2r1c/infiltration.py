# Berechnung Infiltration (Vereinfachtes Verfahren)
from .raum import RaumEingabe


def infiltration_volstr(raum: RaumEingabe) -> float:
    # n_50 Luftwechselrate bei einer Druckdifferenz von 50 Pa
    # e_i Abschirmungsfaktor
    # epsilon_i Höhenkorrekturfaktor

    return 2 * raum.volumen  * raum.e_i * raum.eps_i