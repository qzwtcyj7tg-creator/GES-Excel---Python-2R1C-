import numpy as np
import pandas as pd

# Notitz 1.1.26: Alle Lüftungstemperaturen stimmen jetzt!

def t_abl_prüfen(ta_aktuell):
    return 20.0 if ta_aktuell <= 20.0 else 25.0

def rlt_berechung(ta_aktuell, nutzer_anwesend, raum, ti_aktuell):
    t_abl = t_abl_prüfen(ta_aktuell)
    
    # Soll Temperatur Raum bestimmen mithilfe von Nutzungssignal
    t_soll = raum.theta_soll_h_abw if nutzer_anwesend == 0 else raum.theta_soll_h_anw

    # WRG Signal bestimmen
    wrg_signal = 1 if ta_aktuell < t_abl else 0

    if wrg_signal == 1:
        t_wrg_theoretisch = ta_aktuell + raum.wrg_rlt * (t_abl - ta_aktuell)
        
        # Wenn Ta > T Soll Min ist, dann folgt t nach wrg der Ta
        t_nach_wrg = max(min(t_wrg_theoretisch, t_soll), ta_aktuell)
    else:
        # Bypass
        t_nach_wrg = ta_aktuell

    # Volumenstrom bestimmen
    v_punkt = nutzer_anwesend * raum.volstr
    
    # NHR: nur bei Anwesenheit und t nach wrg < t_soll
    if nutzer_anwesend > 0 and t_nach_wrg < t_soll:
        q_nhr = v_punkt * 0.34 * (t_soll - t_nach_wrg)
    else:
        q_nhr = 0.0

    if v_punkt > 0:
        t_zul = t_nach_wrg + (q_nhr / (0.34 * v_punkt))
    else:
        # Falls V = 0 ist Zuluft = T nach wrg
        t_zul = t_nach_wrg

    # Ventilator Leistung berechnen
    p_vent = nutzer_anwesend * raum.vent_ges

    return t_zul, v_punkt, q_nhr, p_vent, t_nach_wrg, t_abl