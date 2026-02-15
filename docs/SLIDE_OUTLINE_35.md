# 🖥️ SLIDE OUTLINE — 35 Slides

> Outline thuyết trình NCKH: Hệ thống giám sát và điều khiển đèn giao thông qua MQTT

---

## PHẦN 1: MỞ ĐẦU (Slide 1–5)

### Slide 1: Title

- Tên đề tài (tiếng Việt + English)
- Logo trường, khoa
- Tên nhóm, GVHD
- Năm học

### Slide 2: Outline / Nội dung trình bày

- 6 phần chính + demo
- Thời gian dự kiến mỗi phần

### Slide 3: Vấn đề (Problem)

- Hệ thống đèn cố định, không giám sát được
- Không biết khi nào lỗi (offline)
- Khó điều chỉnh real-time
- 📸 Ảnh ngã tư thực tế (tìm ảnh minh họa)

### Slide 4: Mục tiêu (Objective)

- Xây dựng hệ thống điều khiển qua MQTT
- Đảm bảo tin cậy (QoS), an toàn (safety rules)
- Đo lường hiệu năng (RTT < 100ms)
- Giao diện giám sát trực quan (Node-RED)

### Slide 5: Phạm vi & Phương pháp

- 1 ngã tư, 4 hướng, 3 đèn mỗi hướng
- Mock + Hardware demo
- Thiết kế → Triển khai → Test → Đánh giá

---

## PHẦN 2: CƠ SỞ LÝ THUYẾT (Slide 6–10)

### Slide 6: Giao thức MQTT

- Publish/Subscribe model
- Lightweight, phù hợp IoT
- So sánh với HTTP, CoAP
- 📸 Sơ đồ pub/sub

### Slide 7: QoS Levels

- QoS 0: Fire-and-forget
- QoS 1: At-least-once (dùng cho cmd/ack)
- QoS 2: Exactly-once
- Bảng so sánh 3 level

### Slide 8: Last Will and Testament (LWT)

- Broker giữ "di chúc" khi client connect
- Client mất kết nối → broker tự publish
- Use case: phát hiện ESP32 offline
- 📸 Sequence diagram LWT

### Slide 9: ESP32 Microcontroller

- Dual-core, WiFi, BLE
- 34 GPIO pins
- ESP-IDF framework
- 📸 Hình ESP32 DevKit V1

### Slide 10: Docker & Node-RED

- Container hóa broker + dashboard
- Portable, reproducible
- Node-RED: visual programming cho IoT

---

## PHẦN 3: THIẾT KẾ HỆ THỐNG (Slide 11–17)

### Slide 11: Kiến trúc tổng quan

- 3 thành phần: ESP32 ↔ Mosquitto ↔ Node-RED
- 📸 **Cần sơ đồ**: Architecture diagram từ `ARCHITECTURE_OVERVIEW.md`

### Slide 12: MQTT Topic Tree

- 5 topics: cmd, ack, state, status, telemetry
- QoS và Retained cho mỗi topic
- 📸 Bảng topic tree từ `SPEC.md`

### Slide 13: Payload Schema — Command & ACK

- CMD: `{cmd_id, type, mode/phase, ts_ms}`
- ACK: `{cmd_id, ok, err, edge_recv_ts_ms}`
- Giải thích idempotency

### Slide 14: Payload Schema — State & Telemetry

- State (1s): `{mode, phase, ts_ms, uptime_s}`
- Telemetry (5s): `{rssi_dbm, heap_free_kb, uptime_s}`
- Status: `{online, ts_ms}` (retained)

### Slide 15: FSM (Finite State Machine)

- 4 modes: AUTO, MANUAL, BLINK, OFF
- 6 phases cycle
- Safety: no dual green
- 📸 **Cần sơ đồ**: FSM state diagram

### Slide 16: Sơ đồ phần cứng

- ESP32 + 4 LED modules (N, S, E, W)
- Pin mapping table
- 📸 **Cần sơ đồ**: Wiring diagram từ `WIRING.md`

### Slide 17: Safety Rules

- NS và EW không bao giờ cùng xanh
- All-red guard giữa phase transitions
- Fallback MODE_AUTO khi MQTT offline > 10s

---

## PHẦN 4: TRIỂN KHAI (Slide 18–23)

### Slide 18: Cấu trúc dự án

- Repo structure (tree)
- Docker services, ESP32 firmware, Python tools
- 📸 Terminal output `tree` hoặc repo screenshot

### Slide 19: Docker Infrastructure

- Mosquitto: auth, ACL, health check
- Node-RED: dashboard, flows.json
- docker-compose.yml
- 📸 Terminal: `docker compose ps`

### Slide 20: ESP32 Firmware Modules

- wifi_manager, mqtt_handler, fsm_controller, gpio_lights
- Kconfig menuconfig
- Build: `idf.py build flash monitor`

### Slide 21: Node-RED Dashboard

- Control: mode + phase dropdowns
- Intersection View: SVG 4-hướng
- Live status + Telemetry + ACK log
- 📸 **Cần chụp**: Dashboard UI screenshot

### Slide 22: Demo UI — Intersection View

- SVG traffic lights, 4 hướng
- Phase mapping N=S, E=W
- Real-time update khi state thay đổi
- 📸 **Cần chụp**: Intersection SVG close-up

### Slide 23: Testing Tools

- mock_esp32.py (simulate device)
- smoke_test.py (4 test cases)
- run_benchmark_report.py (RTT measurement)

---

## PHẦN 5: DEMO LIVE (Slide 24–27)

### Slide 24: Demo Setup

- Docker running → Mock ESP32 → Dashboard
- 1-click: `.\scripts\demo_up.ps1`

### Slide 25: Demo — SET_MODE

- AUTO → MANUAL transition
- Quan sát ACK + Mode change
- 📸 **Live demo**: Dashboard interaction

### Slide 26: Demo — SET_PHASE

- Phase 0 (NS Green) → Phase 3 (EW Green)
- Intersection SVG update
- 📸 **Live demo**: Intersection view change

### Slide 27: Demo — Safety & LWT

- Safety: NS+EW không cùng xanh
- LWT: stop mock → status OFFLINE
- Restart mock → status ONLINE
- 📸 **Live demo**: Status change

---

## PHẦN 6: THỬ NGHIỆM & ĐÁNH GIÁ (Slide 28–31)

### Slide 28: Benchmark Setup

- 100 requests, QoS 1
- Measure RTT (cmd → ack)
- Mock mode (LAN)

### Slide 29: Benchmark Results

- Mean RTT, P95, P99
- Delivery rate: 100%
- 📸 **Cần biểu đồ**: RTT histogram từ `logger/output/plots/`

### Slide 30: Smoke Test Results

- 4/4 PASS
- Broker connection, SET_MODE, SET_PHASE, ACK
- 📸 Bảng PASS/FAIL từ `VERIFICATION_REPORT.md`

### Slide 31: So sánh với yêu cầu

- SPEC.md requirements vs actual
- Bảng compliance check

---

## PHẦN 7: KẾT LUẬN (Slide 32–35)

### Slide 32: Kết luận (Conclusion)

- Đã xây dựng thành công hệ thống MQTT traffic light
- QoS 1 đảm bảo delivery, LWT phát hiện offline
- RTT < 100ms đáp ứng real-time
- Safety rules hoạt động đúng

### Slide 33: Hạn chế

- Chỉ test 1 ngã tư
- WiFi range limited
- Chưa có AI traffic optimization

### Slide 34: Hướng phát triển (Future Work)

- Multi-intersection network
- Camera AI + traffic density
- 5G/LoRa for wider coverage
- Cloud integration (AWS IoT / Azure)

### Slide 35: Q&A

- Thank you
- Contact info
- GitHub repo link
