# 🚦 RUNBOOK — 10-Minute Quick Start

> Traffic Light MQTT Demo — Docker Setup on Windows

---

## ✅ Prerequisites Checklist

| Item                                        | Check                          |
| ------------------------------------------- | ------------------------------ | --------------------------- |
| Docker Desktop installed                    | `docker version` works         |
| Docker Desktop running (whale icon in tray) | `docker compose version` works |
| Port 1883 free                              | `netstat -an                   | findstr 1883` returns empty |
| Port 1880 free                              | `netstat -an                   | findstr 1880` returns empty |

---

## 🐳 Step 1: Install Docker Desktop (if needed)

1. Download Docker Desktop for Windows from docker.com
2. Run installer, enable WSL 2 backend
3. Restart computer if prompted
4. Start Docker Desktop (wait for whale icon to stabilize)
5. Verify:

```powershell
docker version
docker compose version
```

---

## 📁 Step 2: Navigate to Project

```powershell
cd "d:\Nam 2(D)\NCKH\traffic-mqtt-demo"
```

---

## 🔑 Step 3: Create Password File (pwfile)

```powershell
# Generate pwfile with user: demo, password: demo_pass
docker run --rm -v "${PWD}/docker/mosquitto:/mosquitto/config" eclipse-mosquitto:2 mosquitto_passwd -b -c /mosquitto/config/pwfile demo demo_pass

# Verify file was created
Get-Content docker\mosquitto\pwfile
# Should show: demo:$7$101$...
```

---

## 🚀 Step 4: Start Services

```powershell
# Start Mosquitto + Node-RED in detached mode
docker compose up -d

# Check status (both should be "running")
docker compose ps

# Expected output:
# NAME        SERVICE     STATUS
# mosquitto   mosquitto   running
# nodered     nodered     running
```

---

## 📋 Step 5: View Logs

```powershell
# Mosquitto logs (check for "Running" and no auth errors)
docker compose logs --tail=50 mosquitto

# Node-RED logs (check for "Started flows")
docker compose logs --tail=50 nodered

# Follow logs in real-time (Ctrl+C to exit)
docker compose logs -f
```

**Expected Mosquitto log:**

```
mosquitto | 1234567890: mosquitto version 2.x.x starting
mosquitto | 1234567890: Opening ipv4 listen socket on port 1883.
mosquitto | 1234567890: mosquitto version 2.x.x running
```

---

## 🧪 Step 6: Smoke Test MQTT

**Terminal 1 — Subscribe:**

```powershell
docker exec mosquitto mosquitto_sub -h localhost -u demo -P demo_pass -t "city/demo/intersection/001/#" -v
```

**Terminal 2 — Publish:**

```powershell
# Publish status (retained)
docker exec mosquitto mosquitto_pub -h localhost -u demo -P demo_pass -t "city/demo/intersection/001/status" -r -m '{"online":true,"ts_ms":1234567890}'

# Publish state
docker exec mosquitto mosquitto_pub -h localhost -u demo -P demo_pass -t "city/demo/intersection/001/state" -m '{"mode":"AUTO","phase":0,"since_ms":0,"uptime_s":1}'
```

**Expected in Terminal 1:**

```
city/demo/intersection/001/status {"online":true,"ts_ms":1234567890}
city/demo/intersection/001/state {"mode":"AUTO","phase":0,"since_ms":0,"uptime_s":1}
```

✅ **PASS** if messages appear in subscriber terminal.

---

## 🌐 Step 7: Node-RED Dashboard Setup

### 7.1 Install Dashboard Palette (REQUIRED)

```powershell
# Install node-red-dashboard inside container
docker exec nodered npm install node-red-dashboard

# Restart to load the palette
docker compose restart nodered

# Wait 10s, then verify Node-RED is back
docker compose logs --tail=10 nodered
```

### 7.2 Import Flow

1. Open browser: **<http://localhost:1880>**
2. Click Menu (☰) → **Import**
3. Click **select a file to import**
4. Navigate to: `traffic-mqtt-demo/node-red/flows.json`
5. Click **Import**
6. Click **Deploy** (top-right red button)

### 7.3 Configure MQTT Credentials

After import, if MQTT nodes show "disconnected":

1. Double-click any MQTT node (e.g., "Sub: status")
2. Click pencil icon ✏️ next to "Server"
3. Go to **Security** tab
4. Enter:
   - Username: `demo`
   - Password: `demo_pass`
5. Click **Update** → **Done** → **Deploy**

### 7.4 Access Dashboard

Open: **<http://localhost:1880/ui>**

**Dashboard Features:**

| Section     | Display                                           |
| ----------- | ------------------------------------------------- |
| **Status**  | 🟢 ONLINE / 🔴 OFFLINE                            |
| **Mode**    | 🔄 AUTO / 🎮 MANUAL / ⚠️ BLINK / ⭕ OFF           |
| **Phase**   | Current phase (NS_GREEN, EW_GREEN, ALL_RED, etc.) |
| **Control** | Buttons: AUTO, MANUAL, NS🟢, EW🟢, ALL🔴          |
| **Log**     | Command sent + ACK received + RTT                 |

### 7.5 Test Dashboard

1. Open dashboard: <http://localhost:1880/ui>
2. Click **AUTO** button
3. Check Log panel shows: `[time] SENT: SET_MODE (xxxxxxxx...)`
4. If ESP32 is connected, Log will also show: `[time] ACK: xxxxxxxx... ✅ OK | RTT: xx ms`

---

## 🔌 Step 8: Get Windows IP for ESP32

ESP32 needs to connect to the MQTT broker on your Windows machine.

```powershell
# Get IPv4 addresses
ipconfig | Select-String "IPv4"

# Or more precise (Wi-Fi/Ethernet)
(Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.InterfaceAlias -match "Wi-Fi|Ethernet"}).IPAddress
```

**Example output:** `192.168.1.100`

In `esp32/src/main.cpp`, set:

```cpp
const char* MQTT_BROKER = "192.168.1.100";  // Your IP here
```

---

## 🤖 Step 9.5: Mock ESP32 (No Hardware)

**Use this to test the system without real ESP32 hardware.**

### Terminal 1: Start Mock ESP32

```powershell
cd logger/tools
python mock_esp32.py --host 127.0.0.1 --user demo --password demo_pass
```

**Expected output:**

```text
🤖 MOCK ESP32 TRAFFIC LIGHT CONTROLLER
✅ Connected to MQTT broker
📥 Subscribed to: city/demo/intersection/001/cmd
📤 Published status: online=True
✅ Mock ESP32 running. Press Ctrl+C to stop.
```

### Terminal 2: Run Smoke Test

```powershell
cd logger/tools
python smoke_test.py --host 127.0.0.1
```

**Expected output:**

```text
🎉 ALL TESTS PASSED
```

### Quick E2E Flow (3 Commands)

```powershell
# 1. Start Docker
docker compose up -d

# 2. Start Mock ESP32 (keep running)
python logger/tools/mock_esp32.py --host 127.0.0.1

# 3. In new terminal: Run smoke test
python logger/tools/smoke_test.py --host 127.0.0.1
```

### Options

| Argument             | Description                        |
| -------------------- | ---------------------------------- |
| `--ack_delay_ms 50`  | Add delay before ack (RTT testing) |
| `--city demo`        | City ID for topic                  |
| `--intersection 001` | Intersection ID                    |

---

## 🛡️ Step 9: Firewall (if ESP32 can't connect)

```powershell
# Allow inbound TCP 1883 (run as Administrator)
New-NetFirewallRule -DisplayName "MQTT Broker" -Direction Inbound -Protocol TCP -LocalPort 1883 -Action Allow
```

---

## 📊 Step 10: RTT Benchmark Report (1 Command)

Generate comprehensive RTT benchmark report with plots and analysis.

### Quick Usage

```powershell
# Ensure mock/ESP32 is running, then:
cd logger/tools
python run_benchmark_report.py --host 127.0.0.1
```

### Output Structure

```text
results/bench_YYYYMMDD_HHMM/
├── raw/
│   ├── case_0b.csv
│   ├── case_256b.csv
│   └── case_1024b.csv
├── plots/
│   ├── histogram_case_1.png
│   ├── histogram_case_2.png
│   ├── comparison_chart.png
│   └── ecdf_comparison.png
├── summary.csv
└── report.md          # Vietnamese report for thesis/slides
```

### Options

| Argument        | Default      | Description               |
| --------------- | ------------ | ------------------------- |
| `--host`        | 127.0.0.1    | MQTT broker               |
| `--count`       | 500          | Commands per case         |
| `--interval_ms` | 200          | Interval between commands |
| `--cases`       | "0,256,1024" | Payload sizes to test     |
| `--outdir`      | auto         | Output directory          |

### Example: Full Benchmark

```powershell
python run_benchmark_report.py --host 127.0.0.1 --count 500 --interval_ms 200 --cases "0,256,512,1024"
```

```powershell
# Allow inbound TCP 1883 (run as Administrator)
New-NetFirewallRule -DisplayName "MQTT Broker" -Direction Inbound -Protocol TCP -LocalPort 1883 -Action Allow
```

---

## 🔄 Common Operations

| Action                    | Command                                          |
| ------------------------- | ------------------------------------------------ |
| **Start**                 | `docker compose up -d`                           |
| **Stop**                  | `docker compose down`                            |
| **Restart**               | `docker compose restart`                         |
| **View logs**             | `docker compose logs -f`                         |
| **Status**                | `docker compose ps`                              |
| **Full reset**            | `docker compose down -v && docker compose up -d` |
| **Enter Mosquitto shell** | `docker exec -it mosquitto sh`                   |
| **Enter Node-RED shell**  | `docker exec -it nodered bash`                   |

---

## 🐛 Troubleshooting

### Docker not found

```
Error: 'docker' is not recognized
```

→ Docker Desktop not installed or not in PATH. Restart terminal after installing.

### Docker daemon not running

```
Error: Cannot connect to the Docker daemon
```

→ Start Docker Desktop (whale icon in system tray).

### Auth failed

```
mosquitto: Connection refused: not authorised
```

→ pwfile not created or wrong password. Recreate pwfile (Step 3).

### Port already in use

```
Error: bind: address already in use
```

→ Stop other services using port 1883/1880:

```powershell
netstat -ano | findstr :1883
taskkill /PID <PID> /F
```

### ACL denied

```
mosquitto: Denied PUBLISH to "topic"
```

→ Check `docker/mosquitto/aclfile` topic patterns.

---

## 📊 Status Summary

After completing all steps, verify:

| Check               | Expected         | Command                         |
| ------------------- | ---------------- | ------------------------------- |
| Containers running  | 2 running        | `docker compose ps`             |
| Mosquitto listening | port 1883        | `docker compose logs mosquitto` |
| Node-RED listening  | port 1880        | `docker compose logs nodered`   |
| MQTT auth works     | message received | Smoke test (Step 6)             |
| Browser access      | editor loads     | <http://localhost:1880>         |

**PASS** = All 5 checks pass  
**FAIL** = Any check fails → see Troubleshooting

## 🔬 Step 10: RTT Benchmark (Research)

### 10.1 Setup Python Environment

```powershell
cd logger
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 10.2 Run Benchmark Examples

```powershell
cd tools

# Example 1: Basic 100 commands (SET_MODE AUTO)
python logger.py --host 192.168.1.100 --count 100 --mode AUTO --out test_auto.csv

# Example 2: 500 commands with faster interval
python logger.py --host 192.168.1.100 --count 500 --mode MANUAL --interval_ms 50 --out test_500.csv

# Example 3: 1000 commands with payload padding (stress test)
python logger.py --host 192.168.1.100 --count 1000 --mode AUTO --pad_bytes 200 --out test_padded.csv
```

### 10.3 Analyze Results

```powershell
# Basic analysis
python analyze_results.py test_auto.csv

# With histogram
python analyze_results.py test_500.csv --histogram

# Custom thresholds
python analyze_results.py test_padded.csv --threshold-mean 200 --threshold-p95 500 --threshold-loss 1.0
```

### 10.4 Expected Output

```
📊 RTT BENCHMARK ANALYSIS RESULTS
============================================================
📈 DELIVERY STATISTICS
  Total Sent:            500
  Total Received:        498
  Total Lost:              2
  Loss Rate:            0.40%

📏 RTT DISTRIBUTION (ms)
  Min:             45.00
  Max:            312.50
  Mean:            85.30
  Median:          72.10
  P95:            156.80

✅ THRESHOLD VALIDATION
  Mean <= 200ms:    ✅ PASS (85.30ms)
  P95 <= 500ms:     ✅ PASS (156.80ms)
  Loss <= 1%:       ✅ PASS (0.40%)
============================================================
🎉 OVERALL: ALL THRESHOLDS PASSED
```

---

## 🎯 Demo Rehearsal Checklist (10 bước)

> **Checklist cho hôm thuyết trình NCKH — Làm theo từng bước**

### Trước Demo (T-30 phút)

| #   | Bước                   | Command/Action                       | Check                         |
| --- | ---------------------- | ------------------------------------ | ----------------------------- |
| 1   | **Bật Docker Desktop** | Double-click Docker icon             | ⬜ Whale icon xanh            |
| 2   | **Start containers**   | `docker compose up -d`               | ⬜ mosquitto, nodered Running |
| 3   | **Verify ports**       | `netstat -an \| findstr "1883 1880"` | ⬜ LISTENING                  |
| 4   | **Flash ESP32**        | PlatformIO > Upload (nếu chưa flash) | ⬜ LED nhấp nháy = booting    |

### Demo Live (T-0)

| #   | Bước                     | Command/Action                      | Check                         |
| --- | ------------------------ | ----------------------------------- | ----------------------------- |
| 5   | **Mở Node-RED**          | Browser: `http://localhost:1880/ui` | ⬜ Dashboard hiện Status      |
| 6   | **Verify ESP32 ONLINE**  | Node-RED shows "ONLINE"             | ⬜ Status = ONLINE            |
| 7   | **Demo SET_MODE MANUAL** | Node-RED > Mode dropdown > MANUAL   | ⬜ Ack received, LED thay đổi |
| 8   | **Demo SET_PHASE**       | Node-RED > Phase buttons            | ⬜ NS_GREEN or EW_GREEN       |
| 9   | **Demo SET_MODE AUTO**   | Node-RED > Mode dropdown > AUTO     | ⬜ FSM chạy tự động           |
| 10  | **Show RTT metrics**     | Node-RED RTT display hoặc logger    | ⬜ RTT ~50-100ms              |

### Backup Plan (Nếu ESP32 lỗi)

```powershell
# Terminal 1: Start mock ESP32
cd logger/tools
python mock_esp32.py --host 127.0.0.1

# Terminal 2: Verify with smoke test
python smoke_test.py --host 127.0.0.1
```

### Demo Script (Nói kèm)

1. **"Đây là hệ thống giám sát đèn giao thông qua MQTT..."**
2. **"ESP32 đang ở chế độ AUTO, FSM tự chuyển phase..."**
3. **"Chuyển sang MANUAL để điều khiển thủ công từ Dashboard..."**
4. **"SET_PHASE NS_GREEN — đèn NS chuyển xanh, EW đỏ..."**
5. **"RTT command→ack khoảng 50-80ms qua WiFi..."**

### Quick Troubleshoot

| Vấn đề                     | Giải pháp                                     |
| -------------------------- | --------------------------------------------- |
| ESP32 không connect        | Check WiFi credentials trong `config.h`       |
| Node-RED không hiện status | Refresh page, check MQTT broker               |
| Containers không start     | `docker compose down && docker compose up -d` |
| Port conflict              | Stop other apps using 1883/1880               |

---

## 🔌 Flash ESP32 (ESP-IDF) + Demo 4 Hướng

> Firmware ESP-IDF điều khiển 4 module LED (N, S, E, W)

### Prerequisites

| Tool            | Version           |
| --------------- | ----------------- |
| ESP-IDF         | 5.0+              |
| ESP32 DevKit V1 | Connected via USB |

### Build & Flash

```powershell
# 1. Open ESP-IDF terminal
# Start Menu → "ESP-IDF 5.x CMD"

# 2. Navigate to project
cd "D:\Nam 2(D)\NCKH\traffic-mqtt-demo\esp32_idf"

# 3. Configure (menuconfig)
idf.py menuconfig
# → Traffic Light Configuration
# → WiFi: Set SSID, Password
# → MQTT: Set Broker Host (PC IP), Port, User, Pass

# 4. Build
idf.py build

# 5. Flash (replace COM3 with your port)
idf.py -p COM3 flash

# 6. Monitor
idf.py -p COM3 monitor
```

### Verify MQTT Connection

```powershell
# Terminal 1: Subscribe to all topics
docker exec -it mosquitto mosquitto_sub -t "city/demo/intersection/001/#" -u demo -P demo_pass -v

# Expected output:
# city/demo/intersection/001/status {"online":true,"ts_ms":...}
# city/demo/intersection/001/state {"mode":"AUTO","phase":0,"ts_ms":...}
# city/demo/intersection/001/telemetry {"rssi_dbm":-50,"heap_free_kb":200,...}
```

### Test Commands

```powershell
# SET_MODE MANUAL
docker exec -it mosquitto mosquitto_pub -t "city/demo/intersection/001/cmd" -u demo -P demo_pass -m '{"cmd_id":"test-001","type":"SET_MODE","mode":"MANUAL","ts_ms":1234567890}'

# SET_PHASE (NS_GREEN = 0, EW_GREEN = 3)
docker exec -it mosquitto mosquitto_pub -t "city/demo/intersection/001/cmd" -u demo -P demo_pass -m '{"cmd_id":"test-002","type":"SET_PHASE","phase":3,"ts_ms":1234567890}'
```

### Smoke Test

```powershell
cd logger/tools
python smoke_test.py --host 127.0.0.1
# Expected: Exit code 0 (PASS)
```

### Physical LED Verification

| Phase        | North | South | East | West |
| ------------ | ----- | ----- | ---- | ---- |
| 0: NS_GREEN  | 🟢    | 🟢    | 🔴   | 🔴   |
| 1: NS_YELLOW | 🟡    | 🟡    | 🔴   | 🔴   |
| 2: ALL_RED   | 🔴    | 🔴    | 🔴   | 🔴   |
| 3: EW_GREEN  | 🔴    | 🔴    | 🟢   | 🟢   |
| 4: EW_YELLOW | 🔴    | 🔴    | 🟡   | 🟡   |
| 5: ALL_RED   | 🔴    | 🔴    | 🔴   | 🔴   |

---

## 🔴 Node-RED UI Demo

> Dashboard trực quan điều khiển đèn giao thông

### Import Flows

```powershell
# 1. Verify containers running
docker compose up -d
docker compose ps

# 2. Import flows (Method A: Copy)
# - Mở http://localhost:1880
# - Menu (☰) → Import
# - Paste nội dung từ node-red/flows.json
# - Click Import → Deploy
```

### Open Dashboard

```
http://localhost:1880/ui
```

### Dashboard Features

| Group        | Elements                                            |
| ------------ | --------------------------------------------------- |
| 🎮 Control   | AUTO, MANUAL, NS GO, EW GO buttons + Phase dropdown |
| 📊 Status    | Online, Mode, Phase, Uptime                         |
| 📡 Telemetry | RSSI, Heap, Uptime                                  |
| 📋 ACK Log   | Recent 20 command acknowledgements                  |

### Test with Mock ESP32

```powershell
# Terminal 1: Start mock
cd logger/tools
python mock_esp32.py --host 127.0.0.1

# Terminal 2: Open dashboard
# http://localhost:1880/ui
# Click AUTO/MANUAL/NS GO/EW GO
# Verify ACK log updates
```

### Test with smoke_test

```powershell
cd logger/tools
python smoke_test.py --host 127.0.0.1
# Expected: Exit code 0 (PASS)
# Dashboard should show state updates
```

---

## 📚 References

- [SPEC.md](SPEC.md) — Topic tree & payload schemas
- [QA_CHECKLIST.md](QA_CHECKLIST.md) — Full test checklist
- [README.md](README.md) — Project overview
- [docs/WIRING.md](docs/WIRING.md) — 4-module wiring guide
- [esp32_idf/README_ESP_IDF.md](esp32_idf/README_ESP_IDF.md) — ESP-IDF build guide
- [node-red/NODERED_GUIDE.md](node-red/NODERED_GUIDE.md) — Dashboard import guide
