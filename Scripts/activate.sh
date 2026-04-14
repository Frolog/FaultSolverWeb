#!/bin/bash

PROJECT_PATH="$(cd "$(dirname "$0")/.." && pwd)"

cd "$PROJECT_PATH"

source venv/Scripts/activate

echo "✅ venv activated"
echo "📁 Project: $PROJECT_PATH"