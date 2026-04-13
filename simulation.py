# Klassen Import
from validation import validierung_din_12831
import zeitplan 
from raum_parameter import c320
import wetter_import
from rlt import rlt_berechung
from plotter import Plotter
from schleife import schleife
from vergleich_xl import vergleich_plot
from scenario_loader import load_scenario

# Lib Import
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime
from pathlib import Path

# ----- Beginn Hauptskript -----

# YAML Import TEST!
# data = load_scenario('scenarios/din_en_12831.yaml')

# print("Daten aus YAML-Datei:", data)

# Wetterdaten importieren
ta, stunden, direkt, diffus, global_strahl, nsf = wetter_import.lade_wetterdaten(Path(__file__).parent / "import" / "wetterdaten.xlsx")
# Aktuell wird Zeitplan bzw. Nutzersignal über Excel importiert

# Interne Lasten berechnen
phi_pers = 60 * 70  # 4200 W
phi_geraete = 1400  # 1400 W
phi_licht = 10 * c320.grundflaeche  # 857 W

phi_intern = (phi_pers + phi_geraete + phi_licht) * zeitplan.nutzersignal_final # Mit Nutzungssignal multipliziert

# Ergebnisse in Arrays speichern
ergebnis_t_zul = np.zeros(8760)
ergebnis_v_punkt = np.zeros(8760)
ergebnis_phi_lueftung = np.zeros(8760)
ergebnis_phi_heizregister = np.zeros(8760) 
ergebnis_phi_vent = np.zeros(8760)      
ergebnis_phi_hc = np.zeros(8760)
ergebnis_theta_i = np.zeros(8760)
ergebnis_h_v = np.zeros(8760)
ergebnis_t_nach_wrg = np.zeros(8760)
ergebnis_t_abl = np.zeros(8760)
ergebnis_theta_test_i = np.zeros(8760)
ergebnis_theta_0W = np.zeros(8760)
ergebnis_t_soll = np.zeros(8760)


# 1. Startwerte der Simulation
theta_aktuell = 16.0  # Startwert Temperatur
dt = 1.0              # Zeitschritt 1 Stunde

# Simulationsschleife (Aufruf der Funktion in "schleife.py")
theta_aktuell, dt, ergebnis_h_v, ergebnis_phi_hc, ergebnis_phi_heizregister, \
ergebnis_phi_lueftung, ergebnis_phi_vent, ergebnis_t_zul, ergebnis_theta_i, ergebnis_v_punkt = \
    schleife(theta_aktuell, dt, ergebnis_h_v, ergebnis_phi_hc, ergebnis_phi_heizregister,
             ergebnis_phi_lueftung, ergebnis_phi_vent, ergebnis_t_zul, ergebnis_theta_i,
             ergebnis_v_punkt, ta, zeitplan.nutzersignal_final, nsf, direkt, phi_intern, ergebnis_t_nach_wrg, ergebnis_t_abl, ergebnis_theta_test_i, ergebnis_theta_0W,
             ergebnis_t_soll) 

# --- DATEN FÜR EXPORT VORBEREITEN ---

export_df = pd.DataFrame({
    "Stunde": np.arange(1, 8761), # Da bei 1 Angefangen wird zu zählen
    "Außentemperatur [°C]": ta,
    "Nutzungssignal (Simulation) [-]": nsf,
    "Nutzungssignal (Zeitplan Klasse - Funktioniert noch nicht) [-]": zeitplan.nutzersignal_final,
    "Interne Gewinne [W]": phi_intern,  
    "Zulufttemperatur [°C]": ergebnis_t_zul,
    "Volumenstrom [m3/h]": ergebnis_v_punkt,
    "Heizregister_Leistung [W]": ergebnis_phi_heizregister,
    "Heizung [W]": ergebnis_phi_hc,
    "Innentemp [°C]": ergebnis_theta_i,
    "Solare Einstrahlung [W]": direkt,
    "Temp nach WRG [°C]": ergebnis_t_nach_wrg,
    "Temp Abl [°C]": ergebnis_t_abl,
    "HV": ergebnis_h_v,
    "Theta Test": ergebnis_theta_test_i,
    "Theta 0W": ergebnis_theta_0W,
    "T Soll": ergebnis_t_soll

})

# --- SPEICHERN der Berechnungen ---
# Datum
datum = datetime.now().strftime("%Y%m%d")

try:
    dateiname = f"export\\Zuluft_Ergebnisse_{datum}.xlsx"
    export_df.to_excel(dateiname, index=False)
    print(f"\nERFOLG: '{dateiname}' wurde erstellt.")
except PermissionError:
    print("\nFEHLER: Die Excel-Datei ist noch offen. Bitte schließen und Skript erneut starten.")
except Exception as e:
    print(f"\nFehler beim Export: {e}")

# --- PLOTTEN ---
mein_plotter = Plotter(
    stunden=stunden,
    ta=ta,
    ergebnis_t_zul=ergebnis_t_zul,
    ergebnis_phi_lueftung=ergebnis_phi_lueftung,
    ergebnis_phi_heizregister=ergebnis_phi_heizregister,
    ergebnis_phi_vent=ergebnis_phi_vent,
    raum_name=c320.name,
    flaeche=c320.grundflaeche,
    ergebnis_theta_i=ergebnis_theta_i,
    ergebnis_phi_hc=ergebnis_phi_hc
)

# Plot Funktionen
mein_plotter.plot_raumklima()
# mein_plotter.zeige_bilanz_konsole()
# mein_plotter.zeige_plausibilitaet_konsole()
mein_plotter.zeige_bilanz()
plt.show()

validierung_din_12831(norm_ta=-14, norm_ti=21, ergebnis_phi_hc=np.max(ergebnis_phi_hc))

# Vergleich mit Daten aus der Excel-Datei: Innentemperatur, Heizleistung, und Differenz der Innentemperatur (xl vs py)
vergleich_plot(ergebnis_theta_i, ergebnis_phi_hc, plot_it=True, hl_an=True, plot_diff=False)