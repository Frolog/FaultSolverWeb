from flask import Blueprint, jsonify, request
import logging

logger = logging.getLogger("FaultSolver.api")
api_blueprint = Blueprint("api", __name__)


@api_blueprint.route("/projects")
def projects():
    from backend.app import dp

    logger.info("API: Fetching projects list")
    return jsonify(dp.get_projects())


@api_blueprint.route("/systems/<int:project_id>")
def systems(project_id):
    from backend.app import dp

    logger.info(f"API: Fetching systems for project {project_id}")
    return jsonify(dp.get_systems(project_id))


@api_blueprint.route("/subassemblies/<int:system_id>")
def subassemblies(system_id):
    from backend.app import dp

    return jsonify(dp.get_subassemblies(system_id))


@api_blueprint.route("/faults/async/<level>/<int:level_id>")
def faults_async(level, level_id):
    from backend.app import fetch_faults_task

    sid = request.args.get("sid")
    task = fetch_faults_task.delay(level, level_id, sid=sid)
    logger.info(f"API: Task queued: {task.id} for sid: {sid}")
    return jsonify({"task_id": task.id}), 202


@api_blueprint.route("/tasks/status/<task_id>")
def get_task_status(task_id):
    from backend.app import celery_app

    task = celery_app.AsyncResult(task_id)
    response = {
        "state": task.state,
        "result": task.result if task.state == "SUCCESS" else None,
    }
    return jsonify(response)
