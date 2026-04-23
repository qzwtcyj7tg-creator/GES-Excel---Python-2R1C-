import tkinter as tk
from tkinter import ttk
import sv_ttk
from dataclasses import replace

from ges_2r1c.raum import Fenster

def gui(raum):
    root = tk.Tk()
    result = {"raum": raum} # Dictionary erstellen um später Ergebnisse zurückzugeben
    root.title("Simulation")
    root.minsize(250, 150)

    sv_ttk.set_theme("dark")

    # Variablen für Checkboxen, die automatisch mit den BUttons verbunden sind
    heating_var = tk.BooleanVar(value=raum.heating_ideal_on)
    cooling_var = tk.BooleanVar(value=raum.cooling_ideal_on)

    # Checkboxen ertellen, gekoppelt mit der Variable oben
    ttk.Checkbutton(
        root,
        text="Ideales Heizelement",
        variable=heating_var,
        onvalue=True,
        offvalue=False
    ).pack()

    ttk.Checkbutton(
        root,
        text="Ideales Kühlelement",
        variable=cooling_var,
        onvalue=True,
        offvalue=False,
    ).pack()

    # Aktion für den Simulations Button definieren
    # Erstellt Kopie von raum objekt und die Variablen werden 
    # durch die neuen Werte ersetzt
    def simulate():
        neuer_raum = replace(
            raum,
            heating_ideal_on=heating_var.get(),
            cooling_ideal_on=cooling_var.get()
        )
        # Speichert Objekt in Dictionary
        result["raum"] = neuer_raum
        # Schließt Fenster
        root.destroy()

    # Simulations Button
    ttk.Button(root, text="Simulieren", command=simulate).pack()

    root.mainloop()
    # Gibt aktualisierte Ergebnis zurück
    return result["raum"]