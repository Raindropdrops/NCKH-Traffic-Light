# 🔌 ESP32 FIRMWARE GUIDE

> Hướng dẫn cấu hình, build và test firmware ESP32 cho traffic-mqtt-demo

---

## 1. Tổng Quan Firmware

### 1.1 Chức Năng Chính

| Chức năng        | Mô tả                                          |
| ---------------- | ---------------------------------------------- |
| **WiFi**         | Kết nối Access Point                           |
| **MQTT Client**  | Connect broker, subscribe/publish              |
| **FSM**          | Finite State Machine: AUTO, MANUAL, BLINK, OFF |
| **GPIO Control** | Điều khiển LED R/Y/G cho NS và EW              |
| **Safety Rules** | ALL_RED, single-green enforcement              |

### 1.2 Message Flow

```
                    ┌──────────────────────────────────────┐
                    │           ESP32 Firmware             │
                    │                                      │
    cmd ──────────► │ ┌──────────┐   ┌──────────┐         │
   (MQTT)           │ │  Parser  │──►│   FSM    │         │
                    │ └──────────┘   └────┬─────┘         │
                    │                     │               │
                    │              ┌──────▼──────┐        │
                    │              │    GPIO     │───────►│──► LEDs
                    │              │   Control   │        │
                    │              └──────┬──────┘        │
                    │                     │               │
    ◄────────────── │ ┌──────────┐   ┌────▼─────┐        │
   ack/state        │ │ Publisher│◄──│  State   │        │
   (MQTT)           │ └──────────┘   └──────────┘        │
                    └──────────────────────────────────────┘
```

---

## 2. Cấu Hình

### 2.1 Tạo File Config

```powershell
cd esp32/src
copy config.example.h config.h
```

### 2.2 Chỉnh Biến Trong `config.h`

```cpp
// ===== WiFi Configuration =====
#define WIFI_SSID     "YourWiFiSSID"
#define WIFI_PASS     "YourWiFiPassword"

// ===== MQTT Broker =====
#define MQTT_HOST     "192.168.1.100"  // IP của PC chạy Docker
#define MQTT_PORT     1883
#define MQTT_USER     "demo"
#define MQTT_PASS     "demo_pass"

// ===== Topic Configuration =====
#define CITY_ID       "demo"
#define INTERSECTION  "001"

// ===== GPIO Pins (match SPEC.md Section 10) =====
#define PIN_NS_RED    16
#define PIN_NS_YELLOW 17
#define PIN_NS_GREEN  18
#define PIN_EW_RED    19
#define PIN_EW_YELLOW 21
#define PIN_EW_GREEN  22
```

### 2.3 Tìm IP PC

```powershell
# Windows
ipconfig | findstr "IPv4"

# Hoặc dùng hostname
ping -4 hostname
```

---

## 3. Build & Upload

### 3.1 Yêu Cầu

| Tool        | Version   |
| ----------- | --------- |
| PlatformIO  | Latest    |
| VS Code     | Latest    |
| ESP32 Board | DevKit V1 |

### 3.2 Build

```powershell
cd esp32
pio run
```

### 3.3 Upload

```powershell
pio run --target upload
```

### 3.4 Monitor Serial

```powershell
pio device monitor --baud 115200
```

---

## 4. Firmware Logic

### 4.1 FSM Modes

| Mode     | Behavior                         |
| -------- | -------------------------------- |
| `AUTO`   | Tự động chuyển phase theo timing |
| `MANUAL` | Chờ lệnh SET_PHASE từ dashboard  |
| `BLINK`  | Đèn vàng nhấp nháy (cảnh báo)    |
| `OFF`    | Tất cả LED tắt                   |

### 4.2 Phase Definitions

| Phase        | NS LEDs | EW LEDs | Duration (AUTO) |
| ------------ | ------- | ------- | --------------- |
| 0: NS_GREEN  | 🟢⚫⚫  | ⚫⚫🔴  | 30s             |
| 1: NS_YELLOW | ⚫🟡⚫  | ⚫⚫🔴  | 3s              |
| 2: ALL_RED   | ⚫⚫🔴  | ⚫⚫🔴  | 2s              |
| 3: EW_GREEN  | ⚫⚫🔴  | 🟢⚫⚫  | 30s             |
| 4: EW_YELLOW | ⚫⚫🔴  | ⚫🟡⚫  | 3s              |
| 5: ALL_RED   | ⚫⚫🔴  | ⚫⚫🔴  | 2s              |

### 4.3 Safety Rules

```cpp
// Rule 1: Không bao giờ 2 hướng cùng xanh
if (ns_green && ew_green) {
    emergency_all_red();
}

// Rule 2: ALL_RED giữa mỗi phase transition
if (phase_changing) {
    set_all_red();
    delay(2000);
}
```

---

## 5. MQTT Messages

### 5.1 Subscribe

| Topic     | Purpose                    |
| --------- | -------------------------- |
| `.../cmd` | Nhận commands từ dashboard |

### 5.2 Publish

| Topic           | Frequency      | Purpose         |
| --------------- | -------------- | --------------- |
| `.../ack`       | Per command    | Acknowledgement |
| `.../state`     | 1 Hz           | Current state   |
| `.../status`    | On connect/LWT | Online/Offline  |
| `.../telemetry` | 0.2 Hz         | Metrics         |

### 5.3 Command Schema

```json
{
  "cmd_id": "uuid-v4",
  "type": "SET_MODE",
  "mode": "MANUAL",
  "ts_ms": 1234567890
}
```

### 5.4 Ack Schema

```json
{
  "cmd_id": "uuid-v4",
  "ok": true,
  "ts_ms": 1234567890
}
```

---

## 6. Test Cases

### 6.1 Connectivity Tests

| Test         | Command         | Expected                              |
| ------------ | --------------- | ------------------------------------- |
| WiFi Connect | Power on        | Serial: "WiFi connected, IP: x.x.x.x" |
| MQTT Connect | After WiFi      | Serial: "MQTT connected"              |
| LWT          | Power off ESP32 | Dashboard shows "OFFLINE"             |

### 6.2 Command Tests

| Test               | Action             | Expected                  |
| ------------------ | ------------------ | ------------------------- |
| SET_MODE MANUAL    | Send from Node-RED | Ack received, mode=MANUAL |
| SET_PHASE NS_GREEN | Send while MANUAL  | NS LEDs green, EW red     |
| SET_MODE AUTO      | Send from Node-RED | FSM auto-cycles           |

### 6.3 Latency Test

```powershell
# Dùng benchmark tool
cd logger/tools
python run_benchmark_report.py --host <PC_IP> --count 100
```

Expected: RTT < 100ms qua WiFi

### 6.4 Reconnect Test

1. Disconnect WiFi (router off)
2. Wait 30s
3. Reconnect WiFi
4. ESP32 should auto-reconnect to MQTT

---

## 7. Troubleshoot

| Issue              | Cause         | Solution                   |
| ------------------ | ------------- | -------------------------- |
| WiFi không connect | Sai SSID/PASS | Check config.h             |
| MQTT timeout       | Sai IP broker | Ping từ ESP32 network      |
| LED không sáng     | Sai GPIO      | Check wiring & pinmap      |
| Ack không gửi      | Topic sai     | Check TOPIC_ACK trong code |

### Debug Serial Output

```cpp
// Bật debug trong main.cpp
#define DEBUG_MQTT 1
#define DEBUG_FSM 1
```

---

## 8. Files Quan Trọng

| File                   | Purpose               |
| ---------------------- | --------------------- |
| `esp32/src/main.cpp`   | Main firmware logic   |
| `esp32/src/config.h`   | WiFi/MQTT credentials |
| `esp32/platformio.ini` | Build configuration   |

---

> 📚 Xem thêm: [SPEC.md](../SPEC.md) Section 10 (Pinmap) | [ARCHITECTURE_OVERVIEW.md](ARCHITECTURE_OVERVIEW.md)
