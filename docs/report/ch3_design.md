# Chương 2. Thiết kế Kiến trúc Hệ thống Điều khiển

Hệ thống điều khiển đèn giao thông dựa trên chuẩn MQTT theo mô hình Client-Broker-Client được nhóm thiết kế nhằm khắc phục điểm yếu của điều khiển vòng từ truyền thống [2], cung cấp khả năng giám sát liên tục và phản hồi linh hoạt.

## 2.1 Sơ đồ khối tổng thể của hệ thống

> _Hình 2.1: Sơ đồ khối tổng thể hệ thống (Edge Device ↔ MQTT Broker ↔ Web Dashboard) — chèn hình vào Word_

Hệ thống được chia làm 3 thành phần chính (End-to-end Architecture):

1. **MQTT Broker (Core):** Là máy chủ trung tâm nhận dữ liệu, xử lý phân quyền. Cài đặt trên Docker sử dụng mã nguồn mở Eclipse Mosquitto [9].
2. **Edge Device (ESP32 Controller):** Lắp đặt trực tiếp tại các tủ điều khiển ngã tư. Đọc cảm biến cứng, điều khiển rơ-le đèn, gửi trạng thái về Broker, và lắng nghe lệnh ghi đè (Override Command).
3. **Web Dashboard (HTML/WebSocket):** Trung tâm giám sát. Hiển thị UI trực quan trên web trình duyệt cho người trực ban, vẽ biểu đồ trạng thái thời gian thực.

## 2.2 Thiết kế Topic Tree MQTT

Thay vì giao tiếp theo địa chỉ IP, giao thức MQTT dùng các Topic String [1]. Hệ thống sử dụng Prefix chung: `city/demo/intersection/001/` định danh duy nhất ngã tư thứ 001.

_Bảng 2.1: Thiết kế Topic Tree MQTT_

| Topic Path     | Chiều dữ liệu        | QoS | Chức năng                                                |
| -------------- | -------------------- | --- | -------------------------------------------------------- |
| `../state`     | Edge → Dashboard     | 0   | Phát trạng thái pha đèn, chu kỳ liên tục (Retained=True) |
| `../telemetry` | Edge → Dashboard     | 0   | Phát định kì thông số RSSI mạng, RAM, thời gian sống     |
| `../cmd`       | Dashboard → Edge     | 1   | Lệnh điều khiển khẩn cấp, yêu cầu báo nhận               |
| `../ack`       | Edge → Dashboard     | 1   | Phản hồi xác nhận lệnh `cmd_id` đã thực thi              |
| `../status`    | (Broker) → Dashboard | 1   | Bản tin LWT (Online / Offline) retain trên Server        |

## 2.3 Tiêu chuẩn hóa thông điệp (JSON Payload Schema)

Tất cả gói tin được đóng gói theo chuẩn JSON nhằm đảm bảo khả năng mở rộng đa ngôn ngữ (Python, C++, JavaScript).

Lệnh điều khiển mạng đôi khi có hiện tượng lặp (do cơ chế QoS 1 thử gửi lại). Để giải quyết triệt để, mã JSON chèn thêm trường duy nhất `cmd_id` (UUID). Nếu vi điều khiển nhận lại một mã lệnh đã thực thi, nó sẽ trả về ACK ngay lập tức nhưng không thay đổi ngắt cứng (Hardware Interrupt) — gọi là tính "Idempotent" [10].

## 2.4 Máy trạng thái điều khiển đèn (FSM)

> _Hình 2.2: Sơ đồ máy trạng thái hữu hạn (FSM) cho 4 chế độ và 6 pha đèn — chèn hình vào Word_

Cụm đèn (Bắc-Nam gọi là NS, Đông-Tây gọi là EW) vận hành theo máy trạng thái hữu hạn, bao gồm 4 chế độ (Mode):

- **AUTO:** Tự động đếm vòng chu kì 6 Pha đèn chuẩn mực.
- **MANUAL:** Dừng cấp đông (Freeze) ở một Pha đèn cụ thể và giữ vô thời hạn. Dùng trong tình huống xe ưu tiên hoặc sự cố.
- **BLINK:** Đèn Vàng chớp tắt liên tục 2 hướng nhằm cảnh báo nhường đường.
- **OFF:** Tắt toàn bộ rơ-le đèn khi thi công hoặc cắt điện diện rộng.

_Bảng 2.2: Chi tiết 6 Pha trong chế độ AUTO_

| Pha | Tên       | Đèn NS  | Đèn EW  | Thời gian mặc định |
| :-: | --------- | :-----: | :-----: | :----------------: |
|  0  | NS_GREEN  | 🟢 Xanh |  🔴 Đỏ  |        30s         |
|  1  | NS_YELLOW | 🟡 Vàng |  🔴 Đỏ  |         3s         |
|  2  | ALL_RED   |  🔴 Đỏ  |  🔴 Đỏ  |         4s         |
|  3  | EW_GREEN  |  🔴 Đỏ  | 🟢 Xanh |        30s         |
|  4  | EW_YELLOW |  🔴 Đỏ  | 🟡 Vàng |         3s         |
|  5  | ALL_RED   |  🔴 Đỏ  |  🔴 Đỏ  |         4s         |

Pha ALL_RED (Pha 2 và 5) kéo dài 4 giây được bổ sung nhằm đảm bảo toàn bộ phương tiện thoát khỏi tâm giao lộ trước khi hướng đối diện bật xanh.
