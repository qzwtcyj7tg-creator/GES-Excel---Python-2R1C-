from math import exp

def calc_co2(raum, nsf, v_punkt, co_0, time) -> float:
    co_out = 420
    beta = v_punkt / raum.volumen

    # 20 l/h pers CO2 pro Person * Zeitplan
    # Umrechnung Fakotr 1000 von l/m³ auf ml/m³
    if v_punkt == 0:
        co_unend = 420 # BZW. 0 
    else:
        co_unend = co_out + (20_000 * (nsf * raum.people / v_punkt))
    
    return (co_0 - co_unend) * exp(-beta*time) + co_unend