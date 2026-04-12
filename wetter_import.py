import numpy as np
import pandas as pd

def lade_wetterdaten(dateipfad):
    # Mit pandas einlesen
    df = pd.read_excel(dateipfad)
    
    stunden = np.arange(8760)       # Stunden im Jahr
    ta = df['t'].values             # Außentemp in °C
    direkt = df['B'].values         # Direkte Str. W/m2 (B = Beam)
    diffus = df['D'].values         # Diffuse Str. W/m2 (D = Diffuse)
    global_strahl = direkt + diffus # Global Strahlung als einfache Bilanz
    nutzersignal = df['NSF'].values # Import Nutzungssignal für den Vergleich
    
    return ta, stunden, direkt, diffus, global_strahl, nutzersignal

# ---Struktur TRY Datei---

# Koordinatensystem : Lambert konform konisch
# Rechtswert        : 4064500 Meter
# Hochwert          : 2408500 Meter
# Hoehenlage        : 488 Meter ueber NN
# Erstellung des Datensatzes im Mai 2016

# Art des TRY       : mittleres Jahr
# Bezugszeitraum    : 1995-2012
# Datenbasis        : Beobachtungsdaten Zeitraum 1995-2012

# Format: (i7,1x,i7,1x,i2,1x,i2,1x,i2,1x,f5.1,1x,i4,1x,3i,1x,f4.1,1x,i1,1x,f4.1,1x,i3,1x,i4,1x,i4,1x,i3,1x,i4,2x,i1)

# Reihenfolge der Parameter:
# RW Rechtswert                                                    [m]       {3670500;3671500..4389500}
# HW Hochwert                                                      [m]       {2242500;2243500..3179500}
# MM Monat                                                                   {1..12}
# DD Tag                                                                     {1..28,30,31}
# HH Stunde (MEZ)                                                            {1..24}
# t  Lufttemperatur in 2m Hoehe ueber Grund                        [GradC]
# p  Luftdruck in Standorthoehe                                    [hPa]
# WR Windrichtung in 10 m Hoehe ueber Grund                        [Grad]    {0..360;999}
# WG Windgeschwindigkeit in 10 m Hoehe ueber Grund                 [m/s]
# N  Bedeckungsgrad                                                [Achtel]  {0..8;9}
# x  Wasserdampfgehalt, Mischungsverhaeltnis                       [g/kg]
# RF Relative Feuchte in 2 m Hoehe ueber Grund                     [Prozent] {1..100}
# B  Direkte Sonnenbestrahlungsstaerke (horiz. Ebene)              [W/m^2]   abwaerts gerichtet: positiv
# D  Diffuse Sonnenbetrahlungsstaerke (horiz. Ebene)               [W/m^2]   abwaerts gerichtet: positiv
# A  Bestrahlungsstaerke d. atm. Waermestrahlung (horiz. Ebene)    [W/m^2]   abwaerts gerichtet: positiv
# E  Bestrahlungsstaerke d. terr. Waermestrahlung                  [W/m^2]   aufwaerts gerichtet: negativ
# IL Qualitaetsbit bezueglich der Auswahlkriterien                           {0;1;2;3;4}
