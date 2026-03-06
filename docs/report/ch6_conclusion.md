# Chương 6: Kết Luận và Hướng Phát Triển

## 6.1 Kết luận

Đề tài **"Nghiên cứu ứng dụng IoT – MQTT trong giám sát và điều khiển từ xa hệ thống đèn tín hiệu giao thông"** đã đạt được các mục tiêu đề ra:

### Mục tiêu 1: Xây dựng hệ thống giám sát và điều khiển từ xa

- Đã thiết kế và triển khai hệ thống hoàn chỉnh gồm: ESP32 firmware (4 module), Mosquitto MQTT broker (Docker), và Web Dashboard (standalone HTML).
- Hệ thống hỗ trợ 4 chế độ điều khiển (AUTO, MANUAL, BLINK, OFF), 6 phase chu kỳ đèn, và các quy tắc an toàn (không 2 hướng cùng xanh, ALL_RED guard).
- Dashboard web giám sát real-time: SVG ngã tư, telemetry (RSSI, heap), ACK log, và các công cụ phân tích (RTT chart, QoS indicator, LWT log).

### Mục tiêu 2: Đánh giá hiệu quả và độ trễ

Kết quả benchmark với 500 messages × 6 payload sizes cho thấy:

| Chỉ số              | Kết quả                       |
| ------------------- | ----------------------------- |
| RTT trung bình      | **43.3ms** (yêu cầu < 100ms)  |
| P95                 | **45ms**                      |
| Delivery rate       | **100%** (QoS 1)              |
| Oversize protection | Hoạt động đúng (reject > 1KB) |
| LWT detection       | Hoạt động đúng                |

RTT ổn định bất kể payload size (0B–900B), chứng tỏ **MQTT overhead chủ yếu từ TCP + QoS handshake**, không phải từ kích thước dữ liệu.

### Mục tiêu 3: Đề xuất giải pháp mở rộng

Hệ thống đã được thiết kế sẵn cho mở rộng thông qua cấu trúc topic phân cấp `city/{city_id}/intersection/{id}/...`. Các giải pháp mở rộng cụ thể được đề xuất tại mục 6.2.

## 6.2 Hướng phát triển

### 6.2.1 Mở rộng quy mô (Scalability)

| Giải pháp              | Mô tả                              | Trade-off                                        |
| ---------------------- | ---------------------------------- | ------------------------------------------------ |
| **Multi-intersection** | Mỗi ngã tư là 1 ESP32, cùng broker | Topic tree đã hỗ trợ, cần load testing           |
| **Broker Bridge**      | Mosquitto bridge giữa các khu vực  | Tăng RTT inter-region, giảm tải broker trung tâm |
| **Broker Cluster**     | Multiple broker với load balancing | Phức tạp hóa infrastructure                      |
| **QoS Trade-off**      | QoS 0 cho state, QoS 1 cho cmd/ack | Giảm overhead khi số lượng lớn                   |

### 6.2.2 Cải thiện bảo mật

| Giải pháp                  | Mô tả                                               |
| -------------------------- | --------------------------------------------------- |
| **TLS/mTLS**               | Mã hóa kết nối MQTT (ước tính +5-20ms RTT)          |
| **Certificate-based auth** | Xác thực thiết bị bằng certificate thay vì password |
| **ACL chi tiết**           | Mỗi ESP32 chỉ publish/subscribe topic của mình      |

### 6.2.3 Tích hợp công nghệ tiên tiến

| Công nghệ        | Ứng dụng                                                  | Khả thi  |
| ---------------- | --------------------------------------------------------- | :------: |
| **Camera AI**    | Nhận diện mật độ giao thông, tự điều chỉnh thời gian xanh |  ⭐⭐⭐  |
| **LoRa/5G**      | Thay WiFi cho phạm vi rộng hơn                            |  ⭐⭐⭐  |
| **Cloud IoT**    | AWS IoT Core / Azure IoT Hub thay Mosquitto local         | ⭐⭐⭐⭐ |
| **Edge AI**      | ESP32-S3 chạy TinyML phân tích traffic                    |   ⭐⭐   |
| **Digital Twin** | Mô hình số hóa cả mạng lưới giao thông                    |   ⭐⭐   |

### 6.2.4 Ứng dụng vào đô thị thông minh

Hệ thống có thể tích hợp vào kiến trúc Smart City platform:

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ Intersection │     │ Intersection │     │ Intersection │
│   ESP32 #1   │     │   ESP32 #2   │     │   ESP32 #N   │
└──────┬───────┘     └──────┬───────┘     └──────┬───────┘
       │ MQTT               │ MQTT               │ MQTT
       └────────────────────┼────────────────────┘
                            │
                    ┌───────┴───────┐
                    │  City Broker  │
                    │  (Cluster)    │
                    └───────┬───────┘
                            │
              ┌─────────────┼─────────────┐
              │             │             │
       ┌──────┴──┐   ┌──────┴──┐   ┌──────┴──┐
       │Dashboard│   │  AI     │   │  Data   │
       │  Center │   │ Engine  │   │  Lake   │
       └─────────┘   └─────────┘   └─────────┘
```

---

# Tài Liệu Tham Khảo

[1] OASIS, "MQTT Version 5.0 Specification," OASIS Standard, Mar. 2019. [Online]. Available: https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html

[2] Espressif Systems, "ESP32 Technical Reference Manual," Version 5.1, 2024. [Online]. Available: https://www.espressif.com/en/products/socs/esp32

[3] Espressif Systems, "ESP-IDF Programming Guide," Version 5.5, 2025. [Online]. Available: https://docs.espressif.com/projects/esp-idf/en/v5.5/

[4] Eclipse Foundation, "Eclipse Mosquitto — An open source MQTT broker," 2024. [Online]. Available: https://mosquitto.org/

[5] Docker Inc., "Docker Documentation," 2024. [Online]. Available: https://docs.docker.com/

[6] Node-RED, "Node-RED: Low-code programming for event-driven applications," 2024. [Online]. Available: https://nodered.org/

[7] S. Lee and S. Kim, "IoT-based Smart Traffic Light Control System using MQTT Protocol," in _IEEE International Conference on Internet of Things_, 2022, pp. 145-150.

[8] A. Al-Fuqaha, M. Guizani, M. Mohammadi, M. Aledhari, and M. Ayyash, "Internet of Things: A Survey on Enabling Technologies, Protocols, and Applications," _IEEE Communications Surveys & Tutorials_, vol. 17, no. 4, pp. 2347-2376, 2015.

[9] N. Naik, "Choice of Effective Messaging Protocols for IoT Systems: MQTT, CoAP, AMQP and HTTP," in _IEEE International Systems Engineering Symposium_, 2017, pp. 1-7.

[10] D. Soni and A. Makwana, "A Survey on MQTT: A Protocol of Internet of Things," in _International Conference on Telecommunication, Power Analysis and Computing Techniques_, 2017, pp. 1-5.

[11] R. A. Light, "Mosquitto: server and client implementation of the MQTT protocol," _Journal of Open Source Software_, vol. 2, no. 13, p. 265, 2017.

[12] Paho Project, "Eclipse Paho MQTT Python Client," Eclipse Foundation, 2024. [Online]. Available: https://github.com/eclipse/paho.mqtt.python
