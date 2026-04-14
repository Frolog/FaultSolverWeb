#!/bin/bash

set -e

PROJECT_PATH="$(cd "$(dirname "$0")/../FaultSolverWeb" && pwd)"
cd "$PROJECT_PATH"

echo "=============================="
echo "🔧 Self-Healing Setup Starting"
echo "=============================="

# -----------------------------
# 1. Detect broken venv
# -----------------------------
BROKEN=0

if [ -d "venv" ]; then
    echo "🟡 venv exists → testing..."

    if [ ! -f "venv/Scripts/python.exe" ]; then
        echo "❌ venv is broken"
        BROKEN=1
    else
        echo "🟢 venv looks OK"
    fi
else
    echo "🟡 venv not found"
    BROKEN=1
fi

# -----------------------------
# 2. Rebuild if needed
# -----------------------------
if [ "$BROKEN" -eq 1 ]; then
    echo "🧹 Rebuilding venv..."
    rm -rf venv
    python -m venv venv
fi

# -----------------------------
# 3. Activate venv
# -----------------------------
source venv/Scripts/activate

# -----------------------------
# 4. Fix pip
# -----------------------------
echo "🛠 Fixing pip..."
python -m ensurepip --upgrade || true
python -m pip install --upgrade pip setuptools wheel

# -----------------------------
# 5. Install dependencies
# -----------------------------
echo "📦 Installing dependencies..."
python -m pip install flask flask-cors psycopg2-binary

# -----------------------------
# 6. Freeze requirements
# -----------------------------
python -m pip freeze > requirements.txt

echo "=============================="
echo "✅ Setup completed successfully"
echo "=============================="