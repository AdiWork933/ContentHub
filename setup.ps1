# Setup script for Windows - Creates virtual environment and installs dependencies

# Set execution policy for this process
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force

Write-Host "Setting up Python virtual environment..." -ForegroundColor Green

# Check if venv already exists
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "Virtual environment already exists" -ForegroundColor Yellow
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to activate virtual environment" -ForegroundColor Red
    exit 1
}

# Install requirements
Write-Host "Installing requirements..." -ForegroundColor Yellow
pip install -r requirements.txt --no-warn-script-location

if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to install requirements" -ForegroundColor Red
    exit 1
}

Write-Host "Setup completed successfully!" -ForegroundColor Green
Write-Host "Virtual environment is activated. You can now run the project." -ForegroundColor Cyan
