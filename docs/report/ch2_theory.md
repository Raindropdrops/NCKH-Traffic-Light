# Chương 2: Cơ Sở Lý Thuyết

## 2.1 Tổng quan về Internet of Things (IoT)

**Internet of Things (IoT)** là mạng lưới các thiết bị vật lý được nhúng cảm biến, phần mềm và kết nối mạng, cho phép chúng thu thập và trao đổi dữ liệu. Trong lĩnh vực giao thông thông minh, IoT cho phép:

- Giám sát trạng thái thiết bị từ xa (remote monitoring)
- Thu thập dữ liệu telemetry liên tục (uptime, tín hiệu WiFi, bộ nhớ)
- Điều khiển thiết bị qua mạng (remote control)
- Phát hiện sự cố tự động (fault detection)

### Kiến trúc IoT 3 tầng

| Tầng                  | Vai trò                             | Ứng dụng trong đề tài        |
| --------------------- | ----------------------------------- | ---------------------------- |
| **Perception Layer**  | Thu thập dữ liệu, điều khiển vật lý | ESP32 + LED (đèn giao thông) |
| **Network Layer**     | Truyền dữ liệu                      | WiFi + MQTT protocol         |
| **Application Layer** | Xử lý, hiển thị, ra quyết định      | Dashboard web, Node-RED      |

## 2.2 Giao thức MQTT

### 2.2.1 Giới thiệu

**MQTT (Message Queuing Telemetry Transport)** là giao thức truyền thông nhắn nhẹ, hoạt động theo mô hình **Publish/Subscribe** thông qua một **broker** trung gian. MQTT được thiết kế bởi Andy Stanford-Clark (IBM) và Arlen Nipper (Cirrus Link) năm 1999 cho các thiết bị có băng thông thấp và tài nguyên hạn chế [1].

### 2.2.2 Mô hình Publish/Subscribe

Khác với mô hình Client-Server truyền thống (như HTTP), MQTT tách biệt bên gửi (Publisher) và bên nhận (Subscriber) thông qua broker:

```
Publisher ──► Broker ──► Subscriber(s)
                │
                ├── Topic: "city/demo/intersection/001/state"
                └── Topic: "city/demo/intersection/001/cmd"
```

**Ưu điểm**:

- Publisher không cần biết Subscriber là ai
- Một message có thể được gửi đến nhiều Subscriber cùng lúc
- Subscriber chỉ nhận message từ topic đã đăng ký
- Giảm coupling giữa các thành phần hệ thống

### 2.2.3 Quality of Service (QoS)

MQTT hỗ trợ 3 mức chất lượng dịch vụ:

| QoS Level | Tên gọi                        | Cơ chế                                  | Ứng dụng trong đề tài                     |
| :-------: | ------------------------------ | --------------------------------------- | ----------------------------------------- |
|   **0**   | At-most-once (Fire-and-forget) | Gửi 1 lần, không xác nhận               | `state` (1 msg/s), `telemetry` (1 msg/5s) |
|   **1**   | At-least-once                  | Gửi lại cho đến khi nhận PUBACK         | `cmd`, `ack`, `status` (critical)         |
|   **2**   | Exactly-once                   | 4-way handshake (PUBREC/PUBREL/PUBCOMP) | Không dùng (overhead cao)                 |

**Lý do chọn QoS trong đề tài:**

- `cmd` và `ack` dùng **QoS 1** vì mất lệnh điều khiển là không chấp nhận được.
- `state` dùng **QoS 0** vì gửi mỗi giây, mất 1 message không ảnh hưởng (message tiếp theo sẽ đến sau 1s).
- `status` dùng **QoS 1 + Retained** vì cần đảm bảo trạng thái online/offline luôn chính xác.

### 2.2.4 Last Will and Testament (LWT)

LWT là cơ chế cho phép broker phát hiện client mất kết nối đột ngột:

1. Client kết nối broker, đăng ký một "di chúc" (will message)
2. Client hoạt động bình thường, gửi PINGREQ định kỳ
3. Nếu client mất kết nối mà không gửi DISCONNECT → broker tự động publish will message
4. Các subscriber nhận được thông báo client đã offline

```
ESP32 connects → Will: {"online": false} on .../status (QoS 1, Retained)
                  │
ESP32 publishes → {"online": true} on .../status (QoS 1, Retained)
                  │
ESP32 mất điện → Broker auto-publishes: {"online": false}
                  │
Dashboard nhận → Hiển thị "ESP32 OFFLINE" (LWT)
```

**Ứng dụng**: Trong đề tài, dashboard tự động chuyển trạng thái sang "OFFLINE" khi ESP32 mất kết nối, không cần polling hay heartbeat riêng.

### 2.2.5 Retained Messages

Retained message là message được broker lưu lại và gửi ngay cho bất kỳ subscriber mới nào đăng ký topic đó. Trong đề tài, topic `status` sử dụng retained message để đảm bảo dashboard mở lên luôn biết trạng thái hiện tại (online/offline) mà không cần chờ ESP32 gửi lại.

### 2.2.6 So sánh MQTT với các giao thức IoT khác

| Tiêu chí              |       MQTT        |       HTTP       |        CoAP         |
| --------------------- | :---------------: | :--------------: | :-----------------: |
| **Mô hình**           | Publish/Subscribe | Request/Response |  Request/Response   |
| **Transport**         |        TCP        |       TCP        |         UDP         |
| **Header overhead**   |      2 bytes      |    ~700 bytes    |       4 bytes       |
| **QoS**               | 3 levels (0,1,2)  |     Không có     | Confirmable/Non-con |
| **Bi-directional**    |       ✅ Có       |    ❌ Polling    |     ✅ Observe      |
| **Offline detection** |      ✅ LWT       |     ❌ Không     |      ❌ Không       |
| **Retained state**    |       ✅ Có       |     ❌ Không     |      ❌ Không       |
| **Power consumption** |       Thấp        |       Cao        |      Rất thấp       |
| **Phù hợp IoT**       |    ⭐⭐⭐⭐⭐     |       ⭐⭐       |      ⭐⭐⭐⭐       |

**Kết luận**: MQTT được chọn cho đề tài vì header nhẹ (2 bytes), hỗ trợ QoS đa cấp, có LWT phát hiện offline, và Retained message — đây là các tính năng thiết yếu cho hệ thống giám sát và điều khiển đèn giao thông.

## 2.3 Vi điều khiển ESP32

### 2.3.1 Tổng quan

**ESP32** là vi điều khiển do Espressif Systems phát triển, được sử dụng rộng rãi trong các dự án IoT nhờ tích hợp sẵn WiFi và Bluetooth [2].

| Thông số  | Giá trị                            |
| --------- | ---------------------------------- |
| CPU       | Dual-core Xtensa LX6, 240 MHz      |
| RAM       | 520 KB SRAM                        |
| Flash     | 4 MB                               |
| WiFi      | 802.11 b/g/n, 2.4 GHz              |
| Bluetooth | v4.2 BR/EDR + BLE                  |
| GPIO      | 34 chân (lập trình được)           |
| ADC       | 18 kênh, 12-bit                    |
| Nguồn     | 3.3V, tiêu thụ ~80mA (WiFi active) |

### 2.3.2 ESP-IDF Framework

**ESP-IDF (Espressif IoT Development Framework)** là framework phát triển chính thức cho ESP32, cung cấp:

- FreeRTOS cho multi-tasking
- Driver WiFi, Bluetooth, GPIO
- MQTT client library (`esp_mqtt`)
- Hệ thống cấu hình `menuconfig` (Kconfig)
- OTA (Over-the-Air) update

Trong đề tài, ESP-IDF v5.5 được sử dụng thay vì Arduino framework vì cho phép kiểm soát tốt hơn bộ nhớ, task scheduling, và MQTT client.

## 2.4 Docker và Container hóa

### 2.4.1 Khái niệm

**Docker** là nền tảng container hóa cho phép đóng gói ứng dụng cùng với toàn bộ dependencies vào một container chạy độc lập [3]. Trong đề tài, Docker được sử dụng để triển khai:

| Service       | Image                     | Vai trò          |
| ------------- | ------------------------- | ---------------- |
| **Mosquitto** | `eclipse-mosquitto:2`     | MQTT broker      |
| **Node-RED**  | `nodered/node-red:latest` | Dashboard backup |

### 2.4.2 Lợi ích trong đề tài

- **Portable**: Toàn bộ infrastructure được định nghĩa trong `docker-compose.yml`, chạy được trên mọi máy tính.
- **Reproducible**: Đảm bảo broker cấu hình giống nhau ở mọi lần triển khai.
- **Isolated**: Mosquitto và Node-RED chạy trong network riêng, không ảnh hưởng hệ thống host.
- **Quick setup**: Chỉ cần `docker compose up -d` để khởi động toàn bộ infrastructure.

## 2.5 Mosquitto MQTT Broker

**Eclipse Mosquitto** là MQTT broker mã nguồn mở, nhẹ, hỗ trợ MQTT v3.1, v3.1.1, và v5.0 [4]. Trong đề tài, Mosquitto được cấu hình với:

- **Authentication**: Username/password (`demo`/`demo_pass`)
- **ACL (Access Control List)**: Phân quyền đọc/ghi theo topic
- **Persistence**: Lưu retained messages và session giữa các lần restart
- **WebSocket**: Hỗ trợ kết nối từ browser (port 9001)
- **Health check**: Kiểm tra broker hoạt động định kỳ

## 2.6 Tóm tắt chương

| Công nghệ     | Vai trò trong đề tài   | Lý do chọn                      |
| ------------- | ---------------------- | ------------------------------- |
| **MQTT**      | Giao thức truyền thông | Nhẹ, QoS đa cấp, LWT, Retained  |
| **ESP32**     | Thiết bị biên (edge)   | WiFi tích hợp, 34 GPIO, ESP-IDF |
| **Docker**    | Container hóa broker   | Portable, reproducible          |
| **Mosquitto** | MQTT broker            | Nhẹ, hỗ trợ auth/ACL/WebSocket  |
