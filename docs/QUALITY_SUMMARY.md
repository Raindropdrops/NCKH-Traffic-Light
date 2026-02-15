# 📊 QUALITY SUMMARY — Traffic Light MQTT Demo

> Tổng hợp chất lượng dự án — cập nhật lần cuối: 2026-02-13

---

## 1. Test Summary

| Category           | Total  | PASS   | WARN  | FAIL  | Notes                         |
| ------------------ | ------ | ------ | ----- | ----- | ----------------------------- |
| Repo Structure     | 5      | 5      | 0     | 0     | All required files present    |
| Docker/Infra       | 4      | 4      | 0     | 0     | Compose up, health checks OK  |
| MQTT Broker        | 3      | 3      | 0     | 0     | Auth, ACL, pub/sub verified   |
| Smoke Test (mock)  | 4      | 4      | 0     | 0     | SET_MODE, SET_PHASE, ACK, RTT |
| Node-RED Dashboard | 3      | 3      | 0     | 0     | Import, UI, MQTT integration  |
| Benchmark (mock)   | 2      | 2      | 0     | 0     | RTT < 100ms, report generated |
| **Total**          | **21** | **21** | **0** | **0** |                               |

---

## 2. Testable with Mock vs Requires ESP32

| Feature                     | Mock ✅ | ESP32 Required         |
| --------------------------- | ------- | ---------------------- |
| MQTT pub/sub                | ✅      |                        |
| QoS 1 delivery              | ✅      |                        |
| LWT offline detection       | ✅      |                        |
| ACK + idempotency           | ✅      |                        |
| SET_MODE / SET_PHASE        | ✅      |                        |
| State publish (1s)          | ✅      |                        |
| Telemetry publish (5s)      | ✅      |                        |
| RTT benchmark               | ✅      |                        |
| Node-RED Dashboard          | ✅      |                        |
| Physical LED control        |         | ⚡ ESP32 + LEDs        |
| WiFi reconnect test         |         | ⚡ Real WiFi           |
| GPIO safety (no dual green) |         | ⚡ Oscilloscope verify |
| Power consumption           |         | ⚡ Multimeter          |

**Kết luận**: 90% chức năng có thể demo và test bằng mock, không cần phần cứng.

---

## 3. Rủi Ro Chính + Giảm Thiểu

| Rủi ro                 | Mức độ      | Giảm thiểu                                           |
| ---------------------- | ----------- | ---------------------------------------------------- |
| WiFi drop (ESP32)      | 🟡 Medium   | Auto-reconnect + fallback MODE_AUTO                  |
| MQTT broker down       | 🔴 High     | Docker restart policy `unless-stopped`, health check |
| Duplicate command      | 🟡 Medium   | Idempotency cache 32 cmd_ids trên ESP32              |
| Oversize payload       | 🟢 Low      | Max payload < 256 bytes, cJSON auto-limit            |
| LWT không fire         | 🟡 Medium   | Keep-alive 60s, clean session = true                 |
| Concurrent NS+EW green | 🔴 Critical | Safety rule hardcoded trong FSM, 2ms all-red guard   |
| Docker port conflict   | 🟢 Low      | Check `netstat` trước khi start                      |

---

## 4. Definition of Done

### DoD Software Demo (No ESP32)

| Criteria                                  | Status |
| ----------------------------------------- | ------ |
| Docker compose up thành công              | ✅     |
| Mock ESP32 publish state/telemetry/status | ✅     |
| Dashboard hiển thị đủ 4 groups            | ✅     |
| SET_MODE/SET_PHASE → ACK < 200ms          | ✅     |
| smoke_test.py exit code 0                 | ✅     |
| benchmark report generated                | ✅     |

### DoD Full Hardware

| Criteria                        | Status       |
| ------------------------------- | ------------ |
| ESP32 flash thành công (idf.py) | ⬜ Chưa test |
| 4 LED modules wired đúng pinmap | ⬜ Chưa test |
| Physical LED chuyển phase đúng  | ⬜ Chưa test |
| WiFi reconnect < 5s             | ⬜ Chưa test |
| 24h stress test no crash        | ⬜ Chưa test |
| RTT hardware < 100ms (p95)      | ⬜ Chưa test |
