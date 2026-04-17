#!/bin/bash

echo "🚀 Portal Grobogan Development Mode"

# ======================
# Detect Python (Windows Safe)
# ======================
if command -v python >/dev/null 2>&1; then
    PYTHON=python
else
    PYTHON=py
fi

echo "Using Python: $PYTHON"

# ======================
# Create Virtual Environment
# ======================
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    $PYTHON -m venv venv
fi

# ======================
# Activate venv (Windows Git Bash)
# ======================
source venv/Scripts/activate

# ======================
# Install Dependencies
# ======================
pip install --upgrade pip
pip install -r requirements.txt

# ======================
# Flask Config
# ======================
export FLASK_APP=app.py
export FLASK_ENV=development
export FLASK_DEBUG=1

echo "🔥 Running Flask Server..."
flask run
