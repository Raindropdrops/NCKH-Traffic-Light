# SPEC.md — IoT–MQTT Traffic Light Control System
>
> **Version:** 1.0 | **Status:** LOCKED | **Scope:** ESP32 (Scope 1)
> **Đề tài NCKH:** Giám sát và điều khiển đèn giao thông qua IoT–MQTT

---

## 1. System Architecture

```
┌─────────────┐      MQTT       ┌──────────────┐      MQTT      ┌──────────────────┐
│   ESP32     │ ◄────────────► │  Mosquitto   │ ◄────────────► │   Node-RED       │
│  (Edge)     │    QoS 0/1     │  (Broker)    │    QoS 0/1     │   Dashboard      │
│             │                │  port:1883   │                │                  │
└─────────────┘                └──────────────┘                └──────────────────┘
                                      ▲
                                      │ MQTT Subscribe
                               ┌──────┴──────┐
                               │   Python    │
                               │   Logger    │
                               │  (*.jsonl)  │
                               └─────────────┘
```

| Component | Role | Technology |
|-----------|------|------------|
| **ESP32** | Edge controller, LED output, local FSM | Arduino/PlatformIO |
| **Mosquitto** | MQTT broker | Docker/native |
| **Node-RED** | Dashboard UI, command sender | Docker/native |
| **Python Logger** | Telemetry/event logging | Python 3.11+ |

---

## 2. MQTT Topic Tree (LOCKED)

> **Base prefix:** `city/demo/intersection/001`

| Topic | Direction | Purpose |
|-------|-----------|---------|
| `.../state` | ESP32 → Broker | Current light state, mode, phase |
| `.../telemetry` | ESP32 → Broker | Metrics (WiFi RSSI, heap, uptime) |
| `.../cmd` | Broker → ESP32 | Commands from dashboard |
| `.../ack` | ESP32 → Broker | Command acknowledgement |
| `.../status` | ESP32 → Broker | LWT online/offline status |

### Full Topic Paths

```
city/demo/intersection/001/state
city/demo/intersection/001/telemetry
city/demo/intersection/001/cmd
city/demo/intersection/001/ack
city/demo/intersection/001/status
```

---

## 3. QoS & Retained Settings (LOCKED)

| Topic | QoS | Retained | Rationale |
|-------|-----|----------|-----------|
| `cmd` | **1** | **No** | Commands must be delivered exactly-once attempt, no stale commands |
| `ack` | **1** | **No** | Acknowledgements critical for confirmation |
| `status` | **1** | **Yes** | LWT message, clients must see last known status |
| `state` | **0** *(default)* | **No** | High frequency, loss acceptable. *(Optional experiment: QoS 1 for latency testing — configure via `STATE_QOS` constant)* |
| `telemetry` | **0** | **No** | Metrics, loss acceptable |

---

## 4. Payload JSON Schema (LOCKED)

### 4.1 Command (`cmd`)

```json
{
  "cmd_id": "uuid-v4-string",
  "type": "SET_MODE | SET_PHASE | EMERGENCY",
  "mode": "AUTO | MANUAL | BLINK | OFF",
  "phase": 0,
  "duration_ms": 30000,
  "ts_ms": 1707388800000
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `cmd_id` | string (UUID) | ✅ | Unique command ID for idempotency |
| `type` | enum | ✅ | Command type |
| `mode` | enum | ❌ | Target mode (for SET_MODE) |
| `phase` | int | ❌ | Target phase index (for SET_PHASE) |
| `duration_ms` | int | ❌ | Phase duration in milliseconds |
| `ts_ms` | int64 | ✅ | Sender timestamp (epoch ms) |

### 4.2 Acknowledgement (`ack`)

```json
{
  "cmd_id": "uuid-v4-string",
  "ok": true,
  "err": null,
  "edge_recv_ts_ms": 1707388800123
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `cmd_id` | string | ✅ | Echoed command ID |
| `ok` | bool | ✅ | Success flag |
| `err` | string/null | ✅ | Error message if failed |
| `edge_recv_ts_ms` | int64 | ✅ | ESP32 receive timestamp |

### 4.3 State (`state`)

```json
{
  "mode": "AUTO",
  "phase": 2,
  "since_ms": 15000,
  "uptime_s": 3600,
  "ts_ms": 1707388800000
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `mode` | enum | ✅ | Current operating mode |
| `phase` | int | ✅ | Current phase index |
| `since_ms` | int | ✅ | Time in current phase (ms) |
| `uptime_s` | int | ✅ | Device uptime (seconds) |
| `ts_ms` | int64 | ✅ | State report timestamp |

### 4.4 Status (LWT)

```json
{
  "online": true,
  "ts_ms": 1707388800000
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `online` | bool | ✅ | Connection status (true=connected, false=LWT) |
| `ts_ms` | int64 | ❌ *(recommended)* | Timestamp (required for connect message, absent in LWT) |

### 4.5 Telemetry

```json
{
  "rssi_dbm": -55,
  "heap_free_kb": 120,
  "uptime_s": 3600,
  "ts_ms": 1707388800000
}
```

---

## 5. Safety Rules (LOCKED — CRITICAL)

> ⚠️ **VIOLATION = PROJECT FAIL**

### 5.1 Single Green Direction

```
Rule: Tại mọi thời điểm, CHỈ ĐƯỢC 1 hướng có đèn XANH.
Enforcement: FSM state machine, hardware interlock
Violation: EMERGENCY BLINK mode immediate
```

### 5.2 ALL_RED Transition

```
Rule: Mọi chuyển pha PHẢI có giai đoạn ALL_RED (tối thiểu 2000ms).
Purpose: Xe đang qua giao lộ có thời gian thoát.
Sequence: GREEN_A → YELLOW_A → ALL_RED → GREEN_B
```

### 5.3 MQTT Disconnection Fallback

```
Rule: Mất kết nối MQTT > 10 giây → Tự động chuyển về AUTO mode local.
Implementation: Watchdog timer reset mỗi khi nhận message.
Recovery: Khi reconnect, ESP32 publish state hiện tại.
```

### 5.4 Command Idempotency

```
Rule: Mỗi cmd_id chỉ được xử lý 1 lần.
Implementation: ESP32 cache 32 cmd_id gần nhất.
Duplicate: Trả ack với ok=true, không thực thi lại.
```

### 5.5 Phase Timing Constraints

```
MIN_GREEN_MS:  5000   (5 seconds)
MAX_GREEN_MS:  120000 (2 minutes)
YELLOW_MS:     3000   (fixed)
ALL_RED_MS:    2000   (minimum)
```

---

## 6. Operating Modes

| Mode | Description | Command Source |
|------|-------------|----------------|
| `AUTO` | FSM tự động theo cycle timing | Local ESP32 |
| `MANUAL` | Dashboard điều khiển từng phase | Node-RED |
| `BLINK` | Yellow blink all directions (cảnh báo) | Emergency/Fallback |
| `OFF` | All lights off (maintenance) | Manual only |

---

## 7. Phase Definition (4-Way Intersection)

> **NOTE:**
>
> - **Direction A** = North–South (NS)
> - **Direction B** = East–West (EW)

| Phase | Direction A (NS) | Direction B (EW) | Duration |
|-------|------------------|------------------|----------|
| 0 | GREEN | RED | Configurable |
| 1 | YELLOW | RED | 3000ms |
| 2 | ALL_RED | ALL_RED | 2000ms |
| 3 | RED | GREEN | Configurable |
| 4 | RED | YELLOW | 3000ms |
| 5 | ALL_RED | ALL_RED | 2000ms |

---

## 8. Error Codes

| Code | Meaning | Action |
|------|---------|--------|
| `ERR_INVALID_CMD` | Malformed JSON or missing fields | Ignore, log |
| `ERR_UNKNOWN_TYPE` | Unknown command type | Ignore, log |
| `ERR_DUPLICATE_CMD` | cmd_id already processed | Return ok=true |
| `ERR_SAFETY_VIOLATION` | Command would violate safety | Reject |
| `ERR_TIMEOUT` | Ack not received within 5s | Retry or alert |

---

## 9. Configuration Constants

```cpp
// MQTT
#define MQTT_BROKER      "192.168.x.x"
#define MQTT_PORT        1883
#define MQTT_KEEPALIVE   30
#define MQTT_TIMEOUT_MS  10000

// Topics
#define TOPIC_BASE       "city/demo/intersection/001"
#define TOPIC_STATE      TOPIC_BASE "/state"
#define TOPIC_CMD        TOPIC_BASE "/cmd"
#define TOPIC_ACK        TOPIC_BASE "/ack"
#define TOPIC_STATUS     TOPIC_BASE "/status"
#define TOPIC_TELEMETRY  TOPIC_BASE "/telemetry"

// Timing
#define STATE_PUBLISH_INTERVAL_MS   1000
#define TELEMETRY_INTERVAL_MS       5000
#define CMD_ID_CACHE_SIZE           32
```

---

## 10. Hardware Setup (Demo NCKH)

### 10.1 Phương án Demo

| PA | Mô tả | Ưu điểm | Nhược điểm | Mức độ NCKH |
|----|-------|---------|------------|-------------|
| **PA1** | 1 module LED R/Y/G | Đơn giản, 3 GPIO | Không thể hiện 2-phase | ⭐⭐ Đủ demo concept |
| **PA2** ✅ | 4 module ghép đôi (N=S, E=W) | Thực tế 2-phase intersection | Cần 6 GPIO | ⭐⭐⭐ **Khuyến nghị** |

> **Khuyến nghị: PA2** — Mô phỏng ngã tư thực tế với 2 hướng (NS và EW), dễ defend khi thuyết trình.

### 10.2 ESP32 Pinmap (PA2 - Khuyến nghị)

```
┌─────────────────────────────────────────────────────────────┐
│                        ESP32 DevKit                         │
├─────────────────────────────────────────────────────────────┤
│  GPIO  │  Function      │  LED Module        │  Note        │
├────────┼────────────────┼────────────────────┼──────────────┤
│  GPIO16│  NS_RED        │  North + South RED │  Parallel    │
│  GPIO17│  NS_YELLOW     │  North + South YEL │  Parallel    │
│  GPIO18│  NS_GREEN      │  North + South GRN │  Parallel    │
├────────┼────────────────┼────────────────────┼──────────────┤
│  GPIO19│  EW_RED        │  East + West RED   │  Parallel    │
│  GPIO21│  EW_YELLOW     │  East + West YEL   │  Parallel    │
│  GPIO22│  EW_GREEN      │  East + West GRN   │  Parallel    │
├────────┼────────────────┼────────────────────┼──────────────┤
│  GND   │  Common Ground │  All LED modules   │              │
│  3V3   │  VCC (optional)│  If LED module 3.3V│              │
└─────────────────────────────────────────────────────────────┘
```

### 10.3 Sơ đồ Đấu Dây (ASCII)

```
                    NORTH MODULE
                    ┌─────────┐
                    │ R  Y  G │
                    └─┬──┬──┬─┘
                      │  │  │
    ┌─────────────────┼──┼──┼─────────────────┐
    │                 │  │  │                 │
    │     WEST        │  │  │        EAST     │
    │   ┌─────────┐   │  │  │   ┌─────────┐   │
    │   │ R  Y  G │   │  │  │   │ R  Y  G │   │
    │   └─┬──┬──┬─┘   │  │  │   └─┬──┬──┬─┘   │
    │     │  │  │     │  │  │     │  │  │     │
    │     └──┼──┼─────┼──┼──┼─────┼──┼──┘     │
    │        │  │     │  │  │     │  │        │
    │        └──┼─────┼──┼──┼─────┼──┘        │
    │           │     │  │  │     │           │
    │           └─────┼──┼──┼─────┘           │
    │                 │  │  │                 │
    │                 │  │  │                 │
    │               ┌─┴──┴──┴─┐               │
    │               │ R  Y  G │               │
    │               └─────────┘               │
    │                  SOUTH                  │
    │                 MODULE                  │
    └─────────────────────────────────────────┘

    WIRING:
    ┌──────────────────────────────────────────────────────────┐
    │  ESP32                                                   │
    │  ┌────┐                                                  │
    │  │GPIO│  16 ────────┬───────── NORTH_R ──── SOUTH_R     │
    │  │    │  17 ────────┼───────── NORTH_Y ──── SOUTH_Y     │
    │  │    │  18 ────────┼───────── NORTH_G ──── SOUTH_G     │
    │  │    │             │                                    │
    │  │    │  19 ────────┼───────── EAST_R ───── WEST_R      │
    │  │    │  21 ────────┼───────── EAST_Y ───── WEST_Y      │
    │  │    │  22 ────────┼───────── EAST_G ───── WEST_G      │
    │  │    │             │                                    │
    │  │    │  GND ───────┴───────── ALL GND (Common)         │
    │  └────┘                                                  │
    └──────────────────────────────────────────────────────────┘
```

### 10.4 Lưu Ý Điện

| Thông số | Giá trị | Khuyến nghị |
|----------|---------|-------------|
| Logic level ESP32 | 3.3V | LED module 3.3V hoặc dùng level shifter |
| Dòng GPIO max | 12mA/pin, 40mA tổng | Dùng transistor 2N2222 nếu LED > 12mA |
| LED module VCC | 3.3V hoặc 5V | Check datasheet module |

**Nếu LED module 5V:**

```
GPIO ──┬── R 1kΩ ──── Base (2N2222)
       │              Emitter ──── GND
       │              Collector ── LED ── VCC (5V)
```

### 10.5 Bill of Materials (BOM)

| # | Item | Qty | Note |
|---|------|-----|------|
| 1 | ESP32 DevKit V1 | 1 | 30-pin hoặc 38-pin |
| 2 | LED Traffic Module (R/Y/G) | 4 | Hoặc LED đơn 5mm x12 |
| 3 | Breadboard 830 holes | 1 | |
| 4 | Jumper wires M-M | 20 | |
| 5 | Resistor 220Ω (nếu LED đơn) | 12 | 1/4W |
| 6 | USB Cable | 1 | Micro-USB hoặc Type-C |
| 7 | 5V Power Supply (optional) | 1 | Nếu cần nguồn riêng |

---

## 11. Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-08 | PM/Tech Lead | Initial locked spec |
| 1.0.1 | 2026-02-08 | PM/Tech Lead | Clarified Direction A=NS, B=EW; locked state QoS=0; added status schema table |

---

> **⚠️ Document này là SPEC KHÓA CỨNG. Mọi thay đổi cần được review và approve bởi Tech Lead.**
