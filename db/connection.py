import os

import psycopg2


def _env(primary: str, fallback: str, default: str) -> str:
    return os.environ.get(primary) or os.environ.get(fallback) or default


def get_connection():
    return psycopg2.connect(
        host=_env("ORION_DB_HOST", "DB_HOST", "localhost"),
        database=_env("ORION_DB_NAME", "DB_NAME", "orion"),
        user=_env("ORION_DB_USER", "DB_USER", "orion_user"),
        password=_env("ORION_DB_PASSWORD", "DB_PASSWORD", "orion_dev_password"),
        port=int(_env("ORION_DB_PORT", "DB_PORT", "5432")),
    )
