# 🏗️ CHƯƠNG 1: KIẾN TRÚC HỆ THỐNG & DEVOPS

> **Mục tiêu:** Nắm vững bức tranh tổng thể của dự án và cách các thành phần giao tiếp với nhau. Hội đồng rất thích hỏi "Hệ thống này hoạt động như thế nào?".

## 1. Kiến trúc 3 Cấp (3-Tier Architecture)

Dự án NCKH của bạn áp dụng phương pháp thiết kế **Edge-to-Cloud/Broker** điển hình trong IoT, phân rã làm 3 tầng độc lập:

### Tầng 1: Lớp Thiết Bị Phân Tán (Edge Layer - ESP32)
- **Nhiệm vụ:** Trực tiếp điều khiển phần cứng (đèn tín hiệu), thu thập trạng thái (telemetry: rssi, heap, uptime).
- **Đặc trưng:** Hoạt động độc lập (Autonomous). Nhờ luồng FSM (Finite State Machine), dù mạng có đứt, ESP32 vẫn tiếp tục điều khiển chu kỳ đèn Bình thường (AUTO) nhằm đảm bảo an toàn giao thông tuyệt đối.
- **Vai trò của bạn:** Bạn là người viết Firmware đa luồng cho tầng này.

### Tầng 2: Lớp Trung Tâm (Broker Layer - Eclipse Mosquitto)
- **Nhiệm vụ:** Trạm trung chuyển tin nhắn (Message Broker). Không chứa logic xử lý nghiệp vụ, chỉ làm nhiệm vụ tiếp nhận bản tin và phân định tuyến (Routing).
- **Công nghệ:** Triển khai bằng **Docker** (DevOps) để dễ dàng đóng gói, không phụ thuộc vào hệ điều hành của máy đích.
- **Port:**
  - `1883`: Cổng chuẩn của MQTT (Dùng cho ESP32 và Python Benchmark).
  - `9001`: Cổng WebSockets (Dùng cho Frontend Dashboard vì trình duyệt web không gọi trực tiếp giao thức MQTT thuần được).

### Tầng 3: Lớp Ứng Dụng (Application Layer - Dashboard & Tools)
- **Nhiệm vụ:** Hiển thị trực quan dữ liệu theo thời gian thực (Real-time Monitoring) và cho phép người trạm điều hành ra lệnh từ xa (Remote Control).
- **Công nghệ:** HTML/CSS/JS thuần, không dùng framework nặng nề (giúp load cực nhanh và dễ bảo trì).
- **Luồng dữ liệu:** Dashboard parse chuỗi JSON từ Broker để hiển thị biểu đồ và render giao diện.

---

## 2. Kỹ Thuật DevOps Đạt Điểm Cao

Ban giám khảo sẽ cực kỳ ấn tượng nếu bạn nhắc đến các keyword sau:

- **Docker & Docker Compose:** Bạn đã tự động hóa việc triển khai hệ thống (Infrastructure as Code). Thay vì phải cài cài đặt Mosquitto phức tạp, copy-paste file config, bạn chỉ cần gõ 1 lệnh `docker compose up -d` là toàn bộ hệ thống back-end hoạt động.
- **Mật khẩu & ACL (Access Control List):**
  - Hệ thống không cấu hình dạng "Anonymous" (mở toang) như các project sinh viên thông thường.
  - Bạn đã tạo file `mosquitto.pw` để mã hóa mật khẩu, chặn thiết bị lạ truy cập trái phép vào Broker. Bất kỳ ESP32 hay Dashboard nào muốn connect đều phải có `username/password`.
- **Tương lai mở rộng (Scalability):** Nếu thành phố có 100 ngã tư, kiến trúc này có sập không?
  - Trả lời: **Không**. Broker chỉ là trạm trung chuyển, các MQTT Topic được thiết kế dạng cây (Tree) `city/{id}/intersection/{id}/...`. Broker xử lý hàng chục ngàn kết nối song song tốt vì nó dùng Non-blocking I/O.

---

## 📌 Câu Hỏi Thuyết Trình

**Q: Tại sao em lại dùng WebSockets ở port 9001 thay vì gọi API REST HTTP thông thường?**
👉 **Trả lời:** Dạ, hệ thống đèn tín hiệu giao thông yêu cầu tính thời gian thực (Real-time). Nếu dùng HTTP (REST), trang web phải liên tục gửi request "Hỏi" server xem có thay đổi gì không (gọi là Polling/Pull) rất lãng phí tài nguyên mạng. Dùng WebSockets qua chuẩn MQTT (Push mechanism), máy chủ sẽ TỰ ĐỘNG "đẩy" dữ liệu về trình duyệt ngay khoảnh khắc đèn chuyển màu. Điều này giảm thiểu băng thông (overhead) và đạt phản hồi tức thời ạ.
