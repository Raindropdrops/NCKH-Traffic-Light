# Chương 4: Triển Khai

## 4.1 Môi trường phát triển

| Thành phần     | Phiên bản | Vai trò                   |
| -------------- | --------- | ------------------------- |
| Windows 11     | 24H2      | Hệ điều hành phát triển   |
| Docker Desktop | 4.x       | Container runtime         |
| ESP-IDF        | 5.5       | Framework firmware ESP32  |
| Python         | 3.11+     | Testing tools, mock ESP32 |
| VS Code        | Latest    | IDE phát triển            |
| Git            | 2.x       | Quản lý mã nguồn          |

### Cấu trúc thư mục dự án

```
traffic-mqtt-demo/
├── esp32_idf/              # Firmware ESP32 (ESP-IDF)
│   ├── main/
│   │   ├── main.c          # Entry point
│   │   ├── wifi_manager.*  # Quản lý kết nối WiFi
│   │   ├── mqtt_handler.*  # MQTT client, LWT, subscribe
│   │   ├── fsm_controller.*# FSM logic, phase cycling
│   │   └── gpio_lights.*   # Điều khiển LED output
│   └── CMakeLists.txt
├── docker/                 # Docker configuration
│   └── mosquitto/
│       ├── mosquitto.conf  # Broker config (auth, ACL, WS)
│       └── password_file   # User credentials
├── dashboard/
│   └── index.html          # Web dashboard (standalone)
├── logger/tools/           # Python testing tools
│   ├── mock_esp32.py       # ESP32 simulator
│   ├── smoke_test.py       # 4-scenario integration test
│   ├── run_benchmark_report.py  # RTT benchmark
│   └── logger.py           # MQTT message logger
├── docker-compose.yml      # Infrastructure as Code
├── SPEC.md                 # Đặc tả kỹ thuật (LOCKED)
└── docs/                   # Tài liệu
```

## 4.2 Docker Infrastructure

### 4.2.1 Docker Compose

File `docker-compose.yml` định nghĩa toàn bộ infrastructure:

```yaml
services:
  mosquitto:
    image: eclipse-mosquitto:2
    ports:
      - "1883:1883" # MQTT
      - "9001:9001" # WebSocket (cho dashboard)
    volumes:
      - ./docker/mosquitto/mosquitto.conf:/mosquitto/config/mosquitto.conf
    healthcheck:
      test: ["CMD", "mosquitto_pub", "-u", "demo", "-P", "demo_pass", ...]
      interval: 10s

  nodered:
    image: nodered/node-red:latest
    ports:
      - "1880:1880"
    volumes:
      - ./dashboard:/data/public # Serve dashboard files
```

### 4.2.2 Cấu hình Mosquitto

Mosquitto được cấu hình với các tính năng bảo mật:

| Tính năng              | Cấu hình           | Mục đích                          |
| ---------------------- | ------------------ | --------------------------------- |
| **Authentication**     | `password_file`    | Ngăn truy cập trái phép           |
| **Listener MQTT**      | Port 1883          | Kết nối từ ESP32                  |
| **Listener WebSocket** | Port 9001          | Kết nối từ Dashboard browser      |
| **Persistence**        | `persistence true` | Giữ retained messages qua restart |
| **Logging**            | `log_dest file`    | Ghi log debug/info                |

## 4.3 ESP32 Firmware

### 4.3.1 Module Architecture

Firmware được chia thành 4 module độc lập:

| Module             | File                 | Chức năng                                  |
| ------------------ | -------------------- | ------------------------------------------ |
| **wifi_manager**   | `wifi_manager.c/h`   | Kết nối WiFi, auto-reconnect               |
| **mqtt_handler**   | `mqtt_handler.c/h`   | MQTT client, LWT setup, subscribe, publish |
| **fsm_controller** | `fsm_controller.c/h` | FSM logic: mode, phase, cycling, safety    |
| **gpio_lights**    | `gpio_lights.c/h`    | Điều khiển 6 GPIO → 12 LED                 |

### 4.3.2 Luồng hoạt động chính

```
main() → wifi_init() → mqtt_init() → xTaskCreate(fsm_task)
                                          │
                            ┌──────────────┴──────────────┐
                            │         fsm_task             │
                            │  loop:                       │
                            │    if AUTO → auto_cycle()    │
                            │    update_gpio(phase)        │
                            │    publish_state()           │
                            │    if 5s elapsed:            │
                            │      publish_telemetry()     │
                            │    sleep(1s)                 │
                            └──────────────────────────────┘
```

### 4.3.3 Xử lý lệnh (Command Handler)

Khi nhận message trên topic `cmd`:

1. Parse JSON → lấy `cmd_id`, `type`, `mode`/`phase`
2. Kiểm tra idempotency: nếu `cmd_id` đã có trong cache → bỏ qua
3. Thực thi lệnh: `SET_MODE` → thay đổi mode, `SET_PHASE` → thay đổi phase
4. Lưu `cmd_id` vào cache (deque 32 phần tử)
5. Publish `ack` với `ok: true` hoặc `ok: false` + `err`

## 4.4 Mock ESP32 Simulator

Trong giai đoạn phát triển, **mock_esp32.py** mô phỏng hoàn chỉnh firmware ESP32:

| Tính năng                  | Mô tả                                  |
| -------------------------- | -------------------------------------- |
| MQTT connect + LWT         | Giống firmware thật                    |
| State publishing (1 msg/s) | Mode, phase, uptime                    |
| Telemetry (1 msg/5s)       | RSSI drift (-1dBm/5min), heap giảm dần |
| Command handler + ACK      | Idempotent, deque cache 32             |
| AUTO phase cycling         | 6 phase, configurable duration         |
| BLINK / OFF mode           | ALL_RED toggle / all off               |
| `--speed` flag             | Tăng tốc cycle cho demo (2x, 3x)       |
| `--ack_delay_ms`           | Thêm delay ACK cho benchmark RTT       |

Lệnh chạy:

```bash
python mock_esp32.py --host 127.0.0.1 --speed 2
```

## 4.5 Web Dashboard

### 4.5.1 Kiến trúc

Dashboard là file HTML standalone, kết nối MQTT qua WebSocket trực tiếp (không cần backend):

```
Browser ──► mqtt.min.js ──► WebSocket ws://host:9001 ──► Mosquitto
```

### 4.5.2 Các thành phần giao diện

| Thành phần               | Chức năng                                           |
| ------------------------ | --------------------------------------------------- |
| **Control Panel**        | 4 nút mode (AUTO/MANUAL/BLINK/OFF) + dropdown phase |
| **Intersection View**    | SVG ngã tư 4 hướng, glow effect khi đèn sáng        |
| **Live Status**          | Mode, Phase, Uptime, Last Update                    |
| **Telemetry**            | RSSI (dBm), Heap Free (KB), Device Uptime           |
| **RTT Realtime Chart**   | Biểu đồ line canvas, hiển thị Mean/Min/Max/Last     |
| **QoS Indicator**        | Hiển thị QoS level từng topic với giải thích        |
| **Connection Log (LWT)** | Lịch sử online/offline với timestamps               |
| **ACK Log**              | Danh sách ACK nhận được (✅/❌, cmd_id, thời gian)  |

## 4.6 Testing Tools

### 4.6.1 Smoke Test (`smoke_test.py`)

4 kịch bản kiểm tra tự động:

|  #  | Kịch bản          | Mô tả                  | Pass criteria            |
| :-: | ----------------- | ---------------------- | ------------------------ |
|  1  | Broker Connection | Kết nối MQTT broker    | Connected trong 5s       |
|  2  | SET_MODE MANUAL   | Gửi cmd, nhận ack      | ACK ok=true, RTT < 500ms |
|  3  | SET_PHASE 3       | Chuyển phase, nhận ack | ACK ok=true              |
|  4  | Cleanup AUTO      | Về AUTO mode           | ACK ok=true              |

### 4.6.2 Benchmark (`run_benchmark_report.py`)

Đo RTT với nhiều kích thước payload:

- Gửi N messages (mặc định 500) với payload padding
- Đo thời gian cmd → ack cho mỗi message
- Tự động tạo report với histogram, ECDF, comparison chart
- Export CSV cho phân tích tiếp
