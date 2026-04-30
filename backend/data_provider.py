import os
import logging
import psycopg2
from psycopg2.extras import RealDictCursor

# הגדרת לוגר כדי שלא תקבל שגיאות על logger not defined
logger = logging.getLogger("FaultSolver.dataprovider")


class DataProvider:
    def __init__(self, db_url):
        self.conn = psycopg2.connect(db_url, cursor_factory=RealDictCursor)

    def get_projects(self):
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT id, name FROM projects ORDER BY name")
                return cur.fetchall()
        except Exception as e:
            logger.error(f"Database error in get_projects: {e}")
            self.conn.rollback()
            return []

    def get_systems(self, project_id):
        try:
            with self.conn.cursor() as cur:
                logger.info(
                    f"Executing SQL: SELECT id, name FROM systems WHERE project_id={project_id}"
                )
                cur.execute(
                    "SELECT id, name FROM systems WHERE project_id=%s ORDER BY name",
                    (project_id,),
                )
                rows = cur.fetchall()
                logger.info(f"DB Returned {len(rows)} rows for project {project_id}")
                return rows
        except Exception as e:
            logger.error(f"Database error in get_systems: {e}")
            self.conn.rollback()
            return []

    def get_subassemblies(self, system_id):
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    "SELECT id, name FROM subassemblies WHERE system_id=%s ORDER BY name",
                    (system_id,),
                )
                return cur.fetchall()
        except Exception as e:
            logger.error(f"Database error in get_subassemblies: {e}")
            self.conn.rollback()
            return []

    def get_cards(self, subassembly_id):
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    "SELECT id, name FROM cards WHERE subassembly_id=%s ORDER BY name",
                    (subassembly_id,),
                )
                return cur.fetchall()
        except Exception as e:
            logger.error(f"Database error in get_cards: {e}")
            self.conn.rollback()
            return []

    def get_faults(self, level, level_id):
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    "SELECT id, description FROM faults WHERE level=%s AND level_id=%s",
                    (level, level_id),
                )
                return cur.fetchall()
        except Exception as e:
            logger.error(f"Database error in get_faults: {e}")
            self.conn.rollback()
            return []

    def get_steps(self, fault_id):
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    "SELECT step_number, step, explanation FROM steps WHERE fault_id=%s ORDER BY step_number",
                    (fault_id,),
                )
                return cur.fetchall()
        except Exception as e:
            logger.error(f"Database error in get_steps: {e}")
            self.conn.rollback()
            return []
