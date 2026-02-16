# API Documentation — MQTT Topics & Payloads

> **SPEC Version:** 1.0.1 (LOCKED) | **Base Prefix:** `city/demo/intersection/001`

---

## MQTT Topics

| Topic           | Direction         | QoS | Retained | Purpose                                   |
| --------------- | ----------------- | --- | -------- | ----------------------------------------- |
| `.../state`     | ESP32 → Broker    | 0   | No       | Current mode, phase, uptime (1s interval) |
| `.../telemetry` | ESP32 → Broker    | 0   | No       | WiFi RSSI, heap, uptime (5s interval)     |
| `.../cmd`       | Dashboard → ESP32 | 1   | No       | Commands: SET_MODE, SET_PHASE, EMERGENCY  |
| `.../ack`       | ESP32 → Dashboard | 1   | No       | Command acknowledgement with cmd_id echo  |
| `.../status`    | ESP32 → Broker    | 1   | **Yes**  | LWT online/offline status                 |

---

## Payload Schemas

### 1. Command (`cmd`)

```json
{
  "cmd_id": "a1b2c3d4-e5f6-4789-abcd-ef0123456789",
  "type": "SET_MODE",
  "mode": "MANUAL",
  "ts_ms": 1707388800000
}
```

```json
{
  "cmd_id": "b2c3d4e5-f6a7-4890-bcde-f01234567890",
  "type": "SET_PHASE",
  "phase": 3,
  "ts_ms": 1707388800100
}
```

```json
{
  "cmd_id": "c3d4e5f6-a7b8-4901-cdef-012345678901",
  "type": "EMERGENCY",
  "ts_ms": 1707388800200
}
```

| Field         | Type             | Required | Description                                        |
| ------------- | ---------------- | -------- | -------------------------------------------------- |
| `cmd_id`      | string (UUID v4) | ✅       | Unique command ID for idempotency                  |
| `type`        | enum             | ✅       | `SET_MODE` · `SET_PHASE` · `EMERGENCY`             |
| `mode`        | enum             | ❌       | `AUTO` · `MANUAL` · `BLINK` · `OFF` (for SET_MODE) |
| `phase`       | int (0–5)        | ❌       | Phase index (for SET_PHASE, requires MANUAL mode)  |
| `duration_ms` | int              | ❌       | Optional phase duration override                   |
| `ts_ms`       | int64            | ✅       | Sender timestamp (epoch milliseconds)              |

---

### 2. Acknowledgement (`ack`)

```json
{
  "cmd_id": "a1b2c3d4-e5f6-4789-abcd-ef0123456789",
  "ok": true,
  "err": null,
  "edge_recv_ts_ms": 1707388800050
}
```

```json
{
  "cmd_id": "b2c3d4e5-f6a7-4890-bcde-f01234567890",
  "ok": false,
  "err": "ERR_NOT_MANUAL_MODE",
  "edge_recv_ts_ms": 1707388800150
}
```

| Field             | Type          | Required | Description                              |
| ----------------- | ------------- | -------- | ---------------------------------------- |
| `cmd_id`          | string        | ✅       | Echoed command ID                        |
| `ok`              | bool          | ✅       | `true` = success, `false` = rejected     |
| `err`             | string / null | ✅       | Error code if failed, `null` if success  |
| `edge_recv_ts_ms` | int64         | ✅       | ESP32 receive timestamp (see note below) |

> **Timestamp Convention:** Firmware uses monotonic uptime (ms since boot, no NTP).
> Mock ESP32 uses epoch ms (`time.time() * 1000`).
> Both are valid for RTT calculation: `RTT = now() - cmd.ts_ms` uses the ACK round-trip, not `edge_recv_ts_ms`.

---

### 3. State (`state`)

Published every 1 second.

```json
{
  "mode": "AUTO",
  "phase": 2,
  "since_ms": 15000,
  "uptime_s": 3600,
  "ts_ms": 1707388800000
}
```

| Field      | Type      | Required | Description                |
| ---------- | --------- | -------- | -------------------------- |
| `mode`     | enum      | ✅       | Current operating mode     |
| `phase`    | int (0–5) | ✅       | Current phase index        |
| `since_ms` | int       | ✅       | Time in current phase (ms) |
| `uptime_s` | int       | ✅       | Device uptime (seconds)    |
| `ts_ms`    | int64     | ✅       | State report timestamp     |

**Phase Index Map:**

| Phase | Name      | NS  | EW  |
| ----- | --------- | --- | --- |
| 0     | NS_GREEN  | 🟢  | 🔴  |
| 1     | NS_YELLOW | 🟡  | 🔴  |
| 2     | ALL_RED   | 🔴  | 🔴  |
| 3     | EW_GREEN  | 🔴  | 🟢  |
| 4     | EW_YELLOW | 🔴  | 🟡  |
| 5     | ALL_RED   | 🔴  | 🔴  |

---

### 4. Status — LWT (`status`)

Published on connect (retained). LWT auto-publishes `online: false` on disconnect.

```json
{ "online": true, "ts_ms": 1707388800000 }
```

```json
{ "online": false }
```

| Field    | Type  | Required | Description                        |
| -------- | ----- | -------- | ---------------------------------- |
| `online` | bool  | ✅       | `true` on connect, `false` via LWT |
| `ts_ms`  | int64 | ❌       | Present on connect, absent in LWT  |

---

### 5. Telemetry (`telemetry`)

Published every 5 seconds.

```json
{
  "rssi_dbm": -55,
  "heap_free_kb": 120,
  "uptime_s": 3600,
  "ts_ms": 1707388800000
}
```

| Field          | Type  | Required | Description                                    |
| -------------- | ----- | -------- | ---------------------------------------------- |
| `rssi_dbm`     | int   | ✅       | WiFi signal strength (dBm, typical -30 to -90) |
| `heap_free_kb` | int   | ✅       | Free heap memory (KB)                          |
| `uptime_s`     | int   | ✅       | Device uptime (seconds)                        |
| `ts_ms`        | int64 | ✅       | Telemetry report timestamp                     |

---

## Error Codes

| Code                                         | Meaning                                                 | Source          |
| -------------------------------------------- | ------------------------------------------------------- | --------------- |
| `ERR_INVALID_CMD`                            | Malformed JSON or missing required fields               | Firmware + Mock |
| `ERR_UNKNOWN_TYPE`                           | Unknown command type (not SET_MODE/SET_PHASE/EMERGENCY) | Firmware + Mock |
| `ERR_INVALID_MODE`                           | Invalid mode value                                      | Firmware        |
| `ERR_MISSING_MODE`                           | SET_MODE without mode field                             | Firmware        |
| `ERR_PHASE_REJECTED` / `ERR_NOT_MANUAL_MODE` | SET_PHASE when not in MANUAL mode                       | Firmware / Mock |
| `ERR_MISSING_PHASE`                          | SET_PHASE without phase field                           | Firmware        |
| `ERR_INVALID_PHASE`                          | Phase value outside 0–5 range                           | Mock            |

---

## Authentication

| Parameter | Value                                                  |
| --------- | ------------------------------------------------------ |
| Username  | `demo`                                                 |
| Password  | `demo_pass`                                            |
| Broker    | `localhost:1883` (MQTT) / `localhost:9001` (WebSocket) |

> For production: create separate users with restricted ACLs.

---

## Timestamp Contract

Every message containing `ts_ms` follows a specific convention depending on the source:

| Source               | `ts_ms` Convention               | `edge_recv_ts_ms` Convention     | NTP Available? |
| -------------------- | -------------------------------- | -------------------------------- | -------------- |
| **Firmware (ESP32)** | Monotonic uptime (ms since boot) | Monotonic uptime (ms since boot) | ❌ No          |
| **Mock ESP32**       | Epoch ms (`time.time() * 1000`)  | Epoch ms (`time.time() * 1000`)  | ✅ Yes         |
| **Dashboard**        | Epoch ms (`Date.now()`)          | — (consumer, not producer)       | ✅ Yes         |

### Which Field to Use For What

| Purpose                   | Field                                  | Formula                                    | Notes                                                                        |
| ------------------------- | -------------------------------------- | ------------------------------------------ | ---------------------------------------------------------------------------- |
| **RTT measurement**       | `cmd.ts_ms` (sender) + receive time    | `RTT = now() - cmd.ts_ms`                  | Measured on the **sender side** (dashboard). Does NOT use `edge_recv_ts_ms`. |
| **Edge processing delay** | `ack.edge_recv_ts_ms` - `cmd.ts_ms`    | Only valid if **both** use same clock base | ⚠️ Invalid in mixed mode (firmware uptime vs dashboard epoch)                |
| **Display / logging**     | `state.ts_ms`, `telemetry.ts_ms`       | Use as-is for ordering                     | Monotonic ordering guaranteed per source                                     |
| **Uptime tracking**       | `state.uptime_s`, `telemetry.uptime_s` | Seconds since boot                         | Always monotonic, regardless of NTP                                          |

### Key Rules

1. **RTT is always measured on the sender side** (`now() - cmd.ts_ms`), not from `edge_recv_ts_ms`.
2. **Do NOT subtract `edge_recv_ts_ms` from `cmd.ts_ms`** in mixed mode — different clock bases.
3. The `edge_recv_ts_ms` field is primarily for **diagnostics** (verifying the edge device received the command).

---

## Mixed Mode Deployment (Mock + Firmware)

When running both mock ESP32 and real firmware simultaneously for testing:

### Preconditions

- Both devices connect to the **same Mosquitto broker**.
- Each device must use a **different intersection ID** (e.g., `001` for firmware, `002` for mock).
- Dashboard must subscribe to the correct intersection's topics.

### Configuration

```
# Firmware (sdkconfig / menuconfig)
MQTT_CITY_ID = "demo"
MQTT_INTERSECTION_ID = "001"     # ← unique per device

# Mock ESP32 (mock_esp32.py --intersection 002)
INTERSECTION_ID = "002"          # ← different from firmware
```

### Timestamp Behavior

| Scenario                         | `ts_ms` Comparison     |                     RTT Valid? |
| -------------------------------- | ---------------------- | -----------------------------: |
| Dashboard → Mock → Dashboard     | Epoch ↔ Epoch          |                         ✅ Yes |
| Dashboard → Firmware → Dashboard | Epoch → Uptime → Epoch | ✅ RTT only (via sender clock) |
| Mock vs Firmware timestamps      | Epoch vs Uptime        |              ❌ Not comparable |

### Recommendations

1. **Do not mix intersection IDs** — each device gets its own topic subtree.
2. **Run smoke tests per intersection** — `smoke_test.py --intersection 001`.
3. **Benchmark reports are per-device** — timestamps are only comparable within the same device.
4. **Dashboard can monitor multiple intersections** — subscribe to `city/demo/intersection/+/state`.

### Benchmark Per Intersection

```powershell
# Benchmark intersection 001 (default)
python logger/tools/run_benchmark_report.py --host 127.0.0.1 --count 10

# Benchmark intersection 002
python logger/tools/run_benchmark_report.py --host 127.0.0.1 --count 10 --city demo --intersection 002
```
