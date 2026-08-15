import os

import psycopg2

def get_connection():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "100.71.92.51"),
        database=os.environ.get("DB_NAME", "orion"),
        user=os.environ.get("DB_USER", "orion_user"),
        password=os.environ.get("DB_PASSWORD", "StrongPassword123"),
        port=int(os.environ.get("DB_PORT", "5432")),
    )