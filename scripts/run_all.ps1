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

# Ensure Python subprocess output is UTF-8 (Windows default cp1252 chokes on emoji)
$env:PYTHONIOENCODING = "utf-8"

# ──────────────────────────────────────────
# Step 1: Docker Services
# ──────────────────────────────────────────
if (-not $SkipDocker) {
    Log ">>> Step 1: Starting Docker services..."
    Push-Location $ProjectRoot
    try {
        # docker compose writes progress to stderr — suppress PS terminating errors
        $ErrorActionPreference = "Continue"
        docker compose up -d 2>&1 | Out-File -FilePath "$ResultsDir\docker_up.log" -Encoding utf8
        $dockerExit = $LASTEXITCODE
        $ErrorActionPreference = "Stop"

        if ($dockerExit -ne 0) {
            Log "ERROR: docker compose up failed (exit code $dockerExit). See docker_up.log"
            Get-Content "$ResultsDir\docker_up.log" | ForEach-Object { Log "  $_" }
            exit 1
        }

        Start-Sleep -Seconds 5
        Log "Docker containers started."
    }
    finally {
        Pop-Location
    }
}
else {
    Log ">>> Step 1: SKIPPED (--SkipDocker)"
}

# Wait for Mosquitto readiness
Log "Waiting for Mosquitto readiness..."
$maxWait = 30
$serviceName = "mosquitto"
$status = $null
$usedHealthcheck = $false

# Prefer service status from docker compose ps to avoid depending on container_name.
for ($i = 0; $i -lt $maxWait; $i++) {
    $serviceStatus = docker compose ps $serviceName --format json 2>$null
    if ($serviceStatus) {
        try {
            $serviceObj = $serviceStatus | ConvertFrom-Json
            if ($serviceObj -is [System.Array]) {
                $serviceObj = $serviceObj | Select-Object -First 1
            }

            if ($null -ne $serviceObj) {
                $statusField = "$($serviceObj.Status)"
                if ($statusField -match '\(healthy\)') {
                    $status = "healthy"
                    $usedHealthcheck = $true
                    break
                }
                if ($statusField -match '\(unhealthy\)') {
                    $status = "unhealthy"
                    $usedHealthcheck = $true
                }
                elseif ($statusField -match '^Up') {
                    $status = "no-healthcheck"
                }
            }
        }
        catch {
            # Ignore transient parse errors and keep polling.
        }
    }
    Start-Sleep -Seconds 1
}

if ($usedHealthcheck -and $status -eq "healthy") {
    Log "Mosquitto is healthy (branch=healthcheck, source=docker compose ps)."
}
elseif ($usedHealthcheck) {
    Log "WARNING: Mosquitto healthcheck did not become healthy after ${maxWait}s (status=$status, branch=healthcheck, source=docker compose ps)."
}
else {
    Log "Healthcheck status unavailable (branch=fallback). Probing broker with mosquitto_sub via docker exec..."
    $probeOutput = docker exec mosquitto mosquitto_sub -h localhost -u demo -P demo_pass -t '$SYS/broker/version' -C 1 -W 3 2>&1
    if ($LASTEXITCODE -eq 0) {
        Log "Mosquitto fallback probe succeeded (branch=fallback, method=mosquitto_sub, topic=`$SYS/broker/version)."
    }
    else {
        Log "WARNING: Mosquitto fallback probe failed (branch=fallback, method=mosquitto_sub, exit=$LASTEXITCODE)."
        if ($probeOutput) {
            ($probeOutput | Out-String).Trim().Split([Environment]::NewLine) | ForEach-Object { Log "  $_" }
        }
    }
}

# ──────────────────────────────────────────
# Step 2: Launch Mock ESP32
# ──────────────────────────────────────────
Log ""
Log ">>> Step 2: Launching mock ESP32 (background)..."
$mockScript = "$ProjectRoot\logger\tools\mock_esp32.py"
$mockProcess = Start-Process -FilePath "python" `
    -ArgumentList "`"$mockScript`"", "--host", $Host_ `
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
    $smokeScript = "$ProjectRoot\logger\tools\smoke_test.py"
    $smokeResult = & python $smokeScript --host $Host_ 2>&1
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
# Note: $benchOutDir is consumed in Step 5 below (PSScriptAnalyzer can't track across try/catch)
$benchOutDir = $null
try {
    $benchScript = "$ProjectRoot\logger\tools\run_benchmark_report.py"
    $benchRawOutput = & python $benchScript `
        --host $Host_ --count $BenchCount 2>&1
    $benchRawOutput | Out-File -FilePath "$ResultsDir\benchmark.log" -Encoding utf8
    $benchRawOutput | ForEach-Object { Log "  $_" }
    
    # Parse benchmark output for result directory
    foreach ($line in $benchRawOutput) {
        if ($line -match '(results[\\/]bench_[\w-]+)') {
            $benchOutDir = Join-Path $ProjectRoot $Matches[1]
        }
    }
    
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
Log ">>> Step 5: Cleanup & collect artifacts..."
if (-not $mockProcess.HasExited) {
    Stop-Process -Id $mockProcess.Id -Force -ErrorAction SilentlyContinue
    Log "Mock ESP32 stopped (PID $($mockProcess.Id))."
}

# Collect benchmark artifacts from bench_* directories
$benchOutputDir = "$ProjectRoot\results"

# If benchmark printed a specific outdir, use it; otherwise find latest bench_*
if (-not $benchOutDir) {
    $benchOutDir = Get-ChildItem -Path $benchOutputDir -Directory -Filter "bench_*" -ErrorAction SilentlyContinue |
    Sort-Object LastWriteTime -Descending | Select-Object -First 1 -ExpandProperty FullName
}

if ($benchOutDir -and (Test-Path $benchOutDir)) {
    Log "Collecting benchmark artifacts from: $benchOutDir"
    $artifactsDir = "$ResultsDir\benchmark_artifacts"
    New-Item -ItemType Directory -Force -Path $artifactsDir | Out-Null

    # Copy summary.csv, report.md
    @("summary.csv", "report.md") | ForEach-Object {
        $src = Join-Path $benchOutDir $_
        if (Test-Path $src) {
            Copy-Item $src "$artifactsDir\$_" -ErrorAction SilentlyContinue
            Log "  Copied: $_"
        }
    }

    # Copy raw/ directory
    $rawDir = Join-Path $benchOutDir "raw"
    if (Test-Path $rawDir) {
        Copy-Item $rawDir "$artifactsDir\raw" -Recurse -ErrorAction SilentlyContinue
        $rawCount = (Get-ChildItem "$artifactsDir\raw" -File -ErrorAction SilentlyContinue).Count
        Log "  Copied: raw/ ($rawCount files)"
    }

    # Copy plots/ directory
    $plotsDir = Join-Path $benchOutDir "plots"
    if (Test-Path $plotsDir) {
        Copy-Item $plotsDir "$artifactsDir\plots" -Recurse -ErrorAction SilentlyContinue
        $plotCount = (Get-ChildItem "$artifactsDir\plots" -File -ErrorAction SilentlyContinue).Count
        Log "  Copied: plots/ ($plotCount files)"
    }
}
else {
    Log "NOTE: No benchmark output directory found (bench_* not created or benchmark skipped)."
}

# Also copy any loose recent CSV/MD from results/ root
Get-ChildItem -Path $benchOutputDir -File -ErrorAction SilentlyContinue |
Where-Object { $_.Extension -in '.csv', '.md' -and $_.LastWriteTime -gt (Get-Date).AddMinutes(-10) } |
ForEach-Object {
    Copy-Item $_.FullName "$ResultsDir\$($_.Name)" -ErrorAction SilentlyContinue
    Log "  Copied (root): $($_.Name)"
}

Log ""
Log "==========================================="
Log "  PIPELINE COMPLETE"
Log "  Results: $ResultsDir"
Log "  Files:"
Get-ChildItem -Path $ResultsDir -Recurse -File | ForEach-Object {
    $rel = $_.FullName.Replace($ResultsDir, '').TrimStart('\', '/') 
    Log "    - $rel"
}
Log "==========================================="
