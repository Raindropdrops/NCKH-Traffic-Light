# Chương 4. Thử nghiệm kết quả và Đánh giá

Chương này trình bày các kịch bản thử nghiệm tải, đo lường RTT và đánh giá độ tin cậy hệ thống dựa trên dữ liệu thu thập từ công cụ Benchmark mô phỏng (Mock ESP32).

## 4.1 Môi trường và Công cụ Thử nghiệm

Hệ thống thử nghiệm được thiết lập trên môi trường mạng vòng cục bộ (loopback) để đánh giá khả năng xử lý nguyên bản của lõi MQTT Broker:

_Bảng 4.1: Cấu hình môi trường thử nghiệm_

| Thành phần  | Cấu hình                                   |
| ----------- | ------------------------------------------ |
| Broker      | Mosquitto 2.x (Docker, localhost:1883) [9] |
| Edge Device | mock_esp32.py (Python simulator)           |
| QoS cmd/ack | QoS 1 (At-least-once) [1]                  |
| Topic cmd   | `city/demo/intersection/001/cmd`           |
| Topic ack   | `city/demo/intersection/001/ack`           |

## 4.2 Định nghĩa và Kịch bản Test Độ trễ RTT

Trong bài toán giám sát, độ trễ RTT được định nghĩa là khoảng thời gian từ lúc Dashboard phát đi một lệnh điều khiển cho tới khi nhận lại xác nhận thiết bị đã chuyển pha đèn thành công [4]:

$$\text{RTT} = t_{\text{ack\_recv}} - t_{\text{cmd\_send}} \quad (\text{milliseconds})$$

_Bảng 4.2: Các Case thử nghiệm_

| Case | Payload pad (bytes) | Payload thực tế (bytes) | Số lệnh | Tần suất | Mô tả                |
| :--: | :-----------------: | :---------------------: | :-----: | :------: | -------------------- |
|  1   |          0          |          ~110           |   500   |  200ms   | Baseline             |
|  2   |         256         |          ~377           |   500   |  200ms   | Payload +256B        |
|  3   |         512         |          ~633           |   500   |  200ms   | Payload +512B        |
|  4   |         900         |          ~1021          |   500   |  200ms   | Payload giới hạn 1KB |
|  5   |        1200         |          ~1321          |   500   |  200ms   | **Oversize (>1KB)**  |

## 4.3 Phân tích Kết quả Thử nghiệm

_Bảng 4.3: Kết quả tổng hợp RTT từ 2500 tín hiệu thử nghiệm_

| Case | Sent | Recv | Loss% | Mean (ms) | Median (ms) | **Std Dev (ms)** | P95 (ms) | P99 (ms) | Max (ms) |    Đánh giá    |
| :--: | :--: | :--: | :---: | :-------: | :---------: | :--------------: | :------: | :------: | :------: | :------------: |
|  1   | 500  | 500  | 0.0%  |   43.3    |    43.0     |     **1.2**      |   45.0   |   47.0   |   49.0   |      PASS      |
|  2   | 500  | 500  | 0.0%  |   43.2    |    43.0     |     **1.1**      |   45.0   |   46.0   |   49.0   |      PASS      |
|  3   | 500  | 500  | 0.0%  |   43.3    |    43.0     |     **1.1**      |   45.0   |   46.0   |   48.0   |      PASS      |
|  4   | 500  | 500  | 0.0%  |   43.4    |    43.0     |     **1.2**      |   45.0   |   46.0   |   49.0   |      PASS      |
|  5   | 500  |  0   | 100%  |     —     |      —      |        —         |    —     |    —     |    —     | PASS (Bị chặn) |

> _Hình 4.1: Biểu đồ Histogram phân phối RTT cho Case 1-4 — chèn ảnh từ `results/bench_.../plots/`_
> _Hình 4.2: Biểu đồ ECDF so sánh các Case — chèn ảnh_
> _Hình 4.3: Biểu đồ so sánh RTT giữa các Case (Comparison Chart) — chèn ảnh_

### 4.3.1 Đánh giá Tính kiên định (Consistency) của độ trễ

Xuyên suốt các Case từ 1 đến 4, khi lượng dữ liệu tải (Payload) tăng từ 0 đến 900 Bytes, độ trễ trung bình (Mean) duy trì mức ổn định từ **43.2 ms đến 43.4 ms** (chênh lệch chỉ **0.5%**). Chỉ số phân vị P95 đạt **45.0 ms**, nghĩa là 95% gói tin hoàn tất trong vòng 45ms.

Đặc biệt, **độ lệch chuẩn (Std Dev) đạt chỉ ~1.1-1.2 ms**, cho thấy phân phối RTT rất hẹp và đồng nhất. Điều này chứng minh MQTT không tạo ra biến thiên bất thường ngay cả khi tải thay đổi đáng kể.

### 4.3.2 So sánh với các nghiên cứu liên quan

Kết quả của nhóm được đối chiếu với một số nghiên cứu đã công bố:

- Nghiên cứu của R. K. Kodali và S. R. Mahesh (2016) đo RTT MQTT trên Raspberry Pi qua WiFi đạt trung bình **52 ms** [11].
- Nghiên cứu của D. Mishra và S. P. Muddinagiri (2020) đo MQTT trên ESP8266 qua mạng 4G đạt trung bình **85-120 ms** [12].
- Kết quả của nhóm (**43.3 ms trên loopback**) thấp hơn do không chịu độ trễ truyền dẫn WiFi/4G, chỉ phản ánh overhead của giao thức MQTT + JSON parsing. Khi triển khai qua WiFi thực tế, dự kiến RTT sẽ tăng thêm 10-50ms.

### 4.3.3 Đánh giá Độ tin cậy và Bảo mật (Packet Loss & Rejection)

- **Packet Loss:** Xuyên suốt 2000 gói tin hợp lệ, tỷ lệ mất gói đạt **0.00%** nhờ cơ chế QoS 1 tự động thử gửi lại [1].
- **Oversize Rejection (Case 5):** Khi nhồi kích thước bản tin vượt ngưỡng 1024 Bytes, Mock ESP32 đã tự động loại bỏ bản tin và không trả ACK, đúng theo thiết kế chống DoS [10]. 500 lệnh gửi đi đều bị chặn (Loss 100%).

## 4.4 Giới hạn của Thử nghiệm (Mock vs Physical Device)

Cần nhấn mạnh, RTT ~43ms trên chỉ phản ánh overhead giao thức. Ở môi trường thực tế với ESP32 vật lý, RTT sẽ cộng dồn thêm:

1. Độ trễ sóng WiFi/4G (biến thiên 10ms–200ms) [12].
2. Thời gian chốt Interrupt chuyển đổi Rơ-le (vài ms).
3. Nhiễu điện từ tại giao lộ.

Dữ liệu mô phỏng chứng minh tính khả thi của giao thức về phía phần mềm. Số liệu thực tế sẽ được cập nhật ở giai đoạn 2.

## 4.5 Xác nhận tính năng Last Will And Testament (LWT)

Trong quá trình giả lập ngắt điện đột ngột (Kill Process Mock), Broker Mosquitto đã thành công phát hiện mất kết nối trong khoảng **~10-15 giây** (bằng 1.5× thông số Keep Alive interval = 10s) [7] và tự động thay mặt thiết bị phát tín hiệu Offline về Dashboard.

_Bảng 4.4: Kết quả thử nghiệm LWT_

| Kịch bản                       | Keep Alive (s) | Thời gian phát hiện offline | Kết quả |
| ------------------------------ | :------------: | :-------------------------: | :-----: |
| Kill Process Mock              |       10       |            ~15s             |   ĐẠT   |
| Ngắt mạng (Network disconnect) |       10       |            ~15s             |   ĐẠT   |
| Graceful disconnect (Ctrl+C)   |       —        |            < 1s             |   ĐẠT   |

Tính năng này cho phép điều phối viên giao thông nhận diện ngay lập tức trụ đèn mất tín hiệu, phối hợp cử lực lượng thay thế.
