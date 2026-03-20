# ⚙️ CHƯƠNG 2: ESP32 FIRMWARE (C & ESP-IDF)

> **Mục tiêu:** Chứng minh sự am hiểu sâu sắc về Lập trình Hệ thống (Systems Programming) và lý do tại sao bộ code này đạt "Chuẩn Công Nghiệp" thay vì chỉ là bài tập đồ án sinh viên.

## 1. Tại sao lại dùng ESP-IDF thay vì Arduino C?

Nhiều sinh viên dùng Arduino IDE để lập trình ESP32 vì dễ. Nhưng bạn đã chọn **ESP-IDF** (Internet of Things Development Framework của chính hãng Espressif). 
- **Lý do:** ESP-IDF chạy hệ điều hành thời gian thực **FreeRTOS**. Nó cho phép mã nguồn chạy **Đa luồng (Multi-threading)**.
- **Trong dự án của bạn:** 
  - Nhiệm vụ chớp tắt đèn giao thông (phần cứng) và nhiệm vụ giao tiếp MQTT/WiFi (mạng) được vận hành trên **Hai luồng hoàn toàn song song**. Nhờ đó, nếu mạng bị lag hoặc Broker phản hồi chậm, chu kỳ điếm ngược của đèn LED 100% không bị ảnh hưởng (không bị delay/giật lag gián đoạn). Arduino single-thread rất dễ bị đứng hình (block) khi mạng lag.

---

## 2. Kiến trúc Cỗ Máy Trạng Thái (FSM - Finite State Machine)

Code điều khiển lõi nằm ở file `fsm_controller.c`.
Hệ thống đèn có 4 **Mode (Chế độ)** và 6 **Phase (Pha)**.
- **Mode:** AUTO (tự chạy), MANUAL (chờ lệnh tay), FLASHING (vàng chớp báo khuya), OFF (Tắt).
- **Phân bổ FSM:** Mỗi Phase (Pha) tương ứng với trạng thái kết hợp của các hướng (Bắc-Nam và Đông-Tây).
  - P0: NS(Xanh) - EW(Đỏ)
  - P1: NS(Vàng) - EW(Đỏ)
  - P2: ALL_RED (Vùng đệm dọn giao lộ - Safety buffer)
  - P3: NS(Đỏ) - EW(Xanh)
  - P4: ...

**Điểm ăn tiền:** Mọi hàm thay đổi vòng lặp/trạng thái (`fsm_set_mode`) đều được bọc bởi **freertos/Semaphore**. Biến Mutex (Khóa) bảo vệ dữ liệu không bị ghi đè khi bị 2 luồng cùng tác động (ví dụ: ngã tư đang chuẩn bị tự động chuyển xanh thì đúng lúc có ông thao tác viên bấm nút trên Dashboard bắt buộc chuyển sang màu Vàng chớp).

---

## 3. Ba Vũ Khí "Chuẩn Công Nghiệp" Đỉnh Nhất Trong Firmware

Đừng chờ Giám khảo hỏi, **HÃY TỰ HÀO GIỚI THIỆU 3 TÍNH NĂNG NÀY LÊN CAM:**

### 🚀 Tính năng số 1: Task Watchdog Timer (TWDT)
Bạn đã lập trình sẵn cơ chế WDT có timeout 30 giây trong `app_main.c` (Dòng config `esp_task_wdt_init`).
> **Giải thích:** Phầm mềm nào cũng có khả năng bị "treo" (bộ nhớ tràn, vòng lặp vô tận do ngoại lệ từ vi điều khiển). WDT giống như nhịp tim (feed the dog). Cứ sau 1 vòng code chạy xong, code lại báo cho con chip là "tôi còn sống". Nếu sau 30s con chip không thấy tim đập, Hardware sẽ tự "tát" hệ thống thức dậy (Hardware Panic Reset), tự cắm rễ khởi động lại luôn mà không cần ai ra cột đèn để rút điện cắm lại. Đây là yếu tố cực kỳ then chốt của thiết bị thông minh.

### 🚀 Tính năng số 2: Fallback (Chế Độ Thoái Lui An Toàn)
Điều gì xảy ra nếu Mosquitto server bị mất điện, hoặc hacker cắt đứt cáp quang mạng của thành phố? Nút bấm không ăn nhưng đèn bị tắt luôn ngã tư kẹt cứng?
> **Giải thích:** ESP32 đang theo dõi liên tục trạng thái Offline (`mqtt_get_offline_duration_ms`). Nếu mất kết nối với máy chủ vượt quá 10 giây (OFFLINE_TIMEOUT_MS), vi điều khiển TỰ ĐỘNG thu hồi quyền điều khiển bằng tay và chuyển hệ thống về mốt `AUTO` (Chu kỳ xanh đỏ vàng nội bộ). An toàn giao thông là ưu tiên vượt lên kết nối IoT.

### 🚀 Tính năng số 3: Idempotency Cache (Chống lệnh ma)
> **Giải thích:** Người bấm nút trên Dashboard bị run tay, bấm đúp 2 phát (Hoặc do TCP retry gửi 2 lần 1 bản tin). Firmware có một mảng Ring Buffer (Băng chuyền tròn) lưu trữ 64 cái `cmd_id` gần nhất (`mqtt_handler.c`). Khi có lệnh lạ rơi xuống, nó quét mảng này. Nếu `cmd_id` vừa bị xử lý cách đây 10ms rồi, nó sẽ từ chối thưc thi lại, nhưng vẫn giả vờ gửi `ACK` lên để báo "Tao đã làm rồi". Không bao giờ xảy ra tình trạng nhiễu loạn luồng chạy của LED.

---

## 📌 Câu Hỏi Thuyết Trình

**Q: Tại sao phải dùng FreeRTOS Mutex Semaphore vào cái đèn giao thông này?**
👉 **Trả lời:** Dạ thưa thầy, trên hệ điều hành FreeRTOS của ESP, tài nguyên (Resource - cụ thể là Biến Trạng Thái) được chia sẻ giữa Luồng Đọc MQTT (Đến từ mạng lưới) và Luồng Vòng lặp FSM (Tính chu kỳ). Rất có khả năng một hành động Bấm nút từ Dashboard đến TRÙNG VỚI MILI-GIÂY đèn đang chuyển Vàng. Nếu ghi đè đồng thời (Race Condition), Crash CPU gây treo đèn là chắc chắn. Semaphore đóng vai trò làm Vệ Sĩ, ai vào thì Khoá trái cửa xử lý biến xong mới mở khóa cho người khác vào.
