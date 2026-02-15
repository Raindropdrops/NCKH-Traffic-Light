# scripts/smoke.ps1 — Run smoke test
# Usage: .\scripts\smoke.ps1

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  SMOKE TEST" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Docker
Write-Host "[1/3] Checking Docker..." -ForegroundColor Yellow
Push-Location $repoRoot
$ps = docker compose ps 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Docker not running! Run .\scripts\demo_up.ps1 first." -ForegroundColor Red
    Pop-Location
    exit 1
}
Write-Host "  Docker OK!" -ForegroundColor Green

# Check MQTT port
Write-Host "[2/3] Checking MQTT port 1883..." -ForegroundColor Yellow
$conn = Test-NetConnection localhost -Port 1883 -WarningAction SilentlyContinue
if (-not $conn.TcpTestSucceeded) {
    Write-Host "ERROR: MQTT port 1883 not accessible!" -ForegroundColor Red
    Pop-Location
    exit 1
}
Write-Host "  MQTT port OK!" -ForegroundColor Green

# Run smoke test
Write-Host "[3/3] Running smoke_test.py..." -ForegroundColor Yellow
Write-Host ""
$smokePath = Join-Path $repoRoot "logger\tools\smoke_test.py"
python $smokePath --host 127.0.0.1
$exitCode = $LASTEXITCODE

Write-Host ""
if ($exitCode -eq 0) {
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "  SMOKE TEST: ALL PASS ✅" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
} else {
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "  SMOKE TEST: FAILED ❌ (exit $exitCode)" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
}
Write-Host ""
Pop-Location
exit $exitCode
