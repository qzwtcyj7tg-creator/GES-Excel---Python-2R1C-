# Laden von ymal datei und übegabe der Werte an die Simulation

import yaml

def load_scenario(file_path):
    with open('scenarios/din_en_12831.yaml', 'r') as file:
        data = yaml.load(file, Loader = yaml.SafeLoader)

    for key in dict.keys(data):
        print(key, ":", data[key])  

    # Dictionary übergeben und daraus mit den Variablennamenn die Werte extrahieren?
    # Andere option? 

    # Test V 0.2

    return data