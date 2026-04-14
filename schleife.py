from raum_parameter import c320
from rlt import rlt_berechung
import numpy as np

def bestimme_heiz_sollwert(nutzersignal, raum):
    if nutzersignal > 0:
        return raum.theta_soll_h_anw
    else:
        return raum.theta_soll_h_abw
    
def bestimme_kuhlung_sollwert(nutzersignal, raum):
    if nutzersignal > 0:
        return raum.theta_soll_c_anw
    else:
        return raum.theta_soll_c_abw
    
def calculate_hc(praesenz, raum, t_0W, theta_aktuell, dt_pro_C, ta_stunde, h_v, t_zul, 
                 phi_int, phi_sol, nenner):
    
    t_test = t_0W
    phi_hc_test = 1000

    t_soll_heating = bestimme_heiz_sollwert(praesenz, raum)
    t_soll_cooling = bestimme_kuhlung_sollwert(praesenz, raum)

    # 2. Heizlast-Ermittlung wenn ideales Heizelement an
    if t_0W < t_soll_heating and c320.heating_ideal_on == True:

        # Heizen notwendig um t_soll_h zu erreichen
        t_test = (theta_aktuell + dt_pro_C * (c320.h_t * ta_stunde + h_v * t_zul + phi_int + phi_sol + phi_hc_test)) / nenner

        # Numerische Stabilität
        delta_test = t_test - t_0W
        if abs(delta_test) >= 1e-6:
            phi_hc = phi_hc_test * ((t_soll_heating - t_0W) / delta_test)
        else:
            phi_hc = 0.0 # Fallback Option, falls Test_HL zu klein ist

        # Begrenzung auf max. Heizleistung
        phi_hc = min(phi_hc, c320.phi_hc_max_heiz)
        phi_hc = max(phi_hc, 0.0)
        return phi_hc

    elif t_0W > t_soll_cooling and c320.cooling_ideal_on == True:
        # Kühlen notwendig um t_soll_cooling zu erreichen
        t_test = (theta_aktuell + dt_pro_C * (c320.h_t * ta_stunde + h_v * t_zul + phi_int + phi_sol + phi_hc_test)) / nenner

        # Numerische Stabilität
        delta_test = t_test - t_0W
        if abs(delta_test) >= 1e-6:
            phi_hc = phi_hc_test * ((t_soll_cooling - t_0W) / delta_test)
        else:
            phi_hc = 0.0 # Fallback Option, falls Test_HL zu klein ist

        # Begrenzung auf max. Kühlleistung
        phi_hc = max(phi_hc, c320.phi_hc_max_kuehl) 
        phi_hc = min(phi_hc, 0.0)
        return phi_hc
    else:
        # Kein Heizen notwendig, Innentemperatur ist bereits über Sollwert
        return 0



# Variabler Luftdruck in Abhängigkeit von der Höhe über NN, NOCH NCIHT BENUTZT, ABER FÜR SPÄTER VORGESEHEN!
def variabler_druck(hohe_nn):
    return 101325 * (1 - (0.0065 * hohe_nn) / (288.15)) ** 5.255

# Augsburg Höhe 494m über NN
p_genau = variabler_druck(494)
K_LUFT = (p_genau * 1004) / (3600 * 287.06)

# In der schleife.py
def schleife(theta_aktuell, dt, ergebnis_h_v, ergebnis_phi_hc, ergebnis_phi_heizregister,
            ergebnis_phi_lueftung, ergebnis_phi_vent, ergebnis_t_zul, ergebnis_theta_i,
            ergebnis_v_punkt, ta, nsf, zeitplan, direkt, phi_intern,ergebnis_t_nach_wrg, ergebnis_t_abl, ergebnis_theta_test_i, ergebnis_theta_0W, ergebnis_t_soll):

    # Vorberechnung aller RLT-Werte, da t_zul im GES-Excel um 1 Stunde verschoben ist
    # (Raum1C2R referenziert die Zulufttemperatur der NÄCHSTEN Stunde)
    pre_t_zul = np.zeros(8760)
    pre_v_punkt = np.zeros(8760)
    pre_p_hz = np.zeros(8760)
    pre_p_vent = np.zeros(8760)
    pre_t_nach_wrg = np.zeros(8760)
    pre_t_abl = np.zeros(8760)

    for t in range(8760):
        t_zul, v_punkt, p_hz, p_vent, t_nach_wrg, t_abl = rlt_berechung(ta[t], nsf[t], c320)
        pre_t_zul[t] = t_zul
        pre_v_punkt[t] = v_punkt
        pre_p_hz[t] = p_hz
        pre_p_vent[t] = p_vent
        pre_t_nach_wrg[t] = t_nach_wrg
        pre_t_abl[t] = t_abl

    # Zulufttemperatur um 1 Stunde verschieben (wie im GES-Excel)
    t_zul_shifted = np.zeros(8760)
    t_zul_shifted[:-1] = pre_t_zul[1:]     # t_zul[t] = vorberechnetes t_zul[t+1]
    t_zul_shifted[-1] = pre_t_zul[-1]      # Letzte Stunde: keine Verschiebung möglich

    for t in range(8760):
        ta_stunde = ta[t]
        praesenz = nsf[t]
        phi_int = phi_intern[t]
        phi_sol = direkt[t] # Solare Einstrahlung ist umgerechnet in der Excel drinne, Später verbessern!

        # RLT-Werte: Volumenstrom etc. aus aktueller Stunde, Zulufttemperatur aus nächster Stunde
        t_zul = t_zul_shifted[t]
        v_punkt = pre_v_punkt[t]
        p_hz = pre_p_hz[t]
        p_vent = pre_p_vent[t]
        t_nach_wrg = pre_t_nach_wrg[t]
        t_abl = pre_t_abl[t]

        t_soll_heating = bestimme_heiz_sollwert(praesenz, c320)
        t_soll_cooling = bestimme_kuhlung_sollwert(praesenz, c320)

        # h_v = (K_LUFT / (theta_aktuell + 273.15)) * v_punkt
        h_v = 0.34 * v_punkt

        # Faktoren für die Formel
        dt_pro_C = dt / c320.wkap
        nenner = 1 + dt_pro_C * (c320.h_t + h_v)

        # THERMISCHE BERECHNUNG

        # 1. Innentemperatur ohne Heizung
        t_0W = (theta_aktuell + dt_pro_C * (c320.h_t * ta_stunde + h_v * t_zul + phi_int + phi_sol)) / nenner

        phi_hc = 0.0

        phi_hc = calculate_hc(praesenz, c320, t_0W, theta_aktuell, dt_pro_C, ta_stunde, h_v, 
                              t_zul, phi_int, phi_sol, nenner)

        # 3. Finale Innentemperatur
        theta_neu = (theta_aktuell + dt_pro_C * (c320.h_t * ta_stunde + h_v * t_zul + phi_int + phi_sol + phi_hc)) / nenner

        # SPEICHERUNG DER ERGEBNISSE IN ARRAYS
        ergebnis_theta_i[t] = theta_neu
        ergebnis_phi_hc[t] = phi_hc
        ergebnis_t_zul[t] = t_zul
        ergebnis_v_punkt[t] = v_punkt
        ergebnis_phi_heizregister[t] = p_hz
        ergebnis_phi_vent[t] = p_vent
        ergebnis_phi_lueftung[t] = h_v * (t_zul - theta_neu)
        # ergebnis_theta_test_i[t] = t_test
        ergebnis_theta_0W[t] = t_0W
        ergebnis_t_soll[t] = t_soll_heating
        ergebnis_h_v[t] = h_v
        ergebnis_t_nach_wrg[t] = t_nach_wrg
        ergebnis_t_abl[t] = t_abl


        # UPDATE FÜR NÄCHSTEN ZEITSCHRITT, SPEICHERN
        theta_aktuell = theta_neu

    return (
        theta_aktuell, dt, ergebnis_h_v, ergebnis_phi_hc, ergebnis_phi_heizregister,
        ergebnis_phi_lueftung, ergebnis_phi_vent, ergebnis_t_zul, ergebnis_theta_i, ergebnis_v_punkt
    )
