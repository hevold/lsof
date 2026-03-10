# Sentinel Watch (v1 scaffold)

Sentinel Watch is a lightweight hourly pipeline scaffold for finding potentially suspicious ships in predefined maritime zones using Sentinel-1 SAR imagery, optional AIS matching, and rule-based alerting.

## v1 goals

- Run once per hour (GitHub Actions or cron)
- Query Sentinel-1 scenes from Copernicus Data Space STAC
- Prepare scene subsets per configured zone
- Run ship detection (placeholder YOLO interface)
- Match detections against AIS (placeholder interface)
- Score detections with simple rules
- Persist findings to SQLite
- Send alert emails for high-score events

## Repository layout

```text
.
├─ README.md
├─ requirements.txt
├─ .env.example
├─ config/
│  ├─ zones.yaml
│  ├─ rules.yaml
│  └─ naval_sites.geojson
├─ scripts/
│  └─ init_db.py
├─ src/
│  ├─ main.py
│  ├─ pipeline.py
│  ├─ db.py
│  ├─ settings.py
│  ├─ zones.py
│  ├─ rules_engine.py
│  ├─ notifier.py
│  ├─ sentinel/
│  │  └─ stac_client.py
│  └─ ais/
│     └─ matcher.py
└─ .github/
   └─ workflows/
      └─ hourly.yml
```

## Quick start

1. Create and activate a Python 3.11+ environment.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Copy env template and set values:

   ```bash
   cp .env.example .env
   ```

4. Initialize database:

   ```bash
   python scripts/init_db.py
   ```

5. Run once locally:

   ```bash
   python -m src.main
   ```

## Notes

- This scaffold intentionally includes placeholders for heavy operations (download, SAR preprocessing, YOLO inference, AIS API calls).
- GitHub Actions scheduled workflows use UTC.
