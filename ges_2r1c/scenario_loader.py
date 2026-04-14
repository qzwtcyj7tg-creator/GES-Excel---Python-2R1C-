from pathlib import Path

import yaml


def load_scenario(file_path: str | Path) -> dict:
    """Lädt Simulationsparameter aus einer YAML-Datei."""
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)
