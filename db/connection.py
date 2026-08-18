import os
from pathlib import Path

import psycopg2

_ENV_LOADED = False
# Shared Tailscale Postgres at 100.71.92.51 still uses StrongPassword123.
# Local Homebrew / cloud-agent Postgres uses orion_dev_password.
_PASSWORDS = ("orion_dev_password", "StrongPassword123", "change-me-strong-password")
_TAILSCALE_DB_HOST = "100.71.92.51"


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


def _env(primary: str, fallback: str, default: str) -> str:
    return os.environ.get(primary) or os.environ.get(fallback) or default


def _connect_params():
    _load_dotenv()
    host = _env("ORION_DB_HOST", "DB_HOST", "localhost")
    default_password = (
        "StrongPassword123" if host == _TAILSCALE_DB_HOST else "orion_dev_password"
    )
    return {
        "host": host,
        "database": _env("ORION_DB_NAME", "DB_NAME", "orion"),
        "user": _env("ORION_DB_USER", "DB_USER", "orion_user"),
        "password": _env("ORION_DB_PASSWORD", "DB_PASSWORD", default_password),
        "port": int(_env("ORION_DB_PORT", "DB_PORT", "5432")),
    }


def get_connection():
    params = _connect_params()
    tried = []
    last_error = None
    for password in (params["password"], *_PASSWORDS):
        if password in tried:
            continue
        tried.append(password)
        try:
            return psycopg2.connect(**{**params, "password": password})
        except psycopg2.OperationalError as exc:
            if "password authentication failed" not in str(exc):
                raise
            last_error = exc
    raise last_error
