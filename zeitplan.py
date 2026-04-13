import numpy as np
from raum_parameter import c320

# --- Zeitplan wie in GES Excel ---

# 1. Zeitachse erstellen mit 8760 Stunden (1 Jahr, nicht Schaltjahr)
stunden_jahr = np.arange(8760) # Eindimensionaler Array von 0 bis 8759, repräsentiert jede Stunde im Jahr.

# 2. Tägliche Belegung (9:00 bis 17:00 Uhr)
t_0 = np.zeros(24) # 24 Stunden, alle mit 0 (keine Belegung)
t_work = np.zeros(24)
t_work[9:18] = 0.5   # 09:00–17:00 Uhr (9 Stunden, Stunde 9-17 wie im Zeitplan)

# Verschiebung um -1 Stunde: TRY-Wetterdaten nutzen 1-basierte Stunden (HH=1..24),
# das Excel bildet den Zeitplan über MOD(Stunde,24) ab, wodurch Stunde 9 im Zeitplan
# auf den 0-basierten Array-Index 8 fällt.
t_work = np.roll(t_work, -1)

# Profile zuordnen (Montag bis Freitag = Arbeitstag, Samstag und Sonntag = Wochenende)
t_mo, t_di, t_mi, t_do, t_fr = [t_work.copy() for _ in range(5)]
t_sa, t_so = [t_0.copy() for _ in range(2)]

# 3. Starttag ist Donnerstag (01.01.), daher Reihenfolge: Do, Fr, Sa, So, Mo, Di, Mi
tage_liste = [t_do, t_fr, t_sa, t_so, t_mo, t_di, t_mi]
wochen_signal = np.concatenate(tage_liste) # Verbindet Arrays auf einer existierenden Achse, 168 Stunden (7 Tage * 24 Stunden) ergeben ein Wochenprofil.
stundenplan_jahr = np.tile(wochen_signal, 53)[:8760] # Wiederholt das Wochenprofil 53 Mal, um 8760 Stunden abzudecken (53*7=371 Tage, mehr als genug für 365 Tage)

# 4. Ferienzeiten (Tag-Nummern 0-basiert, Ende exklusiv wie im GES-Excel Zeitplan)
ferien_maske = np.ones(8760) # Erstellt Array mit 8760 Einsen, damit erstmal standardmäßig belegt ist
ferien_tage = [
    (0, 6),      # 01.01. bis 06.01. (Tag 0-5), ab Tag 6 (07.01.) wieder Nutzung
    (45, 74),    # 15.02. bis 14.03. (Tag 45-73), ab Tag 74 (15.03.) wieder Nutzung
    (105, 106),  # 15.04. (Tag 105), ab Tag 106 (16.04.) wieder Nutzung
    (211, 275),  # 30.07. bis 01.10. (Tag 211-274), ab Tag 275 (02.10.) wieder Nutzung
    (356, 366)   # 22.12. bis Jahresende (Tag 356-365)
] # Definieren der Ferienperioden

for start_tag, ende_tag in ferien_tage:
    ferien_maske[start_tag*24 : ende_tag*24] = 0 # Setzt die Ferientage als 0 in der Maske

# 5. Finale Kombination von Stundenplan und Ferienmaske
nutzersignal_final = stundenplan_jahr * ferien_maske
