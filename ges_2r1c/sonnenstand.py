# Berechnung des Sonnenstands und der solaren Einstrahlung
# Geographische Länge und Breite für Augsburg (48,1° Nord, 10,5° Ost)

from math import sin, cos, radians
from xml.etree.ElementTree import PI
from math import asin as arcsin

from numpy import arccos


def sonnenstand(breite, lange, stunde, zeitzonen_offset, direktstrahlung, diffuse_strahlung, neigungswinkel, azimut_oberflaeche, azimuth_eingabe):
    tag = stunde // 24 + 1
    # uhrzeit = stunde % 24

    I_ext_mod = 1360 * 0,9

    korrektur_stundenwinkel = -(zeitzonen_offset - lange)
    # korrektur_stundenwinkel_min = (korrektur_stundenwinkel / 15) * 60

    # Stundenwinkel in Grad 
    delta = (stunde - 12) * 15 + korrektur_stundenwinkel

    # Absolute Hähe Mittagssonne eps
    eps = 23.43 * sin((tag - 81) / 180 * PI)


    # Elevation
    # elevation = arcsin(sin(radians(eps)) * sin(radians(breite)) - cos(radians(eps)) * cos(radians(breite)))
     
    # Theta
    theta = arcsin(sin(radians(eps)) * sin(radians(breite)) + cos(radians(eps)) * cos(radians(breite)) * cos(radians(delta)))

    # Azimut (Hier vermutlich besser arccot formel, da direkt die Richtung angegeben wird)
    azimut = arccos(sin(radians) * sin(radians(breite)) - sin(radians(eps)) / cos(radians(theta)) * cos(radians(breite)))

    if delta < 0: 
        azimut = -azimut

    # Soonne da (ja/nein)
    if sin(radians(theta)) > 0:
        sonne_da = True
    else:
        sonne_da = False

    # Berechnung der solaren Einstrahlung |n sonne| = 1
    # x = cos theta * cos alpha (Süden)
    # y = cos theta * sin alpha (Osten)
    # z = sin theta (Oben)

    if sonne_da:
        x_S = cos(radians(theta)) * cos(radians(azimut)) * -1 # Damit der Normal Vektor in die Horizontsle Ebene kommt 
        y_S = -cos(radians(theta)) * sin(radians(azimut)) * -1 # Nicht in Richtung Sonne
        z_S = sin(radians(theta)) * -1
    else:
        x_S = 0
        y_S = 0
        z_S = 0

    # Einstrahlung auf Normalen Vektor der Oberfläche
    # Leistungs Erhaltung I_n * A_N = I_Hori * A_Hori
    # A_N / A_Hori = l_N / l_Hori = sin(theta)
    # I_n = I_Hori / sin(theta)
    # I_N muss kleiner als extraterrestrische Einstrahlung sein! 

    if sonne_da:
        I_B_N = direktstrahlung / sin(radians(theta))
        if I_B_N > I_ext_mod:
            I_B_N = I_ext_mod
    else:
        I_B_N = 0

    # Energieerhaltung I_B,n * l_s = I_B,F * l_F
    # cos beta = l_s / l_F 
    # I_B,F / I_B,n = l_s / l_F = cos(radians(beta))
    # cos beta = n_s (Skalarprodukt) n_F / (|n_s| * |n_F|)
    # Gemäß vereinbarung ist betrag von n_s = n_F = 1
    # cos beta = n_s (Skalarprodukt) n_F

    # z_F - cos beta
    # x_F = - sin beta cos alpha
    # y_F = sin beta sin alpha

    # Normalen Vektor der Oberfläche
    x_F = -sin(radians(neigungswinkel)) * cos(radians(azimut_oberflaeche))
    y_F = sin(radians(neigungswinkel)) * sin(radians(azimut_oberflaeche))
    z_F = -cos(radians(neigungswinkel))

    view_faktor = (1 + cos(radians(neigungswinkel) /2))
    view_faktor_2 = (1 - cos(radians(neigungswinkel) /2))

    I_g_h = direktstrahlung + diffuse_strahlung

    ref_boden = 0,2

    einstrahlung = (x_S * x_F + y_S * y_F + z_S * z_F) * I_B_N + view_faktor * diffuse_strahlung + view_faktor_2 * ref_boden * I_g_h

    return einstrahlung