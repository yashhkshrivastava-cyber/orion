import psycopg2

def get_connection():
    return psycopg2.connect(
        host="100.71.92.51",
        database="orion",
        user="orion_user",
        password="StrongPassword123",
        port=5432   # change if needed
    )