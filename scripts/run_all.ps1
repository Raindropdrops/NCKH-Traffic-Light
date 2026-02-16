<# 
.SYNOPSIS
    NCKH Traffic Light — One-Command Mock Test Pipeline
.DESCRIPTION
    Runs the full test pipeline without hardware:
    1) Start Docker services (Mosquitto + Node-RED)
    2) Launch mock ESP32
    3) Run smoke test (4 scenarios)
    4) Run RTT benchmark
    5) Generate timestamped report in results/
.EXAMPLE
    .\scripts\run_all.ps1
    .\scripts\run_all.ps1 -SkipDocker   # If Docker is already running
    .\scripts\run_all.ps1 -BenchCount 5  # Fewer benchmark messages
#>
param(
    [switch]$SkipDocker,
    [int]$BenchCount = 10,
    [string]$Host_ = "127.0.0.1"
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
if (-not (Test-Path "$ProjectRoot\docker-compose.yml")) {
    $ProjectRoot = Split-Path -Parent $PSScriptRoot
}
if (-not (Test-Path "$ProjectRoot\docker-compose.yml")) {
    $ProjectRoot = (Get-Location).Path
}

$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$ResultsDir = "$ProjectRoot\results\run_$Timestamp"
New-Item -ItemType Directory -Force -Path $ResultsDir | Out-Null

$LogFile = "$ResultsDir\pipeline.log"
function Log {
    param([string]$Msg)
    $line = "[$(Get-Date -Format 'HH:mm:ss')] $Msg"
    Write-Host $line
    Add-Content -Path $LogFile -Value $line
}

Log "=== NCKH Traffic Light Test Pipeline ==="
Log "Project root: $ProjectRoot"
Log "Results dir : $ResultsDir"
Log "Timestamp   : $Timestamp"
Log ""

# ──────────────────────────────────────────
# Step 1: Docker Services
# ──────────────────────────────────────────
if (-not $SkipDocker) {
    Log ">>> Step 1: Starting Docker services..."
    Push-Location $ProjectRoot
    try {
        docker compose up -d 2>&1 | Tee-Object -FilePath "$ResultsDir\docker_up.log"
        Start-Sleep -Seconds 5
        $health = docker compose ps --format json 2>$null
        Log "Docker containers started."
    }
    finally {
        Pop-Location
    }
}
else {
    Log ">>> Step 1: SKIPPED (--SkipDocker)"
}

# Wait for Mosquitto to be healthy
Log "Waiting for Mosquitto health check..."
$maxWait = 30
for ($i = 0; $i -lt $maxWait; $i++) {
    $status = docker inspect --format='{{.State.Health.Status}}' traffic-mosquitto 2>$null
    if ($status -eq "healthy") { break }
    Start-Sleep -Seconds 1
}
if ($status -ne "healthy") {
    Log "WARNING: Mosquitto not healthy after ${maxWait}s (status=$status), continuing anyway..."
}
else {
    Log "Mosquitto is healthy."
}

# ──────────────────────────────────────────
# Step 2: Launch Mock ESP32
# ──────────────────────────────────────────
Log ""
Log ">>> Step 2: Launching mock ESP32 (background)..."
$mockProcess = Start-Process -FilePath "python" `
    -ArgumentList "$ProjectRoot\logger\tools\mock_esp32.py --host $Host_" `
    -PassThru -NoNewWindow -RedirectStandardOutput "$ResultsDir\mock_esp32.log" `
    -RedirectStandardError "$ResultsDir\mock_esp32_err.log"
Log "Mock ESP32 PID: $($mockProcess.Id)"
Start-Sleep -Seconds 3

if ($mockProcess.HasExited) {
    Log "ERROR: Mock ESP32 exited early (code=$($mockProcess.ExitCode))"
    Log "Check $ResultsDir\mock_esp32_err.log"
    exit 1
}
Log "Mock ESP32 running."

# ──────────────────────────────────────────
# Step 3: Smoke Test
# ──────────────────────────────────────────
Log ""
Log ">>> Step 3: Running smoke test..."
try {
    $smokeResult = & python "$ProjectRoot\logger\tools\smoke_test.py" --host $Host_ 2>&1
    $smokeResult | Out-File -FilePath "$ResultsDir\smoke_test.log" -Encoding utf8
    $smokeResult | ForEach-Object { Log "  $_" }
    
    if ($LASTEXITCODE -eq 0) {
        Log "SMOKE TEST: PASS"
    }
    else {
        Log "SMOKE TEST: FAIL (exit code $LASTEXITCODE)"
    }
}
catch {
    Log "SMOKE TEST: ERROR - $_"
}

# ──────────────────────────────────────────
# Step 4: RTT Benchmark
# ──────────────────────────────────────────
Log ""
Log ">>> Step 4: Running RTT benchmark (count=$BenchCount)..."
try {
    $benchResult = & python "$ProjectRoot\logger\tools\run_benchmark_report.py" `
        --host $Host_ --count $BenchCount 2>&1
    $benchResult | Out-File -FilePath "$ResultsDir\benchmark.log" -Encoding utf8
    $benchResult | ForEach-Object { Log "  $_" }
    
    if ($LASTEXITCODE -eq 0) {
        Log "BENCHMARK: PASS"
    }
    else {
        Log "BENCHMARK: FAIL (exit code $LASTEXITCODE)"
    }
}
catch {
    Log "BENCHMARK: ERROR - $_"
}

# ──────────────────────────────────────────
# Step 5: Cleanup & Report
# ──────────────────────────────────────────
Log ""
Log ">>> Step 5: Cleanup..."
if (-not $mockProcess.HasExited) {
    Stop-Process -Id $mockProcess.Id -Force -ErrorAction SilentlyContinue
    Log "Mock ESP32 stopped (PID $($mockProcess.Id))."
}

# Copy any generated benchmark CSVs/reports to results
$benchOutputDir = "$ProjectRoot\results"
Get-ChildItem -Path $benchOutputDir -Filter "*.csv" -ErrorAction SilentlyContinue | 
Where-Object { $_.LastWriteTime -gt (Get-Date).AddMinutes(-10) } |
ForEach-Object { 
    Copy-Item $_.FullName "$ResultsDir\$($_.Name)" -ErrorAction SilentlyContinue
    Log "  Copied: $($_.Name)"
}
Get-ChildItem -Path $benchOutputDir -Filter "*.md" -ErrorAction SilentlyContinue | 
Where-Object { $_.LastWriteTime -gt (Get-Date).AddMinutes(-10) } |
ForEach-Object { 
    Copy-Item $_.FullName "$ResultsDir\$($_.Name)" -ErrorAction SilentlyContinue
    Log "  Copied: $($_.Name)"
}

Log ""
Log "==========================================="
Log "  PIPELINE COMPLETE"
Log "  Results: $ResultsDir"
Log "  Files:"
Get-ChildItem -Path $ResultsDir | ForEach-Object { Log "    - $($_.Name)" }
Log "==========================================="
