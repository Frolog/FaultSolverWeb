from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os
from celery import Celery

from backend.data_provider import DataProvider
from backend.routes.projects import projects_bp

# --- הגדרת Celery מחוץ ל-create_app כדי שה-Worker יוכל לזהות אותו ---
celery_app = Celery(
    "fault_tasks",
    broker="redis://127.0.0.1:6379/0",
    backend="redis://127.0.0.1:6379/0"
)

# הגדרת אובייקט הנתונים גלובלית לצורך המשימות
DB_URL = "postgresql://postgres:frolog@127.0.0.1:5432/faultsolver_db"
dp = DataProvider(db_url=DB_URL)

# --- הגדרת המשימה (Task) ---
@celery_app.task
def fetch_faults_task(level, level_id):
    # כאן מתבצעת השליפה הכבדה מה-DB
    # הפעולה הזו תרוץ בטרמינל נפרד (Worker)
    return dp.get_faults(level, level_id)

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(projects_bp)

    # =========================
    # FRONTEND SERVING
    # =========================

    @app.route("/")
    def serve_frontend():
        return send_from_directory(
            os.path.join(os.path.dirname(__file__), "..", "frontend"),
            "index.html"
        )

    @app.route("/<path:path>")
    def serve_static(path):
        return send_from_directory(
            os.path.join(os.path.dirname(__file__), "..", "frontend"),
            path
        )

    # =========================
    # API ROUTES (EXISTING)
    # =========================

    @app.route("/projects")
    def projects():
        return jsonify(dp.get_projects())

    @app.route("/systems/<int:project_id>")
    def systems(project_id):
        return jsonify(dp.get_systems(project_id))

    # =========================
    # NEW ASYNC ROUTES (CELERY)
    # =========================

    # נתיב חדש ששולח משימה לתור ומחזיר ID
    @app.route("/faults/async/<level>/<int:level_id>")
    def faults_async(level, level_id):
        task = fetch_faults_task.delay(level, level_id)
        return jsonify({"task_id": task.id}), 202

    # נתיב לבדיקת סטטוס המשימה
    @app.route("/tasks/status/<task_id>")
    def get_task_status(task_id):
        task_result = fetch_faults_task.AsyncResult(task_id)
        
        result_data = {
            "task_id": task_id,
            "state": task_result.state, # PENDING, PROGRESS, SUCCESS
        }
        
        if task_result.state == 'SUCCESS':
            result_data["result"] = task_result.result
            
        return jsonify(result_data)

    # ה-Routes המקוריים נשארים לתאימות
    @app.route("/subassemblies/<int:system_id>")
    def subassemblies(system_id):
        return jsonify(dp.get_subassemblies(system_id))

    @app.route("/faults/<level>/<int:level_id>")
    def faults(level, level_id):
        return jsonify(dp.get_faults(level, level_id))

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)