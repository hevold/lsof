from datetime import datetime, timezone

from src.ais.matcher import match_ais
from src.notifier import send_alert_email
from src.rules_engine import evaluate_detection, load_rules
from src.sentinel.stac_client import search_new_products
from src.settings import settings
from src.zones import load_active_zones


# Placeholder detection so pipeline wiring can be tested end-to-end.
def detect_ships(_scene: dict) -> list[dict]:
    return []


def run_pipeline() -> None:
    zones = load_active_zones(settings.zones_path)
    rules = load_rules(settings.rules_path)

    for zone in zones:
        products = search_new_products(zone_id=zone.id, bbox=zone.bbox, since=None)

        for product in products:
            detections = detect_ships(product)

            for det in detections:
                ais_result = match_ais(lat=det["lat"], lon=det["lon"], detected_at=det["detected_at"])
                distance_to_naval_base_km = det.get("distance_to_naval_base_km")

                rule_result = evaluate_detection(
                    size_class=det["size_class"],
                    ais_match=bool(ais_result["matched"]),
                    distance_to_naval_base_km=distance_to_naval_base_km,
                    rules=rules,
                )

                if rule_result.alerted:
                    subject = f"[Sentinel Watch] Suspicious vessel - {zone.name}"
                    body = (
                        f"Tid: {datetime.now(timezone.utc).isoformat()}\n"
                        f"Sone: {zone.name}\n"
                        f"Posisjon: {det['lat']}, {det['lon']}\n"
                        f"Størrelseklasse: {det['size_class']}\n"
                        f"AIS-match: {ais_result['matched']}\n"
                        f"Score: {rule_result.score}\n"
                        f"Forklaring: {', '.join(rule_result.reasons)}"
                    )
                    send_alert_email(subject, body)
