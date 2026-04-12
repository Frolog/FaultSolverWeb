# setup_db.py
from ast import Import

import psycopg2
from psycopg2 import sql, OperationalError

# -----------------------------
# Database connection info
# -----------------------------
DB_NAME = "faultsolver_db"
DB_USER = "postgres"      # שנה בהתאם למשתמש שלך
DB_PASSWORD = "frolog" # שנה בהתאם לסיסמה שלך
DB_HOST = "127.0.0.1"
DB_PORT = "5432"


def create_database():
    try:
        # Connect to default postgres DB to create our DB
        conn = psycopg2.connect(
            dbname="postgres",
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.autocommit = True
        cur = conn.cursor()

        # Create database if it doesn't exist
        cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{DB_NAME}'")
        exists = cur.fetchone()
        if not exists:
            cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME)))
            print(f"Database {DB_NAME} created.")
        else:
            print(f"Database {DB_NAME} already exists.")

        cur.close()
        conn.close()
    except OperationalError as e:
        print("❌ Error connecting to PostgreSQL:", e)
        print("בדוק את שם המשתמש והסיסמה, או שהשרת רץ בלוקאלי")
        exit(1)

def create_tables():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cur = conn.cursor()

        tables = {
            "projects": """
                CREATE TABLE IF NOT EXISTS projects (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL UNIQUE
                );
            """,
            "systems": """
                CREATE TABLE IF NOT EXISTS systems (
                    id SERIAL PRIMARY KEY,
                    project_id INTEGER REFERENCES projects(id),
                    name TEXT NOT NULL
                );
            """,
            "subassemblies": """
                CREATE TABLE IF NOT EXISTS subassemblies (
                    id SERIAL PRIMARY KEY,
                    system_id INTEGER REFERENCES systems(id),
                    name TEXT NOT NULL
                );
            """,
            "cards": """
                CREATE TABLE IF NOT EXISTS cards (
                    id SERIAL PRIMARY KEY,
                    subassembly_id INTEGER REFERENCES subassemblies(id),
                    name TEXT NOT NULL
                );
            """,
            "faults": """
                CREATE TABLE IF NOT EXISTS faults (
                    id SERIAL PRIMARY KEY,
                    level TEXT NOT NULL,
                    level_id INTEGER NOT NULL,
                    description TEXT NOT NULL
                );
            """,
            "steps": """
                CREATE TABLE IF NOT EXISTS steps (
                    id SERIAL PRIMARY KEY,
                    fault_id INTEGER REFERENCES faults(id),
                    step_number INTEGER NOT NULL,
                    step TEXT NOT NULL,
                    explanation TEXT
                );
            """,
            "documents": """
                CREATE TABLE IF NOT EXISTS documents (
                    id SERIAL PRIMARY KEY,
                    level TEXT NOT NULL,
                    level_id INTEGER NOT NULL,
                    file_path TEXT NOT NULL
                );
            """
        }

        for name, ddl in tables.items():
            cur.execute(ddl)
            print(f"Table {name} ready.")

        conn.commit()
        cur.close()
        conn.close()
        print("✅ Database setup completed successfully!")
    except OperationalError as e:
        print("❌ Error connecting to PostgreSQL:", e)
        exit(1)

if __name__ == "__main__":
    create_database()
    create_tables()