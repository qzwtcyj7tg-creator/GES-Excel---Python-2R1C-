from dataclasses import dataclass, field
import numpy as np


HOURS_PER_YEAR = 8760


def _zeros() -> np.ndarray:
    return np.zeros(HOURS_PER_YEAR)


@dataclass
class SimulationResults:
    """Container for all hourly simulation output arrays (8760 values each)."""

    # Temperatures
    theta_i: np.ndarray = field(default_factory=_zeros)       # Indoor temperature [°C]
    theta_0W: np.ndarray = field(default_factory=_zeros)       # Indoor temp without heating [°C]
    t_zul: np.ndarray = field(default_factory=_zeros)          # Supply air temperature [°C]
    t_nach_wrg: np.ndarray = field(default_factory=_zeros)     # Temp after heat recovery [°C]
    t_abl: np.ndarray = field(default_factory=_zeros)          # Exhaust air temperature [°C]
    t_soll: np.ndarray = field(default_factory=_zeros)         # Setpoint temperature [°C]

    # Powers / loads
    phi_hc: np.ndarray = field(default_factory=_zeros)         # Heating/cooling power [W]
    phi_heizregister: np.ndarray = field(default_factory=_zeros)  # NHR power [W]
    phi_lueftung: np.ndarray = field(default_factory=_zeros)   # Ventilation heat flow [W]
    phi_vent: np.ndarray = field(default_factory=_zeros)       # Fan power [W]
    phi_sol: np.ndarray = field(default_factory=lambda: np.zeros(HOURS_PER_YEAR))  # Solar gains [W]

    # Airflow
    v_punkt: np.ndarray = field(default_factory=_zeros)        # Volume flow [m³/h]
    h_v: np.ndarray = field(default_factory=_zeros)            # Ventilation heat transfer coeff [W/K]
    v_punkt_inf_liste: np.ndarray= field(default_factory=_zeros)     # Volume flow infiltration [m³/h]

    # CO2
    co2_liste: np.ndarray = field(default_factory=_zeros)      # CO2 in [ppm]

