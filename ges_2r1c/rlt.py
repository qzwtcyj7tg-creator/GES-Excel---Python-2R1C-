from .raum import RaumEingabe


def t_abl_pruefen(ta_aktuell: float) -> float:
    return 20.0 if ta_aktuell <= 20.0 else 25.0


def rlt_berechnung(ta_aktuell: float, nutzer_anwesend: float, raum: RaumEingabe):
    """Berechnet die RLT-Anlage (Lüftung, WRG, Heizregister, Ventilator).

    Returns:
        Tuple of (t_zul, v_punkt, q_nhr, p_vent, t_nach_wrg, t_abl)
    """
    t_abl = t_abl_pruefen(ta_aktuell)

    t_soll = raum.theta_soll_h_abw if nutzer_anwesend == 0 else raum.theta_soll_h_anw

    # WRG Signal
    wrg_signal = 1 if ta_aktuell < t_abl else 0

    if wrg_signal == 1:
        t_wrg_theoretisch = ta_aktuell + raum.wrg_rlt * (t_abl - ta_aktuell)
        t_nach_wrg = max(min(t_wrg_theoretisch, t_soll), ta_aktuell)
    else:
        t_nach_wrg = ta_aktuell

    # Volumenstrom
    v_punkt = nutzer_anwesend * raum.volstr

    # NHR: nur bei Anwesenheit und t nach wrg < t_soll
    if nutzer_anwesend > 0 and t_nach_wrg < t_soll:
        q_nhr = v_punkt * 0.34 * (t_soll - t_nach_wrg)
    else:
        q_nhr = 0.0

    if v_punkt > 0:
        t_zul = t_nach_wrg + (q_nhr / (0.34 * v_punkt))
    else:
        t_zul = t_nach_wrg

    # Ventilator Leistung
    p_vent = nutzer_anwesend * raum.vent_ges

    return t_zul, v_punkt, q_nhr, p_vent, t_nach_wrg, t_abl
