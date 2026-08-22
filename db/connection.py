import os

import psycopg2


def get_connection():
    """Connect to the on-prem Postgres (Tailscale host by default).

    Override any value with ORION_DB_HOST, ORION_DB_NAME, ORION_DB_USER,
    ORION_DB_PASSWORD, or ORION_DB_PORT when running against a different server.
    """
    return psycopg2.connect(
        host=os.getenv("ORION_DB_HOST", "100.71.92.51"),
        database=os.getenv("ORION_DB_NAME", "orion"),
        user=os.getenv("ORION_DB_USER", "orion_user"),
        password=os.getenv("ORION_DB_PASSWORD", "StrongPassword123"),
        port=int(os.getenv("ORION_DB_PORT", "5432")),
    )
