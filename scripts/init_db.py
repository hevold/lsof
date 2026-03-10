from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.db import connect, init_schema
from src.settings import settings


if __name__ == "__main__":
    conn = connect(settings.db_path)
    init_schema(conn)
    conn.close()
    print(f"Initialized database at {settings.db_path}")
