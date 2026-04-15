import numpy as np

from .results import HOURS_PER_YEAR


def create_zeitplan() -> np.ndarray:
    """Erstellt das jährliche Nutzungssignal (8760 Stunden).

    Returns:
        Array mit Belegungsfaktor (0.0 bis 1.0) für jede Stunde des Jahres.
    """
    # Tägliche Belegung (9:00 bis 17:00 Uhr)
    t_0 = np.zeros(24)
    t_work = np.zeros(24)
    t_work[9:18] = 0.5

    # Verschiebung um -1 Stunde: TRY-Wetterdaten nutzen 1-basierte Stunden
    t_work = np.roll(t_work, -1)

    # Wochenprofil (Mo-Fr Arbeitstag, Sa+So frei)
    t_mo, t_di, t_mi, t_do, t_fr = [t_work.copy() for _ in range(5)]
    t_sa, t_so = [t_0.copy() for _ in range(2)]

    # Starttag ist Donnerstag (01.01.)
    tage_liste = [t_do, t_fr, t_sa, t_so, t_mo, t_di, t_mi]
    wochen_signal = np.concatenate(tage_liste)
    stundenplan_jahr = np.tile(wochen_signal, 53)[:HOURS_PER_YEAR]

    # Ferienzeiten (Tag-Nummern 0-basiert, Ende exklusiv)
    ferien_maske = np.ones(HOURS_PER_YEAR)
    ferien_tage = [
        (0, 6),       # 01.01. bis 06.01.
        (45, 74),     # 15.02. bis 14.03.
        (105, 106),   # 15.04.
        (211, 275),   # 30.07. bis 01.10.
        (356, 366),   # 22.12. bis Jahresende
    ]

    for start_tag, ende_tag in ferien_tage:
        ferien_maske[start_tag * 24 : ende_tag * 24] = 0

    return stundenplan_jahr * ferien_maske
