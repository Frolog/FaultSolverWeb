import os
import logging
from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
from flask_socketio import SocketIO
from celery import Celery
from backend.data_provider import DataProvider

# --- הגדרת Logging מסודר ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler("app.log"),  # כתיבה לקובץ
        logging.StreamHandler()         # כתיבה לטרמינל (Console)
    ]
)
logger = logging.getLogger("FaultSolver")

# --- הגדרת כתובות (תמיכה ב-Docker ובמקומית) ---
# קריאת הכתובות מהסביבה, עם ברירת מחדל למקרה שאתה מריץ ללא דוקר
REDIS_URL = os.getenv("CELERY_BROKER_URL", "redis://127.0.0.1:6379/0")
DB_URL = os.getenv("DATABASE_URL", "postgresql://postgres:frolog@127.0.0.1:5432/faultsolver_db")
# --- הגדרת Celery ---
celery_app = Celery("fault_tasks", broker=REDIS_URL, backend=REDIS_URL)

dp = DataProvider(db_url=DB_URL)

@celery_app.task(bind=True, max_retries=3, name="backend.app.fetch_faults_task")
def fetch_faults_task(self, level, level_id, sid=None):
    try:
        logger.info(f"🚀 Starting task: level={level}, id={level_id}, sid={sid}")
        
        # ביצוע השאילתה מול ה-Database
        result = dp.get_faults(level, level_id)
        
        # אם יש sid, אנחנו דוחפים את התוצאה ישירות ל-Socket דרך Redis
        if sid:
            # יצירת מופע זמני של SocketIO לשידור מה-Worker
            external_si = SocketIO(message_queue=REDIS_URL)
            external_si.emit('task_completed', {'result': result}, room=sid)
            logger.info(f"✅ WebSocket message sent to sid: {sid}")
            
        return result
    except Exception as exc:
        logger.error(f"❌ Error in task: {exc}. Retrying...")
        raise self.retry(exc=exc)

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    socketio = SocketIO(app, cors_allowed_origins="*", message_queue=REDIS_URL)

    # תיקון חישוב הנתיב - וודא שזה תואם למבנה התיקיות שלך
    current_dir = os.path.dirname(os.path.abspath(__file__))
    frontend_dir = os.path.abspath(os.path.join(current_dir, "..", "frontend"))
    
    # הוספת לוג לבדיקה - זה יופיע לך בטרמינל של דוקר!
    logger.info(f"📁 Checking frontend path: {frontend_dir}")
    if not os.path.exists(frontend_dir):
        logger.error(f"❌ Frontend directory NOT FOUND at: {frontend_dir}")
        
    # --- ROUTES ---

    @app.route("/")
    def serve_frontend():
        logger.info("Serving index.html")
        return send_from_directory(frontend_dir, "index.html")

    @app.route("/<path:path>")
    def serve_static(path):
        return send_from_directory(frontend_dir, path)

    @app.route("/projects")
    def projects():
        logger.info("Fetching projects list")
        return jsonify(dp.get_projects())

    @app.route("/systems/<int:project_id>")
    def systems(project_id):
        return jsonify(dp.get_systems(project_id))

    @app.route("/subassemblies/<int:system_id>")
    def subassemblies(system_id):
        return jsonify(dp.get_subassemblies(system_id))

    @app.route("/faults/async/<level>/<int:level_id>")
    def faults_async(level, level_id):
        # קבלת ה-sid מה-Query Parameters של הבקשה
        sid = request.args.get('sid')
        task = fetch_faults_task.delay(level, level_id, sid=sid)
        logger.info(f"Task queued: {task.id} for sid: {sid}")
        return jsonify({"task_id": task.id}), 202

    @app.route("/tasks/status/<task_id>")
    def get_task_status(task_id):
        task_result = fetch_faults_task.AsyncResult(task_id)
        result_data = {"task_id": task_id, "state": task_result.state}
        if task_result.state == 'SUCCESS':
            result_data["result"] = task_result.result
        return jsonify(result_data)

    return app, socketio

if __name__ == "__main__":
    app, socketio = create_app()
    logger.info("🔥 Starting Flask-SocketIO Server on port 5000")
    # הרצה באמצעות socketio לתמיכה ב-WebSockets
    socketio.run(app, debug=True, host="0.0.0.0", port=5000, allow_unsafe_werkzeug=True)