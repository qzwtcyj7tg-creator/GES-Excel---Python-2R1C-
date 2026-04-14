from pathlib import Path

import numpy as np
import pandas as pd

from .results import HOURS_PER_YEAR


def lade_wetterdaten(dateipfad: Path) -> tuple[np.ndarray, ...]:
    """Lädt TRY-Wetterdaten aus einer Excel-Datei.

    Returns:
        Tuple of (ta, stunden, direkt, diffus, global_strahl, nutzersignal)
    """
    df = pd.read_excel(dateipfad)

    stunden = np.arange(HOURS_PER_YEAR)
    ta = df['t'].values
    direkt = df['B'].values
    diffus = df['D'].values
    global_strahl = direkt + diffus
    nutzersignal = df['NSF'].values

    return ta, stunden, direkt, diffus, global_strahl, nutzersignal
