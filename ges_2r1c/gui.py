import tkinter as tk
from tkinter import ttk
import sv_ttk
from dataclasses import replace

# from ges_2r1c.raum import Fenster

def gui(raum):
    root = tk.Tk()
    result = {"raum": None}
    root.title("Simulation")
    root.minsize(300, 350)
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)

    sv_ttk.set_theme("light")

    PAD = {"padx": 10, "pady": 6}

    # Variablen für Checkboxen, die automatisch mit den BUttons verbunden sind
    heating_var = tk.BooleanVar(value=raum.heating_ideal_on)
    cooling_var = tk.BooleanVar(value=raum.cooling_ideal_on)

    heating_max = tk.DoubleVar(value=raum.phi_hc_max_heiz)
    cooling_max = tk.DoubleVar(value=raum.phi_hc_max_kuehl)

    heating_label = ttk.Label(root, text="Maximale Heizlast (W):")
    heating_entry = ttk.Entry(root, textvariable=heating_max, width=10)

    cooling_label = ttk.Label(root, text="Maximale Kühllast (W):")
    cooling_entry = ttk.Entry(root, textvariable=cooling_max, width=10)

    # Ein und ausblenden von eingabe Felder
    def toggle_heating(*_):
        if heating_var.get():
            heating_label.grid(row=1, column=0, sticky="w", **PAD)
            heating_entry.grid(row=1, column=1, sticky="ew", **PAD)
        else:
            heating_label.grid_remove()
            heating_entry.grid_remove()

    def toggle_cooling(*_):
        if cooling_var.get():
            cooling_label.grid(row=3, column=0, sticky="w", **PAD)
            cooling_entry.grid(row=3, column=1, sticky="ew", **PAD)
        else:
            cooling_label.grid_remove()
            cooling_entry.grid_remove()

    # Checkboxen ertellen, gekoppelt mit der Variable oben
    ttk.Checkbutton(root, text="Ideales Heizelement", variable=heating_var,
        onvalue=True, offvalue=False, command=toggle_heating).grid(row=0, column=0, columnspan=2, sticky="w", **PAD)

    ttk.Checkbutton(root, text="Ideales Kühlelement", variable=cooling_var,
        onvalue=True, offvalue=False, command=toggle_cooling).grid(row=2, column=0, columnspan=2, sticky="w", **PAD)

    toggle_heating()
    toggle_cooling()

    # Aktion für den Simulations Button definieren
    def simulate():
        neuer_raum = replace(
            raum,
            heating_ideal_on=heating_var.get(),
            cooling_ideal_on=cooling_var.get(),
            heating_max_value=heating_max.get(),
            cooling_max_value=cooling_max.get()
        )
        result["raum"] = neuer_raum
        root.destroy()

    # Schließt ohne Simulation
    root.protocol("WM_DELETE_WINDOW", root.destroy)

    # Simulations Button
    ttk.Button(root, text="▶  Simulation starten", command=simulate).grid(
        row=4, column=0, columnspan=2, sticky="ew", **PAD)

    root.mainloop()
    return result["raum"]