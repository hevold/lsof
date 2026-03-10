def match_ais(lat: float, lon: float, detected_at: str) -> dict:
    """Placeholder AIS matcher.

    Returns a minimal shape expected by pipeline.
    """
    _ = (lat, lon, detected_at)
    return {
        "matched": False,
        "source": None,
        "vessel_name": None,
        "mmsi": None,
        "distance_km": None,
        "time_offset_min": None,
    }
