import os
import sys
from pathlib import Path

import psycopg2
from psycopg2 import sql

_ENV_LOADED = False
# Previous hardcoded / example passwords. Used only to rotate the role to
# ORION_DB_PASSWORD (orion_dev_password) on first successful connect.
_LEGACY_PASSWORDS = ("StrongPassword123", "change-me-strong-password")


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
    return {
        "host": _env("ORION_DB_HOST", "DB_HOST", "localhost"),
        "database": _env("ORION_DB_NAME", "DB_NAME", "orion"),
        "user": _env("ORION_DB_USER", "DB_USER", "orion_user"),
        "password": _env("ORION_DB_PASSWORD", "DB_PASSWORD", "orion_dev_password"),
        "port": int(_env("ORION_DB_PORT", "DB_PORT", "5432")),
    }


def _rotate_role_password(conn, user: str, new_password: str) -> None:
    with conn.cursor() as cur:
        cur.execute(
            sql.SQL("ALTER ROLE {} PASSWORD %s").format(sql.Identifier(user)),
            (new_password,),
        )
    conn.commit()


def get_connection():
    params = _connect_params()
    try:
        return psycopg2.connect(**params)
    except psycopg2.OperationalError as exc:
        message = str(exc)
        if "password authentication failed" not in message:
            raise
        wanted = params["password"]
        if wanted in _LEGACY_PASSWORDS:
            raise
        for legacy in _LEGACY_PASSWORDS:
            if not legacy or legacy == wanted:
                continue
            try:
                conn = psycopg2.connect(**{**params, "password": legacy})
            except psycopg2.OperationalError:
                continue
            try:
                _rotate_role_password(conn, params["user"], wanted)
            finally:
                conn.close()
            print(
                "Updated orion_user to ORION_DB_PASSWORD on "
                f"{params['host']}:{params['port']}.",
                file=sys.stderr,
            )
            return psycopg2.connect(**params)
        raise
