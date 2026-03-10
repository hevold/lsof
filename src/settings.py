from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel
import os

load_dotenv()


class Settings(BaseModel):
    db_path: Path = Path(os.getenv("DB_PATH", "data/db/sentinel_watch.db"))
    zones_path: Path = Path("config/zones.yaml")
    rules_path: Path = Path("config/rules.yaml")

    smtp_host: str | None = os.getenv("SMTP_HOST")
    smtp_port: int = int(os.getenv("SMTP_PORT", "587"))
    smtp_user: str | None = os.getenv("SMTP_USER")
    smtp_pass: str | None = os.getenv("SMTP_PASS")
    alert_to: str | None = os.getenv("ALERT_TO")
    alert_from: str | None = os.getenv("ALERT_FROM")


settings = Settings()
