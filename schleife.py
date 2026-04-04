from raum_parameter import c320
from rlt import rlt_berechung

def bestimme_heiz_sollwert(nutzersignal, raum):
    if nutzersignal > 0:
        return raum.theta_soll_h_anw
    else:
        return raum.theta_soll_h_abw

# Variabler Luftdruck in Abhängigkeit von der Höhe über NN, NOCH NCIHT BENUTZT, ABER FÜR SPÄTER VORGESEHEN!
def variabler_druck(hohe_nn): 
    return 101325 * (1 - (0.0065 * hohe_nn) / (288.15)) ** 5.255

# Augsburg Höhe 494m über NN
p_genau = variabler_druck(494)
K_LUFT = (p_genau * 1004) / (3600 * 287.06)

# In der schleife.py
def schleife(theta_aktuell, dt, ergebnis_h_v, ergebnis_phi_hc, ergebnis_phi_heizregister, 
            ergebnis_phi_lueftung, ergebnis_phi_vent, ergebnis_t_zul, ergebnis_theta_i, 
            ergebnis_v_punkt, ta, nsf, zeitplan, direkt, phi_intern,ergebnis_t_nach_wrg, ergebnis_t_abl):
    
    for t in range(8760):
        ta_stunde = ta[t]
        praesenz = nsf[t]
        phi_int = phi_intern[t]
        phi_sol = direkt[t] # Solare Einstrahlung ist umgerechnet in der Excel drinne, Später verbessern!

        # RLT-Werte berechnen in "rlt.py"
        t_zul, v_punkt, p_hz, p_vent,t_nach_wrg, t_abl = rlt_berechung(ta_stunde, praesenz, c320, theta_aktuell)
        t_soll_h = bestimme_heiz_sollwert(praesenz, c320)

        # Für minimal mehr Genauigkeit, aktuell nicht um genau die GES-Excel abzubilden
        # p_t = variabler_druck(494)  
        # K_LUFT = (p_t * 1004) / (3600 * 287.06)

        h_v = (K_LUFT / (theta_aktuell + 273.15)) * v_punkt

        ergebnis_h_v[t] = h_v
        ergebnis_t_nach_wrg[t] = t_nach_wrg
        ergebnis_t_abl[t] = t_abl

        # Faktoren für die Formel
        dt_pro_C = dt / c320.wkap
        nenner = 1 + dt_pro_C * (c320.h_t + h_v)

        # THERMISCHE BERECHNUNG

        # 1. Innentemperatur ohne Heizung 
        t_0W = (theta_aktuell + dt_pro_C * (c320.h_t * ta_stunde + h_v * t_zul + phi_int + phi_sol)) / nenner

        # 2. Heizlast-Ermittlung
        phi_hc = 0
        if t_0W < t_soll_h:
            # Heizen notwendig um t_soll_h zu erreichen
            phi_hc_test = 1000.0 # Beinflusst nicht das Ergebnis
            t_test = (theta_aktuell + dt_pro_C * (c320.h_t * ta_stunde + h_v * t_zul + phi_int + phi_sol + phi_hc_test)) / nenner
            
            # Dreisatz für exakte Heizlast
            phi_hc = phi_hc_test * ((t_soll_h - t_0W) / (t_test - t_0W))
            
            # Begrenzung auf max. Heizkapazität 
            phi_hc = min(phi_hc, c320.phi_hc_max_heiz) 

        # 3. Finale Innentemperatur
        theta_neu = (1 / nenner) * (theta_aktuell + dt_pro_C * (c320.h_t * ta_stunde + h_v * t_zul + phi_int + phi_sol + phi_hc))

        # === DEBUG 10 Stunden ===
        if t < 10:
            heizt = "JA" if phi_hc > 0 else "NEIN"
            print(f"{t:5d} | {t_0W:6.2f} | {t_soll_h:6.2f} | {phi_hc:7.1f} | {theta_neu:8.2f} | {heizt}")

        # SPEICHERUNG DER ERGEBNISSE IN ARRAYS
        ergebnis_theta_i[t] = theta_neu
        ergebnis_phi_hc[t] = phi_hc
        ergebnis_t_zul[t] = t_zul
        ergebnis_v_punkt[t] = v_punkt
        ergebnis_phi_heizregister[t] = p_hz
        ergebnis_phi_vent[t] = p_vent
        ergebnis_phi_lueftung[t] = h_v * (t_zul - theta_neu)  

        # UPDATE FÜR NÄCHSTEN ZEITSCHRITT, IT SPEICHERN
        theta_aktuell = theta_neu
    
    return theta_aktuell, dt, ergebnis_h_v, ergebnis_phi_hc, ergebnis_phi_heizregister, ergebnis_phi_lueftung, ergebnis_phi_vent, ergebnis_t_zul, ergebnis_theta_i, ergebnis_v_punkt