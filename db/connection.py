import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="orion",
        user="orion_user",
        password="StrongPassword123",
        port=5432   # change if needed
    )
