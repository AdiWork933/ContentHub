# Run script for Windows - Starts the Flask application

Write-Host "Starting Flask application..." -ForegroundColor Green

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "Virtual environment not found. Please run setup.ps1 first." -ForegroundColor Red
    exit 1
}

# Activate virtual environment if not already activated
if (-not $env:VIRTUAL_ENV) {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & ".\venv\Scripts\Activate.ps1"
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to activate virtual environment" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "Virtual environment already activated" -ForegroundColor Yellow
}

# Run the Flask app
Write-Host "Running Flask application on http://localhost:5000" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Cyan
python app.py
