

# Profil für eine Schule bzw Uni
def calc_interne_lasten_schule(raum, nutzersignal) -> float:

    phi_personen = raum.people * 70 # 4200 Watt furch Personen
    phi_geraete = raum.people / 2 * 40 + 200 # Die hälfte der Personen Laptop + 200 W für Beamer und weitere El. Ausrüstung
    phi_licht = 10 * raum.grundflaeche # 10 W/m²

    return (phi_geraete + phi_licht + phi_personen) * nutzersignal

# Profil Büro 
def calc_interne_lasten_buero() -> float:
    return None

# Usw. 