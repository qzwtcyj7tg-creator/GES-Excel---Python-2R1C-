import numpy as np

from .raum import RaumEingabe
from .results import HOURS_PER_YEAR, SimulationResults
from .rlt import rlt_berechnung


def bestimme_heiz_sollwert(nutzersignal: float, raum: RaumEingabe) -> float:
    return raum.theta_soll_h_anw if nutzersignal > 0 else raum.theta_soll_h_abw


def bestimme_kuhlung_sollwert(nutzersignal: float, raum: RaumEingabe) -> float:
    return raum.theta_soll_c_anw if nutzersignal > 0 else raum.theta_soll_c_abw


def calculate_hc(
    praesenz: float,
    raum: RaumEingabe,
    t_0W: float,
    theta_aktuell: float,
    dt_pro_C: float,
    ta_stunde: float,
    h_v: float,
    t_zul: float,
    phi_int: float,
    phi_sol: float,
    nenner: float,
) -> float:
    """Berechnet die benötigte Heiz-/Kühlleistung."""
    phi_hc_test = 1000

    t_soll_heating = bestimme_heiz_sollwert(praesenz, raum)
    t_soll_cooling = bestimme_kuhlung_sollwert(praesenz, raum)

    if t_0W < t_soll_heating and raum.heating_ideal_on:
        t_test = (theta_aktuell + dt_pro_C * (raum.h_t * ta_stunde + h_v * t_zul + phi_int + phi_sol + phi_hc_test)) / nenner

        delta_test = t_test - t_0W
        if abs(delta_test) >= 1e-6:
            phi_hc = phi_hc_test * ((t_soll_heating - t_0W) / delta_test)
        else:
            phi_hc = 0.0

        phi_hc = min(phi_hc, raum.phi_hc_max_heiz)
        phi_hc = max(phi_hc, 0.0)
        return phi_hc

    elif t_0W > t_soll_cooling and raum.cooling_ideal_on:
        t_test = (theta_aktuell + dt_pro_C * (raum.h_t * ta_stunde + h_v * t_zul + phi_int + phi_sol + phi_hc_test)) / nenner

        delta_test = t_test - t_0W
        if abs(delta_test) >= 1e-6:
            phi_hc = phi_hc_test * ((t_soll_cooling - t_0W) / delta_test)
        else:
            phi_hc = 0.0

        phi_hc = max(phi_hc, raum.phi_hc_max_kuehl)
        phi_hc = min(phi_hc, 0.0)
        return phi_hc

    return 0.0


def run_simulation(
    raum: RaumEingabe,
    ta: np.ndarray,
    nsf: np.ndarray,
    direkt: np.ndarray,
    diffus: np.ndarray,
    phi_intern: np.ndarray,
    theta_start: float = 16.0,
    dt: float = 1.0,
) -> SimulationResults:
    """Führt die thermische Jahressimulation durch (8760 Stunden).

    Args:
        raum: Raumparameter
        ta: Außentemperatur [°C] (8760 Werte)
        nsf: Nutzungssignal [-] (8760 Werte)
        direkt: Solare Einstrahlung [W] (8760 Werte)
        phi_intern: Interne Gewinne [W] (8760 Werte)
        theta_start: Starttemperatur [°C]
        dt: Zeitschritt [h]

    Returns:
        SimulationResults mit allen Stundenwerten
    """
    res = SimulationResults()

    # Vorberechnung aller RLT-Werte
    pre_t_zul = np.zeros(HOURS_PER_YEAR)
    pre_v_punkt = np.zeros(HOURS_PER_YEAR)
    pre_p_hz = np.zeros(HOURS_PER_YEAR)
    pre_p_vent = np.zeros(HOURS_PER_YEAR)
    pre_t_nach_wrg = np.zeros(HOURS_PER_YEAR)
    pre_t_abl = np.zeros(HOURS_PER_YEAR)

    for t in range(HOURS_PER_YEAR):
        t_zul, v_punkt, p_hz, p_vent, t_nach_wrg, t_abl = rlt_berechnung(ta[t], nsf[t], raum)
        pre_t_zul[t] = t_zul
        pre_v_punkt[t] = v_punkt
        pre_p_hz[t] = p_hz
        pre_p_vent[t] = p_vent
        pre_t_nach_wrg[t] = t_nach_wrg
        pre_t_abl[t] = t_abl

    # Zulufttemperatur um 1 Stunde verschieben (wie im GES-Excel)
    t_zul_shifted = np.zeros(HOURS_PER_YEAR)
    t_zul_shifted[:-1] = pre_t_zul[1:]
    t_zul_shifted[-1] = pre_t_zul[-1]

    theta_aktuell = theta_start

    for t in range(HOURS_PER_YEAR):
        ta_stunde = ta[t]
        praesenz = nsf[t]
        phi_int = phi_intern[t]
        phi_sol_dir = direkt[t]

        t_zul = t_zul_shifted[t]
        v_punkt = pre_v_punkt[t]
        p_hz = pre_p_hz[t]
        p_vent = pre_p_vent[t]
        t_nach_wrg = pre_t_nach_wrg[t]
        t_abl = pre_t_abl[t]

        h_v = 0.34 * v_punkt

        dt_pro_C = dt / raum.wkap
        nenner = 1 + dt_pro_C * (raum.h_t + h_v)

        # 1. Innentemperatur ohne Heizung
        t_0W = (theta_aktuell + dt_pro_C * (raum.h_t * ta_stunde + h_v * t_zul + phi_int + phi_sol_dir)) / nenner

        # 2. Heiz-/Kühlleistung
        phi_hc = calculate_hc(praesenz, raum, t_0W, theta_aktuell, dt_pro_C,
                              ta_stunde, h_v, t_zul, phi_int, phi_sol_dir, nenner)

        # 3. Finale Innentemperatur
        theta_neu = (theta_aktuell + dt_pro_C * (raum.h_t * ta_stunde + h_v * t_zul + phi_int + phi_sol_dir + phi_hc)) / nenner

        # Ergebnisse speichern
        res.theta_i[t] = theta_neu
        res.phi_hc[t] = phi_hc
        res.t_zul[t] = t_zul
        res.v_punkt[t] = v_punkt
        res.phi_heizregister[t] = p_hz
        res.phi_vent[t] = p_vent
        res.phi_lueftung[t] = h_v * (t_zul - theta_neu)
        res.theta_0W[t] = t_0W
        res.t_soll[t] = bestimme_heiz_sollwert(praesenz, raum)
        res.h_v[t] = h_v
        res.t_nach_wrg[t] = t_nach_wrg
        res.t_abl[t] = t_abl

        theta_aktuell = theta_neu

    return res
