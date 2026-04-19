import psycopg2
from psycopg2.extras import RealDictCursor

DB_CONFIG = {
    "dbname": "faultsolver_db",
    "user": "postgres",
    "password": "frolog",
    "host": "127.0.0.1",
    "port": "5432"
}

def get_connection():
    return psycopg2.connect(
        **DB_CONFIG,
        cursor_factory=RealDictCursor
    )