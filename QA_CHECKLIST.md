# QA_CHECKLIST.md — End-to-End Smoke Test Checklist

> **Đề tài NCKH:** IoT–MQTT Giám sát & Điều khiển Đèn Giao Thông
> **Purpose:** Verify toàn bộ system hoạt động đúng trước khi demo/release

---

## Section 0: Automated Smoke Test (Quick Verification)

**Chạy trước khi test manual để verify hệ thống hoạt động:**

```powershell
cd logger/tools
python smoke_test.py --host <BROKER_IP>
```

### Expected Output (PASS)

```text
🧪 SMOKE TEST - Traffic Light MQTT Demo
============================================================
  Host: 192.168.1.100:1883
  User: demo
  Timeout: 5.0s
============================================================

  🔌 Testing broker connection... ✅ PASS
  📤 Testing SET_MODE MANUAL... ✅ PASS (RTT: 45.2ms)
  📤 Testing SET_PHASE 0 (NS_GREEN)... ✅ PASS (RTT: 38.7ms)
  📤 Testing SET_MODE AUTO (cleanup)... ✅ PASS (RTT: 41.1ms)

============================================================
📋 SUMMARY
============================================================
  ✅ Broker Connection
  ✅ SET_MODE MANUAL (45.2ms)
  ✅ SET_PHASE NS_GREEN (38.7ms)
  ✅ SET_MODE AUTO (41.1ms)

🎉 ALL TESTS PASSED
============================================================
```

### Exit Codes

| Code | Meaning | Action |
|------|---------|--------|
| 0 | All tests passed | ✅ Proceed to manual tests |
| 1 | One or more tests failed | ❌ Fix issues before continuing |
| 2 | Connection/setup error | ❌ Check Docker, network, credentials |

---

## Pre-Test Checklist

| # | Item | Status |
|---|------|--------|
| 1 | Mosquitto broker đang chạy | ☐ |
| 2 | Node-RED đang chạy, dashboard accessible | ☐ |
| 3 | Python logger đang chạy | ☐ |
| 4 | ESP32 đã flash firmware mới nhất | ☐ |
| 5 | ESP32 đã kết nối WiFi | ☐ |
| 6 | Tất cả LED đều hoạt động (manual test) | ☐ |

---

## Section 1: MQTT Connectivity

### 1.1 ESP32 → Broker Connection

| # | Test Case | Expected | Actual | Pass |
|---|-----------|----------|--------|------|
| 1.1.1 | ESP32 boot lên | Connect Mosquitto trong < 5s | | ☐ |
| 1.1.2 | Subscribe `cmd` topic | Broker shows subscription | | ☐ |
| 1.1.3 | LWT message | `status` topic = JSON có `"online":true` (retained). `ts_ms` optional. | | ☐ |

### 1.2 Broker Health

| # | Test Case | Expected | Actual | Pass |
|---|-----------|----------|--------|------|
| 1.2.1 | Broker uptime | Running > 1 min without restart | | ☐ |
| 1.2.2 | Client count | ≥ 3 clients (ESP32, Node-RED, Logger) | | ☐ |

---

## Section 2: State Publishing

### 2.1 State Message Format

| # | Test Case | Expected | Actual | Pass |
|---|-----------|----------|--------|------|
| 2.1.1 | `state` topic có message | Message mỗi 1s (±100ms) | | ☐ |
| 2.1.2 | JSON valid | Parse không lỗi | | ☐ |
| 2.1.3 | Required fields | `mode`, `phase`, `since_ms`, `uptime_s`, `ts_ms` đều có | | ☐ |
| 2.1.4 | `mode` value | Enum: AUTO/MANUAL/BLINK/OFF | | ☐ |
| 2.1.5 | `phase` value | Integer 0-5 | | ☐ |

### 2.2 State Accuracy

| # | Test Case | Expected | Actual | Pass |
|---|-----------|----------|--------|------|
| 2.2.1 | `uptime_s` tăng | Giá trị tăng đều mỗi giây | | ☐ |
| 2.2.2 | `since_ms` reset khi đổi phase | Reset về ~0 khi phase change | | ☐ |
| 2.2.3 | `ts_ms` reasonable | Epoch timestamp gần thời gian hiện tại | | ☐ |

---

## Section 3: Command → Acknowledgement

### 3.1 Basic Command Flow

| # | Test Case | Expected | Actual | Pass |
|---|-----------|----------|--------|------|
| 3.1.1 | Publish `SET_MODE:MANUAL` | Ack trong < 500ms | | ☐ |
| 3.1.2 | Ack JSON valid | Parse không lỗi | | ☐ |
| 3.1.3 | Ack `cmd_id` match | Same as command `cmd_id` | | ☐ |
| 3.1.4 | Ack `ok` = true | Command thành công | | ☐ |
| 3.1.5 | Mode changed | State shows `mode: MANUAL` | | ☐ |

### 3.2 Command Types

| # | Test Case | Expected | Actual | Pass |
|---|-----------|----------|--------|------|
| 3.2.1 | `SET_MODE:AUTO` | Switch về AUTO mode | | ☐ |
| 3.2.2 | `SET_MODE:BLINK` | All yellow blink | | ☐ |
| 3.2.3 | `SET_PHASE:0` (in MANUAL) | Go to phase 0 | | ☐ |
| 3.2.4 | `EMERGENCY` | Immediate BLINK mode | | ☐ |

### 3.3 Command Error Handling

| # | Test Case | Expected | Actual | Pass |
|---|-----------|----------|--------|------|
| 3.3.1 | Invalid JSON | Ignored, no ack | | ☐ |
| 3.3.2 | Missing `cmd_id` | `ok:false`, `err:ERR_INVALID_CMD` | | ☐ |
| 3.3.3 | Unknown `type` | `ok:false`, `err:ERR_UNKNOWN_TYPE` | | ☐ |

---

## Section 4: Safety Rules

### 4.1 Single Green Direction

| # | Test Case | Expected | Actual | Pass |
|---|-----------|----------|--------|------|
| 4.1.1 | Observe AUTO mode 1 cycle | Chỉ 1 hướng GREEN tại mọi thời điểm | | ☐ |
| 4.1.2 | Manual force 2 green | Command rejected hoặc override prevented | | ☐ |

### 4.2 ALL_RED Transition

| # | Test Case | Expected | Actual | Pass |
|---|-----------|----------|--------|------|
| 4.2.1 | GREEN_A → GREEN_B | Phải qua YELLOW → ALL_RED trước | | ☐ |
| 4.2.2 | ALL_RED duration | ≥ 2000ms | | ☐ |

### 4.3 MQTT Disconnection

| # | Test Case | Expected | Actual | Pass |
|---|-----------|----------|--------|------|
| 4.3.1 | Stop broker 5s | ESP32 vẫn hoạt động bình thường | | ☐ |
| 4.3.2 | Stop broker 12s | ESP32 chuyển AUTO mode | | ☐ |
| 4.3.3 | Restart broker | ESP32 reconnect, publish state | | ☐ |
| 4.3.4 | LWT triggered | `status` = JSON có `"online":false` when ESP32 disconnects. `ts_ms` absent (LWT). | | ☐ |

### 4.4 Command Idempotency

| # | Test Case | Expected | Actual | Pass |
|---|-----------|----------|--------|------|
| 4.4.1 | Send same cmd_id 2 lần | Both ack `ok:true`, chỉ execute 1 lần | | ☐ |
| 4.4.2 | Send 33 unique commands | Oldest cmd_id removed from cache | | ☐ |

---

## Section 5: Telemetry

| # | Test Case | Expected | Actual | Pass |
|---|-----------|----------|--------|------|
| 5.1 | `telemetry` topic có message | Message mỗi 5s | | ☐ |
| 5.2 | JSON valid | Parse không lỗi | | ☐ |
| 5.3 | `rssi_dbm` reasonable | -90 to -30 | | ☐ |
| 5.4 | `heap_free_kb` reasonable | > 50 KB | | ☐ |
| 5.5 | `uptime_s` match state | Same value ± 1s | | ☐ |

---

## Section 6: Dashboard UI

### 6.1 Status Display

| # | Test Case | Expected | Actual | Pass |
|---|-----------|----------|--------|------|
| 6.1.1 | Mode display | Match ESP32 state | | ☐ |
| 6.1.2 | Phase display | Match ESP32 state | | ☐ |
| 6.1.3 | Online indicator | Green khi ESP32 connected | | ☐ |
| 6.1.4 | Offline indicator | Red khi ESP32 disconnects | | ☐ |

### 6.2 Control Buttons

| # | Test Case | Expected | Actual | Pass |
|---|-----------|----------|--------|------|
| 6.2.1 | Click AUTO button | Cmd sent, ack received, UI updated | | ☐ |
| 6.2.2 | Click MANUAL button | Switch to manual mode | | ☐ |
| 6.2.3 | Click EMERGENCY | Immediate BLINK | | ☐ |
| 6.2.4 | Phase buttons (in MANUAL) | Phase changes correctly | | ☐ |

### 6.3 Traffic Light Visualization

| # | Test Case | Expected | Actual | Pass |
|---|-----------|----------|--------|------|
| 6.3.1 | Visualization matches state | LEDs in UI match physical/state | | ☐ |
| 6.3.2 | Update latency | < 1s delay from state change | | ☐ |

### 6.4 Charts

| # | Test Case | Expected | Actual | Pass |
|---|-----------|----------|--------|------|
| 6.4.1 | RSSI chart updates | New point mỗi 5s | | ☐ |
| 6.4.2 | Heap chart updates | New point mỗi 5s | | ☐ |
| 6.4.3 | Chart history | Shows last 5 minutes | | ☐ |

---

## Section 7: Logger

| # | Test Case | Expected | Actual | Pass |
|---|-----------|----------|--------|------|
| 7.1 | Log file exists | `logs/YYYY-MM-DD.jsonl` created | | ☐ |
| 7.2 | All topics logged | state, cmd, ack, status, telemetry | | ☐ |
| 7.3 | Each line valid JSON | Parse không lỗi | | ☐ |
| 7.4 | Timestamp present | Each log entry has timestamp | | ☐ |
| 7.5 | File rotation | New file at midnight (if tested) | | ☐ |

---

## Section 8: Performance

| # | Test Case | Expected | Actual | Pass |
|---|-----------|----------|--------|------|
| 8.1 | Cmd → Ack latency | < 200ms average | | ☐ |
| 8.2 | State publish jitter | 1000ms ± 50ms | | ☐ |
| 8.3 | ESP32 memory stable | Heap không giảm liên tục (no leak) | | ☐ |
| 8.4 | Dashboard responsive | UI không lag | | ☐ |
| 8.5 | Run 30 minutes | System stable, no crashes | | ☐ |

---

## Section 9: Edge Cases

| # | Test Case | Expected | Actual | Pass |
|---|-----------|----------|--------|------|
| 9.1 | Rapid commands (10/s) | All processed, no crash | | ☐ |
| 9.2 | Large JSON payload | Rejected if > 1KB | | ☐ |
| 9.3 | WiFi disconnect/reconnect | ESP32 recovers gracefully | | ☐ |
| 9.4 | Broker restart | All clients reconnect | | ☐ |
| 9.5 | Power cycle ESP32 | Boots to AUTO mode, connects | | ☐ |

---

## Test Summary

| Section | Total | Pass | Fail | N/A |
|---------|-------|------|------|-----|
| 1. MQTT Connectivity | 5 | | | |
| 2. State Publishing | 8 | | | |
| 3. Command → Ack | 11 | | | |
| 4. Safety Rules | 8 | | | |
| 5. Telemetry | 5 | | | |
| 6. Dashboard UI | 12 | | | |
| 7. Logger | 5 | | | |
| 8. Performance | 5 | | | |
| 9. Edge Cases | 5 | | | |
| **TOTAL** | **64** | | | |

---

## Sign-Off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| QA Engineer | | | |
| Dev Lead | | | |
| Project Manager | | | |

---

## Notes & Issues Found

| # | Description | Severity | Status |
|---|-------------|----------|--------|
| 1 | | | |
| 2 | | | |
| 3 | | | |

---

> **⚠️ SMOKE TEST PASS CRITERIA: Tất cả Section 1-4 phải 100% pass. Section 5-9 cho phép tối đa 3 fails không critical.**
