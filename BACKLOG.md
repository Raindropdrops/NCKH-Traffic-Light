# BACKLOG.md — Work Breakdown Structure
>
> **Đề tài NCKH:** IoT–MQTT Giám sát & Điều khiển Đèn Giao Thông
> **Scope:** ESP32 (Scope 1)

---

## WP0: Project Setup & Environment

### WP0.1 — Development Environment Setup

| Field | Value |
|-------|-------|
| **Mô tả** | Cài đặt môi trường phát triển: PlatformIO, Docker, Python venv |
| **Output** | `README.md` với hướng dẫn setup, `.env.example` |
| **DONE khi** | Clone repo → chạy script → môi trường sẵn sàng trong < 10 phút |
| **Phụ thuộc** | Không |

### WP0.2 — Mosquitto Broker Deployment

| Field | Value |
|-------|-------|
| **Mô tả** | Deploy Mosquitto broker via Docker hoặc native |
| **Output** | `docker-compose.yml`, `mosquitto.conf` |
| **DONE khi** | `mosquitto_sub -t test` nhận được message từ `mosquitto_pub` |
| **Phụ thuộc** | WP0.1 |

### WP0.3 — Repository Structure

| Field | Value |
|-------|-------|
| **Mô tả** | Tạo folder structure theo convention |
| **Output** | Folders: `esp32/`, `node-red/`, `logger/`, `docs/` |
| **DONE khi** | Cấu trúc folder match với SPEC architecture |
| **Phụ thuộc** | WP0.1 |

---

## WP1: ESP32 Firmware Core

### WP1.1 — MQTT Client Connection

| Field | Value |
|-------|-------|
| **Mô tả** | Implement MQTT client với auto-reconnect, LWT setup |
| **Output** | `esp32/src/mqtt_client.cpp`, `mqtt_client.h` |
| **DONE khi** | ESP32 connect broker, publish LWT, auto-reconnect sau 5s disconnect |
| **Phụ thuộc** | WP0.2 |

### WP1.2 — FSM State Machine

| Field | Value |
|-------|-------|
| **Mô tả** | Implement Finite State Machine cho traffic light phases |
| **Output** | `esp32/src/fsm.cpp`, `fsm.h` |
| **DONE khi** | FSM cycle qua 6 phases đúng timing, tuân thủ ALL_RED rule |
| **Phụ thuộc** | WP0.3 |

### WP1.3 — Command Handler

| Field | Value |
|-------|-------|
| **Mô tả** | Parse JSON cmd, validate, execute, send ack |
| **Output** | `esp32/src/cmd_handler.cpp`, `cmd_handler.h` |
| **DONE khi** | Nhận cmd → parse → execute → publish ack trong < 100ms |
| **Phụ thuộc** | WP1.1, WP1.2 |

### WP1.4 — State Publisher

| Field | Value |
|-------|-------|
| **Mô tả** | Publish state mỗi 1s theo JSON schema |
| **Output** | `esp32/src/state_publisher.cpp` |
| **DONE khi** | State message match SPEC schema, interval đúng 1000ms ± 50ms |
| **Phụ thuộc** | WP1.1, WP1.2 |

### WP1.5 — Telemetry Publisher

| Field | Value |
|-------|-------|
| **Mô tả** | Publish telemetry (RSSI, heap, uptime) mỗi 5s |
| **Output** | `esp32/src/telemetry.cpp` |
| **DONE khi** | Telemetry message valid JSON, values realistic |
| **Phụ thuộc** | WP1.1 |

### WP1.6 — Safety Module

| Field | Value |
|-------|-------|
| **Mô tả** | Implement safety rules: single green, ALL_RED, MQTT timeout |
| **Output** | `esp32/src/safety.cpp`, `safety.h` |
| **DONE khi** | Unit test pass cho mọi safety rule, violation → BLINK mode |
| **Phụ thuộc** | WP1.2 |

### WP1.7 — Command Idempotency Cache

| Field | Value |
|-------|-------|
| **Mô tả** | Cache 32 cmd_id gần nhất, reject duplicate |
| **Output** | `esp32/src/cmd_cache.cpp` |
| **DONE khi** | Duplicate cmd_id → ok=true, không re-execute |
| **Phụ thuộc** | WP1.3 |

### WP1.8 — LED Output Driver

| Field | Value |
|-------|-------|
| **Mô tả** | GPIO control cho LED matrix 2 hướng x 3 màu |
| **Output** | `esp32/src/led_driver.cpp`, `led_driver.h` |
| **DONE khi** | LED states match FSM phase, no glitches |
| **Phụ thuộc** | WP0.3 |

---

## WP2: Node-RED Dashboard

### WP2.1 — Flow Import & MQTT Nodes

| Field | Value |
|-------|-------|
| **Mô tả** | Setup Node-RED, configure MQTT-in/out nodes |
| **Output** | `node-red/flows.json` |
| **DONE khi** | Node-RED subscribe state, publish cmd thành công |
| **Phụ thuộc** | WP0.2 |

### WP2.2 — Dashboard UI - Status Panel

| Field | Value |
|-------|-------|
| **Mô tả** | Hiển thị mode, phase, uptime, online status |
| **Output** | Updated `flows.json` |
| **DONE khi** | UI update realtime khi state thay đổi |
| **Phụ thuộc** | WP2.1 |

### WP2.3 — Dashboard UI - Control Panel

| Field | Value |
|-------|-------|
| **Mô tả** | Buttons: SET_MODE, SET_PHASE, EMERGENCY |
| **Output** | Updated `flows.json` |
| **DONE khi** | Click button → cmd published → ack displayed |
| **Phụ thuộc** | WP2.2 |

### WP2.4 — Dashboard UI - Traffic Light Visualization

| Field | Value |
|-------|-------|
| **Mô tả** | SVG/Canvas visualization của đèn giao thông |
| **Output** | `node-red/ui_templates/traffic_light.html` |
| **DONE khi** | Visualization match current phase realtime |
| **Phụ thuộc** | WP2.2 |

### WP2.5 — Dashboard UI - Telemetry Charts

| Field | Value |
|-------|-------|
| **Mô tả** | Line charts cho RSSI, heap over time |
| **Output** | Updated `flows.json` |
| **DONE khi** | Charts update với telemetry data, 5 min window |
| **Phụ thuộc** | WP2.1 |

---

## WP3: Python Logger

### WP3.1 — MQTT Subscriber

| Field | Value |
|-------|-------|
| **Mô tả** | Subscribe all topics dưới base prefix |
| **Output** | `logger/mqtt_subscriber.py` |
| **DONE khi** | Receive messages từ tất cả 5 topics |
| **Phụ thuộc** | WP0.2 |

### WP3.2 — JSONL File Writer

| Field | Value |
|-------|-------|
| **Mô tả** | Ghi mỗi message thành 1 line JSON vào file |
| **Output** | `logger/file_writer.py`, output: `logs/YYYY-MM-DD.jsonl` |
| **DONE khi** | File rotate daily, mỗi line là valid JSON |
| **Phụ thuộc** | WP3.1 |

### WP3.3 — Log Rotation & Cleanup

| Field | Value |
|-------|-------|
| **Mô tả** | Giữ logs 7 ngày, delete cũ hơn |
| **Output** | `logger/log_rotation.py` |
| **DONE khi** | Chạy 8 ngày → chỉ còn 7 files |
| **Phụ thuộc** | WP3.2 |

### WP3.4 — Startup Script

| Field | Value |
|-------|-------|
| **Mô tả** | Script để chạy logger như service |
| **Output** | `logger/run.py`, `requirements.txt` |
| **DONE khi** | `python run.py` chạy continuous, graceful shutdown |
| **Phụ thuộc** | WP3.1, WP3.2, WP3.3 |

### WP3.5 — RTT Benchmark Tool (cmd→ack)

| Field | Value |
|-------|-------|
| **Mô tả** | Tool đo RTT (Round-Trip Time) từ cmd → ack cho mục tiêu nghiên cứu |
| **Output** | `logger/tools/bench_rtt.py`, `logger/tools/analyze_results.py`, `logger/requirements.txt` (updated) |
| **DONE khi** | Chạy 500 lệnh → xuất CSV với columns: cmd_id, send_ts, recv_ts, rtt_ms. `analyze_results.py` in mean/median/p95/max/loss_rate. |
| **Phụ thuộc** | WP3.1, WP1.3 |

---

## WP4: Integration Testing

### WP4.1 — ESP32 ↔ Broker Connection Test

| Field | Value |
|-------|-------|
| **Mô tả** | Verify ESP32 kết nối, publish, subscribe |
| **Output** | `tests/test_esp32_mqtt.py` |
| **DONE khi** | Test script pass: connect, pub/sub, LWT |
| **Phụ thuộc** | WP1.1 |

### WP4.2 — Command → Ack Round Trip

| Field | Value |
|-------|-------|
| **Mô tả** | Đo latency cmd → ack sử dụng RTT benchmark tool, verify < 500ms |
| **Output** | `tests/test_cmd_ack.py` (wrapper cho `bench_rtt.py`), `results/rtt_benchmark.csv` |
| **DONE khi** | 500 commands via `bench_rtt.py` → `analyze_results.py` xuất: mean < 200ms, p95 < 500ms, loss_rate < 1% |
| **Phụ thuộc** | WP1.3, WP2.3, **WP3.5** |

### WP4.3 — Safety Rule Verification

| Field | Value |
|-------|-------|
| **Mô tả** | Test từng safety rule: single green, ALL_RED, timeout |
| **Output** | `tests/test_safety.py` |
| **DONE khi** | Mỗi rule có test case, all pass |
| **Phụ thuộc** | WP1.6 |

### WP4.4 — MQTT Disconnect Recovery

| Field | Value |
|-------|-------|
| **Mô tả** | Test ESP32 behavior khi mất broker |
| **Output** | `tests/test_disconnect.py` |
| **DONE khi** | Disconnect 10s → AUTO mode, reconnect → state publish |
| **Phụ thuộc** | WP1.1, WP1.6 |

### WP4.5 — End-to-End Smoke Test

| Field | Value |
|-------|-------|
| **Mô tả** | Full flow: dashboard → cmd → ESP32 → ack → UI update |
| **Output** | `tests/test_e2e.py` |
| **DONE khi** | Automated E2E pass, manual verification OK |
| **Phụ thuộc** | WP1.*, WP2.*, WP3.* |

---

## WP5: Documentation

### WP5.1 — API Documentation

| Field | Value |
|-------|-------|
| **Mô tả** | Document tất cả MQTT topics, payloads |
| **Output** | `docs/API.md` |
| **DONE khi** | Doc match SPEC, có examples |
| **Phụ thuộc** | WP1.* |

### WP5.2 — Hardware Wiring Guide

| Field | Value |
|-------|-------|
| **Mô tả** | Sơ đồ đấu nối ESP32 → LED matrix |
| **Output** | `docs/WIRING.md`, `docs/wiring_diagram.png` |
| **DONE khi** | Team member mới đọc → đấu được |
| **Phụ thuộc** | WP1.8 |

### WP5.3 — User Manual

| Field | Value |
|-------|-------|
| **Mô tả** | Hướng dẫn sử dụng dashboard |
| **Output** | `docs/USER_MANUAL.md` |
| **DONE khi** | Non-technical user đọc → dùng được dashboard |
| **Phụ thuộc** | WP2.* |

### WP5.4 — Deployment Guide

| Field | Value |
|-------|-------|
| **Mô tả** | Steps deploy Mosquitto, Node-RED, Logger production |
| **Output** | `docs/DEPLOYMENT.md` |
| **DONE khi** | Fresh server → deploy thành công theo guide |
| **Phụ thuộc** | WP0.*, WP2.*, WP3.* |

---

## WP6: Demo & Presentation

### WP6.1 — Demo Script

| Field | Value |
|-------|-------|
| **Mô tả** | Kịch bản demo 5 phút cho NCKH |
| **Output** | `docs/DEMO_SCRIPT.md` |
| **DONE khi** | Script rõ ràng, practiced, timing OK |
| **Phụ thuộc** | WP4.5 |

### WP6.2 — Video Recording

| Field | Value |
|-------|-------|
| **Mô tả** | Record video demo hoạt động của system |
| **Output** | `docs/demo_video.mp4` hoặc YouTube link |
| **DONE khi** | Video clear, shows all features, < 3 min |
| **Phụ thuộc** | WP6.1 |

### WP6.3 — Poster/Slides

| Field | Value |
|-------|-------|
| **Mô tả** | Poster hoặc slides cho báo cáo NCKH |
| **Output** | `docs/NCKH_Poster.pdf` hoặc `slides.pptx` |
| **DONE khi** | Review bởi mentor, approved |
| **Phụ thuộc** | WP5.*, WP6.1 |

---

## Dependency Graph

```
WP0.1 ─────┬───► WP0.2 ───────────────────────────────────────┐
           │                                                   │
           └───► WP0.3 ───┬───► WP1.2 ───► WP1.6 ◄───┐        │
                          │         │           │     │        │
                          │         ▼           ▼     │        │
                          │    WP1.8      WP1.3 ◄─────┤        │
                          │                  │        │        │
                          │                  ▼        │        │
                          │              WP1.7        │        │
                          │                           │        │
                          └───────────────────────────┼────────┼───► WP1.1
                                                      │        │        │
                                                      │        │        ▼
                                                      │        │    WP1.4, WP1.5
                                                      │        │
                    WP2.1 ◄───────────────────────────┼────────┘
                       │                              │
                       ▼                              │
                    WP2.2 ───► WP2.3 ───► WP2.4      │
                       │                              │
                       ▼                              │
                    WP2.5                             │
                                                      │
                    WP3.1 ◄───────────────────────────┘
                       │
                       ▼
                    WP3.2 ───► WP3.3
                       │
                       ▼
                    WP3.4

                    WP4.* (depends on WP1.*, WP2.*, WP3.*)
                       │
                       ▼
                    WP5.* (depends on implementation)
                       │
                       ▼
                    WP6.* (depends on WP4.5, WP5.*)
```

---

## Priority Matrix

| Priority | Work Packages | Rationale |
|----------|--------------|-----------|
| **P0** | WP0.*, WP1.1, WP1.2 | Foundation, không có thì không chạy được gì |
| **P1** | WP1.3-WP1.8 | Core functionality |
| **P2** | WP2.*, WP3.* | User interface & logging |
| **P3** | WP4.* | Verification |
| **P4** | WP5.*, WP6.* | Documentation & demo |

---

## Estimated Effort

| WP | Tasks | Est. Hours | Owner |
|----|-------|------------|-------|
| WP0 | 3 | 4h | DevOps/All |
| WP1 | 8 | 24h | Embedded Dev |
| WP2 | 5 | 12h | Frontend Dev |
| WP3 | 5 | 8h | Backend Dev |
| WP4 | 5 | 10h | QA/All |
| WP5 | 4 | 8h | All |
| WP6 | 3 | 6h | All |
| **Total** | **33** | **72h** | |

---

> **⚠️ BACKLOG này cần được update khi có thay đổi scope. Mọi task mới phải có đủ 4 fields: Mô tả, Output, DONE khi, Phụ thuộc.**
