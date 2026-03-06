# Chương 3. Nội dung Triển khai xây dựng

## 3.1 Xây dựng hệ thống Broker Mosquitto

Hệ thống sử dụng Docker Compose cài đặt Eclipse Mosquitto [9] trên Linux/Windows cho độ đồng nhất mã nguồn cao trên mọi hệ sinh thái thực thi.

Tập cấu hình chính `mosquitto.conf`:

- **Port 1883:** Lắng nghe giao tiếp giao thức gốc MQTT cho vi điều khiển.
- **Port 9001:** Lắng nghe WebSocket cho phép giao tiếp xuyên trình duyệt, phục vụ Dashboard giám sát.
- **Authentication:** Kích hoạt file mật khẩu `passwordfile` chặn truy cập trái phép [9].

## 3.2 Lập trình Firmware vi điều khiển ESP32

Firmware xây dựng trên nền tảng C/C++ của nhà sản xuất (ESP-IDF v5.5) [8] thay vì Framework Arduino nhằm tận dụng trọn vẹn sức mạnh đa luồng FreeRTOS.

Thành phần chia làm 4 luồng xử lý đồng thời (FreeRTOS Tasks):

1. **MQTT Task Network:** Khởi tạo mạng WiFi, xử lý vòng lặp Reconnect. Duy trì tín hiệu Keep Alive. Khai báo bản tin "Offline" cho LWT ngay trước khi kết nối [1][7].
2. **Command Handler:** Parsing JSON điều khiển bằng thư viện cJSON. Lọc `cmd_id` trùng lặp và kích hoạt rơ-le thay đổi Phase. Nếu JSON kích thước lớn hơn 1024 Bytes, hệ thống tự động loại bỏ để phòng thủ tấn công DoS tràn bộ nhớ đệm [10].
3. **GPIO LED Control:** Cấp dòng tải 3.3V điều khiển Relay kích các chân GPIO cho 6 đèn.
4. **Telemetry Publisher:** Mỗi 5 giây đọc Free Heap Memory, thời gian sống Uptime, độ nhiễu mạng RSSI và gửi lên QoS 0 về Dashboard.

## 3.3 Phát triển giao diện Dashboard điều khiển

> _Hình 3.1: Ảnh chụp màn hình Dashboard giám sát đèn giao thông (Dark Theme) — chèn ảnh vào Word_

Hệ thống sử dụng nền tảng HTML5/CSS3/JavaScript thuần, kết nối theo phương thức WebSocket. Màn hình Dark Theme được chia thành các khu vực chức năng:

- **Control Panel:** 4 nút chế độ (AUTO, MANUAL, BLINK, OFF) và bộ chọn Phase kèm nút SET PHASE.
- **Intersection SVG:** Mô phỏng đồ họa ngã tư thời gian thực với hiệu ứng glow trên đèn đang sáng.
- **Live Status:** Hiển thị Mode, Phase, Uptime hiện tại.
- **Telemetry Panel:** Hiển thị RSSI, Heap Free, Device Uptime.
- **ACK Log:** Lịch sử các lệnh đã gửi và xác nhận.

Ba tính năng khoa học then chốt được bổ sung nhằm phục vụ mục tiêu đánh giá hiệu năng MQTT:

- **Biểu đồ RTT Realtime (Canvas Chart):** Tính toán và biểu diễn RTT ngay trên Dashboard mỗi khi gửi lệnh và nhận ACK. Hiển thị Mean, Last, Min, Max và số lượng mẫu.
- **QoS Indicator Panel:** Hiện rõ mức QoS đang dùng cho từng topic MQTT, giúp giải thích thiết kế.
- **Connection Log (LWT):** Ghi lại lịch sử sự kiện Online/Offline với timestamp.

## 3.4 Xây dựng công cụ kiểm thử Mock ESP32 và Benchmark

> _Hình 3.2: Kiến trúc quy trình kiểm thử tự động (Mock ESP32 → Broker → Benchmark Script) — vẽ sơ đồ_

Do phần cứng ESP32 có rủi ro can nhiễu kết nối WiFi khi thử nghiệm số lượng gói lớn [8], nhóm đã lập trình thiết bị mô phỏng "Mock ESP32" bằng Python. Công cụ này giả lập 100% logic xử lý thiết bị thật bao gồm: vòng tuần hoàn đèn, trả về ACK, publish trạng thái, và telemetry giả lập thực tế (RSSI drift -1dBm/5 phút, Heap giảm dần). Mock ESP32 cho phép thiết lập tăng tốc quá trình đèn (`--speed 2x`) dùng cho demo.

Công cụ Benchmark `run_benchmark_report.py` gửi tự động lệnh điều khiển theo tần suất cố định và thu thập RTT, tự động tạo biểu đồ Histogram, ECDF và báo cáo Markdown.
