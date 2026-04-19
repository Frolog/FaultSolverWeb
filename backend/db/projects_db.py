from backend.db.connection import get_connection

def get_all_projects():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, name FROM projects ORDER BY id")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows