# Các Phần Mở Đầu

## 5. Mở đầu

Sự bùng nổ của Internet of Things (IoT) đã mở ra những hướng đi mới trong việc quản lý và vận hành thông minh cơ sở hạ tầng đô thị. Trong đó, hệ thống giao thông tín hiệu đóng vai trò xương sống trong việc duy trì trật tự và an toàn công cộng. Phương thức điều khiển đèn giao thông truyền thống hiện nay phần lớn dựa trên các bộ định thời (timer-based) được thiết lập sẵn, thiếu khả năng giám sát từ xa và khó khăn trong việc thay đổi chu kỳ linh hoạt. Điều này đặt ra yêu cầu cấp thiết về một giải pháp quản lý tập trung, có độ trễ thấp và độ tin cậy cao. Đề tài "Nghiên cứu ứng dụng IoT - MQTT trong giám sát và điều khiển từ xa hệ thống đèn tín hiệu giao thông" được thực hiện nhằm mục đích giải quyết vấn đề này.

## 6. Tổng quan tình hình nghiên cứu thuộc lĩnh vực

### Tình hình trong nước

Tại Việt Nam, các thành phố lớn như Hà Nội và TP.HCM đang bước đầu thử nghiệm các hệ thống giao thông thông minh (ITS). Tuy nhiên, hầu hết các hệ thống hiện tại đều sử dụng hạ tầng mạng cáp quang tốn kém và các giao thức truyền thông độc quyền tĩnh. Việc giám sát thiết bị ở các điểm nút giao thông nhỏ vẫn còn hạn chế do chi phí kết nối cao.

### Tình hình thế giới

Trên thế giới, kiến trúc IoT với các giao thức nhẹ như MQTT hoặc CoAP đã trở thành tiêu chuẩn công nghiệp cho liên lạc máy-máy (M2M). Các quốc gia phát triển sử dụng vi điều khiển biên (Edge devices) kết nối không dây để gửi dữ liệu giao thông theo thời gian thực về máy chủ trung tâm (Cloud), cho phép thuật toán AI phân luồng giao thông động.

## 7. Lý do lựa chọn đề tài

Giao thức MQTT (Message Queuing Telemetry Transport) được đánh giá là đặc biệt phù hợp cho mạng IoT băng thông thấp và không ổn định do dung lượng header cực nhỏ (chỉ 2 bytes) và cơ chế QoS (Quality of Service) linh hoạt. Dù vậy, ứng dụng thực tế và việc đo đạc hiệu năng định lượng của MQTT trong bài toán đặc thù như điều khiển đèn giao thông tại Việt Nam vẫn chưa được nghiên cứu toàn diện. Do đó, việc thực nghiệm đo lường độ trễ (RTT) và tính ổn định của MQTT là lý do chính để nhóm lựa chọn đề tài này, làm tiền đề cho hệ thống giao thông thông minh.

## 8. Mục tiêu, nội dung, phương pháp nghiên cứu

**Mục tiêu:**

- Xây dựng thành công mô hình hệ thống giám sát và điều khiển tín hiệu đèn giao thông từ xa thông qua giao thức MQTT.
- Đánh giá hiệu quả, đo lường độ trễ mạng (Round-Trip Time) và tỷ lệ mất gói tin (Packet Loss).
- Xây dựng giao diện Dashboard thời gian thực hiện đại, hiển thị giám sát và cung cấp cơ chế điều khiển khẩn cấp.

**Nội dung nghiên cứu:**

- Nghiên cứu kiến trúc IoT, giao thức MQTT, và các chuẩn thông điệp (Payload).
- Cấu hình MQTT Broker (Mosquitto) với tính năng bảo mật và WebSocket.
- Lập trình firmware cho vi điều khiển (ESP32) hoạt động như một thiết bị biên (Edge worker).
- Phát triển phần mềm Dashboard hiển thị.

**Phương pháp nghiên cứu:**

- **Nghiên cứu lý thuyết:** Tham khảo tiêu chuẩn MQTT v5.0 của quy chuẩn OASIS.
- **Nghiên cứu thực nghiệm:** Thiết kế kịch bản Benchmark, gửi hàng nghìn gói tin tự động để thu thập dữ liệu về độ trễ, lưu trữ thành tệp CSV, và viết mã Python vẽ biểu đồ xác suất (ECDF, Histogram).

## 9. Đối tượng và phạm vi nghiên cứu

- **Đối tượng nghiên cứu:**
  - Giao thức truyền thông MQTT và các cơ chế QoS (0, 1).
  - Vi điều khiển ESP32 và công nghệ web thời gian thực (WebSocket).
- **Phạm vi nghiên cứu:**
  - Đề tài giới hạn mô phỏng và thực nghiệm ở quy mô một nút giao thông (intersection) dạng ngã tư tiêu chuẩn gồm 4 hướng đi.
  - Thử nghiệm độ trễ thực hiện trong môi trường mạng giả lập (Mock) và mạng cục bộ (LAN/WiFi).
