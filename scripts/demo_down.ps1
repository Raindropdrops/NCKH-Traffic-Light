# scripts/demo_down.ps1 — Stop demo environment
# Usage: .\scripts\demo_down.ps1

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot

Write-Host ""
Write-Host "========================================" -ForegroundColor Yellow
Write-Host "  Traffic Light MQTT Demo - STOP" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Yellow
Write-Host ""

# Step 1: Stop mock ESP32 processes
Write-Host "[1/2] Stopping mock ESP32..." -ForegroundColor Yellow
$mockProcs = Get-Process python -ErrorAction SilentlyContinue | Where-Object {
    try { $_.MainModule.FileName -match "python" } catch { $false }
}
if ($mockProcs) {
    # Find mock_esp32 by command line
    Get-WmiObject Win32_Process -Filter "Name='python.exe'" | Where-Object {
        $_.CommandLine -match "mock_esp32"
    } | ForEach-Object {
        Write-Host "  Stopping PID $($_.ProcessId)..."
        Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue
    }
    Write-Host "  Mock processes stopped." -ForegroundColor Green
} else {
    Write-Host "  No mock processes found." -ForegroundColor Gray
}

# Step 2: Docker Compose Down
Write-Host "[2/2] Stopping Docker containers..." -ForegroundColor Yellow
Push-Location $repoRoot
docker compose down
Pop-Location

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Demo environment stopped." -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
