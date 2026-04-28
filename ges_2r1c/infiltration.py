# Berechnung Infiltration (Vereinfachtes Verfahren nach DIN EN 12831)
from .raum import RaumEingabe  


def infiltration_volstr(raum: RaumEingabe) -> float:
    # n_50 Luftwechselrate bei einer Druckdifferenz von 50 Pa
    # e_i Abschirmungsfaktor
    # epsilon_i Höhenkorrekturfaktor
    # Konstant: 2 * (10,85 * 7,9 * 3,13) * 0,02 * 1 * 1,5 = 16,09 m³/h (Vereinfacht!)
    # Effektiver Luftwechsel von 0,06h-1

    return 2 * raum.volumen * raum.e_i * raum.eps_i * raum.n_50

def infiltration_volstr_2():
    # Genaueres Verfahren
    return None