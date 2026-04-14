from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

from .results import HOURS_PER_YEAR, SimulationResults


def export_results(
    res: SimulationResults,
    ta: np.ndarray,
    nsf: np.ndarray,
    nutzersignal: np.ndarray,
    phi_intern: np.ndarray,
    direkt: np.ndarray,
    output_dir: Path,
) -> Path:
    """Exportiert Simulationsergebnisse als Excel-Datei.

    Returns:
        Pfad zur erstellten Datei.
    """
    export_df = pd.DataFrame({
        "Stunde": np.arange(1, HOURS_PER_YEAR + 1),
        "Außentemperatur [°C]": ta,
        "Nutzungssignal (Simulation) [-]": nsf,
        "Nutzungssignal (Zeitplan Klasse) [-]": nutzersignal,
        "Interne Gewinne [W]": phi_intern,
        "Zulufttemperatur [°C]": res.t_zul,
        "Volumenstrom [m3/h]": res.v_punkt,
        "Heizregister_Leistung [W]": res.phi_heizregister,
        "Heizung [W]": res.phi_hc,
        "Innentemp [°C]": res.theta_i,
        "Solare Einstrahlung [W]": direkt,
        "Temp nach WRG [°C]": res.t_nach_wrg,
        "Temp Abl [°C]": res.t_abl,
        "HV": res.h_v,
        "Theta Test": np.zeros(HOURS_PER_YEAR),
        "Theta 0W": res.theta_0W,
        "T Soll": res.t_soll,
    })

    output_dir.mkdir(parents=True, exist_ok=True)
    datum = datetime.now().strftime("%Y%m%d")
    dateiname = output_dir / f"Zuluft_Ergebnisse_{datum}.xlsx"

    try:
        export_df.to_excel(dateiname, index=False)
        print(f"\nERFOLG: '{dateiname}' wurde erstellt.")
    except PermissionError:
        print("\nFEHLER: Die Excel-Datei ist noch offen. Bitte schließen und Skript erneut starten.")
    except Exception as e:
        print(f"\nFehler beim Export: {e}")

    return dateiname
