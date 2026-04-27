#!/bin/bash

echo "🎬 Starting Video Generation System API..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Start the server
echo "🚀 Starting FastAPI server..."
echo "📖 API docs will be available at: http://localhost:8000/docs"
echo ""
uvicorn app.main_sqlite:app --reload --host 0.0.0.0 --port 8000
