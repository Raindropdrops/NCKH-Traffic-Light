# 🏗️ ARCHITECTURE OVERVIEW

> **traffic-mqtt-demo** — Kiến trúc hệ thống giám sát đèn giao thông qua IoT–MQTT

---

## 1. Sơ Đồ Kiến Trúc

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              DOCKER HOST (PC)                               │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                        docker-compose.yml                            │   │
│  │  ┌─────────────────┐         ┌─────────────────┐                     │   │
│  │  │   MOSQUITTO     │◄───────►│   NODE-RED      │                     │   │
│  │  │   :1883         │  MQTT   │   :1880         │                     │   │
│  │  │   (Broker)      │         │   (Dashboard)   │                     │   │
│  │  └────────┬────────┘         └─────────────────┘                     │   │
│  └───────────┼──────────────────────────────────────────────────────────┘   │
│              │                                                              │
│              │ MQTT (QoS 0/1)                                               │
│              │                                                              │
│  ┌───────────┴──────────────────────────────────────────────────────────┐   │
│  │                        PYTHON TOOLS                                   │   │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐       │   │
│  │  │   mock_esp32    │  │   smoke_test    │  │   benchmark     │       │   │
│  │  │   (Simulator)   │  │   (QA)          │  │   (RTT Report)  │       │   │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘       │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
              │
              │ WiFi + MQTT
              ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              ESP32 (Edge Device)                            │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  WiFi → MQTT Client → FSM (AUTO/MANUAL/BLINK/OFF) → GPIO → LEDs     │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Lu(QoS 0)ồng Dữ Liệu

```
┌─────────────┐     cmd (QoS 1)      ┌─────────────┐     cmd (QoS 1)      ┌─────────────┐
│  Node-RED   │ ──────────────────► │  Mosquitto  │ ──────────────────► │    ESP32    │
│  Dashboard  │                      │   Broker    │                      │    Edge     │
└─────────────┘                      └─────────────┘                      └─────────────┘
      ▲                                    │                                    │
      │                                    │                                    │
      │         ack (QoS 1)                │         ack (QoS 1)                │
      └────────────────────────────────────┼────────────────────────────────────┘
                                           │
      ┌────────────────────────────────────┼────────────────────────────────────┐
      │          state (QoS 0)             │         state               │
      ▼                                    ▼                                    │
┌─────────────┐                      ┌─────────────┐                            │
│  Node-RED   │ ◄────────────────── │  Mosquitto  │ ◄──────────────────────────┘
│  Dashboard  │                      │   Broker    │
└─────────────┘                      └─────────────┘
      │
      │ (Display RTT, Mode, Phase)
      ▼
   [Browser UI]
```

### Sequence Diagram (SET_MODE)

```
User        Node-RED      Mosquitto       ESP32
 │            │              │              │
 │──Click────►│              │              │
 │            │──publish────►│              │
 │            │  cmd/        │──forward────►│
 │            │              │              │──Process FSM
 │            │              │              │──Update GPIO
 │            │              │◄──ack────────│
 │            │◄─────────────│              │
 │◄──RTT──────│              │              │
 │            │              │◄──state──────│
 │            │◄─────────────│              │
 │◄──Update───│              │              │
```

---

## 3. MQTT Topic Map

> **Base prefix:** `city/demo/intersection/001`

| Topic           | Direction         | QoS | Retained | Purpose                                   |
| --------------- | ----------------- | --- | -------- | ----------------------------------------- |
| `.../cmd`       | Dashboard → ESP32 | 1   | No       | Commands (SET_MODE, SET_PHASE, EMERGENCY) |
| `.../ack`       | ESP32 → Dashboard | 1   | No       | Command acknowledgement with cmd_id       |
| `.../state`     | ESP32 → All       | 0   | No       | Current mode, phase, LED states (1Hz)     |
| `.../status`    | ESP32 → All       | 1   | Yes      | LWT: "ONLINE" / "OFFLINE"                 |
| `.../telemetry` | ESP32 → Logger    | 0   | No       | WiFi RSSI, heap, uptime (5s interval)     |

### Full Topic Paths

```
city/demo/intersection/001/cmd
city/demo/intersection/001/ack
city/demo/intersection/001/state
city/demo/intersection/001/status
city/demo/intersection/001/telemetry
```

---

## 4. What Runs Where

| Component          | Runs On      | Technology            | Port |
| ------------------ | ------------ | --------------------- | ---- |
| **Mosquitto**      | Docker (PC)  | Eclipse Mosquitto 2.x | 1883 |
| **Node-RED**       | Docker (PC)  | Node-RED + Dashboard  | 1880 |
| **Python Tools**   | PC (native)  | Python 3.11+          | -    |
| **ESP32 Firmware** | ESP32 DevKit | Arduino/PlatformIO    | -    |

---

## 5. Directory Structure

```
traffic-mqtt-demo/
├── docker-compose.yml          # Docker services orchestration
├── docker/
│   ├── mosquitto/
│   │   ├── mosquitto.conf      # Broker configuration
│   │   ├── aclfile             # Access control list
│   │   └── pwfile              # Password file (generated)
│   └── nodered/data/           # Node-RED persistent data
├── esp32/
│   ├── platformio.ini          # PlatformIO build config
│   └── src/
│       ├── main.cpp            # Firmware main logic
│       └── config.example.h    # WiFi/MQTT config template
├── logger/tools/
│   ├── mock_esp32.py           # ESP32 simulator
│   ├── smoke_test.py           # E2E smoke test
│   ├── run_benchmark_report.py # RTT benchmark + report
│   └── analyze_results.py      # CSV analyzer
├── node-red/flows.json         # Dashboard flows (backup)
├── SPEC.md                     # Protocol specification
├── RUNBOOK.md                  # Quick start guide
└── QA_CHECKLIST.md             # QA test checklist
```

---

## 6. Dependencies

| Service      | Dependency | Version                                     |
| ------------ | ---------- | ------------------------------------------- |
| Mosquitto    | Docker     | eclipse-mosquitto:2                         |
| Node-RED     | Docker     | nodered/node-red:latest                     |
| Python Tools | Local      | Python 3.11+, paho-mqtt, pandas, matplotlib |
| ESP32        | PlatformIO | Arduino framework, PubSubClient             |

---

> 📚 Xem thêm: [SPEC.md](SPEC.md) | [RUNBOOK.md](RUNBOOK.md) | [NODE_RED_GUIDE.md](docs/NODE_RED_GUIDE.md)
