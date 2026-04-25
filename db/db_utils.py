from db.connection import get_connection

def insert(table, columns, values):
    conn = get_connection()
    cur = conn.cursor()

    cols = ', '.join(columns)
    placeholders = ', '.join(['%s'] * len(values))

    query = f"INSERT INTO {table} ({cols}) VALUES ({placeholders})"
    cur.execute(query, values)

    conn.commit()
    cur.close()
    conn.close()


def update(table, columns, values, record_id):
    conn = get_connection()
    cur = conn.cursor()

    set_clause = ', '.join([f"{col} = %s" for col in columns])
    set_clause += ", updated_timestamp = CURRENT_TIMESTAMP"

    query = f"UPDATE {table} SET {set_clause} WHERE id = %s"
    cur.execute(query, values + [record_id])

    conn.commit()
    cur.close()
    conn.close()


def delete_record(table, record_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(f"DELETE FROM {table} WHERE id = %s", (record_id,))
    conn.commit()

    cur.close()
    conn.close()


def fetch_dropdown(table, display_col):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(f"SELECT id, {display_col} FROM {table}")
    data = cur.fetchall()

    cur.close()
    conn.close()
    return data


def fetch_by_id(table, record_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(f"SELECT * FROM {table} WHERE id = %s", (record_id,))
    row = cur.fetchone()

    cols = [desc[0] for desc in cur.description]

    cur.close()
    conn.close()

    return dict(zip(cols, row)) if row else None

def fetch_top_n(table, n=10):
    conn = get_connection()
    cur = conn.cursor()

    query = f"""
    SELECT * FROM {table}
    ORDER BY created_timestamp DESC
    LIMIT {n}
    """

    cur.execute(query)
    data = cur.fetchall()

    cols = [desc[0] for desc in cur.description]

    cur.close()
    conn.close()

    return cols, data