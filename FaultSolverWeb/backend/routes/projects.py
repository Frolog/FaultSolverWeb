from flask import Blueprint, jsonify
from backend.services.project_service import get_projects

projects_bp = Blueprint("projects", __name__)

@projects_bp.route("/projects")
def projects():
    return jsonify(get_projects())