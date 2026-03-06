# Chương 4. Thử nghiệm kết quả và Đánh giá

Chương này trình bày các kịch bản thử nghiệm tải (Load Testing), đo lường độ trễ mạng (Round-Trip Time - RTT) và đánh giá độ tin cậy của hệ thống dựa trên dữ liệu thu thập từ công cụ Benchmark mô phỏng (Mock ESP32).

## 4.1 Môi trường và Công cụ Thử nghiệm

Hệ thống thử nghiệm được thiết lập trên môi trường mạng vòng cục bộ (loopback) để đánh giá khả năng xử lý nguyên bản của lõi MQTT Broker và Node-RED Dashboard:

- **Broker:** Mosquitto 2.x (Docker, localhost:1883)
- **Thiết bị ảo (Edge Device):** Mã nguồn mô phỏng `mock_esp32.py`
- **Công cụ sinh tải:** Mã lệnh tự động `run_benchmark_report.py`
- **Mức QoS:** QoS 1 (At-least-once) cho luồng Gửi lệnh `cmd` và Nhận phản hồi `ack`.

## 4.2 Định nghĩa và Kịch bản Test Độ trễ RTT

Trong bài toán giám sát, độ trễ RTT được định nghĩa là khoảng thời gian từ lúc Dashboard phát đi một lệnh điều khiển (bấm nút) cho tới khi nhận lại xác nhận thiết bị đã chuyển pha đèn thành công.

$$\text{RTT} = t_{\text{ack\_recv}} - t_{\text{cmd\_send}}$$

- **Kịch bản:** Gửi tự động 500 tín hiệu điều khiển liên tiếp, với cường độ 1 lệnh mỗi 200 mili-giây.
- **Biến độc lập:** Tăng dần kích thước gói tin điều khiển (Payload pad) từ 0 Bytes lên 1200 Bytes nhằm thử tải và kiểm tra giới hạn bảo mật hệ thống.

## 4.3 Phân tích Kết quả Thử nghiệm

Dưới đây là bảng tổng hợp kết quả đo đạc từ 2500 tín hiệu thử nghiệm phân bổ đều trên 5 Case kích cỡ gói tin:

| Case | Payload pad | Giới hạn  | Số lệnh | Nhận  | RTT Mean | Median  |   P95   | Packet Loss |        Đánh giá        |
| :--: | :---------: | :-------: | :-----: | :---: | :------: | :-----: | :-----: | :---------: | :--------------------: |
|  1   |     0 B     |   ≤ 1KB   |   500   |  500  | 43.3 ms  | 43.0 ms | 45.0 ms |     0%      |          PASS          |
|  2   |    256 B    |   ≤ 1KB   |   500   |  500  | 43.2 ms  | 43.0 ms | 45.0 ms |     0%      |          PASS          |
|  3   |    512 B    |   ≤ 1KB   |   500   |  500  | 43.3 ms  | 43.0 ms | 45.0 ms |     0%      |          PASS          |
|  4   |    900 B    |   ≤ 1KB   |   500   |  500  | 43.4 ms  | 43.0 ms | 45.0 ms |     0%      |          PASS          |
|  5   | **1200 B**  | **> 1KB** | **500** | **0** |  **—**   |  **—**  |  **—**  |  **100%**   | **PASS (Bị loại trừ)** |

### 4.3.1 Đánh giá Tính kiên định (Consistency) của độ trễ

Xuyên suốt các Case từ 1 đến 4, khi lượng dữ liệu tải (Payload) nhồi thêm tăng từ 0 đến 900 Bytes, độ trễ trung bình (Mean) duy trì mức ổn định tịnh tiến rất nhỏ, giao động từ **43.2 ms đến 43.4 ms**. Chỉ số phân vị P95 đạt **45.0 ms** (nghĩa là 95% số lượng gói tin đều mất chưa tới 45ms để hoàn tất một chặng khứ hồi hoàn chỉnh).

Có thể đánh giá MQTT thể hiện tính hiệu quả băng thông vượt trội, gần như không gây quá tải cho bộ xử lý của Broker khi dữ liệu phình to.

### 4.3.2 Đánh giá Tính độ tin cậy và Bảo mật (Packet Loss và Rejection)

- **Packet Loss:** Xuyên suốt 2000 gói tin nội bộ ở giới hạn kích thước cho phép, tỷ lệ Packet Loss đạt mức tuyệt đối 0% nhờ cơ chế QoS 1 của MQTT tự động thử gửi lại (Retry) khi phát hiện mất mát tín hiệu.
- **Oversize Rejection (Tại Case 5):** Khi nhồi kích thước bản tin vượt qua ngưỡng chịu đựng thiết kế (1024 Bytes), thiết bị Mock ESP32 đã hoạt động chính xác theo kịch bản chống tấn công từ chối dịch vụ (DoS): Tự động cô lập, huỷ bỏ tín hiệu vi phạm và không trả về ACK. Điều này dẫn tới 500 lệnh gửi đi thất bại (Loss 100%), chứng minh mô hình hoạt động phòng vệ đúng thiết kế.

## 4.4 Giới hạn của Thử nghiệm (Mock vs Physical Device)

Cần làm rõ, các dữ liệu RTT ~43ms trên chỉ phản ánh "Overhead" của riêng giao thức TCP/MQTT và quá trình Parse chuỗi JSON tại trung tâm.

Ở môi trường ngã tư thực tế khi thay Mock ESP32 bằng mạch ESP32 vật lý, độ trễ RTT sẽ bị cộng dồn thêm:

1. Độ trễ vật lý sóng WiFi/4G (Biến thiên từ 10ms - 200ms).
2. Thời gian chốt Interrupt chuyển đổi vi mạch Rơ-le điện (Vài ms).
3. Độ trễ do sụt nguồn, nhiễu điện từ.

Dữ liệu mô phỏng này đóng vai trò chứng minh tính khả thi của giao thức về phía phần mềm. Việc thử nghiệm với thiết bị phần cứng thật sẽ được thực nghiệm và cập nhật số liệu ở tiến trình kế tiếp của đề tài.

## 4.5 Xác nhận tính năng Last Will And Testament (LWT)

Trong quá trình giả lập ngắt điện ngột ngột (Kill Process Mock), Broker Mosquitto đã thành công bắt lỗi rớt mạng ngang hàng và thay mặt thiết bị phát tín hiệu Offline về Dashboard. Tính năng này cho phép điều phối viên giao thông nhận diện ngay lập tức trụ đèn nào đang mất tín hiệu để phối hợp cử cảnh sát giao thông ra thay thế. Đánh giá tính năng này: ĐẠT.
