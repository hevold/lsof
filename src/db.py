import sqlite3
from pathlib import Path


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS zones (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  bbox TEXT NOT NULL,
  active INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS scenes (
  id TEXT PRIMARY KEY,
  zone_id TEXT NOT NULL,
  scene_time TEXT NOT NULL,
  ingested_at TEXT NOT NULL,
  product_id TEXT NOT NULL,
  FOREIGN KEY(zone_id) REFERENCES zones(id)
);

CREATE TABLE IF NOT EXISTS detections (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  scene_id TEXT NOT NULL,
  zone_id TEXT NOT NULL,
  detected_at TEXT NOT NULL,
  lat REAL NOT NULL,
  lon REAL NOT NULL,
  bbox TEXT NOT NULL,
  confidence REAL NOT NULL,
  size_class TEXT NOT NULL,
  thumbnail_path TEXT,
  FOREIGN KEY(scene_id) REFERENCES scenes(id),
  FOREIGN KEY(zone_id) REFERENCES zones(id)
);

CREATE TABLE IF NOT EXISTS ais_matches (
  detection_id INTEGER PRIMARY KEY,
  matched INTEGER NOT NULL,
  source TEXT,
  vessel_name TEXT,
  mmsi TEXT,
  distance_km REAL,
  time_offset_min REAL,
  FOREIGN KEY(detection_id) REFERENCES detections(id)
);

CREATE TABLE IF NOT EXISTS rule_results (
  detection_id INTEGER PRIMARY KEY,
  score INTEGER NOT NULL,
  reasons_json TEXT NOT NULL,
  distance_to_naval_base_km REAL,
  alerted INTEGER NOT NULL,
  FOREIGN KEY(detection_id) REFERENCES detections(id)
);
"""


def connect(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(db_path)


def init_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA_SQL)
    conn.commit()
