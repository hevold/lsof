from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass
class RuleResult:
    score: int
    alerted: bool
    reasons: list[str]


def load_rules(path: Path) -> dict:
    return yaml.safe_load(path.read_text())


def evaluate_detection(size_class: str, ais_match: bool, distance_to_naval_base_km: float | None, rules: dict) -> RuleResult:
    weights = rules["weights"]
    naval_cfg = rules["naval"]

    score = 0
    reasons: list[str] = []

    if size_class == "large":
        score += weights["large_ship"]
        reasons.append("klassifisert som stort fartøy")

    if not ais_match:
        score += weights["no_ais"]
        reasons.append("ingen AIS-match innen terskel")

    if distance_to_naval_base_km is not None and distance_to_naval_base_km <= naval_cfg["near_km"]:
        score += weights["near_naval"]
        reasons.append("nær kjent marineanlegg")

    if distance_to_naval_base_km is not None and distance_to_naval_base_km <= naval_cfg["very_near_km"]:
        score += weights["very_near_naval"]

    alert_threshold = rules["alert_threshold"]
    return RuleResult(score=score, alerted=score >= alert_threshold, reasons=reasons)
