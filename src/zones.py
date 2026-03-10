from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass
class Zone:
    id: str
    name: str
    bbox: list[float]
    active: bool = True


def load_active_zones(path: Path) -> list[Zone]:
    data = yaml.safe_load(path.read_text())
    zones = [Zone(**zone) for zone in data.get("zones", [])]
    return [zone for zone in zones if zone.active]
