# 📝 REPORT OUTLINE — Báo Cáo NCKH

> Bố cục báo cáo nghiên cứu khoa học: Hệ thống giám sát và điều khiển đèn giao thông qua MQTT

---

## Tóm Tắt (Abstract)

- Mục tiêu nghiên cứu (1-2 câu)
- Phương pháp: MQTT + ESP32 + Docker
- Kết quả chính: RTT < 100ms, QoS 1 đảm bảo delivery, LWT phát hiện offline
- Kết luận ngắn

---

## Chương 1: Mở Đầu

### 1.1 Lý do chọn đề tài

- Hạn chế hệ thống đèn giao thông truyền thống
- Xu hướng IoT trong giao thông thông minh

### 1.2 Mục tiêu nghiên cứu

- Xây dựng hệ thống điều khiển đèn giao thông qua MQTT
- Đo lường và đánh giá hiệu năng (RTT, reliability)

### 1.3 Phạm vi

- Demo 1 ngã tư (4 hướng), mock + hardware

### 1.4 Phương pháp

- Thiết kế hệ thống → Triển khai → Thử nghiệm → Đánh giá

---

## Chương 2: Cơ Sở Lý Thuyết

### 2.1 Giao thức MQTT

- Publish/Subscribe model
- QoS Levels (0, 1, 2) — giải thích chi tiết QoS 0 vs 1
- Last Will and Testament (LWT)
- Retained messages

> 📊 **Bảng**: So sánh MQTT vs HTTP vs CoAP → lấy từ tài liệu tham khảo

### 2.2 ESP32 và IoT

- Kiến trúc ESP32, WiFi, GPIO
- ESP-IDF vs Arduino framework

### 2.3 Docker và Microservices

- Container hóa Mosquitto + Node-RED
- Lợi ích: portable, reproducible

---

## Chương 3: Thiết Kế Hệ Thống

### 3.1 Kiến trúc tổng quan

> 📊 **Hình**: Sơ đồ kiến trúc → lấy từ `docs/ARCHITECTURE_OVERVIEW.md`

### 3.2 MQTT Topic Tree

> 📊 **Bảng**: Topic tree + QoS + Retained → lấy từ `SPEC.md` Section 4

```
city/demo/intersection/001/
├── cmd        (Sub, QoS1)
├── ack        (Pub, QoS1)
├── status     (Pub, QoS1, Retained)
├── state      (Pub, QoS0)
└── telemetry  (Pub, QoS0)
```

### 3.3 Payload Schema

> 📊 **Bảng**: JSON schema cho mỗi topic → lấy từ `SPEC.md` Section 5

### 3.4 FSM (Finite State Machine)

- 4 modes: AUTO, MANUAL, BLINK, OFF
- 6 phases: NS_GREEN → NS_YELLOW → ALL_RED → EW_GREEN → EW_YELLOW → ALL_RED
- Safety rule: không bao giờ 2 hướng cùng xanh

### 3.5 Sơ đồ phần cứng

> 📊 **Hình**: Wiring diagram → lấy từ `docs/WIRING.md`

---

## Chương 4: Triển Khai

### 4.1 Môi trường phát triển

- Windows + Docker Desktop + ESP-IDF
- Python tools (mock, smoke test, benchmark)

### 4.2 Docker Infrastructure

- Mosquitto config (auth, ACL)
- Node-RED Dashboard

### 4.3 ESP32 Firmware

- Modules: wifi_manager, mqtt_handler, fsm_controller, gpio_lights
- Kconfig menuconfig

### 4.4 Node-RED Dashboard

> 📊 **Ảnh chụp**: Dashboard UI → chụp từ http://localhost:1880/ui

### 4.5 Testing Tools

- mock_esp32.py, smoke_test.py, run_benchmark_report.py

---

## Chương 5: Thử Nghiệm & Đánh Giá

### 5.1 Thiết lập thử nghiệm

- Mock mode vs Hardware mode
- Metrics: RTT, delivery rate, offline detection time

### 5.2 Kết quả Benchmark

> 📊 **Bảng + Biểu đồ**: RTT statistics → lấy từ `logger/output/report.md` và `summary.csv`
> 📊 **Hình**: RTT histogram → lấy từ `logger/output/plots/`

### 5.3 Smoke Test Results

> 📊 **Bảng**: Pass/Fail → lấy từ `VERIFICATION_REPORT.md`

### 5.4 Đánh giá

- So sánh với yêu cầu trong SPEC.md
- Hạn chế

---

## Chương 6: Kết Luận & Hướng Phát Triển

### 6.1 Kết luận

- Đạt được mục tiêu: điều khiển real-time qua MQTT
- RTT < 100ms, QoS 1 reliable, LWT hoạt động

### 6.2 Hướng phát triển

- Multi-intersection (pub/sub scale)
- Machine learning traffic optimization
- 5G/LoRa thay WiFi
- Tích hợp camera AI

---

## Tài Liệu Tham Khảo

**Format**: IEEE (số thứ tự [1], [2], ...)

Gợi ý:

1. OASIS MQTT v5.0 Specification
2. Espressif ESP-IDF Documentation
3. Eclipse Mosquitto Documentation
4. Node-RED Documentation
5. Docker Documentation
6. Các bài báo IoT traffic light (IEEE Xplore, Google Scholar)

> ⚠️ Kiểm tra file "Trinh bay tai lieu tham khao.doc" nếu có trong repo để follow đúng format yêu cầu.
