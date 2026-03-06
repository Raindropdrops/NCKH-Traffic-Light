# Danh mục những từ viết tắt

| Từ viết tắt | Ý nghĩa                                                             |
| :---------: | ------------------------------------------------------------------- |
|     ACK     | Acknowledgment — Bản tin xác nhận                                   |
|     ACL     | Access Control List — Danh sách kiểm soát truy cập                  |
|    CoAP     | Constrained Application Protocol                                    |
|     DoS     | Denial of Service — Tấn công từ chối dịch vụ                        |
|    ECDF     | Empirical Cumulative Distribution Function                          |
|    ESP32    | Vi điều khiển Espressif Systems 32-bit                              |
|     FSM     | Finite State Machine — Máy trạng thái hữu hạn                       |
|    GPIO     | General Purpose Input/Output                                        |
|     IoT     | Internet of Things — Internet vạn vật                               |
|     ITS     | Intelligent Transportation Systems — Hệ thống giao thông thông minh |
|    JSON     | JavaScript Object Notation                                          |
|     LWT     | Last Will and Testament — Di chúc cuối cùng (MQTT)                  |
|     M2M     | Machine-to-Machine — Liên lạc máy-máy                               |
|    MQTT     | Message Queuing Telemetry Transport                                 |
|    mTLS     | Mutual Transport Layer Security — Bảo mật tầng vận chuyển 2 chiều   |
|     QoS     | Quality of Service — Chất lượng dịch vụ                             |
|    RSSI     | Received Signal Strength Indicator — Cường độ tín hiệu thu          |
|     RTT     | Round-Trip Time — Thời gian khứ hồi                                 |
|     SVG     | Scalable Vector Graphics                                            |
|     TCP     | Transmission Control Protocol                                       |
|     TLS     | Transport Layer Security — Bảo mật tầng vận chuyển                  |
|     UDP     | User Datagram Protocol                                              |
|    UUID     | Universally Unique Identifier — Mã định danh duy nhất toàn cầu      |

---

# Các Phần Mở Đầu

## 5. Mở đầu

Sự bùng nổ của Internet of Things (IoT) đã mở ra những hướng đi mới trong việc quản lý và vận hành thông minh cơ sở hạ tầng đô thị [1]. Trong đó, hệ thống giao thông tín hiệu đóng vai trò xương sống trong việc duy trì trật tự và an toàn công cộng. Phương thức điều khiển đèn giao thông truyền thống hiện nay phần lớn dựa trên các bộ định thời (timer-based) được thiết lập sẵn, thiếu khả năng giám sát từ xa và khó khăn trong việc thay đổi chu kỳ linh hoạt [2]. Điều này đặt ra yêu cầu cấp thiết về một giải pháp quản lý tập trung, có độ trễ thấp và độ tin cậy cao. Đề tài "Nghiên cứu ứng dụng IoT - MQTT trong giám sát và điều khiển từ xa hệ thống đèn tín hiệu giao thông" được thực hiện nhằm mục đích giải quyết vấn đề này.

## 6. Tổng quan tình hình nghiên cứu thuộc lĩnh vực

### Tình hình trong nước

Tại Việt Nam, hệ thống điều khiển đèn tín hiệu giao thông tập trung SCATS (Sydney Coordinated Adaptive Traffic System) đã được thí điểm triển khai tại TP. Hồ Chí Minh từ năm 2014 trên một số tuyến đường chính [2]. Tại Hà Nội, hệ thống UTC (Urban Traffic Control) của Siemens đã được lắp đặt cho khoảng 100 nút giao thông từ năm 2017 [3]. Tuy nhiên, cả hai hệ thống trên đều sử dụng hạ tầng mạng cáp quang tốn kém và giao thức truyền thông đóng (proprietary). Việc giám sát thiết bị ở các điểm nút giao thông nhỏ lẻ vẫn còn hạn chế do chi phí triển khai cao.

### Tình hình thế giới

Trên thế giới, kiến trúc IoT với các giao thức nhẹ như MQTT hoặc CoAP đã trở thành tiêu chuẩn công nghiệp cho liên lạc máy-máy (M2M) [4]. Năm 2019, C. S. Nandy và cộng sự đã đề xuất mô hình "IoT Based Smart Traffic Control System" sử dụng vi điều khiển Arduino kết hợp cảm biến hồng ngoại đếm phương tiện, tuy nhiên nghiên cứu này không đo lường hiệu năng định lượng của giao thức truyền thông [5]. Nghiên cứu của A. Al-Fuqaha và cộng sự (2015) đã khảo sát toàn diện các giao thức IoT và kết luận MQTT là lựa chọn tối ưu cho các ứng dụng yêu cầu push notification thời gian thực [6].

### Khoảng trống nghiên cứu

Qua khảo sát, nhóm nhận thấy phần lớn các nghiên cứu tập trung vào kiến trúc hệ thống hoặc thuật toán AI đếm xe, mà chưa đi sâu vào việc **đo lường định lượng hiệu năng truyền thông MQTT** (độ trễ RTT, tỷ lệ mất gói tin, cơ chế phát hiện offline) trong bài toán điều khiển đèn giao thông.

## 7. Lý do lựa chọn đề tài

Giao thức MQTT (Message Queuing Telemetry Transport) được đánh giá là đặc biệt phù hợp cho mạng IoT băng thông thấp và không ổn định nhờ dung lượng header cực nhỏ (chỉ 2 bytes) và cơ chế QoS linh hoạt [1][4]. Dù vậy, ứng dụng thực tế và việc đo đạc hiệu năng định lượng của MQTT trong bài toán đặc thù như điều khiển đèn giao thông tại Việt Nam vẫn chưa được nghiên cứu toàn diện. Do đó, việc thực nghiệm đo lường độ trễ (RTT) và tính ổn định của MQTT là lý do chính để nhóm lựa chọn đề tài này, làm tiền đề cho hệ thống giao thông thông minh.

## 8. Mục tiêu, nội dung, phương pháp nghiên cứu

**Mục tiêu:**

- Xây dựng thành công mô hình hệ thống giám sát và điều khiển tín hiệu đèn giao thông từ xa thông qua giao thức MQTT.
- Đánh giá hiệu quả, đo lường độ trễ mạng (Round-Trip Time) và tỷ lệ mất gói tin (Packet Loss).
- Xây dựng giao diện Dashboard thời gian thực hiện đại, hiển thị giám sát và cung cấp cơ chế điều khiển khẩn cấp.

**Nội dung nghiên cứu:**

- Nghiên cứu kiến trúc IoT, giao thức MQTT, và các chuẩn thông điệp (Payload).
- Cấu hình MQTT Broker (Mosquitto) với tính năng bảo mật và WebSocket.
- Lập trình firmware cho vi điều khiển (ESP32) hoạt động như một thiết bị biên (Edge worker).
- Phát triển phần mềm Dashboard hiển thị trực quan.

**Phương pháp nghiên cứu:**

- **Nghiên cứu lý thuyết:** Tham khảo tiêu chuẩn MQTT v5.0 của quy chuẩn OASIS [1].
- **Nghiên cứu thực nghiệm:** Thiết kế kịch bản Benchmark gồm 500 lệnh điều khiển × 5 mức kích cỡ payload (0B, 256B, 512B, 900B, 1200B) với tần suất 1 lệnh mỗi 200ms. Thu thập dữ liệu về độ trễ, lưu trữ thành tệp CSV, viết mã Python vẽ biểu đồ phân phối (Histogram) và hàm phân phối tích lũy thực nghiệm (ECDF).

## 9. Đối tượng và phạm vi nghiên cứu

- **Đối tượng nghiên cứu:**
  - Giao thức truyền thông MQTT và các cơ chế QoS (0, 1).
  - Vi điều khiển ESP32 và công nghệ web thời gian thực (WebSocket).
- **Phạm vi nghiên cứu:**
  - Đề tài giới hạn mô phỏng và thực nghiệm ở quy mô một nút giao thông (intersection) dạng ngã tư tiêu chuẩn gồm 4 hướng đi.
  - **Giai đoạn 1:** Thử nghiệm độ trễ trong môi trường mạng nội bộ (loopback) với thiết bị mô phỏng Mock ESP32.
  - **Giai đoạn 2:** Thử nghiệm với thiết bị ESP32 vật lý qua mạng WiFi thực tế (dự kiến cập nhật).
