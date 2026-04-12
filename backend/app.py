from flask import Flask, jsonify
from data_provider import DataProvider

app = Flask(__name__)

# התחברות ל‑DB
dp = DataProvider(db_url="postgresql://postgres:frolog@127.0.0.1:5432/faultsolver_db")

# --- Routes ---
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

if __name__ == "__main__":
    app.run(debug=True)