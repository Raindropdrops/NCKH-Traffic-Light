# 🎭 SLIDE OUTLINE (35 Slides) — Cấp Trường (Theo mẫu PL3)

> Mẫu PL3 khá mở, ta bám theo sườn của PL1 và tiêu chí chấm điểm PL5 để rải nội dung vào 35 slide. Ưu tiên Hình Ảnh/Biểu Đồ hơn chữ.

---

## Phần 1: Giới thiệu & Tổng Quan (Slides 1-6)

- **Slide 1:** Bìa (Tên đề tài, GVHD, SVTH - Theo đúng font mẫu PL3).
- **Slide 2:** Tổng quan tình hình nghiên cứu (Giao thông thông minh hiện nay).
- **Slide 3:** Lý do chọn đề tài (Giới hạn của Timer truyền thống vs Thế mạnh của IoT realtime).
- **Slide 4:** Cấu trúc bài thuyết trình (5 phần chính).
- **Slide 5:** Mục tiêu nghiên cứu (3 gạch đầu dòng ngắn: Xây dựng > Điều khiển > Đo RTT).
- **Slide 6:** Phương pháp & Đối tượng/Phạm vi (Thực nghiệm định lượng trên MQTT QoS).

## Phần 2: Cơ Sở Lý Thuyết IoT & MQTT (Slides 7-11)

- **Slide 7:** Protocol MQTT - Publish & Subscribe (Hình ảnh trực quan).
- **Slide 8:** Tại sao MQTT phù hợp? (Topic filter, Overhead thấp).
- **Slide 9:** 3 mức QoS (0, 1, 2) — Focus vào QoS 1 cho lệnh.
- **Slide 10:** Cơ chế LWT (Last Will Testament) để phát hiện offline.
- **Slide 11:** ESP32 và kiến trúc Event-Driven.

## Phần 3: Thiết Kế Hệ Thống Đèn Giao Thông (Slides 12-19)

- **Slide 12:** Sơ đồ khối tổng thể hệ thống (Dashboard -> Broker <- Edge).
- **Slide 13:** Cấu trức Topic Tree (`cmd`, `ack`, `state`, `telemetry`).
- **Slide 14:** Thiết kế JSON Payload chuẩn hóa.
- **Slide 15:** Cơ chế chống lặp lệnh (Idempotency) với `cmd_id`.
- **Slide 16:** State Machine (FSM): 4 Chế độ hoạt động (AUTO, MANUAL, BLINK, OFF).
- **Slide 17:** Logic luân chuyển chu kỳ đèn 6 Pha.
- **Slide 18:** Dashboard: Giao diện trực quan realtime.
- **Slide 19:** Dashboard UI Elements (Các khối chức năng SVG, Control).

## Phần 4: Thử Nghiệm Kết Quả & Đánh Giá Benchmark (Slides 20-30) **[TRỌNG TÂM - 40/100 Điểm]**

- **Slide 20:** Giới thiệu công cụ Mock ESP32 và công cụ Benchmark tự động.
- **Slide 21:** Kịch bản Benchmark: Thử nghiệm gửi 500 lệnh x 5 kích thước Payload.
- **Slide 22:** Định nghĩa và cách đo Độ trễ RTT (vòng lặp Cmd -> Broker -> ESP -> Broker -> Ack).
- **Slide 23:** Kết quả Benchmark: Payload chuẩn (0 - 900 Bytes).
- **Slide 24:** Biểu đồ Histogram: Phân phối RTT (Tập trung ở ~43ms).
- **Slide 25:** Biểu đồ ECDF (Xác suất RTT theo thời gian).
- **Slide 26:** Biểu đồ so sánh độ mượt giữa các chuẩn mức tải (Comparison Chart).
- **Slide 27:** Phân tích Oversize Rejection (Bảo mật MQTT, chặn Payload > 1KB).
- **Slide 28:** Kết quả Demo LWT Connection Log (Online/Offline Realtime).
- **Slide 29:** Bảng thông số: Tỷ lệ mất gói tin (Packet Loss = 0% trên 2000 lệnh nội bộ).
- **Slide 30:** Kết luận đánh giá tính ưu việt của hệ thống thực nghiệm.

## Phần 5: Kết Luận & Demo (Slides 31-35)

- **Slide 31:** Video Demo quay hệ thống (1 phút: Gửi lệnh và đèn nhảy).
- **Slide 32:** Đặc tính nổi bật của đồ án (Dashboard khoa học, Firmware tối ưu, Benchmark Data).
- **Slide 33:** Kết luận chung đóng góp của đề tài.
- **Slide 34:** Hướng phát triển đô thị (Cluster Broker, Edge AI đếm xe).
- **Slide 35:** Cảm ơn Hội đồng (Trang cuối).
