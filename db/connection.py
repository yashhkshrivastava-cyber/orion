import os
from pathlib import Path

import psycopg2

_ENV_LOADED = False
_TAILSCALE_DB_HOST = "100.71.92.51"
_TAILSCALE_DB_USER = "orion_user"
_TAILSCALE_DB_PASSWORD = "StrongPassword123"


def _load_dotenv():
    global _ENV_LOADED
    if _ENV_LOADED:
        return
    _ENV_LOADED = True
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if not env_path.is_file():
        return
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.startswith("export "):
            line = line[7:].strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]
        if key and key not in os.environ:
            os.environ[key] = value


def get_connection():
    _load_dotenv()
    host = os.environ.get("ORION_DB_HOST") or os.environ.get("DB_HOST") or "localhost"
    # Mac checkouts still point at this Tailscale Postgres. Its role password is
    # StrongPassword123; ignore a mismatched ORION_DB_PASSWORD from .env.
    if host == _TAILSCALE_DB_HOST:
        return psycopg2.connect(
            host=_TAILSCALE_DB_HOST,
            database="orion",
            user=_TAILSCALE_DB_USER,
            password=_TAILSCALE_DB_PASSWORD,
            port=5432,
        )
    return psycopg2.connect(
        host=host,
        database=os.environ.get("ORION_DB_NAME") or os.environ.get("DB_NAME") or "orion",
        user=os.environ.get("ORION_DB_USER") or os.environ.get("DB_USER") or "orion_app",
        password=os.environ.get("ORION_DB_PASSWORD") or os.environ.get("DB_PASSWORD") or "orion_dev_password",
        port=int(os.environ.get("ORION_DB_PORT") or os.environ.get("DB_PORT") or "5432"),
    )
