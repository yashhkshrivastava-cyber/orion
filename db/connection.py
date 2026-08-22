import os

import psycopg2


def get_connection():
    return psycopg2.connect(
        host=os.getenv("ORION_DB_HOST", "localhost"),
        database=os.getenv("ORION_DB_NAME", "orion"),
        user=os.getenv("ORION_DB_USER", "orion_user"),
        password=os.getenv("ORION_DB_PASSWORD", "orion_dev_password"),
        port=int(os.getenv("ORION_DB_PORT", "5432")),
    )
