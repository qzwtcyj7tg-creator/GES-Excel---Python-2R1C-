from pathlib import Path

import matplotlib.pyplot as plt

# from ges_2r1c import vergleich

from .engine import run_simulation
from .export import export_results
from .plotter import Plotter
from .raum import create_c320
from .wetter import lade_wetterdaten
from .zeitplan import create_zeitplan
from .sonnenstand import sonnenstand
from .gui import gui
from .interne_lasten import calc_interne_lasten, calc_interne_lasten_schule


def main():
    project_root = Path(__file__).parent.parent

    # Raum erstellen
    raum = create_c320()

    # GUI aufrufen
    raum = gui(raum)

    if raum is None:
        return print("None")

    for f in raum.fenster:
        print(f"{f.name} erfolgreich angelegt!")

    print(f"Raum {raum.name} erfolgreich angelegt!")

    # Wetterdaten laden
    ta, stunden, direkt, diffus = lade_wetterdaten(
        project_root / "data" / "input" / "wetterdaten.xlsx"
    )

    # Nutzungssignal erstellen
    nutzersignal = create_zeitplan()

    # Sonnenstand berechnen für das ganze Jahr (Augsburg)
    alpha_liste, theta_liste, delta_liste = sonnenstand(lange = 10.5, breite = 48.1, zeitzonen_offset = 15)

    # Interne Lasten berechnen (Profil Schule bzw. Uni)
    phi_intern = calc_interne_lasten_schule(raum, nutzersignal)

    # Simulation durchführen
    res = run_simulation(
        raum=raum,
        ta=ta,
        nsf=nutzersignal,
        direkt=direkt,
        diffus=diffus,
        phi_intern=phi_intern,
        alpha_liste=alpha_liste,
        theta_liste=theta_liste,
    )

    # Ergebnisse exportieren
    output_dir = project_root / "data" / "output"
    export_results(res, ta, nutzersignal, nutzersignal, phi_intern, direkt, alpha_liste, theta_liste, delta_liste, output_dir)

    # Plotten
    plotter = Plotter(stunden=stunden, ta=ta, res=res,
                      raum_name=raum.name, flaeche=raum.grundflaeche)
    plotter.plot_raumklima()
    plotter.zeige_bilanz()
    plt.show()

    # Vergleich mit Referenzdaten
    # from .vergleich import vergleich_plot
    # vergleich_plot(
    #     it_py=res.theta_i,
    #     hl_py=res.phi_hc,
    #     referenz_pfad=project_root / "data" / "input" / "vergleich_hl_it.xlsx",
    #     hl_an=True,
    #     plot_it=True,   
    #     plot_diff=True)


if __name__ == "__main__":
    main()
