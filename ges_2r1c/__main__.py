from pathlib import Path

import matplotlib.pyplot as plt

from ges_2r1c import vergleich
# import numpy as np

from .engine import run_simulation
from .export import export_results
from .plotter import Plotter
from .raum import create_c320
from .wetter import lade_wetterdaten
from .zeitplan import create_zeitplan
from .sonnenstand import sonnenstand


def main():
    project_root = Path(__file__).parent.parent

    # Raum erstellen
    raum = create_c320()
    print(f"Raum {raum.name} erfolgreich angelegt!")

    # Wetterdaten laden
    ta, stunden, direkt, diffus = lade_wetterdaten(
        project_root / "data" / "input" / "wetterdaten.xlsx"
    )

    # Nutzungssignal erstellen
    nutzersignal = create_zeitplan()

    # Interne Lasten berechnen
    phi_pers = 60 * 70       # 4200 W
    phi_geraete = 1400        # 1400 W
    phi_licht = 10 * raum.grundflaeche  # 857 W
    phi_intern = (phi_pers + phi_geraete + phi_licht) * nutzersignal

    # einstrahlung_fenster_1 = sonnenstand(48.2, 10.5 )

    # Simulation durchführen
    res = run_simulation(
        raum=raum,
        ta=ta,
        nsf=nutzersignal,
        direkt=direkt,
        diffus=diffus,
        phi_intern=phi_intern,
    )

    # Ergebnisse exportieren
    output_dir = project_root / "data" / "output"
    export_results(res, ta, nutzersignal, nutzersignal, phi_intern, direkt, output_dir)

    # Plotten
    plotter = Plotter(stunden=stunden, ta=ta, res=res,
                      raum_name=raum.name, flaeche=raum.grundflaeche)
    plotter.plot_raumklima()
    plotter.zeige_bilanz()
    plt.show()

    # Vergleich mit Referenzdaten
    from .vergleich import vergleich_plot
    vergleich_plot(
        it_py=res.theta_i,
        hl_py=res.phi_hc,
        referenz_pfad=project_root / "data" / "input" / "vergleich_hl_it.xlsx",
        hl_an=True,
        plot_it=True,   
        plot_diff=True)


if __name__ == "__main__":
    main()
