import matplotlib.pyplot as plt
import numpy as np

class Plotter:
    def __init__(self, stunden, ta, ergebnis_t_zul, ergebnis_phi_lueftung, 
                 ergebnis_phi_heizregister, ergebnis_phi_vent, raum_name, flaeche,
                 ergebnis_theta_i, ergebnis_phi_hc):
        self.stunden = stunden
        self.ta = ta
        self.t_zul = ergebnis_t_zul
        self.phi_lueftung = ergebnis_phi_lueftung
        self.phi_heizregister = ergebnis_phi_heizregister
        self.phi_vent = ergebnis_phi_vent
        self.raum_name = raum_name
        self.flaeche = flaeche 
        self.theta_i = ergebnis_theta_i
        self.phi_hc = ergebnis_phi_hc

    def plot_raumklima(self):
        # Kombinierter Plot für Temperaturen und Raumlasten
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10), sharex=True)

        # Plot 1: Innentemperatur vs. Außentemperatur
        ax1.plot(self.theta_i, label='Innentemperatur (T_i)', color='red', linewidth=1)
        ax1.plot(self.ta, label='Außentemperatur (T_a)', color='orange', alpha=0.4)
        ax1.set_ylabel('Temperatur [°C]')
        ax1.set_title(f'Raumklima Analyse - {self.raum_name}')
        ax1.legend(loc='upper right')
        ax1.grid(True, alpha=0.3)

        # Plot 2: Raumlasten (Heizen/Kühlen statisch)
        ax2.fill_between(range(8760), 0, self.phi_hc, where=(self.phi_hc > 0), 
                         color='red', alpha=0.3, label='Heizleistung Raum (statisch)')
        ax2.fill_between(range(8760), 0, self.phi_hc, where=(self.phi_hc < 0), 
                         color='blue', alpha=0.3, label='Kühlleistung Raum (statisch)')
        ax2.set_ylabel('Leistung [W]')
        ax2.set_xlabel('Stunde des Jahres')
        ax2.legend(loc='upper right')
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.show()

    def zeige_bilanz(self):
        # Erweiterte Bilanz inklusive Raum-Heizung und Kühlung
        # 1. RLT-Werte
        kwh_hz_rlt = np.sum(self.phi_heizregister) / 1000
        kwh_vent = np.sum(self.phi_vent) / 1000
        
        # 2. Raum-Werte (Trennung von Heizen und Kühlen)
        phi_raum_heiz = np.where(self.phi_hc > 0, self.phi_hc, 0)
        phi_raum_kuehl = np.where(self.phi_hc < 0, self.phi_hc, 0)
        
        kwh_hz_raum = np.sum(phi_raum_heiz) / 1000
        kwh_kuehl_raum = np.sum(phi_raum_kuehl) / 1000 # Ist negativ
        
        # Spezifische Werte
        spec_hz_rlt = kwh_hz_rlt / self.flaeche
        spec_hz_raum = kwh_hz_raum / self.flaeche
        spec_kuehl_raum = abs(kwh_kuehl_raum) / self.flaeche
        spec_vent_raum = kwh_vent / self.flaeche

        bilanz_text = (
            f"Jahres-Energiebilanz ({self.raum_name}):\n"
            f"Grundfläche: {self.flaeche:.2f} m2\n"
            f"--------------------------------------------------\n"
            f"RLT-Heizregister:   {kwh_hz_rlt:>8.1f} kWh/a  ({spec_hz_rlt:>5.2f} kWh/m2a)\n"
            f"Statische Heizung:  {kwh_hz_raum:>8.1f} kWh/a  ({spec_hz_raum:>5.2f} kWh/m2a)\n"
            f"Raumkühlung:        {abs(kwh_kuehl_raum):>8.1f} kWh/a  ({spec_kuehl_raum:>5.2f} kWh/m2a)\n"
            f"Ventilatoren:       {kwh_vent:>8.1f} kWh/a ({spec_vent_raum:>5.2f} kWh/m2a)\n"
            f"--------------------------------------------------\n"
            f"Heizwärme Gesamt:   {(spec_hz_rlt + spec_hz_raum):>5.2f} kWh/m2a\n"
            f"Kältebedarf Gesamt: {spec_kuehl_raum:>5.2f} kWh/m2a"
        )
        
        plt.figure(figsize=(10, 5))
        plt.text(0.1, 0.5, bilanz_text, fontsize=11, family='monospace', verticalalignment='center')
        plt.axis('off')
        plt.title("Auswertung (absolut & spezifisch)")
        plt.show()

    def zeige_bilanz_konsole(self):
        # Gibt die Jahres-Energiebilanz ohne Analyse direkt in die Konsole aus
        # 1. RLT-Werte
        kwh_hz_rlt = np.sum(self.phi_heizregister) / 1000
        kwh_vent = np.sum(self.phi_vent) / 1000
        
        # 2. Raum-Werte (Heizen/Kühlen)
        phi_raum_heiz = np.where(self.phi_hc > 0, self.phi_hc, 0)
        phi_raum_kuehl = np.where(self.phi_hc < 0, self.phi_hc, 0)
        
        kwh_hz_raum = np.sum(phi_raum_heiz) / 1000
        kwh_kuehl_raum = np.sum(phi_raum_kuehl) / 1000
        
        # Spezifische Werte
        spec_hz_rlt = kwh_hz_rlt / self.flaeche
        spec_hz_raum = kwh_hz_raum / self.flaeche
        spec_kuehl_raum = abs(kwh_kuehl_raum) / self.flaeche
        spec_vent_raum = kwh_vent / self.flaeche
        
        # Konsolen-Ausgabe
        print(f"\nJahres-Energiebilanz ({self.raum_name}):")
        print(f"Grundfläche: {self.flaeche:.2f} m2")
        print("-" * 55)
        print(f"RLT-Heizregister:   {kwh_hz_rlt:>8.1f} kWh/a  ({spec_hz_rlt:>6.2f} kWh/m2a)")
        print(f"Statische Heizung:  {kwh_hz_raum:>8.1f} kWh/a  ({spec_hz_raum:>6.2f} kWh/m2a)")
        print(f"Raumkühlung:        {abs(kwh_kuehl_raum):>8.1f} kWh/a  ({spec_kuehl_raum:>6.2f} kWh/m2a)")
        print(f"Ventilatoren:       {kwh_vent:>8.1f} kWh/a  ({spec_vent_raum:>6.2f} kWh/m2a)")
        print("-" * 55)
        print(f"Heizwärme Gesamt:   {(spec_hz_rlt + spec_hz_raum):>6.2f} kWh/m2a")
        print(f"Kältebedarf Gesamt: {spec_kuehl_raum:>6.2f} kWh/m2a")
        print("-" * 55 + "\n")

    def zeige_plausibilitaet_konsole(self):
        # Rein tabellarische Ausgabe der statistischen Kennwerte
        
        daten = [
            ("Innentemperatur", self.theta_i, "°C"),
            ("Zulufttemperatur", self.t_zul, "°C"),
            ("Außentemperatur", self.ta, "°C"),
            ("Heizlast Raum (HC)", self.phi_hc, "W"),
            ("NHR Leistung (RLT)", self.phi_heizregister, "W"),
            ("Ventilator Leist.", self.phi_vent, "W"),
            ("Volumenstrom", (self.phi_vent / 2000 * 3600) if hasattr(self, 'phi_vent') else np.zeros(8760), "m3/h")
        ]

        # Header
        print(f"ÜBERSICHT: {self.raum_name}")
        print(f"{'-'*85}")
        print(f"{'Parameter':<22} | {'Min':>12} | {'Max':>12} | {'Mittel':>12} | {'Einheit'}")
        print(f"{'-'*85}")

        # Zeilenweise Ausgabe
        for name, werte, einheit in daten:
            if name == "Volumenstrom" and hasattr(self, 'v_punkt'):
                 v_min, v_max, v_mean = np.min(self.v_punkt), np.max(self.v_punkt), np.mean(self.v_punkt)
            else:
                v_min, v_max, v_mean = np.min(werte), np.max(werte), np.mean(werte)
            
            print(f"{name:<22} | {v_min:>12.2f} | {v_max:>12.2f} | {v_mean:>12.2f} | {einheit}")
        
        print(f"{'-'*85}\n")