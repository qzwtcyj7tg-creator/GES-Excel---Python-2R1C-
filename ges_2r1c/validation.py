from .raum import RaumEingabe


def validierung_din_12831(raum: RaumEingabe, norm_ta: float, norm_ti: float, ergebnis_phi_hc: float):
    """Berechnung der Heizlast nach DIN 12831.

    Formel: Q = HT * (T_i - T_a)
    """
    berechnete_heizlast = raum.h_t * (norm_ti - norm_ta)

    print(f"Berechnete Heizlast nach DIN 12831: {berechnete_heizlast:.2f} W")
    print(f"Maximale Heizlast der Heizkörper: {raum.phi_hc_max_heiz:.2f} W")
    print(f"Maximale angewendete Heizlast in Simulation: {ergebnis_phi_hc:.2f} W")
    print(f"Abweichung: {berechnete_heizlast - raum.phi_hc_max_heiz:.2f} W")


def validierung_din_4108():
    print("Validierung nach DIN 4108:")
