import os
import logging
from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
from flask_socketio import SocketIO
from celery import Celery
from backend.data_provider import DataProvider
from backend.api import api_blueprint  # הייבוא מהקובץ החדש

# --- הגדרת Logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
)
logger = logging.getLogger("FaultSolver")

# --- הגדרת כתובות ---
REDIS_URL = os.getenv("CELERY_BROKER_URL", "redis://127.0.0.1:6379/0")
DB_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:frolog@127.0.0.1:5432/test_DB1"
)

# --- הגדרת Celery (גלובלי עבור ה-Worker) ---
celery_app = Celery("fault_tasks", broker=REDIS_URL, backend=REDIS_URL)

dp = DataProvider(db_url=DB_URL)


@celery_app.task(bind=True, max_retries=3, name="backend.app.fetch_faults_task")
def fetch_faults_task(self, level, level_id, sid=None):
    try:
        logger.info(f"Starting task: level={level}, id={level_id}, sid={sid}")
        result = dp.get_faults(level, level_id)
        if sid:
            external_si = SocketIO(message_queue=REDIS_URL)
            external_si.emit("task_completed", {"result": result}, room=sid)
            logger.info(f"WebSocket message sent to sid: {sid}")
        return result
    except Exception as exc:
        logger.error(f"❌ Error in task: {exc}. Retrying...")
        raise self.retry(exc=exc)


def create_app():
    # שים לב לנתיבים: static ו-template מכוונים לתיקיית ה-frontend
    app = Flask(
        __name__,
        static_folder="../frontend",
        static_url_path="/",
        template_folder="../frontend",
    )
    CORS(app)

    # רישום ה-Blueprint (זה פותר את בעיית ה-/api)
    app.register_blueprint(api_blueprint, url_prefix="/api")

    socketio = SocketIO(app, cors_allowed_origins="*", message_queue=REDIS_URL)

    # וידוא נתיב ה-Frontend
    current_dir = os.path.dirname(os.path.abspath(__file__))
    frontend_dir = os.path.abspath(os.path.join(current_dir, "..", "frontend"))

    logger.info(f"Checking frontend path: {frontend_dir}")

    # --- ROUTES להגשת קבצים ---

    @app.route("/")
    def serve_index():
        logger.info("Serving index.html")
        return send_from_directory(frontend_dir, "index.html")

    @app.route("/<path:path>")
    def serve_static(path):
        # הגשה גנרית של כל קובץ (js, css) מתוך תיקיית frontend
        return send_from_directory(frontend_dir, path)

    return app, socketio


# יצירת המופעים להרצה
app, socketio = create_app()

if __name__ == "__main__":
    logger.info("Starting Flask-SocketIO Server on port 5000")
    socketio.run(app, debug=True, host="0.0.0.0", port=5000, allow_unsafe_werkzeug=True)
