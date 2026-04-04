import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

dateien_pfad = r"C:\Users\nicol\OneDrive - Technische Hochschule Augsburg\THA\M12\2025\Python_Modell_2R1C\import\vergleich1r1c.xlsx"
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
        plt.figure(figsize=(12,6))
        plt.plot(stunden, heizleistung, label = 'Heizleistung Excel', color = 'red')
        plt.plot(stunden, hl_py, label = 'Heizleistung Python',color = 'blue')
        plt.title(f"Vergleich Heizleistung")
        plt.xlabel("Zeit [Stunden]")
        plt.ylabel("Leistung [W]")
        plt.grid(True, linestyle='--', alpha=0.7) 
        plt.legend() 
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



