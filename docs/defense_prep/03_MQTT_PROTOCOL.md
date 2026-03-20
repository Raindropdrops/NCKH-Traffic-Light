# 🌐 CHƯƠNG 3: GIAO THỨC MQTT & BẢO ĐẢM TÍN HIỆU

> **Mục tiêu:** Chứng minh thiết kế Network bài bản, tiết kiệm băng thông 3G/4G và tối ưu năng lượng.

## 1. Topic Tree (Cây thư mục Topic)

Các hệ thống cơ bản thường gửi chung mọi thứ vào 1 topic kiểu `traffic/data`. Hệ thống của bạn chia Topic rất chuyên nghiệp (`mqtt_handler.c`):

1. `city/{id}/intersection/{id}/cmd`: (Nhận) Lệnh điều khiển từ xa.
2. `city/{id}/intersection/{id}/ack`: (Gửi) Phản hồi xác nhận lệnh (Đã nhận - Thành công/Thất bại).
3. `city/{id}/intersection/{id}/state`: (Gửi) Tình trạng màu đèn hiện thời.
4. `city/{id}/intersection/{id}/status`: (Gửi) Tình trạng Online/Offline (LWT).
5. `city/{id}/intersection/{id}/telemetry`: (Gửi) Thông số kỹ thuật (Ram, Ping, Rssi).

👉 **Lợi ích:** Dashboard chỉ Subscribe những gì nó cần, không bị ngập lụt rác dữ liệu. Dễ debug.

---

## 2. QoS - Quality of Service (Chất lượng dịch vụ)

QoS là điểm ăn tiền nhất trong bài luận văn IoT:
- **Telemetry & State dùng QoS 0 (At most once):** Bắn và quên (Fire and Forget). 
  - Tại sao? Vì trạng thái đèn chớp liên tục 1 giây/lần. Rớt mạng mất 1 gói tin cũng không sao, giây tiếp theo sẽ có gói mới đè lên. Tối ưu tốc độ, xả bộ đệm nhanh.
- **Command & Ack dùng QoS 1 (At least once):** Bắn và phải có xác nhận. 
  - Tại sao? Lệnh Chuyển sang Vàng Nhấp Nháy là lệnh sống còn. Nếu Dashboard bắn lệnh xuống mà ngã tư không nhận được (Do QoS 0 bay mất dép) thì tai nạn xảy ra. QoS 1 đảm bảo Broker sẽ gửi đi gửi lại cho đến khi ESP32 nhận được. 

---

## 3. LWT - Last Will and Testament (Di chúc thư)

> "Làm sao trang web Dashboard biết cái đèn giao thông đã bị xe tải đâm gãy trụ cáp mạng mà đổi icon Đỏ (Disconnected)?"

Đây là sức mạnh của **Retained Message** và **LWT**:
- Lúc ESP32 login vào Broker, nó "ký gửi" một tờ Di chúc nội dung `{ "online": false }`.
- Nó gửi thêm 1 tin Message `{ "online": true }` (Retained - Lưu mãi trên Broker). Trang web vào sau đọc được luôn: "À, chốt này đang Online xanh lá".
- Nếu ESP32 đứt cáp, nó không kịp gửi tin Offline. Nhưng Broker đợi hết `KeepAlive` (Ví dụ 30s) mà không thấy ESP32 "thở" (Ping), Broker sẽ **TỰ ĐỘNG BÓC TỜ DI CHÚC VÀ GỬI CHO WEB**. Nhờ đó web lập tức chớp đèn "Reconnecting/Offline" đỏ.

---

## 📌 Câu Hỏi Thuyết Trình

**Q: Theo em MQTT có ưu điểm gì so với HTTP cho đề tài mạng cảm biến/IOT?**
👉 **Trả lời:** Dạ ESP32 là thiết bị tài nguyên thấp. Chuẩn MQTT sử dụng mô hình Pub/Sub (Publish/Subscribe) chạy đè trên TCP/IP nhưng cái phần "header" của gói tin rất nhỏ (có thể chỉ 2 Bytes). HTTP header rất cồng kềnh (hàng trăm Bytes Text). Giao thức này lại có QoS và duy trì kết nối (Persistent connection) thay vì đóng-mở liên tục như HTTP, nên cực kỳ tiết kiệm Pin và băng thông viễn thông (rất hợp lý nếu lắp trạm đèn ngoài cao tốc dùng SIM 4G ạ).
