#!/bin/bash

set -e

PROJECT_PATH="$(cd "$(dirname "$0")/.." && pwd)"

echo "======================================"
echo "🚀 FaultSolver Backend Launcher"
echo "======================================"

cd "$PROJECT_PATH"

# Activate venv
source venv/Scripts/activate

echo "🚀 Starting backend..."

cd backend
python app.py