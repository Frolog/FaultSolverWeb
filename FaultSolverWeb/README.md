# 🛠 FaultSolverWeb

A local web-based Fault Analysis System with Flask backend, PostgreSQL database, and simple SPA frontend.

---

# 📦 Project Structure

FaultSolverWeb/
├── backend/
│ ├── app.py
│ ├── data_provider.py
│ ├── models.py
│ └── requirements.txt
│
├── frontend/
│ ├── index.html
│ ├── script.js
│ └── style.css
│
├── venv/ # (auto-generated)
└── README.md


---

# ⚙️ Requirements

- Python 3.10+
- PostgreSQL (local installation)
- Git Bash / CMD / PowerShell

---

# 🚀 Setup Instructions (First Time Only)

## 1️⃣ Clone the project

```bash
git clone https://github.com/USERNAME/FaultSolverWeb.git
cd FaultSolverWeb

2️⃣ Create Virtual Environment (venv)
python -m venv venv

3️⃣ Activate Virtual Environment
Git Bash (recommended)
source venv/Scripts/activate
CMD
venv\Scripts\activate
PowerShell
venv\Scripts\Activate.ps1

4️⃣ Upgrade pip
python -m pip install --upgrade pip

5️⃣ Install dependencies
python -m pip install flask flask-cors psycopg2-binary

6️⃣ Setup PostgreSQL Database

Make sure PostgreSQL is running locally.

Create database:
CREATE DATABASE faultsolver_db;

7️⃣ Run Database Setup (if exists)
python backend/setup_db.py

🚀 Run the Application
Start Backend (Flask API)
cd backend
python app.py

Server will run on:
http://127.0.0.1:5000

🌐 Frontend Usage
Open:
frontend/index.html
Or serve it via browser directly.

🧠 API Endpoints
/projects
/systems/<project_id>
/subassemblies/<project_id>/<system_id>
/faults/<level>/<identifier>
🛠 Common Issues
❌ pip install error (WinError 5)

Solution: taskkill /F /IM python.exe
Then reinstall:
python -m pip install --force-reinstall psycopg2-binary
❌ Flask not found

Make sure venv is activated:

source venv/Scripts/activate
❌ Wrong Python version

Check:

python --version
where python

Always install packages using:

python -m pip install <package>

NOT:

pip install <package>
🧩 Development Notes
Backend: Flask (REST API)
DB: PostgreSQL (local)
Frontend: Vanilla JS SPA
Environment: venv (isolated Python environment)
🚀 Future Improvements
React frontend migration
Role-based authentication
Fault tree visualization
Real-time diagnostics dashboard
👨‍💻 Author

Lior A.
Fault Analysis System Project