import numpy as np
from raum_parameter import c320
 
# --- Zeitplan wie in GES Excel ---
# Funktioniert noch nicht! 
# Problem: Fängt immer eine Stunde später an
# Aktuell wird aber NSF über GES EXCEL Tabelle importiert

# 1. Zeitachse erstellen mit 8760 Stunden (1 Jahr, nicht Schaltjahr)
stunden_jahr = np.arange(8760) # Eindimensionaler Array von 0 bis 8759, repräsentiert jede Stunde im Jahr.

# 2. Tägliche Belegung (9:00 bis 17:00 Uhr)
t_0 = np.zeros(24) # 24 Stunden, alle mit 0 (keine Belegung)
t_work = np.zeros(24) 
t_work[9:17] = 0.5   # 09:00–17:00 Uhr (8 Stunden)

# Profile zuordnen (Montag bis Freitag = Arbeitstag, Samstag und Sonntag = Wochenende)
t_mo, t_di, t_mi, t_do, t_fr = [t_work.copy() for _ in range(5)]
t_sa, t_so = [t_0.copy() for _ in range(2)]

# 3. Starttag ist Mittwoch (01.01.), daher Reihenfolge: Mi, Do, Fr, Sa, So, Mo, Di
# Index: 0=Mi, 1=Do, 2=Fr, 3=Sa, 4=So, 5=Mo, 6=Di
tage_liste = [t_mi, t_do, t_fr, t_sa, t_so, t_mo, t_di] 
wochen_signal = np.concatenate(tage_liste) # Verbindet Arrays auf einer existierenden Achse, 168 Stunden (7 Tage * 24 Stunden) ergeben ein Wochenprofil.
stundenplan_jahr = np.tile(wochen_signal, 53)[:8760] # Wiederholt das Wochenprofil 53 Mal, um 8760 Stunden abzudecken (53*7=371 Tage, mehr als genug für 365 Tage)

# 4. Ferienzeiten
ferien_maske = np.ones(8760) # Erstellt Array mit 8760 Einsen, damit erstmal standardmäßig belegt ist
ferien_tage = [
    (0, 6),      # 01.01. bis 06.01. (Stunde 0 bis 144) sind Ferien.
                 # Tag 0(Mi), 1(Do), 2(Fr), 3(Sa), 4(So), 5(Mo) = GELÖSCHT.
                 # Damit ist Dienstagmorgen (Stunde 153) der erste Wert.
    (45, 75),    # Feb/Mär
    (105, 107),  # Apr
    (211, 276),  # Sommer
    (356, 366)   # Dez
] # Definieren der Ferienperioden

for start_tag, ende_tag in ferien_tage:
    ferien_maske[start_tag*24 : ende_tag*24] = 0 # Setzt die Ferientage als 0 in der Maske

# 5. Finale Kombination von Stundenplan und Ferienmaske
nutzersignal_final = stundenplan_jahr * ferien_maske
