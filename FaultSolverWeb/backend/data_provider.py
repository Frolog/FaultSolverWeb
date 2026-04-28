import os
import psycopg2
from psycopg2.extras import RealDictCursor

DB_URL = os.getenv("DB_URL")

class DataProvider:
    def __init__(self, db_url):
        self.conn = psycopg2.connect(db_url, cursor_factory=RealDictCursor)

    def get_projects(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT id, name FROM projects ORDER BY name")
            return cur.fetchall()

    def get_systems(self, project_id):
        with self.conn.cursor() as cur:
            cur.execute("SELECT id, name FROM systems WHERE project_id=%s ORDER BY name", (project_id,))
            return cur.fetchall()

    def get_subassemblies(self, system_id):
        with self.conn.cursor() as cur:
            cur.execute("SELECT id, name FROM subassemblies WHERE system_id=%s ORDER BY name", (system_id,))
            return cur.fetchall()

    def get_cards(self, subassembly_id):
        with self.conn.cursor() as cur:
            cur.execute("SELECT id, name FROM cards WHERE subassembly_id=%s ORDER BY name", (subassembly_id,))
            return cur.fetchall()

    def get_faults(self, level, level_id):
        with self.conn.cursor() as cur:
            cur.execute("SELECT id, description FROM faults WHERE level=%s AND level_id=%s", (level, level_id))
            return cur.fetchall()

    def get_steps(self, fault_id):
        with self.conn.cursor() as cur:
            cur.execute("SELECT step_number, step, explanation FROM steps WHERE fault_id=%s ORDER BY step_number", (fault_id,))
            return cur.fetchall()