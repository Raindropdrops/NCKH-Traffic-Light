# Chương 1: Mở Đầu

## 1.1 Lý do chọn đề tài

Hệ thống đèn tín hiệu giao thông là một thành phần quan trọng trong quản lý giao thông đô thị. Tuy nhiên, phần lớn hệ thống đèn giao thông hiện nay tại Việt Nam vẫn hoạt động theo cơ chế **chu kỳ cố định** (fixed-time), không có khả năng giám sát từ xa cũng như điều chỉnh linh hoạt theo tình hình giao thông thực tế. Điều này dẫn đến một số hạn chế:

- **Không giám sát được trạng thái hoạt động**: Khi đèn gặp sự cố (mất nguồn, hỏng bóng, lỗi bộ điều khiển), cơ quan quản lý không biết cho đến khi nhận được phản ánh từ người dân.
- **Không điều chỉnh real-time**: Trong các tình huống khẩn cấp (tai nạn, cứu hộ), việc thay đổi chu kỳ đèn đòi hỏi nhân viên đến tận nơi.
- **Thiếu dữ liệu vận hành**: Không có số liệu thống kê về thời gian hoạt động, tần suất lỗi, hay hiệu suất hệ thống.

Trong bối cảnh **Internet of Things (IoT)** đang được ứng dụng rộng rãi vào các lĩnh vực đô thị thông minh (smart city), giao thức **MQTT (Message Queuing Telemetry Transport)** nổi lên như một giải pháp truyền thông nhẹ, hiệu quả, phù hợp cho các thiết bị IoT với tài nguyên hạn chế. MQTT hoạt động theo mô hình **Publish/Subscribe**, hỗ trợ nhiều mức chất lượng dịch vụ (QoS), và có cơ chế phát hiện thiết bị mất kết nối (Last Will and Testament – LWT).

Xuất phát từ những vấn đề trên, nhóm nghiên cứu lựa chọn đề tài **"Nghiên cứu ứng dụng IoT – MQTT trong giám sát và điều khiển từ xa hệ thống đèn tín hiệu giao thông"** nhằm xây dựng một mô hình minh chứng (proof-of-concept) cho việc hiện đại hóa hệ thống đèn giao thông bằng công nghệ IoT.

## 1.2 Mục tiêu nghiên cứu

Đề tài hướng đến ba mục tiêu chính:

1. **Xây dựng hệ thống giám sát và điều khiển từ xa** đèn tín hiệu giao thông thông qua giao thức MQTT, sử dụng vi điều khiển ESP32 làm thiết bị biên (edge device).

2. **Đánh giá hiệu quả và độ trễ truyền dữ liệu** trong môi trường IoT, thông qua phép đo Round-Trip Time (RTT) giữa dashboard điều khiển và thiết bị biên, với các kích thước payload khác nhau.

3. **Đề xuất giải pháp mở rộng** áp dụng vào quy mô đô thị thông minh, bao gồm kiến trúc multi-intersection, cân bằng tải broker, và tích hợp bảo mật.

## 1.3 Phạm vi nghiên cứu

- **Quy mô**: 1 ngã tư, 4 hướng (Bắc, Nam, Đông, Tây), mỗi hướng 3 đèn (đỏ, vàng, xanh).
- **Phần cứng**: ESP32 DevKit V1 điều khiển 12 LED qua GPIO.
- **Phần mềm**: Mosquitto MQTT broker (Docker), Dashboard web, Mock ESP32 simulator.
- **Môi trường thử nghiệm**: Mạng LAN (localhost) và WiFi nội bộ.
- **Giới hạn**: Chưa tích hợp camera AI hoặc cảm biến mật độ giao thông thực tế.

## 1.4 Phương pháp nghiên cứu

Nghiên cứu được thực hiện theo quy trình 4 giai đoạn:

```
Thiết kế hệ thống → Triển khai → Thử nghiệm → Đánh giá
```

| Giai đoạn      | Nội dung                                                                | Công cụ                          |
| -------------- | ----------------------------------------------------------------------- | -------------------------------- |
| **Thiết kế**   | Kiến trúc hệ thống, MQTT topic tree, FSM đèn, sơ đồ phần cứng           | Draw.io, Markdown                |
| **Triển khai** | Firmware ESP32, Docker infrastructure, Dashboard, Testing tools         | ESP-IDF, Docker, HTML/JS, Python |
| **Thử nghiệm** | Smoke test (4 kịch bản), Benchmark RTT (500 messages × 6 payload sizes) | Python scripts                   |
| **Đánh giá**   | Phân tích RTT, reliability, so sánh với yêu cầu SPEC                    | Matplotlib, CSV analysis         |

## 1.5 Bố cục báo cáo

Báo cáo gồm 6 chương:

- **Chương 1**: Mở đầu — trình bày lý do, mục tiêu, phạm vi, phương pháp.
- **Chương 2**: Cơ sở lý thuyết — giao thức MQTT, vi điều khiển ESP32, Docker.
- **Chương 3**: Thiết kế hệ thống — kiến trúc, MQTT topic tree, FSM, phần cứng.
- **Chương 4**: Triển khai — firmware, Docker infrastructure, dashboard, testing tools.
- **Chương 5**: Thử nghiệm và đánh giá — benchmark, smoke test, phân tích kết quả.
- **Chương 6**: Kết luận và hướng phát triển.
