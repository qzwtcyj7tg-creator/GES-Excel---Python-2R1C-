# Berechnung des Sonnenstands und der solaren Einstrahlung
# Geographische Länge und Breite für Augsburg (48,1° Nord, 10,5° Ost)

# Stundenwinkel: Delta = (h-12 * 15°) h: Stunde des Tages 

# Korrektur Zeitzone Abweichung dDelta = gamma_zeitzone - gamma = 10,5° - 15° (15° Zeitzone Berlin)

# Ekliptik e: e = 23,45° * sin(d-81)/365 * 2*pi/360 d 81: 21. März (Frühlingsanfang bzw. Tag/Nacht-Gleiche)

# Sonnenhöhe: sin theta = sin e * sin phi + cos e * cos phi * cos Delta
# theta = arcsin(sin e * sin phi + cos e * cos phi * cos Delta)

# Azimuth (Der Sonnenazimut ist der Winkel zwischen der Nordrichtung und der Richtung zur Sonne, gemessen im Uhrzeigersinn von 0° bis 360°.) 
# cos alpha = sin delta * sin phi - sin e / cos delta * cos phi
# alpha = arccos(sin delta * sin phi - sin e / cos delta * cos phi)
# cot alpha = cos delta * sin phi - tan e * sin e * cos phi / sin delta
