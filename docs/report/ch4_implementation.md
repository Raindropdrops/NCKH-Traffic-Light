# Chương 3. Nội dung Triển khai xây dựng

## 3.1 Xây dựng hệ thống Broker Mosquitto

Môi trường Broker là khối óc xương sống. Hệ thống sử dụng Docker Compose cài đặt trên Linux/Windows cho độ đồng nhất mã nguồn cực cao trên mọi hệ sinh thái thực thi (Write once run everywhere).

Tập cấu hình chính `mosquitto.conf`:

- **Port 1883:** Lắng nghe giao tiếp giao thức gốc MQTT, giao tiếp vi điều khiển.
- **Port 9001:** Lắng nghe Websocket - một tính năng được kích hoạt bổ sung cho phép giao tiếp xuyên trình duyệt, phục vụ Dashboard giám sát.
- **Authentication:** Kích hoạt mã hoá TLS cơ bản và file mật khẩu `passwordfile` chặn trái phép truy cập (ACL) trái luồng.

## 3.2 Lập trình Firmware vi điều khiển ESP32

Firmware xây dựng dựa vào nền tảng C/C++ trực tiếp của nhà sản xuất (ESP-IDF phiên bản cao cấp v5.5) thay vì Framework Arduino đơn giản nhằm tận dụng trọn vẹn sức mạnh vi tính luồng.

Thành phần hệ thống chia làm 4 luồng xử lý đồng dạng (FreeRTOS Tasks):

1. **MQTT Task Network:** Khởi tạo mạng Wifi, xử lý vòng lặp Reconnect tĩnh. Duy trì tín hiệu Keep Alive. Khai báo chuỗi bản tin "Offline" cho LWT ngay trước khi thực thi kết nối.
2. **Command Handler:** Parsing file JSON điều khiển bằng thư viện cJSON. Cấp phát cơ chế lọc `cmd_id` và kích hoạt rơ_le thay đổi Phase. Nếu JSON kích thước lớn hơn 1024 Bytes, hệ thống tự động loại bỏ phòng thủ tấn công DoS tràn bộ nhớ đệm.
3. **GPIO LED Control:** Cấp dòng tải 3.3v điều khiến Relay kích các chân GPIO cho 6 đèn.
4. **Telemetry Publisher:** Mỗi 5s đọc Free Heap Mem, thời gian sống Uptime, độ nhiễu mạng gửi lên QoS 0 về Dashboard đánh giá.

## 3.3 Phát triển giao diện phần mềm Dashboard điều khiển

Hệ thống sử dụng nền tảng HTML5/CSS3 cho trải nghiệm tốc độ (Performatic Interface), kết nối theo phương thức WebSocket. Màn hình Dark Theme được chia ra các khu vực quản lý chuyên nghiệp: Cụm điều khiển khẩn cấp Control Mode; Ngã tư đồ họa SVG thể hiện sống động quá trình luân chuyển chu kỳ màu; Live Status thông số máy lẻ.

Hai tính năng khoa học then chốt được bổ sung:

- **Biểu đồ thời gian thực RTT (Realtime Chart):** Tính toán và biểu diễn ngay lập tức trên hệ tọa độ thời gian (Canvas) tốc độ khứ hồi mạng tính từ milliseconds lệnh gửi (cmd) gửi đi so với thời gian nhận xác thực (ack).
- **QoS Level Panels / Event LWT:** Lịch sử ghi log tự động ngắt thiết bị cho giám thị.

## 3.4 Kịch bản mô phỏng kiểm thử với Mock ESP32

Do phần cứng ESP32 có rủi ro về can nhiễu kết nối sóng Wifi khi thử nghiệm đo đạc ở số lượng gói siêu lớn (Load testing). Nhóm đã lập trình thiết bị mô phỏng linh kiện ảo "Mock ESP32" bằng mã nguồn Python. Công cụ này xử lý giả lập 100% giống thiết bị thật về logic xử lý, vòng tuần hoàn đèn, trả về ACK và Publish trạng thái. Mock ESP32 cho phép thiết lập độ trễ nhân tạo và tùy biến tăng tốc quá trình đèn `Speed=2x` dùng cho demo. Khối lượng gói benchmark 2000 Requests gửi liên tiếp đã được công cụ mô phỏng gồng gánh xuất sắc làm nền tảng kiểm thử cho phần đánh giá tại Chương 4.
