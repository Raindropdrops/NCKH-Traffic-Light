# 📝 REPORT OUTLINE — Báo Cáo NCKH (Chuẩn mẫu PL1 - ĐHGTVT)

> Bố cục báo cáo NCKH tuân thủ chính xác Mẫu PL1 năm học 2024-2025.
> Tiêu chí đánh giá dựa trên Mẫu PL5 (Thang 100đ).

---

## Các Phần Mở Đầu

1. Trang bìa (Theo Mẫu 01)
2. Mục lục
3. Danh mục bảng biểu, hình vẽ
4. Danh mục những từ viết tắt
5. **Mở đầu** (Giới thiệu chung bối cảnh IoT giao thông)
6. **Tổng quan tình hình nghiên cứu thuộc lĩnh vực công trình/đề tài (10 điểm)**
   - Các hệ thống đèn truyền thống (hẹn giờ cứng, vòng từ tử)
   - Ứng dụng IoT trong giao thông thông minh trên thế giới và tại Việt Nam
7. **Lý do lựa chọn công trình/đề tài**
   - Khắc phục độ trễ, dễ dàng mở rộng, giám sát thời gian thực
8. **Mục tiêu, nội dung, phương pháp nghiên cứu (35 điểm)**
   - _Mục tiêu:_ Xây dựng mô hình, đo lường độ trễ mạng, đề xuất giải pháp đô thị.
   - _Nội dung:_ Broker, ESP32 firmware, Dashboard.
   - _Phương pháp:_ Nghiên cứu thực nghiệm, đo test benchmark.
9. **Đối tượng và phạm vi nghiên cứu**
   - _Đối tượng:_ Giao thức MQTT QoS 0/1/2, vi điều khiển ESP32, ứng dụng web.
   - _Phạm vi:_ Mô phỏng và thực nghiệm ngã tư 4 hướng trong mạng tĩnh.

---

## 10. Kết quả nghiên cứu và thảo luận (40 điểm)

> Đây là phần thân bài chính, chứa các CHƯƠNG.

### Chương 1. Cơ sở lý thuyết về IoT và giao thức MQTT

- Kiến trúc Publish/Subscribe của MQTT
- Các mức QoS (0, 1, 2) và tính năng Retained/LWT
- Tổng quan về ESP32 và Broker (Mosquitto)

### Chương 2. Thiết kế và Kiến trúc hệ thống điều khiển

- Sơ đồ khối tổng thể (Edge - Broker - Dashboard)
- Thiết kế Topic Tree và chuẩn hóa JSON Payload (Tránh trùng lặp `cmd_id`)
- Máy trạng thái (FSM) cho ngã tư (Chế độ AUTO, MANUAL, BLINK, OFF)
- Thiết kế Dashboard UI/UX cho điều khiển giao thông

### Chương 3. Nội dung Triển khai xây dựng

- Thiết lập Mosquitto với Docker (Authentication, WebSocket)
- Lập trình Firmware vi điều khiển ESP32 (Các hàm xử lý MQTT, non-blocking delay)
- Xây dựng hệ thống Mock ESP32 để Auto-test mô phỏng (Có nhiễu RSSI, Heap)
- Xây dựng Node-RED Dashboard (Vẽ giao diện SVG, xử lý realtime)

### Chương 4. Thử nghiệm kết quả và Đánh giá (THẢO LUẬN - Rất quan trọng)

- Kịch bản thử nghiệm tải: Gửi 500 tín hiệu điều khiển với các mức độ Payload (0 - 1200 bytes)
- Kết quả đo độ trễ RTT (Round-Trip Time): Phân tích Mean, Median, P95 (Chèn biểu đồ Histogram, ECDF)
- Đánh giá khả năng chặn tin nhắn vượt quá kích thước (Oversize Rejection)
- Phân tích sự kiện ngắt kết nối LWT (Last Will Testament)
- Bàn luận về độ ổn định (Packet Loss 0% cho tín hiệu hợp lệ) và tính thực tiễn.

---

## 11. Kết luận và kiến nghị

- **a) Phần kết luận:** Tóm tắt 3 kết quả chính (Xây dựng thành công, đo đạc được thông số <50ms, tính ổn định cao).
- **b) Phần kiến nghị:** Đề xuất triển khai MQTT Cluster (Mosquitto Bridge) cho giao thông cấp thành phố; cân nhắc TSL/SSL bảo mật.

## 12. Tài liệu tham khảo

- Danh sách tài liệu (Chuẩn IEEE/APA, xếp theo ABC).
- Ví dụ: MQTT OASIS Standard v5.0, ESP-IDF Documentation.

## 13. Phụ lục

- Sơ đồ nối dây phần cứng (Nếu có)
- Source code đại diện hoặc Log file Benchmark (Tóm tắt)
- Ảnh chụp thực tế của màn hình Dashboard và thiết bị
