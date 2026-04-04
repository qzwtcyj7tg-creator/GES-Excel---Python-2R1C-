# Laden von ymal datei und übegabe der Werte an die Simulation

import yaml

with open('scenarios/din_en_12831.yaml', 'r') as file:
    data = yaml.load(file, Loader = yaml.SafeLoader)

print(data)

for key in dict.keys(data):
    print(key, ":", data[key])  

print("UserName:", data["UserName"])

# Dictionary übergeben und daraus mit den Variablennamenn die Werte extrahieren?
# Andere option? 