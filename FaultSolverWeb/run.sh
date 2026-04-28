#!/bin/bash

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$BASE_DIR"

echo "🚀 Starting FaultSolver (PRODUCTION MODE)"

source venv/Scripts/activate

python -m backend.app