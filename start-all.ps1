# DocWeaver - Start All Services Script (PowerShell)
# This script starts all three services in separate PowerShell windows

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  DocWeaver - Starting All Services" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $null = python --version
} catch {
    Write-Host "[ERROR] Python not found. Please install Python 3.9+" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if Node is installed
try {
    $null = node --version
} catch {
    Write-Host "[ERROR] Node.js not found. Please install Node.js 18+" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if .env exists
if (-not (Test-Path ".env")) {
    Write-Host "[WARNING] .env file not found" -ForegroundColor Yellow
    Write-Host "   Create .env with: GEMINI_API_KEY=your_key_here" -ForegroundColor Yellow
    Write-Host ""
}

Write-Host "[1/3] Installing dependencies..." -ForegroundColor Green
Write-Host ""

# Install Python dependencies
Write-Host "  - Installing Python dependencies..."
pip install -r REQUIREMENTS.txt | Out-Null

# Install Node dependencies
Write-Host "  - Installing Node dependencies..."
Set-Location frontend
npm install | Out-Null
Set-Location ..

Write-Host ""
Write-Host "[2/3] Dependencies installed!" -ForegroundColor Green
Write-Host ""
Write-Host "[3/3] Starting services..." -ForegroundColor Green
Write-Host ""

$currentPath = Get-Location

# Start FastAPI Backend
Write-Host "  - Starting FastAPI Backend (Port 8000)" -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$currentPath\clinical_orchestrator'; python api.py"

# Wait a bit
Start-Sleep -Seconds 3

# Start Streamlit Demo
Write-Host "  - Starting Streamlit Demo (Port 8501)" -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$currentPath\clinical_orchestrator'; streamlit run app.py"

# Wait a bit
Start-Sleep -Seconds 3

# Start Next.js Frontend
Write-Host "  - Starting Next.js Frontend (Port 3000)" -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$currentPath\frontend'; npm run dev"

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  All Services Starting!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Services will be available at:" -ForegroundColor White
Write-Host "  - Frontend:  http://localhost:3000" -ForegroundColor Yellow
Write-Host "  - API:       http://localhost:8000" -ForegroundColor Yellow
Write-Host "  - Demo:      http://localhost:8501" -ForegroundColor Yellow
Write-Host ""
Write-Host "Check the new PowerShell windows for startup progress" -ForegroundColor Gray
Write-Host ""
Write-Host "To stop services, close the PowerShell windows or press Ctrl+C in each" -ForegroundColor Gray
Write-Host ""

Read-Host "Press Enter to exit"
