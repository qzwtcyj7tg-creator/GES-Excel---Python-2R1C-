import tkinter as tk
from tkinter import ttk
import sv_ttk
from dataclasses import replace

def gui(raum):
    root = tk.Tk()
    result = {"raum": raum}
    root.title("Simulation")
    root.minsize(250, 150)

    sv_ttk.set_theme("dark")

    heating_var = tk.BooleanVar(value=raum.heating_ideal_on)
    cooling_var = tk.BooleanVar(value=raum.cooling_ideal_on)

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

    def simulate():
        neuer_raum = replace(
            raum,
            heating_ideal_on=heating_var.get(),
            cooling_ideal_on=cooling_var.get()
        )
        result["raum"] = neuer_raum
        root.destroy()

    ttk.Button(root, text="Simulieren", command=simulate).pack()

    root.mainloop()

    return result["raum"]