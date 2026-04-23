# Berechnung des Sonnenstands und der solaren Einstrahlung
# Geographische Länge und Breite für Augsburg (48,1° Nord, 10,5° Ost)

from .results import HOURS_PER_YEAR

import numpy as np

i_ext_mod = 1360 * 0.9

def sonnenstand(lange, breite, zeitzonen_offset):

    alpha_liste = []
    theta_liste = []
    delta_liste = []

    print_count = 0

    for stunde in range(HOURS_PER_YEAR):

        tag = stunde // 24 
        stunde_d = stunde % 24
        

        korrektur_stundenwinkel = -(zeitzonen_offset - lange)
        korrektur_stundenwinkel_mttw = -15 * 0.5

        # Stundenwinkel in Grad (Delta)
        delta = (stunde_d - 12) * 15 + korrektur_stundenwinkel + korrektur_stundenwinkel_mttw

        # if print_count < 10:
        #     print(f"Delta: {delta}")
        #     print_count += 1
        # Delta korrekt!
        
        # Absolute Höhe Mittagssonne (Epsilon)
        eps = 23.43 * np.sin((tag - 81) / 180 * np.pi)

        # if print_count < 10:
        #     print(f"Epsilon: {eps}")
        #     print_count += 1
        # Epsilon korrekt!

        # Elevation (Theta) in Grad
        theta = np.degrees(np.arcsin(np.sin(np.radians(eps)) * np.sin(np.radians(breite)) + np.cos(np.radians(eps)) * np.cos(np.radians(breite)) * np.cos(np.radians(delta))))

        # if print_count < 10:
        #     print(f"Theta: {theta}")
        #     print_count += 1
        # Theta korrekt !

        # Azimut (Alpha) in Grad
        alpha = np.degrees(np.arctan2(
            np.sin(np.radians(delta)),
            np.cos(np.radians(delta)) * np.sin(np.radians(breite)) - np.tan(np.radians(eps)) * np.cos(np.radians(breite))
        ))

        if print_count < 10:
            print(f"Alpha: {alpha}")
            print_count += 1
        # Fehler hier

        alpha_liste.append(alpha)
        theta_liste.append(theta)
        delta_liste.append(delta)

    return np.array(alpha_liste), np.array(theta_liste), np.array(delta_liste)


def berechnung_einstrahlung(alpha_sonne, theta, alpha_f, diffuse_strahlung, direktstrahlung, neigungswinkel, rho):

    # alpha = alpha_sonne[HOURS_PER_YEAR]
    # diffuse_strahlung = diffuse_strahlung[HOURS_PER_YEAR]
    # direktstrahlung = direktstrahlung[HOURS_PER_YEAR]

    # Sonne da (ja/nein)
    if np.sin(np.radians(theta)) > 0:
        sonne_da = True
    else:
        sonne_da = False

    # Berechnung der solaren Einstrahlung |n sonne| = 1
    # x = cos theta * cos alpha (Süden)
    # y = cos theta * sin alpha (Osten)
    # z = sin theta (Oben)

    if sonne_da:
        x_s = np.cos(np.radians(theta)) * np.cos(np.radians(alpha_sonne)) # Damit der Normalvektor in die Horizontale Ebene kommt
        y_s = - np.cos(np.radians(theta)) * np.sin(np.radians(alpha_sonne)) # Nicht in Richtung Sonne
        z_s = np.sin(np.radians(theta))
    else:
        x_s = 0
        y_s = 0
        z_s = 0

    # Einstrahlung auf Normalen Vektor der Oberfläche
    # Leistungserhaltung I_n * A_N = I_Hori * A_Hori
    # A_N / A_Hori = l_N / l_Hori = sin(theta)
    # I_n = I_Hori / sin(theta)
    # I_N muss kleiner als extraterrestrische Einstrahlung sein! 

    if sonne_da:
        i_b_n = direktstrahlung / np.sin(np.radians(theta))
        if i_b_n > i_ext_mod:
            i_b_n = i_ext_mod
    else:
        i_b_n = 0

    # Energieerhaltung I_B,n * l_s = I_B,F * l_F
    # cos beta = l_s / l_F 
    # I_B,F / I_B,n = l_s / l_F = cos(np.radians(beta))
    # cos beta = n_s (Skalarprodukt) n_F / (|n_s| * |n_F|)
    # Gemäß vereinbarung ist betrag von n_s = n_F = 1
    # cos beta = n_s (Skalarprodukt) n_F

    # z_F - cos beta
    # x_F = - sin beta cos alpha
    # y_F = sin beta sin alpha

    # Normalen Vektor der Oberfläche
    x_f = -np.sin(np.radians(neigungswinkel)) * np.cos(np.radians(alpha_f))
    y_f = np.sin(np.radians(neigungswinkel)) * np.sin(np.radians(alpha_f))
    z_f = -np.cos(np.radians(neigungswinkel))

    view_faktor = (1 + np.cos(np.radians(neigungswinkel))) / 2
    view_faktor_2 = (1 - np.cos(np.radians(neigungswinkel))) / 2

    i_g_h = direktstrahlung + diffuse_strahlung

    skalarprodukt = x_s * x_f + y_s * y_f + z_s * z_f
    direkte_einstrahlung = skalarprodukt * i_b_n
    diffuse_einstrahlung = view_faktor * diffuse_strahlung
    bodenref_strahlung =  view_faktor_2 * rho * i_g_h


    # print(f"Alpha Sonne: {alpha_sonne:.2f}°, Delta: {delta:.2f}°, Theta: {theta:.2f}°")
    # print(f"Direkte Einstrahlung: {direkte_einstrahlung:.2f} W/m², Diffuse Einstrahlung: {diffuse_einstrahlung:.2f} W/m², Bodenreflektierte Einstrahlung: {bodenref_strahlung:.2f} W/m²")

    return direkte_einstrahlung + diffuse_einstrahlung + bodenref_strahlung