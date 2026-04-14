#!/bin/bash

PROJECT_PATH="$(cd "$(dirname "$0")/.." && pwd)"

cd "$PROJECT_PATH"

# activate venv
source venv/Scripts/activate

echo "🚀 Starting backend..."

cd backend
python app.py