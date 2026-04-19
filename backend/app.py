from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os

from backend.data_provider import DataProvider
from backend.routes.projects import projects_bp


def create_app():
    app = Flask(__name__)
    CORS(app)

    # --- DB connection ---
    dp = DataProvider(
        db_url="postgresql://postgres:frolog@127.0.0.1:5432/faultsolver_db"
    )

    # --- Blueprints ---
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
    # API ROUTES
    # =========================

    @app.route("/projects")
    def projects():
        return jsonify(dp.get_projects())

    @app.route("/systems/<int:project_id>")
    def systems(project_id):
        return jsonify(dp.get_systems(project_id))

    @app.route("/subassemblies/<int:system_id>")
    def subassemblies(system_id):
        return jsonify(dp.get_subassemblies(system_id))

    @app.route("/cards/<int:subassembly_id>")
    def cards(subassembly_id):
        return jsonify(dp.get_cards(subassembly_id))

    @app.route("/faults/<level>/<int:level_id>")
    def faults(level, level_id):
        return jsonify(dp.get_faults(level, level_id))

    @app.route("/steps/<int:fault_id>")
    def steps(fault_id):
        return jsonify(dp.get_steps(fault_id))

    @app.route("/debug/db")
    def debug_db():
        from backend.db.projects_db import get_all_projects
        return {"projects": get_all_projects()}

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)