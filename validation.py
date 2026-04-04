# Validation mit DIN 12831 und DIN 4108

from raum_parameter import c320


def validierung_din_12831(norm_ta, norm_ti, ergebnis_phi_hc):
    # Berechnung der Heizlast nach DIN 12831
    # Formel: Q = HT * (T_i - T_a) 
    # HT: Wärmestrom, T_i: Innentemperatur, T_a: Außentemperatur

    HT = c320.h_t
    T_i = norm_ti
    T_a = norm_ta

    berechnete_heizlast = HT * (T_i - T_a)

    print(f"Berechnete Heizlast nach DIN 12831: {berechnete_heizlast:.2f} W")
    print(f"Maximale Heizlast der Heizkörper: {c320.phi_hc_max_heiz:.2f} W")
    # print(f"Maximale angewendete Heizlast in Simulation: {ergebnis_phi_hc:.2f} W")
    # print(f"Abweichung: {berechnete_heizlast - c320.phi_hc_max_heiz:.2f} W")


# def validierung_din_4108():