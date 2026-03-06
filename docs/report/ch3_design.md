# Chương 2. Thiết kế Kiến trúc Hệ thống Điều khiển

Hệ thống điều khiển đèn giao thông dựa trên chuẩn MQTT theo mô hình Client-Broker-Client được nhóm thiết kế nhằm khắc phục điểm yếu của điều khiển vòng từ truyền thống, cung cấp khả năng phát hiện liên tục luồng giao thông và phản hồi linh hoạt.

## 2.1 Sơ đồ khối tổng thể của hệ thống

Hệ thống được chia làm 3 thành phần chính tuyến tính yếu cầu (End-to-end Architecture).

1. **MQTT Broker (Core):** Là máy chủ trung tâm nhận dữ liệu, xử lý phân quyền. Cài đặt trên Docker sử dụng mã nguồn mở Eclipse Mosquitto.
2. **Edge Device (ESP32 Controller):** Lắp đặt trực tiếp tại các tủ điều khiển ngã tư. Đọc cảm biến cứng, điều khiển rơ-le đèn, gửi trạng thái về Broker, và lắng nghe lệnh ghi đè (Override Command).
3. **Web Dashboard (Node-RED/HTML):** Trung tâm giám sát thành phố. Hiển thị UI trực quan trên web trình duyệt cho người trực ban, vẽ biểu đồ trạng thái thời gian thực.

## 2.2 Thiết kế Topic Tree MQTT

Thay vì giao tiếp theo địa chỉ IP khó dự đoán, giao thức MQTT dùng các Topic String. Hệ thống sử dụng Prefix chung: `city/demo/intersection/001/` định danh duy nhất ngã tư thứ 001.

| Topic Path     | Chiều dữ liệu        | QoS | Chức năng (Ý nghĩa)                                      |
| -------------- | -------------------- | --- | -------------------------------------------------------- |
| `../state`     | Edge → Dashboard     | 0   | Phát trạng thái pha đèn, chu kỳ liên tục (Retained=True) |
| `../telemetry` | Edge → Dashboard     | 0   | Phát định kì thông số RSSI mạng, RAM, thời gian sống     |
| `../cmd`       | Dashboard → Edge     | 1   | Lệnh điều khiển khẩn cấp, yêu cầu báo nhận               |
| `../ack`       | Edge → Dashboard     | 1   | Phản hồi xác nhận lệnh `cmd_id` đã thực thi              |
| `../status`    | (Broker) → Dashboard | 1   | Bản tin LWT (Online / Offline) giữ lại trên Server       |

## 2.3 Tiêu chuẩn hóa thông điệp (JSON Payload Schema)

Nhằm đảm bảo khả năng mở rộng thuật toán đa ngôn ngữ (Python, C++, JS), tất cả gói tin được đóng gói theo định dạng chuẩn JSON.

Đặc biệt lưu ý, lệnh điều khiển mạng đôi khi có hiện tượng lặp (do cơ chế QoS 1 thử gửi lại). Để giải quyết triệt để tính chất này, mã JSON chèn thêm trường duy nhất `cmd_id` (UUID). Nếu vi điều khiển nhận lại một mã lệnh đã thực thi, nó sẽ trả về ACK ngay lập tức nhưng không thay đổi ngắt cứng (Hardware Interrupt), gọi là tính "Idempotent" (Kỹ thuật thường dùng trong DevOps ngân hàng).

## 2.4 Máy trạng thái điều khiển đèn (FSM)

Cụm đèn (Bắc-Nam gọi là NS, Đông-Tây gọi là EW) vận hành theo máy trạng thái hữu hạn, bao gồm 4 chế độ (Mode):

- **AUTO:** Tự động đếm vòng chu kì 6 Pha đèn chuẩn mực.
- **MANUAL:** Dừng cấp đông (Freeze) ở một Pha đèn cụ thể và giữ vô thời hạn. Lệnh này được gửi trong tình huống có xe ưu tiên, sự cố tai nạn tĩnh.
- **BLINK:** Đèn Vàng chớp tắt liên tục 2 hướng nhằm cảnh báo nhường đường.
- **OFF:** Tắt toàn bộ rơ le đèn khi thi công hoặc cắt điện ngã tư diện rộng.

Tại mô hình AUTO, 6 Pha được quy định theo tỷ lệ thời gian vàng. (1-NS_GREEN, 2-NS_YELLOW, 3-ALL_RED_CLEAR, 4-EW_GREEN, 5-EW_YELLOW, 6-ALL_RED_CLEAR). Bốn giây ALL_RED_CLEAR được bổ sung kĩ lưỡng nhằm đảm bảo toàn bộ phương tiện thoát khỏi tâm giao lộ, hạn chế nguy cơ va chạm.
