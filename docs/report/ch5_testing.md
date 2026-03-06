# Chương 5: Thử Nghiệm và Đánh Giá

## 5.1 Thiết lập thử nghiệm

### 5.1.1 Môi trường

| Thành phần  | Cấu hình                                   |
| ----------- | ------------------------------------------ |
| Máy tính    | Windows 11, CPU Intel/AMD multi-core       |
| Broker      | Mosquitto 2.x (Docker, localhost:1883)     |
| Edge Device | mock_esp32.py (Python, chạy trên cùng máy) |
| Dashboard   | Chrome/Edge, kết nối WebSocket port 9001   |
| Network     | Localhost (loopback)                       |

### 5.1.2 Hai chế độ thử nghiệm

| Chế độ            | Mô tả                             | Mục đích                               |
| ----------------- | --------------------------------- | -------------------------------------- |
| **Mock mode**     | mock_esp32.py thay thế ESP32 thật | Đo overhead MQTT protocol + JSON parse |
| **Hardware mode** | ESP32 thật qua WiFi               | Đo độ trễ thực tế (planned)            |

> **Lưu ý**: Kết quả trong báo cáo này sử dụng Mock mode. RTT đo được phản ánh overhead của MQTT protocol, không bao gồm độ trễ WiFi và xử lý phần cứng.

## 5.2 Smoke Test — Kiểm tra tích hợp

### 5.2.1 Kịch bản

4 kịch bản kiểm tra end-to-end:

|  #  | Test              | Input             | Expected                 |     Kết quả      |
| :-: | ----------------- | ----------------- | ------------------------ | :--------------: |
|  1  | Broker Connection | Connect MQTT      | Connected < 5s           |     ✅ PASS      |
|  2  | SET_MODE MANUAL   | Gửi SET_MODE cmd  | ACK ok=true, RTT < 500ms | ✅ PASS (50.7ms) |
|  3  | SET_PHASE 3       | Gửi SET_PHASE cmd | ACK ok=true, phase=3     |     ✅ PASS      |
|  4  | Cleanup AUTO      | SET_MODE AUTO     | ACK ok=true              |     ✅ PASS      |

**Kết quả**: **4/4 PASS** — Hệ thống hoạt động đúng thiết kế.

### 5.2.2 Lệnh chạy

```bash
python logger/tools/smoke_test.py --host 127.0.0.1
```

## 5.3 Benchmark RTT — Đo độ trễ

### 5.3.1 Thiết kế thí nghiệm

- **Số lượng**: 500 messages mỗi case
- **Interval**: 200ms giữa các message
- **QoS**: cmd (QoS 1), ack (QoS 1)
- **Payload sizes**: 0B, 256B, 512B, 900B, 1200B (padding thêm vào JSON)
- **Cách đo**: RTT = t_ack_recv − t_cmd_send (milliseconds)

### 5.3.2 Kết quả

| Case |   Payload (bytes)   | Sent | Recv | Loss |  Mean RTT  | Median | P95  | P99  | Max  |  Status   |
| :--: | :-----------------: | :--: | :--: | :--: | :--------: | :----: | :--: | :--: | :--: | :-------: |
|  1   |   0 (110B actual)   | 500  | 500  |  0%  | **43.3ms** |  43.0  | 45.0 | 47.0 | 49.0 |  ✅ PASS  |
|  2   |  256 (377B actual)  | 500  | 500  |  0%  | **43.2ms** |  43.0  | 45.0 | 46.0 | 49.0 |  ✅ PASS  |
|  3   |  512 (633B actual)  | 500  | 500  |  0%  | **43.3ms** |  43.0  | 45.0 | 46.0 | 48.0 |  ✅ PASS  |
|  4   | 900 (1021B actual)  | 500  | 500  |  0%  | **43.4ms** |  43.0  | 45.0 | 46.0 | 49.0 |  ✅ PASS  |
|  5   | 1200 (1321B actual) | 500  |  0   | 100% |    N/A     |  N/A   | N/A  | N/A  | N/A  | ✅ PASS\* |

> \*Case 5: Payload vượt giới hạn 1KB → Mock ESP32 reject, không gửi ACK. Đây là hành vi đúng thiết kế (oversize protection).

### 5.3.3 Phân tích kết quả

#### Xu hướng theo payload size

- RTT **hầu như không thay đổi** khi payload tăng từ 0B đến 900B (43.2ms → 43.4ms, chênh lệch < 0.5%)
- Điều này cho thấy MQTT overhead chủ yếu đến từ:
  - TCP handshake và MQTT QoS 1 PUBACK
  - JSON parse trên mock ESP32
  - Không phải từ kích thước payload (trong phạm vi < 1KB)

#### Độ ổn định

- **P95 = 45ms**, **P99 = 47ms**: 99% messages được trả lời trong 47ms
- **Max = 49ms**: Không có outlier lớn
- Spread (Max - Min) < 10ms: RTT rất ổn định

#### So sánh với yêu cầu

| Tiêu chí           | Yêu cầu      | Kết quả            |       Đánh giá        |
| ------------------ | ------------ | ------------------ | :-------------------: |
| RTT trung bình     | < 100ms      | 43.3ms             |        ✅ Đạt         |
| Delivery rate      | 100%         | 100% (Case 1-4)    |        ✅ Đạt         |
| Oversize rejection | Reject > 1KB | 100% reject Case 5 |        ✅ Đạt         |
| P95                | < 200ms      | 45ms               | ✅ Đạt (22.5% ngưỡng) |

## 5.4 Kiểm tra LWT (Last Will and Testament)

### Kịch bản

1. Mock ESP32 kết nối → Status = `{"online": true}` (Retained)
2. Dashboard nhận → hiển thị 🟢 ONLINE
3. Dừng mock ESP32 đột ngột (kill process)
4. Sau ~5-10 giây → Broker publish LWT: `{"online": false}`
5. Dashboard nhận → hiển thị 🔴 OFFLINE
6. Khởi động lại mock → Status = `{"online": true}` → 🟢 ONLINE

**Kết quả**: LWT hoạt động đúng. Thời gian phát hiện offline phụ thuộc vào `keepalive` (30 giây) × 1.5 = tối đa 45 giây.

## 5.5 Hạn chế của thử nghiệm

| Hạn chế                            | Ảnh hưởng                                             | Giải pháp                        |
| ---------------------------------- | ----------------------------------------------------- | -------------------------------- |
| Mock chạy trên cùng máy với Broker | RTT không bao gồm độ trễ WiFi thực                    | Lặp lại benchmark với ESP32 thật |
| Mạng localhost                     | Không có packet loss tự nhiên                         | Test trên WiFi hoặc qua internet |
| Chỉ test 1 intersection            | Chưa đánh giá scalability                             | Multi-mock test                  |
| Chưa có tải concurrent             | RTT có thể tăng khi nhiều intersection cùng hoạt động | Load testing                     |

## 5.6 Tóm tắt chương

Kết quả thử nghiệm cho thấy hệ thống **đáp ứng tốt tất cả yêu cầu thiết kế**:

- ✅ RTT trung bình **43.3ms** (< 100ms yêu cầu)
- ✅ Delivery rate **100%** (QoS 1)
- ✅ Smoke test **4/4 PASS**
- ✅ LWT **hoạt động đúng**
- ✅ Oversize protection **hoạt động đúng**
