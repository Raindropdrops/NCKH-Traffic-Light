# scripts/demo_up.ps1 — Start full demo environment
# Usage: .\scripts\demo_up.ps1

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Traffic Light MQTT Demo - START" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Docker Compose Up
Write-Host "[1/5] Starting Docker containers..." -ForegroundColor Yellow
Push-Location $repoRoot
docker compose up -d
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: docker compose up failed!" -ForegroundColor Red
    Pop-Location
    exit 1
}

# Step 2: Wait for health
Write-Host "[2/5] Waiting for services to be ready..." -ForegroundColor Yellow
$maxWait = 30
$waited = 0
while ($waited -lt $maxWait) {
    $ps = docker compose ps --format json 2>$null
    if ($ps) {
        break
    }
    Start-Sleep 2
    $waited += 2
    Write-Host "  Waiting... ($waited/$maxWait s)"
}
Start-Sleep 5
Write-Host "  Services ready!" -ForegroundColor Green

# Step 3: Copy flows into Node-RED
Write-Host "[3/5] Loading Node-RED flows..." -ForegroundColor Yellow
$flowsPath = Join-Path $repoRoot "node-red\flows.json"
if (Test-Path $flowsPath) {
    docker cp $flowsPath nodered:/data/flows_nodered.json
    docker compose restart nodered
    Start-Sleep 8
    Write-Host "  Flows loaded!" -ForegroundColor Green
}
else {
    Write-Host "  WARNING: flows.json not found at $flowsPath" -ForegroundColor Red
}

# Step 4: Start mock ESP32 in new window
Write-Host "[4/5] Starting Mock ESP32..." -ForegroundColor Yellow
$mockPath = Join-Path $repoRoot "logger\tools\mock_esp32.py"
if (Test-Path $mockPath) {
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$repoRoot'; python '$mockPath' --host 127.0.0.1"
    Start-Sleep 3
    Write-Host "  Mock ESP32 running in new window!" -ForegroundColor Green
}
else {
    Write-Host "  WARNING: mock_esp32.py not found" -ForegroundColor Red
}

# Step 5: Open Dashboard
Write-Host "[5/5] Opening Dashboard..." -ForegroundColor Yellow
Start-Process "http://localhost:1880/ui"

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  DEMO READY!" -ForegroundColor Green
Write-Host "  Dashboard: http://localhost:1880/ui" -ForegroundColor Green
Write-Host "  Editor:    http://localhost:1880" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Pop-Location
