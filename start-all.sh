#!/bin/bash

# DocWeaver - Start All Services Script
# This script starts all three services in separate terminal windows

echo "🏥 DocWeaver - Starting All Services..."echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python 3.9+"
    exit 1
fi

# Check if Node is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js 18+"
    exit 1
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found"
    echo "   Create .env with: GEMINI_API_KEY=your_key_here"
    echo ""
fi

echo "📦 Installing dependencies..."
echo ""

# Install Python dependencies
echo "  → Installing Python dependencies..."
pip install -r REQUIREMENTS.txt > /dev/null 2>&1

# Install Node dependencies
echo "  → Installing Node dependencies..."
cd frontend && npm install > /dev/null 2>&1 && cd ..

echo ""
echo "✅ Dependencies installed!"
echo ""
echo "🚀 Starting services..."
echo ""

# Detect OS and open terminals accordingly
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    echo "  → FastAPI Backend (Port 8000)"
    osascript -e 'tell app "Terminal" to do script "cd '$(pwd)'/clinical_orchestrator && python api.py"'
    
    sleep 2
    
    echo "  → Streamlit Demo (Port 8501)"
    osascript -e 'tell app "Terminal" to do script "cd '$(pwd)'/clinical_orchestrator && streamlit run app.py"'
    
    sleep 2
    
    echo "  → Next.js Frontend (Port 3000)"
    osascript -e 'tell app "Terminal" to do script "cd '$(pwd)'/frontend && npm run dev"'
    
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    echo "  → FastAPI Backend (Port 8000)"
    gnome-terminal -- bash -c "cd clinical_orchestrator && python3 api.py; exec bash"
    
    sleep 2
    
    echo "  → Streamlit Demo (Port 8501)"
    gnome-terminal -- bash -c "cd clinical_orchestrator && streamlit run app.py; exec bash"
    
    sleep 2
    
    echo "  → Next.js Frontend (Port 3000)"
    gnome-terminal -- bash -c "cd frontend && npm run dev; exec bash"
    
else
    # Windows Git Bash or other
    echo "❌ Automatic terminal opening not supported on this OS"
    echo ""
    echo "Please manually open 3 terminals and run:"
    echo ""
    echo "Terminal 1:"
    echo "  cd clinical_orchestrator"
    echo "  python api.py"
    echo ""
    echo "Terminal 2:"
    echo "  cd clinical_orchestrator"
    echo "  streamlit run app.py"
    echo ""
    echo "Terminal 3:"
    echo "  cd frontend"
    echo "  npm run dev"
    exit 1
fi

echo ""
echo "✅ All services starting!"
echo ""
echo "📍 Services will be available at:"
echo "   - Frontend:  http://localhost:3000"
echo "   - API:       http://localhost:8000"
echo "   - Demo:      http://localhost:8501"
echo ""
echo "💡 Check the new terminal windows for startup progress"
echo ""
echo "🛑 To stop services, close the terminal windows or press Ctrl+C in each"
echo ""
