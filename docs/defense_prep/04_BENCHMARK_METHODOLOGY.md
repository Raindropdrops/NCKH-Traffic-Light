# 📊 CHƯƠNG 4: BENCHMARK & ĐO LƯỜNG (PHẦN NÂNG CẠO NHẤT ĐỂ ĐẠT 90+ ĐIỂM)

> **Mục tiêu:** Trong NCKH, có "Làm" thì phải có "Đo lường". Giám khảo sẽ soi kỹ kết quả Benchmark vì nó chứng minh hệ thống của bạn thực sự chạy được với độ trễ bao nhiêu.

## 1. Sự khác biệt giữa Ping thuần và Tool Benchmark của nhóm

Sinh viên thường dùng lệnh `ping` trong CMD để khoe mạng nhanh (1ms-5ms). Nhưng đó chỉ là ICMP layer network, không chứng minh Application MQTT chạy nhanh.

Tool `run_benchmark_report.py` do bạn viết làm nhiệm vụ giả lập "Thao tác tay của người trực chốt":
- Bắn lệnh CMD xuống (Kèm theo sinh ra 1 cái Ticket `cmd_id` duy nhất và lưu thời gian `T1`).
- ESP32 nhận được Ticket, làm nhiệm vụ đổi đèn (FSM), xuất ra cái biên lai ACK ghi kèm `cmd_id` đó.
- Python bắt được cái biên lai, ghi nhận thời gian `T2`.
- Tính **Độ trễ toàn trình RTT (Round-Trip Time) = T2 - T1**. (Đóng ngoặc quy trình khép kín).

---

## 2. One-Way Latency (Độ trễ đi và về bóc tách)

Bạn đã nâng cấp code để ESP32 gắn thêm thời gian của chính nó `edge_ts` vào cái gói ACK trả về. Nhờ đấy có số liệu 1 chiều:
- **T1:** Giây thứ 0. Thao tác trên Web (Publisher).
- **T2:** Giây thứ 25ms. ESP32 (Edge) nhận được lệnh thực thi: 👉 Đoạn này là **Edge Latency** (Chờ tải lệnh xuống).
- **T3:** Giây thứ 30ms. Máy tính Web nhận được ACK Confirm. 👉 Đoạn từ 25->30ms gọi là **Return Latency** (Đợi ESP xử lý mất 5ms).

**Lợi ích phản biện:** Khi hỏi *"Sao độ trễ tổng 200ms cao thế em?"*, thay vì ú ớ, bạn đưa chỉ số ra: *"Dạ, máy tính truyền lệnh mất có 50ms, nhưng con ESP32 chạy hàm Set Phase mất tới 150ms để tính toán chu kỳ an toàn."* (Cực kỳ thuyết phục).

---

## 3. Cụm Thuật Ngữ Payload và P99

Tool benchmark xuất ra thông số `p50`, `p95`, `p99`. Đây là **Percentile (Bách phân vị)**.
- **Trung bình (Mean) bị lừa dối:** Có 100 gói gửi mất 10ms. Có 1 gói bị nghẽn mạng mất 5000ms. Số Average bị đội lên tận 60ms làm hệ thống có vẻ kém.
- **P99 = 45ms:** Nghĩa là 99% người dùng trên thực tế Bấm Phát Đèn Đổi ngay lập tức chưa tới 45 Mili-giây. Chỉ có 1% cá biệt rơi vào điểm mù WiFi. (Bạn nói được câu này GV sẽ cho max điểm chuyên ngành Khoa học máy tính).

---

## 4. Multi-Device Benchmark Stress Test

Bạn dùng thêm `multi_device_test.py` giả lập 2 ngã tư bắn đồng thời để test độ nghẽn cốt lõi của máy chủ MQTT. (Chứng minh hệ thống scale tốt). Kết luận: Broker Mosquitto docker xử lý mượt mà, "Nút thắt cổ chai không nằm ở máy chủ, mà nằm ở băng thông mạng không dây của cột ESP32".

---

## 📌 Câu Hỏi Thuyết Trình

**Q: Bảng Data này em đo bằng cách nào? Liệu có đảm bảo tính khách quan không?**
👉 **Trả lời:** Thay vì em bấm tay 100 lần và bấm đồng hồ bấm giây không chính xác, em đã code 1 Script Python giả lập cường độ cao. Bắn liên tục 1000 yêu cầu (Stress payload rác ngẫu nhiên). Payload json đều sinh mã UUID riêng biệt để khi ACK trả lại về, thuật toán lấy đúng T2 trừ T1 chặn đứng rủi ro nhận láo gói tin cũ. Mọi file kết quả đều bung thẳng rãnh CSV để chạy Excel thống kê P90 P99 cực kỳ khách quan ạ.
