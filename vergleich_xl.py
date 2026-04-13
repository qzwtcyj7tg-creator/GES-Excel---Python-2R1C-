import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

dateien_pfad = Path(__file__).parent / "import" / "vergleich_hl_it.xlsx"
df = pd.read_excel(dateien_pfad)

stunden = np.arange(8760)       # Stunden im Jahr
innentemp = df['it'].values             # Innentemp 1C1R
heizleistung = df['hl'].values         # Heizleistung 1C1R

def vergleich_plot(it_py, hl_py, hl_an, plot_it, plot_diff):
    # Vergleich Plots Innentemperatur und Heizleistung, Differenz Innentemperatur

    if plot_it:
        plt.figure(figsize=(12,6))
        plt.plot(stunden, innentemp, label = 'Innentemperatur Excel', color = 'red')
        plt.plot(stunden, it_py, label = 'Innentemperatur Python',color = 'blue')
        plt.title(f"Vergleich Innentemperatur")
        plt.xlabel("Zeit [Stunden]")
        plt.ylabel("Temperatur [°C]")
        plt.grid(True, linestyle='--', alpha=0.7) 
        plt.legend() 
        plt.show()

    if hl_an:
        fig, (ax1, ax2) = plt.subplots(
            2, 1, figsize=(12, 8), sharex=True,
            gridspec_kw={'height_ratios': [3, 1]}
        )

        # Oberer Plot: beide Kurven
        ax1.plot(stunden, heizleistung, label='Heizleistung Excel', color='blue', linewidth=2)
        ax1.plot(stunden, hl_py, label='Heizleistung Python', color='red', linewidth=1.8, linestyle='--')

        ax1.set_title("Vergleich Heizleistung")
        ax1.set_ylabel("Leistung [W]")
        ax1.grid(True, linestyle='--', alpha=0.7)
        ax1.legend()

        # Unterer Plot: Differenz
        diff = np.array(hl_py) - np.array(heizleistung)
        ax2.plot(stunden, diff, color='blue', linewidth=1.5, label='Python - Excel')
        ax2.axhline(0, color='black', linewidth=1)
        ax2.set_xlabel("Zeit [Stunden]")
        ax2.set_ylabel("Δ [W]")
        ax2.grid(True, linestyle='--', alpha=0.7)
        ax2.legend()

        plt.tight_layout()
        plt.show()

    if plot_diff:
        differenz = innentemp - it_py 
        plt.figure(figsize=(10, 4))
        plt.plot(differenz, label='Abweichung (Python - Excel)', color='red')
        plt.title("Wo weicht Python von Excel ab?")
        plt.ylabel("Delta Temperatur [K]")
        plt.xlabel("Stunde")
        plt.grid(True)
        plt.legend()
        plt.show()



