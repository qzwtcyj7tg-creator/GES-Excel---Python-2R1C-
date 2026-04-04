from dataclasses import dataclass

@dataclass(frozen=True) 
class RaumEingabe:
    # Geometrie & Bauphysik
    laenge: float           # m
    breite: float           # m
    hoehe: float            # m
    grundflaeche: float     # m2
    volumen: float          # m3

    # Thermische Hülle 
    u_wert_mittel: float
    h_t: float              # W/K
    a_huell: float          # m2

    # Fenster
    a_eff_nord: float       # m2
    a_eff_west: float       # m2

    # Luftdaten 
    c_v_luft: float         
    rho_luft: float         # KG/m3
    temp_luft_ref: float    # °C

    # Setpoints
    t_soll_heiz: float      # °C
    t_soll_hoff: float      # °C

    # Lüftung 
    volstr: float           # m3/h
    wrg_rlt: float          # 5
    vent_zul: float         # W
    vent_abl: float         # W
    vent_ges: float         # W

    # Wärmekapazität
    wkap: float          # Wh/k
    
    theta_soll_h_anw: float  # Heizen bei Anwesenheit
    theta_soll_h_abw: float  # Heizen bei Abwesenheit / Absenkung
    # theta_soll_c_anw: float  # Kühlen bei Anwesenheit
    # theta_soll_c_abw: float  # Kühlen bei Abwesenheit

    # Beispielwerte für raum_parameter.py
    phi_hc_max_heiz: float   # Maximale Heizleistung in Watt 
    phi_hc_max_kuehl: float # Maximale Kühlleistung in Watt

    name: str


L, B, H = 10.85, 7.90, 3.13
volumenstrom = 2500  # m3/h
sfp_wert = 2000      # Ws/m3 

# Ventilator Leistung
p_vent_ges = 2 * ((volumenstrom / 3600) * sfp_wert)

# --- Raum definieren ---
c320 = RaumEingabe(
    laenge = L,
    breite = B,
    hoehe = H,
    grundflaeche = L * B,    
    volumen = L * B * H,
    
    u_wert_mittel = 0.55,
    h_t = 45.8,
    a_huell = 203.1,
    
    c_v_luft = 0.34, 
    rho_luft = 1.13,
    temp_luft_ref = 18.0,
    
    a_eff_nord = 3.986,
    a_eff_west = 1.993,

    t_soll_heiz = 21,
    t_soll_hoff = 16,

    volstr = volumenstrom,
    wrg_rlt = 0.6,
    vent_zul = volumenstrom,
    vent_abl = volumenstrom,
    vent_ges = p_vent_ges,

    wkap = 7714,

    theta_soll_h_anw = 21,
    theta_soll_h_abw = 16,

    phi_hc_max_heiz = 1500, # Maximale Heizleistungen 
    phi_hc_max_kuehl = -0,

    name = "C3.20"
)

print(f"Raum {c320.name} erfolgreich angelegt!")