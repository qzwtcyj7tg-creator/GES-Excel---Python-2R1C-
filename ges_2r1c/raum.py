from dataclasses import dataclass


@dataclass(frozen=True)
class RaumEingabe:
    # Geometrie & Bauphysik
    laenge: float           # m
    breite: float           # m
    hoehe: float            # m
    grundflaeche: float     # m²
    volumen: float          # m³

    # Thermische Hülle
    u_wert_mittel: float    # W/m²K
    h_t: float              # W/K
    a_huell: float          # m²

    # Fenster
    a_eff_nord: float       # m²
    a_eff_west: float       # m²

    # Luftdaten
    c_v_luft: float         # Wh/m³K
    rho_luft: float         # kg/m³
    temp_luft_ref: float    # °C

    # Setpoints
    t_soll_heiz: float      # °C
    t_soll_hoff: float      # °C

    # Lüftung
    volstr: float           # m³/h
    wrg_rlt: float          # Wirkungsgrad WRG [-]
    vent_zul: float         # W
    vent_abl: float         # W
    vent_ges: float         # W

    # Wärmekapazität
    wkap: float             # Wh/K

    # Heizen und Kühlen
    heating_ideal_on: bool
    cooling_ideal_on: bool

    theta_soll_h_anw: float   # Heizen bei Anwesenheit [°C]
    theta_soll_h_abw: float   # Heizen bei Abwesenheit [°C]
    theta_soll_c_anw: float   # Kühlen bei Anwesenheit [°C]
    theta_soll_c_abw: float   # Kühlen bei Abwesenheit [°C]

    phi_hc_max_heiz: float    # Maximale Heizleistung [W]
    phi_hc_max_kuehl: float   # Maximale Kühlleistung [W] (negativ)

    name: str


def create_c320() -> RaumEingabe:
    """Erstellt die Raumdefinition für Raum C3.20."""
    L, B, H = 10.85, 7.90, 3.13
    volumenstrom = 2500  # m³/h
    sfp_wert = 2000      # Ws/m³
    p_vent_ges = 2 * ((volumenstrom / 3600) * sfp_wert)

    return RaumEingabe(
        laenge=L,
        breite=B,
        hoehe=H,
        grundflaeche=L * B,
        volumen=L * B * H,

        u_wert_mittel=0.55,
        h_t=45.812828645084096,
        a_huell=203.1 + 83.4,

        c_v_luft=0.34,
        rho_luft=1.13,
        temp_luft_ref=18.0,

        a_eff_nord=3.986,
        a_eff_west=1.993,

        t_soll_heiz=21,
        t_soll_hoff=16,

        volstr=volumenstrom,
        wrg_rlt=0.6,
        vent_zul=volumenstrom,
        vent_abl=volumenstrom,
        vent_ges=p_vent_ges,

        wkap=L * B * 90,

        heating_ideal_on=True,
        cooling_ideal_on=False,

        theta_soll_c_anw=25,
        theta_soll_c_abw=32,

        theta_soll_h_anw=21,
        theta_soll_h_abw=16,

        phi_hc_max_heiz=9500,
        phi_hc_max_kuehl=-9500,

        name="C3.20",
    )
