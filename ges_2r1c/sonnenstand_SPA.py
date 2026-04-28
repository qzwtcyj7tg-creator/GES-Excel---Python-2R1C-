import math

# ==============================================================================
# TABELLE A4.2 — VSOP87 Periodische Terme für Erdposition (L, B, R)
# Jeder Eintrag: [A, B, C]
# Formel: Σ A·cos(B + C·JME)
# ==============================================================================

# Noch nicht in der Simulation, aktuell für einen Tag zu einer bestimmten Zeit 

L0_TERMS = [
    [175347046, 0, 0],
    [3341656, 4.6692568, 6283.07585],
    [34894, 4.6261, 12566.1517],
    [3497, 2.7441, 5753.3849],
    [3418, 2.8289, 3.5231],
    [3136, 3.6277, 77713.7715],
    [2676, 4.4181, 7860.4194],
    [2343, 6.1352, 3930.2097],
    [1324, 0.7425, 11506.7698],
    [1273, 2.0371, 529.691],
    [1199, 1.1096, 1577.3435],
    [990, 5.233, 5884.927],
    [902, 2.045, 26.298],
    [857, 3.508, 398.149],
    [780, 1.179, 5223.694],
    [753, 2.533, 5507.553],
    [505, 4.583, 18849.228],
    [492, 4.205, 775.523],
    [357, 2.92, 0.067],
    [317, 5.849, 11790.629],
    [284, 1.899, 796.298],
    [271, 0.315, 10977.079],
    [243, 0.345, 5486.778],
    [206, 4.806, 2544.314],
    [205, 1.869, 5573.143],
    [202, 2.458, 6069.777],
    [156, 0.833, 213.299],
    [132, 3.411, 2942.463],
    [126, 1.083, 20.775],
    [115, 0.645, 0.98],
    [103, 0.636, 4694.003],
    [102, 0.976, 15720.839],
    [102, 4.267, 7.114],
    [99, 6.21, 2146.17],
    [98, 0.68, 155.42],
    [86, 5.98, 161000.69],
    [85, 1.3, 6275.96],
    [85, 3.67, 71430.7],
    [80, 1.81, 17260.15],
    [79, 3.04, 12036.46],
    [75, 1.76, 5088.63],
    [74, 3.5, 3154.69],
    [74, 4.68, 801.82],
    [70, 0.83, 9437.76],
    [62, 3.98, 8827.39],
    [61, 1.82, 7084.9],
    [57, 2.78, 6286.6],
    [56, 4.39, 14143.5],
    [56, 3.47, 6279.55],
    [52, 0.19, 12139.55],
    [52, 1.33, 1748.02],
    [51, 0.28, 5856.48],
    [49, 0.49, 1194.45],
    [41, 5.37, 8429.24],
    [41, 2.4, 19651.05],
    [39, 6.17, 10447.39],
    [37, 6.04, 10213.29],
    [37, 2.57, 1059.38],
    [36, 1.71, 2352.87],
    [36, 1.78, 6812.77],
    [33, 0.59, 17789.85],
    [30, 0.44, 83996.85],
    [30, 2.74, 1349.87],
    [25, 3.16, 4690.48],
]

L1_TERMS = [
    [628331966747, 0, 0],
    [206059, 2.678235, 6283.07585],
    [4303, 2.6351, 12566.1517],
    [425, 1.59, 3.523],
    [119, 5.796, 26.298],
    [109, 2.966, 1577.344],
    [93, 2.59, 18849.23],
    [72, 1.14, 529.69],
    [68, 1.87, 398.15],
    [67, 4.41, 5507.55],
    [59, 2.89, 5223.69],
    [56, 2.17, 155.42],
    [45, 0.4, 796.3],
    [36, 0.47, 775.52],
    [29, 2.65, 7.11],
    [21, 5.34, 0.98],
    [19, 1.85, 5486.78],
    [19, 4.97, 213.3],
    [17, 2.99, 6275.96],
    [16, 0.03, 2544.31],
    [16, 1.43, 2146.17],
    [15, 1.21, 10977.08],
    [12, 2.83, 1748.02],
    [12, 3.26, 5088.63],
    [12, 5.27, 1194.45],
    [12, 2.08, 4694],
    [11, 0.77, 553.57],
    [10, 1.3, 6286.6],
    [10, 4.24, 1349.87],
    [9, 2.7, 242.73],
    [9, 5.64, 951.72],
    [8, 5.3, 2352.87],
    [6, 2.65, 9437.76],
    [6, 4.67, 4690.48],
]

L2_TERMS = [
    [52919, 0, 0],
    [8720, 1.0721, 6283.0758],
    [309, 0.867, 12566.152],
    [27, 0.05, 3.52],
    [16, 5.19, 26.3],
    [16, 3.68, 155.42],
    [10, 0.76, 18849.23],
    [9, 2.06, 77713.77],
    [7, 0.83, 775.52],
    [5, 4.66, 1577.34],
    [4, 1.03, 7.11],
    [4, 3.44, 5573.14],
    [3, 5.14, 796.3],
    [3, 6.05, 5507.55],
    [3, 1.19, 242.73],
    [3, 6.12, 529.69],
    [3, 0.31, 398.15],
    [3, 2.28, 553.57],
    [2, 4.38, 5223.69],
    [2, 3.75, 0.98],
]

L3_TERMS = [
    [289, 5.844, 6283.076],
    [35, 0, 0],
    [17, 5.49, 12566.15],
    [3, 5.2, 155.42],
    [1, 4.72, 3.52],
    [1, 5.3, 18849.23],
    [1, 5.97, 242.73],
]

L4_TERMS = [
    [114, 3.142, 0],
    [8, 4.13, 6283.08],
    [1, 3.84, 12566.15],
]

L5_TERMS = [
    [1, 3.14, 0],
]

B0_TERMS = [
    [280, 3.199, 84334.662],
    [102, 5.422, 5507.553],
    [80, 3.88, 5223.69],
    [44, 3.7, 2352.87],
    [32, 4, 1577.34],
]

B1_TERMS = [
    [9, 3.9, 5507.55],
    [6, 1.73, 5223.69],
]

R0_TERMS = [
    [100013989, 0, 0],
    [1670700, 3.0984635, 6283.07585],
    [13956, 3.05525, 12566.1517],
    [3084, 5.1985, 77713.7715],
    [1628, 1.1739, 5753.3849],
    [1576, 2.8469, 7860.4194],
    [925, 5.453, 11506.77],
    [542, 4.564, 3930.21],
    [472, 3.661, 5884.927],
    [346, 0.964, 5507.553],
    [329, 5.9, 5223.694],
    [307, 0.299, 5573.143],
    [243, 4.273, 11790.629],
    [212, 5.847, 1577.344],
    [186, 5.022, 10977.079],
    [175, 3.012, 18849.228],
    [110, 5.055, 5486.778],
    [98, 0.89, 6069.78],
    [86, 5.69, 15720.84],
    [86, 1.27, 161000.69],
    [65, 0.27, 17260.15],
    [63, 0.92, 529.69],
    [57, 2.01, 83996.85],
    [56, 5.24, 71430.7],
    [49, 3.25, 2544.31],
    [47, 2.58, 775.52],
    [45, 5.54, 9437.76],
    [43, 6.01, 6275.96],
    [39, 5.36, 4694],
    [38, 2.39, 8827.39],
    [37, 0.83, 19651.05],
    [37, 4.9, 12139.55],
    [36, 1.67, 12036.46],
    [35, 1.84, 2942.46],
    [33, 0.24, 7084.9],
    [32, 0.18, 5088.63],
    [32, 1.78, 398.15],
    [28, 1.21, 6286.6],
    [28, 1.9, 6279.55],
    [26, 4.59, 10447.39],
]

R1_TERMS = [
    [103019, 1.10749, 6283.07585],
    [1721, 1.0644, 12566.1517],
    [702, 3.142, 0],
    [32, 1.02, 18849.23],
    [31, 2.84, 5507.55],
    [25, 1.32, 5223.69],
    [18, 1.42, 1577.34],
    [10, 5.91, 10977.08],
    [9, 1.42, 6275.96],
    [9, 0.27, 5486.78],
]

R2_TERMS = [
    [4359, 5.7846, 6283.0758],
    [124, 5.579, 12566.152],
    [12, 3.14, 0],
    [9, 3.63, 77713.77],
    [6, 1.87, 5573.14],
    [3, 5.47, 18849.23],
]

R3_TERMS = [
    [145, 4.273, 6283.076],
    [7, 3.92, 12566.15],
]

R4_TERMS = [
    [4, 2.56, 6283.08],
]

# ==============================================================================
# TABELLE A4.3 — Nutation in Länge und Schiefe
# Format: [Y0, Y1, Y2, Y3, Y4, a, b, c, d]
# ==============================================================================

NUTATION_TERMS = [
    [0,0,0,0,1,   -171996,-174.2, 92025, 8.9],
    [-2,0,0,2,2,  -13187,  -1.6,  5736, -3.1],
    [0,0,0,2,2,   -2274,   -0.2,   977, -0.5],
    [0,0,0,0,2,    2062,    0.2,  -895,  0.5],
    [0,1,0,0,0,    1426,   -3.4,    54, -0.1],
    [0,0,1,0,0,     712,    0.1,    -7,  0.0],
    [-2,1,0,2,2,   -517,    1.2,   224, -0.6],
    [0,0,0,2,1,    -386,   -0.4,   200,  0.0],
    [0,0,1,2,2,    -301,    0.0,   129, -0.1],
    [-2,-1,0,2,2,   217,   -0.5,   -95,  0.3],
    [-2,0,1,0,0,   -158,    0.0,     0,  0.0],
    [-2,0,0,2,1,    129,    0.1,   -70,  0.0],
    [0,0,-1,2,2,    123,    0.0,   -53,  0.0],
    [2,0,0,0,0,      63,    0.0,     0,  0.0],
    [0,0,1,0,1,      63,    0.1,   -33,  0.0],
    [2,0,-1,2,2,    -59,    0.0,    26,  0.0],
    [0,0,-1,0,1,    -58,   -0.1,    32,  0.0],
    [0,0,1,2,1,     -51,    0.0,    27,  0.0],
    [-2,0,2,0,0,     48,    0.0,     0,  0.0],
    [0,0,-2,2,1,     46,    0.0,   -24,  0.0],
    [2,0,0,2,2,     -38,    0.0,    16,  0.0],
    [0,0,2,2,2,     -31,    0.0,    13,  0.0],
    [0,0,2,0,0,      29,    0.0,     0,  0.0],
    [-2,0,1,2,2,     29,    0.0,   -12,  0.0],
    [0,0,0,2,0,      26,    0.0,     0,  0.0],
    [-2,0,0,2,0,    -22,    0.0,     0,  0.0],
    [0,0,-1,2,1,     21,    0.0,   -10,  0.0],
    [0,2,0,0,0,      17,   -0.1,     0,  0.0],
    [2,0,-1,0,1,     16,    0.0,    -8,  0.0],
    [-2,2,0,2,2,    -16,    0.1,     7,  0.0],
    [0,1,0,0,1,     -15,    0.0,     9,  0.0],
    [-2,0,1,0,1,    -13,    0.0,     7,  0.0],
    [0,-1,0,0,1,    -12,    0.0,     6,  0.0],
    [0,0,2,-2,0,     11,    0.0,     0,  0.0],
    [2,0,-1,2,1,    -10,    0.0,     5,  0.0],
    [2,0,1,2,2,      -8,    0.0,     3,  0.0],
    [0,1,0,2,2,       7,    0.0,    -3,  0.0],
    [-2,1,1,0,0,     -7,    0.0,     0,  0.0],
    [0,-1,0,2,2,     -7,    0.0,     3,  0.0],
    [2,0,0,2,1,      -7,    0.0,     3,  0.0],
    [2,0,1,0,0,       6,    0.0,     0,  0.0],
    [-2,0,2,2,2,      6,    0.0,    -3,  0.0],
    [-2,0,1,2,1,      6,    0.0,    -3,  0.0],
    [2,0,-2,0,1,     -6,    0.0,     3,  0.0],
    [2,0,0,0,1,      -6,    0.0,     3,  0.0],
    [0,-1,1,0,0,      5,    0.0,     0,  0.0],
    [-2,-1,0,2,1,    -5,    0.0,     3,  0.0],
    [-2,0,0,0,1,     -5,    0.0,     3,  0.0],
    [0,0,2,2,1,      -5,    0.0,     3,  0.0],
    [-2,0,2,0,1,      4,    0.0,     0,  0.0],
    [-2,1,0,2,1,      4,    0.0,     0,  0.0],
    [0,0,1,-2,0,      4,    0.0,     0,  0.0],
    [-1,0,1,0,0,     -4,    0.0,     0,  0.0],
    [-2,1,0,0,0,     -4,    0.0,     0,  0.0],
    [1,0,0,0,0,      -4,    0.0,     0,  0.0],
    [0,0,1,2,0,       3,    0.0,     0,  0.0],
    [0,0,-2,2,2,     -3,    0.0,     0,  0.0],
    [-1,-1,1,0,0,    -3,    0.0,     0,  0.0],
    [0,1,1,0,0,      -3,    0.0,     0,  0.0],
    [0,-1,1,2,2,     -3,    0.0,     0,  0.0],
    [2,-1,-1,2,2,    -3,    0.0,     0,  0.0],
    [0,0,3,2,2,      -3,    0.0,     0,  0.0],
    [2,-1,0,2,2,     -3,    0.0,     0,  0.0],
]


# ==============================================================================
# HILFSFUNKTIONEN
# ==============================================================================

def limit_degrees(deg):
    """Begrenzt einen Winkel auf [0°, 360°) — Schritt 3.2.6"""
    d = deg / 360.0
    result = 360.0 * (d - math.floor(d))
    if result < 0:
        result += 360.0
    return result


def vsop_sum(terms, jme):
    """Berechnet Σ A·cos(B + C·JME) über alle Terme einer VSOP87-Reihe"""
    return sum(A * math.cos(B + C * jme) for A, B, C in terms)


# ==============================================================================
# SCHRITT 3.1 — Julianisches Datum und abgeleitete Zeitskalen
# ==============================================================================

def julian_day(jahr, monat, tag, ut_stunden):
    """
    Berechnet das Julianische Datum (JD).
    Dokument Gl. 4 — WICHTIG: Korrektur für Januar/Februar!
    """
    y, m = jahr, monat
    if m <= 2:          # ← Das war in deinem Skript auskommentiert!
        y -= 1
        m += 12

    A = math.floor(y / 100)
    B = 2 - A + math.floor(A / 4)  # Gregorianische Kalenderkorrektur

    JD = (math.floor(365.25 * (y + 4716))
        + math.floor(30.6001 * (m + 1))
        + tag + B - 1524.5
        + ut_stunden / 24.0)
    return JD


def zeitskalen(JD, delta_t=0):
    """
    Berechnet JDE, JC, JCE, JME aus JD.
    delta_t: Differenz TT - UT in Sekunden (aktuell ca. 69s, Standard: 0)
    Dokument Gl. 5-8
    """
    JDE = JD + delta_t / 86400.0          # Gl. 5
    JC  = (JD  - 2451545.0) / 36525.0     # Gl. 6
    JCE = (JDE - 2451545.0) / 36525.0     # Gl. 7
    JME = JCE / 10.0                       # Gl. 8
    return JDE, JC, JCE, JME


# ==============================================================================
# SCHRITT 3.2 — Heliozentrische Erdposition L, B, R (VSOP87)
# ==============================================================================

def erdposition_heliozentrisch(JME):
    """
    Berechnet L (Länge), B (Breite), R (Radiusvektor) der Erde.
    Dokument Schritte 3.2.1 - 3.2.8, Gl. 9-14
    """
    # --- Länge L ---
    L0 = vsop_sum(L0_TERMS, JME)
    L1 = vsop_sum(L1_TERMS, JME)
    L2 = vsop_sum(L2_TERMS, JME)
    L3 = vsop_sum(L3_TERMS, JME)
    L4 = vsop_sum(L4_TERMS, JME)
    L5 = vsop_sum(L5_TERMS, JME)

    L_rad = (L0 + L1*JME + L2*JME**2 + L3*JME**3
             + L4*JME**4 + L5*JME**5) / 1e8        # Gl. 11
    L_deg = math.degrees(L_rad)                      # Gl. 12
    L_deg = limit_degrees(L_deg)                     # Gl. 3.2.6

    # --- Breite B ---
    B0 = vsop_sum(B0_TERMS, JME)
    B1 = vsop_sum(B1_TERMS, JME)
    B_rad = (B0 + B1*JME) / 1e8
    B_deg = math.degrees(B_rad)

    # --- Radiusvektor R (in Astronomischen Einheiten) ---
    R0 = vsop_sum(R0_TERMS, JME)
    R1 = vsop_sum(R1_TERMS, JME)
    R2 = vsop_sum(R2_TERMS, JME)
    R3 = vsop_sum(R3_TERMS, JME)
    R4 = vsop_sum(R4_TERMS, JME)
    R = (R0 + R1*JME + R2*JME**2 + R3*JME**3 + R4*JME**4) / 1e8

    return L_deg, B_deg, R


# ==============================================================================
# SCHRITT 3.3 — Geozentrische Länge und Breite
# ==============================================================================

def geozentrisch(L, B):
    """Dokument Gl. 13-14"""
    theta = limit_degrees(L + 180)   # Geozentrische Länge Θ
    beta  = -B                        # Geozentrische Breite β
    return theta, beta


# ==============================================================================
# SCHRITT 3.4 — Nutation in Länge (Δψ) und Schiefe (Δε)
# ==============================================================================

def nutation(JCE):
    """
    Berechnet Δψ (Nutation in Länge) und Δε (Nutation in Schiefe).
    Dokument Gl. 15-23, Tabelle A4.3
    """
    # Hilfswinkel X0..X4 (Gl. 15-19)
    X0 = (297.85036 + 445267.111480*JCE
          - 0.0019142*JCE**2 + JCE**3/189474)
    X1 = (357.52772 + 35999.050340*JCE
          - 0.0001603*JCE**2 - JCE**3/300000)
    X2 = (134.96298 + 477198.867398*JCE
          + 0.0086972*JCE**2 + JCE**3/56250)
    X3 = (93.27191  + 483202.017538*JCE
          - 0.0036825*JCE**2 + JCE**3/327270)
    X4 = (125.04452 - 1934.136261*JCE
          + 0.0020708*JCE**2 + JCE**3/450000)
    X = [X0, X1, X2, X3, X4]

    sum_psi = 0.0
    sum_eps = 0.0

    for row in NUTATION_TERMS:
        Y = row[0:5]
        a, b, c, d = row[5], row[6], row[7], row[8]

        arg = sum(math.radians(X[j] * Y[j]) for j in range(5))
        sum_psi += (a + b * JCE) * math.sin(arg)   # Gl. 20
        sum_eps += (c + d * JCE) * math.cos(arg)   # Gl. 21

    delta_psi = sum_psi / 36000000.0   # Gl. 22 → in Grad
    delta_eps = sum_eps / 36000000.0   # Gl. 23 → in Grad
    return delta_psi, delta_eps


# ==============================================================================
# SCHRITT 3.5 — Wahre Schiefe der Ekliptik ε
# ==============================================================================

def wahre_schiefe(JME, delta_eps):
    """
    Berechnet die wahre Schiefe der Ekliptik ε.
    Dokument Gl. 24-25
    """
    U = JME / 10.0
    # Mittlere Schiefe ε₀ (in Bogensekunden) — Gl. 24
    eps0 = (84381.448
            - 4680.93  * U
            - 1.55     * U**2
            + 1999.25  * U**3
            - 51.38    * U**4
            - 249.67   * U**5
            - 39.05    * U**6
            + 7.12     * U**7
            + 27.87    * U**8
            + 5.79     * U**9
            + 2.45     * U**10)
    epsilon = eps0 / 3600.0 + delta_eps   # Gl. 25 → in Grad
    return epsilon


# ==============================================================================
# SCHRITT 3.6 & 3.7 — Aberration und scheinbare Sonnenlänge λ
# ==============================================================================

def scheinbare_sonnenlange(theta, delta_psi, R):
    """
    Aberrationskorrektur und scheinbare Länge λ.
    Dokument Gl. 26-27
    """
    delta_tau = -20.4898 / (3600.0 * R)          # Gl. 26
    lam = theta + delta_psi + delta_tau            # Gl. 27
    return lam


# ==============================================================================
# SCHRITT 3.8 — Scheinbare Sternzeit zu Greenwich (GAST) ν
# ==============================================================================

def sternzeit_greenwich(JD, JC, delta_psi, epsilon):
    """
    Berechnet die scheinbare Sternzeit ν (GAST).
    Dokument Gl. 28-29
    Das war der fehlende Unterschied zu GMST in deinem Skript!
    """
    nu0 = (280.46061837
           + 360.98564736629 * (JD - 2451545)
           + 0.000387933 * JC**2
           - JC**3 / 38710000)                    # Gl. 28
    nu0 = limit_degrees(nu0)
    nu  = nu0 + delta_psi * math.cos(math.radians(epsilon))  # Gl. 29
    return nu


# ==============================================================================
# SCHRITT 3.9 & 3.10 — Rektaszension α und Deklination δ
# ==============================================================================

def rektaszension_deklination(lam, beta, epsilon):
    """
    Berechnet geozentrische Rektaszension α und Deklination δ.
    Dokument Gl. 30-31
    """
    lam_r   = math.radians(lam)
    beta_r  = math.radians(beta)
    eps_r   = math.radians(epsilon)

    # Rektaszension α (Gl. 30)
    y = math.cos(eps_r) * math.sin(lam_r) - math.tan(beta_r) * math.sin(eps_r)
    x = math.cos(lam_r)
    alpha = math.degrees(math.atan2(y, x))
    alpha = limit_degrees(alpha)

    # Deklination δ (Gl. 31)
    delta = math.degrees(
        math.asin(math.sin(beta_r) * math.cos(eps_r)
                  + math.cos(beta_r) * math.sin(eps_r) * math.sin(lam_r))
    )
    return alpha, delta


# ==============================================================================
# SCHRITT 3.11 — Lokaler Stundenwinkel H
# ==============================================================================

def stundenwinkel(nu, sigma, alpha):
    """
    Lokaler Stundenwinkel H.
    Dokument Gl. 32
    sigma: geographische Länge des Beobachters (positiv = Ost)
    """
    H = nu + sigma - alpha    # Gl. 32
    H = limit_degrees(H)
    if H > 180:
        H -= 360
    return H


# ==============================================================================
# SCHRITT 3.14 — Zenitwinkel θ und Höhe e (mit Refraktion)
# ==============================================================================

def elevation_und_zenit(phi, delta, H, P=1013.25, T=15.0):
    """
    Berechnet topozentrische Sonnenhöhe e und Zenitwinkel θ.
    phi:   geographische Breite (Grad)
    delta: Deklination (Grad)
    H:     Stundenwinkel (Grad)
    P:     Luftdruck (mbar), Standard 1013.25
    T:     Temperatur (°C), Standard 15

    Dokument Gl. 41-44
    """
    phi_r   = math.radians(phi)
    delta_r = math.radians(delta)
    H_r     = math.radians(H)

    # Höhe ohne Refraktion e₀ (Gl. 41)
    sin_e0 = (math.sin(phi_r) * math.sin(delta_r)
              + math.cos(phi_r) * math.cos(delta_r) * math.cos(H_r))
    e0 = math.degrees(math.asin(sin_e0))

    # Atmosphärische Refraktionskorrektur Δe (Gl. 42)
    # Nur wenn Sonne über/nahe Horizont
    if e0 > -0.575:
        delta_e = ((P / 1010.0) * (283.0 / (273.0 + T))
                   * 1.02 / (60.0 * math.tan(math.radians(e0 + 10.3 / (e0 + 5.11)))))
    else:
        delta_e = 0.0

    e     = e0 + delta_e       # Wahre Höhe (Gl. 43)
    theta = 90.0 - e           # Zenitwinkel (Gl. 44)
    return e, theta, e0


# ==============================================================================
# SCHRITT 3.15 — Azimut
# ==============================================================================

def azimut(H, phi, delta):
    """
    Topozentrische Azimutwinkel.
    Γ: Astronomen-Azimut (von Süd, westwärts)
    Φ: Navigations-Azimut (von Nord, ostwärts) ← das ist der gebräuchliche
    Dokument Gl. 45-46
    """
    H_r     = math.radians(H)
    phi_r   = math.radians(phi)
    delta_r = math.radians(delta)

    y = math.sin(H_r)
    x = math.cos(H_r) * math.sin(phi_r) - math.tan(delta_r) * math.cos(phi_r)
    Gamma = math.degrees(math.atan2(y, x))
    Gamma = limit_degrees(Gamma)

    Phi = limit_degrees(Gamma + 180)   # Gl. 46 — von Nord, ostwärts
    return Phi, Gamma


# ==============================================================================
# HAUPTFUNKTION — alles zusammen
# ==============================================================================

def sonnenposition(jahr, monat, tag, lokale_stunde, laenge, breite,
                   zeitzone=1, delta_t=69.0, P=1013.25, T=15.0):
    """
    Berechnet Sonnenhöhe und Azimut für einen Ort und Zeitpunkt.

    Parameter:
        jahr, monat, tag   : Datum
        lokale_stunde      : Lokale Zeit in Stunden (z.B. 12.5 = 12:30 Uhr)
        laenge             : Geographische Länge in Grad (positiv = Ost)
        breite             : Geographische Breite in Grad (positiv = Nord)
        zeitzone           : Zeitzone in Stunden (MEZ = +1, MESZ = +2)
        delta_t            : TT - UT in Sekunden (aktuell ~69s, für grobe
                             Berechnungen kann 0 verwendet werden)
        P                  : Luftdruck in mbar (für Refraktion)
        T                  : Temperatur in °C (für Refraktion)

    Rückgabe:
        dict mit Sonnenhöhe, Azimut, und allen Zwischenwerten
    """
    # UT aus lokaler Zeit
    UT = lokale_stunde - zeitzone

    # 3.1 Julianisches Datum
    JD = julian_day(jahr, monat, tag, UT)
    JDE, JC, JCE, JME = zeitskalen(JD, delta_t)

    # 3.2 Heliozentrische Erdposition (VSOP87)
    L, B, R = erdposition_heliozentrisch(JME)

    # 3.3 Geozentrisch
    theta, beta = geozentrisch(L, B)

    # 3.4 Nutation
    delta_psi, delta_eps = nutation(JCE)

    # 3.5 Wahre Schiefe der Ekliptik
    epsilon = wahre_schiefe(JME, delta_eps)

    # 3.6 + 3.7 Scheinbare Sonnenlänge
    lam = scheinbare_sonnenlange(theta, delta_psi, R)

    # 3.8 Sternzeit (GAST)
    nu = sternzeit_greenwich(JD, JC, delta_psi, epsilon)

    # 3.9 + 3.10 Rektaszension und Deklination
    alpha, delta = rektaszension_deklination(lam, beta, epsilon)

    # 3.11 Stundenwinkel
    H = stundenwinkel(nu, laenge, alpha)

    # 3.14 Höhe und Zenit (mit Refraktion)
    e, theta_z, e0 = elevation_und_zenit(breite, delta, H, P, T)

    # 3.15 Azimut
    Phi, Gamma = azimut(H, breite, delta)

    return {
        "hoehe":        e,        # Sonnenhöhe in Grad (mit Refraktion)
        "hoehe_geo":    e0,       # Sonnenhöhe ohne Refraktion
        "azimut":       Phi,      # Azimut: 0°=Nord, 90°=Ost, 180°=Süd, 270°=West
        "zenitwinkel":  theta_z,  # Zenitwinkel in Grad
        "deklination":  delta,
        "rektaszension": alpha,
        "stundenwinkel": H,
        "JD":           JD,
        "R_AU":         R,        # Erd-Sonne-Abstand in AE
    }