# 🚦 Traffic Light MQTT Demo

> IoT–MQTT Traffic Light Monitoring & Control System
> **Đề tài NCKH** | Scope: ESP32 (Scope 1)

## 📋 Requirements

| Tool               | Version | Install                                                                |
| ------------------ | ------- | ---------------------------------------------------------------------- |
| **Docker Desktop** | 4.x+    | [Download](https://www.docker.com/products/docker-desktop)             |
| **PlatformIO**     | 6.x+    | [VS Code Extension](https://platformio.org/install/ide?install=vscode) |
| **Python**         | 3.11+   | [Download](https://www.python.org/downloads/)                          |

## 🚀 Quick Start

### 1. Tạo Password File (pwfile)

> ⚠️ **BẮT BUỘC** trước khi chạy docker compose

```powershell
# Chạy từ thư mục traffic-mqtt-demo/
cd "d:\Nam 2(D)\NCKH\traffic-mqtt-demo"

# Tạo pwfile với user từ .env (mặc định: demo / demo_pass)
# Chạy container tạm để generate password hash
docker run --rm -it -v "${PWD}/docker/mosquitto:/mosquitto/config" eclipse-mosquitto:2 mosquitto_passwd -c /mosquitto/config/pwfile demo

# Nhập password khi được hỏi (ví dụ: demo_pass)
# File pwfile sẽ được tạo tại docker/mosquitto/pwfile
```

**Hoặc** tạo không cần nhập interactive:

```powershell
# Sử dụng biến môi trường từ .env
$env:MOSQUITTO_PASS = "demo_pass"
docker run --rm -v "${PWD}/docker/mosquitto:/mosquitto/config" eclipse-mosquitto:2 mosquitto_passwd -b /mosquitto/config/pwfile demo $env:MOSQUITTO_PASS
```

### 2. Start Docker Services

```powershell
# Start Mosquitto broker + Node-RED
docker compose up -d

# Verify containers are running
docker compose ps

# Xem logs Mosquitto
docker compose logs mosquitto
```

**Ports:**

| Service            | Port    | URL                        |
| ------------------ | ------- | -------------------------- |
| MQTT Broker        | 1883    | `mqtt://localhost:1883`    |
| Node-RED           | 1880    | <http://localhost:1880>    |
| Node-RED Dashboard | 1880/ui | <http://localhost:1880/ui> |

### 3. Kiểm Tra Broker (Smoke Test)

```powershell
# Terminal 1: Subscribe (chạy trong container)
docker exec mosquitto mosquitto_sub -h localhost -u demo -P demo_pass -t "city/demo/intersection/001/#" -v

# Terminal 2: Publish test message
docker exec mosquitto mosquitto_pub -h localhost -u demo -P demo_pass -t "city/demo/intersection/001/state" -m '{"mode":"AUTO","phase":0,"since_ms":0,"uptime_s":1,"ts_ms":1234567890}'

# Kỳ vọng: Terminal 1 hiện message vừa publish
```

**Test từng topic theo SPEC:**

```powershell
# Test state topic
docker exec mosquitto mosquitto_pub -h localhost -u demo -P demo_pass -t "city/demo/intersection/001/state" -m '{"mode":"AUTO","phase":0}'

# Test cmd topic
docker exec mosquitto mosquitto_pub -h localhost -u demo -P demo_pass -t "city/demo/intersection/001/cmd" -m '{"cmd_id":"test-001","type":"SET_MODE","mode":"MANUAL"}'

# Test status topic (retained)
docker exec mosquitto mosquitto_pub -h localhost -u demo -P demo_pass -t "city/demo/intersection/001/status" -m '{"online":true}' -r

# Verify retained message
docker exec mosquitto mosquitto_sub -h localhost -u demo -P demo_pass -t "city/demo/intersection/001/status" -C 1 -v
```

**Test ACL (phải fail):**

```powershell
# Test publish to topic không được phép (sẽ không nhận)
docker exec mosquitto mosquitto_pub -h localhost -u demo -P demo_pass -t "unauthorized/topic" -m "test"

# Test với sai password (sẽ lỗi connection)
docker exec mosquitto mosquitto_pub -h localhost -u demo -P wrong_pass -t "city/demo/intersection/001/state" -m "test"
```

### 4. Get Your Windows IP (for ESP32)

```powershell
# Option 1: PowerShell
(Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.InterfaceAlias -like "*Wi-Fi*" -or $_.InterfaceAlias -like "*Ethernet*"}).IPAddress

# Option 2: Command Prompt
ipconfig | findstr /i "IPv4"
```

📝 **Note:** Use this IP as `MQTT_BROKER` in `esp32/src/main.cpp`

### 5. Flash ESP32

```powershell
cd esp32

# Edit src/main.cpp:
# - Set WIFI_SSID
# - Set WIFI_PASS
# - Set MQTT_BROKER to your Windows IP
# - Set MQTT_USER = "demo"
# - Set MQTT_PASS = "demo_pass"

# Build and upload
pio run --target upload

# Monitor serial output
pio device monitor
```

### 6. Import Node-RED Flow

1. Open <http://localhost:1880>
2. Menu (☰) → Import
3. Select file: `node-red/flows.json`
4. Click Import → Deploy

**Configure MQTT in Node-RED:**

- Server: `mosquitto` (container name, not localhost!)
- Port: `1883`
- Username: `demo`
- Password: `demo_pass`

### 7. Access Dashboard

Open <http://localhost:1880/ui>

---

## ⚡ End-to-End in 15 Minutes

**Mục tiêu:** Chạy toàn bộ hệ thống và verify hoạt động.

### Step 1: Start Docker Services (2 min)

```powershell
cd "d:\Nam 2(D)\NCKH\traffic-mqtt-demo"

# Generate pwfile (nếu chưa có)
docker run --rm -v "${PWD}/docker/mosquitto:/mosquitto/config" eclipse-mosquitto:2 mosquitto_passwd -b /mosquitto/config/pwfile demo demo_pass

# Start services
docker compose up -d
docker compose ps  # Verify: 2 containers running
```

### Step 2: Flash ESP32 (5 min)

```powershell
cd esp32

# Edit src/main.cpp:
# - WIFI_SSID = "your_wifi"
# - WIFI_PASS = "your_password"
# - MQTT_HOST = "192.168.x.x"  # Your Windows IP

pio run --target upload
pio device monitor  # Should see: "Connected to MQTT"
```

### Step 3: Import Node-RED Flow (2 min)

1. Open <http://localhost:1880>
2. Menu (☰) → Import → Select: `node-red/flows.json`
3. Deploy

### Step 4: Run Smoke Test (1 min)

```powershell
cd logger/tools
pip install -r ../requirements.txt  # Once only

# Run automated smoke test
python smoke_test.py --host 192.168.x.x

# Expected:
# 🎉 ALL TESTS PASSED
```

### Step 5: Open Dashboard & Control (1 min)

1. Open <http://localhost:1880/ui>
2. Verify: Status = ONLINE, Mode = AUTO
3. Click MANUAL → Phase buttons work
4. Click AUTO → Return to auto cycle

### ✅ Success Criteria

| Check             | Expected         |
| ----------------- | ---------------- |
| Docker containers | 2 running        |
| ESP32 serial      | "MQTT connected" |
| smoke_test.py     | Exit code 0      |
| Dashboard         | Status = ONLINE  |

---

## 📁 Project Structure

```
traffic-mqtt-demo/
├── docker/
│   ├── mosquitto/
│   │   ├── mosquitto.conf    # Broker config
│   │   ├── aclfile           # Access control
│   │   ├── pwfile            # Password file (generated)
│   │   ├── data/             # Persistence
│   │   └── log/              # Logs
│   └── nodered/
│       └── data/             # Node-RED data
├── esp32/
│   ├── platformio.ini
│   └── src/main.cpp
├── logger/
│   ├── tools/
│   │   ├── bench_rtt.py
│   │   └── analyze_results.py
│   └── requirements.txt
├── node-red/
│   └── flows.json
├── docs/
│   ├── API.md
│   ├── WIRING.md
│   ├── USER_MANUAL.md
│   └── DEPLOYMENT.md
├── docker-compose.yml
├── .env.example
├── SPEC.md                   # 🔒 Locked specification
├── BACKLOG.md
├── QA_CHECKLIST.md
└── README.md
```

---

## 🔐 Authentication Design

**Single user approach:**

- User `demo` dùng chung cho ESP32 và Node-RED
- Đơn giản cho demo/development
- Production: tạo separate users với restricted ACLs

**ACL Rules (xem `docker/mosquitto/aclfile`):**

| User | Topic Pattern                     | Permission |
| ---- | --------------------------------- | ---------- |
| demo | `city/+/intersection/+/state`     | read/write |
| demo | `city/+/intersection/+/telemetry` | read/write |
| demo | `city/+/intersection/+/cmd`       | read/write |
| demo | `city/+/intersection/+/ack`       | read/write |
| demo | `city/+/intersection/+/status`    | read/write |
| demo | `$SYS/#`                          | read       |

---

## 🛠 Troubleshooting

### Docker Issues

```powershell
# Xem logs chi tiết
docker compose logs -f mosquitto

# Restart services
docker compose restart

# Full reset
docker compose down -v
docker compose up -d
```

### Mosquitto Auth Errors

```
# Log: "Connection refused: not authorised"
# → Sai username/password hoặc pwfile chưa tạo đúng

# Verify pwfile exists and has content
type docker\mosquitto\pwfile
```

### ACL Denied

```
# Log: "Denied PUBLISH/SUBSCRIBE"
# → Topic không match ACL rules
# → Kiểm tra aclfile syntax
```

---

## 📚 Documentation

| Document                           | Description                        |
| ---------------------------------- | ---------------------------------- |
| [SPEC.md](SPEC.md)                 | 🔒 Locked technical specification  |
| [BACKLOG.md](BACKLOG.md)           | Work breakdown structure (WP0-WP6) |
| [QA_CHECKLIST.md](QA_CHECKLIST.md) | End-to-end smoke test checklist    |
| [docs/API.md](docs/API.md)         | MQTT API documentation             |
| [docs/WIRING.md](docs/WIRING.md)   | Hardware wiring guide              |

---

## 📄 License

Academic project - NCKH 2026
