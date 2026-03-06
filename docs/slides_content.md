# 📊 NỘI DUNG SLIDE THUYẾT TRÌNH NCKH (35 SLIDES)

> Copy/paste vào PowerPoint. Mỗi slide bao gồm: Tiêu đề, Bullet points, và Ghi chú thuyết trình.

---

## PHẦN 1: GIỚI THIỆU & TỔNG QUAN (Slides 1–6)

---

### 🔹 SLIDE 1 — Trang bìa

**TRƯỜNG ĐẠI HỌC GIAO THÔNG VẬN TẢI**
**NCKH SINH VIÊN CẤP TRƯỜNG NĂM 2025**

**Tên đề tài:**
NGHIÊN CỨU ỨNG DỤNG IoT – MQTT TRONG GIÁM SÁT VÀ ĐIỀU KHIỂN TỪ XA HỆ THỐNG ĐÈN TÍN HIỆU GIAO THÔNG

- **Sinh viên thực hiện:** <Họ tên — in đậm SV chính>
- **Lớp:** <Tên lớp>
- **Khoa:** <Tên Khoa>
- **Người hướng dẫn:** <Chức danh, họ tên GVHD>

HÀ NỘI, 2025

---

### 🔹 SLIDE 2 — Tổng quan vấn đề

**Tình hình giao thông đô thị hiện nay**

- 🚦 Hệ thống đèn truyền thống chủ yếu dùng **bộ hẹn giờ cứng** (timer-based)
- ❌ Không giám sát từ xa được → khó phát hiện đèn hỏng
- ❌ Không thay đổi chu kỳ linh hoạt → gây ùn tắc cục bộ
- 🌍 Xu hướng thế giới: **IoT + Smart City** kết nối thiết bị qua mạng không dây

> 🎤 _"Hệ thống giao thông hiện tại tại Việt Nam, dù đã có SCATS tại TP.HCM và UTC Siemens tại Hà Nội, nhưng phần lớn dùng cáp quang đắt đỏ và giao thức độc quyền."_

---

### 🔹 SLIDE 3 — Lý do chọn đề tài

**Tại sao chọn MQTT cho đèn giao thông?**

- ✅ Header MQTT chỉ **2 bytes** (HTTP: hàng trăm bytes)
- ✅ Mô hình **Publish/Subscribe**: không cần biết IP thiết bị
- ✅ **QoS 1**: đảm bảo lệnh điều khiển không bị mất
- ✅ **LWT**: tự động phát hiện thiết bị mất kết nối
- 🔬 **Khoảng trống NC:** Chưa có nghiên cứu đo lường RTT của MQTT cho đèn giao thông tại VN

> 🎤 _"MQTT là giao thức nhẹ nhất trong IoT, nhưng chưa được đo hiệu năng cụ thể cho bài toán đèn tín hiệu. Đó là lý do chúng tôi chọn đề tài này."_

---

### 🔹 SLIDE 4 — Cấu trúc bài thuyết trình

**Nội dung trình bày**

1. ⚡ Cơ sở lý thuyết (IoT & MQTT)
2. 🏗️ Thiết kế hệ thống
3. 💻 Triển khai xây dựng
4. 📊 **Thử nghiệm & Đánh giá** ← Trọng tâm (40 điểm)
5. 🎯 Kết luận & Demo

---

### 🔹 SLIDE 5 — Mục tiêu nghiên cứu

**3 Mục tiêu chính**

|  #  | Mục tiêu                               |   Kết quả dự kiến   |
| :-: | -------------------------------------- | :-----------------: |
|  1  | Xây dựng mô hình giám sát & điều khiển |   Demo hoạt động    |
|  2  | Đo lường độ trễ RTT & tỷ lệ mất gói    | Số liệu định lượng  |
|  3  | Dashboard thời gian thực               | Giao diện trực quan |

---

### 🔹 SLIDE 6 — Phương pháp & Phạm vi

**Phương pháp nghiên cứu**

- 📚 **Lý thuyết:** Nghiên cứu tiêu chuẩn MQTT v5.0 (OASIS)
- 🔬 **Thực nghiệm:** Benchmark 500 lệnh × 5 mức payload, tần suất 1 lệnh/200ms
- **Phạm vi:** 1 ngã tư 4 hướng
  - Giai đoạn 1: Mock ESP32 (loopback) ✅
  - Giai đoạn 2: ESP32 thật qua WiFi (đang phát triển)

---

## PHẦN 2: CƠ SỞ LÝ THUYẾT (Slides 7–11)

---

### 🔹 SLIDE 7 — Giao thức MQTT

**MQTT — Publish / Subscribe**

> _Chèn Hình 1.1: Sơ đồ mô hình Pub/Sub_

- **Publisher** gửi tin lên **Broker** theo **Topic**
- **Subscriber** lắng nghe Topic → nhận dữ liệu realtime
- Broker = "Bưu điện trung tâm" → Publisher & Subscriber không cần biết nhau

> 🎤 _"Khác với HTTP phải gọi-đáp, MQTT cho phép Dashboard tự động nhận dữ liệu ngay khi ESP32 gửi, không cần polling."_

---

### 🔹 SLIDE 8 — Tại sao MQTT phù hợp?

**So sánh MQTT vs HTTP vs CoAP**

| Tiêu chí      |     MQTT     |    HTTP    |  CoAP  |
| ------------- | :----------: | :--------: | :----: |
| Header        |    **2B**    |   ~200B    |   4B   |
| Realtime Push |    ✅ Tốt    | ❌ Polling | ⚠️ Khá |
| Giao thức     |     TCP      |    TCP     |  UDP   |
| Băng thông    | **Cực thấp** |    Cao     |  Thấp  |

→ **MQTT = Lựa chọn tối ưu cho IoT giao thông**

---

### 🔹 SLIDE 9 — QoS (Quality of Service)

**3 mức QoS trong MQTT**

|  QoS  | Tên               | Đặc điểm                  | Dùng cho                   |
| :---: | ----------------- | ------------------------- | -------------------------- |
|   0   | Fire-and-forget   | Nhanh, không xác nhận     | Telemetry (nhiệt độ, RSSI) |
| **1** | **At-least-once** | **Có ACK, retry nếu mất** | **Lệnh điều khiển đèn**    |
|   2   | Exactly-once      | Bắt tay 4 bước            | Giao dịch tài chính        |

> 🎤 _"Chúng tôi chọn QoS 1 cho lệnh điều khiển vì không thể chấp nhận bỏ sót lệnh đổi đèn. QoS 0 dùng cho dữ liệu telemetry liên tục."_

---

### 🔹 SLIDE 10 — LWT (Last Will & Testament)

**Phát hiện thiết bị offline tự động**

1. ESP32 kết nối Broker → gửi kèm bản tin LWT: `{"online": false}`
2. ESP32 hoạt động bình thường → gửi `{"online": true}`
3. ESP32 **mất điện đột ngột** → Broker phát hiện → **tự động gửi LWT cho Dashboard**
4. Dashboard hiện 🔴 **OFFLINE** ngay lập tức (~15 giây)

→ Điều phối viên biết ngay trụ đèn nào bị sự cố!

---

### 🔹 SLIDE 11 — Vi điều khiển ESP32

**ESP32 — Bộ não tại ngã tư**

- Lõi kép 240MHz + WiFi/Bluetooth tích hợp
- Hệ điều hành FreeRTOS: đa luồng đồng thời
- Framework ESP-IDF v5.5 (không dùng Arduino)
- 4 luồng chính: MQTT Network, Command Handler, GPIO LED, Telemetry

---

## PHẦN 3: THIẾT KẾ HỆ THỐNG (Slides 12–19)

---

### 🔹 SLIDE 12 — Sơ đồ khối tổng thể

**Kiến trúc 3 tầng**

> _Chèn Hình 2.1: Sơ đồ khối Edge ↔ Broker ↔ Dashboard_

```
[ESP32 Edge] ←──MQTT──→ [Mosquitto Broker] ←──WebSocket──→ [Web Dashboard]
   GPIO LEDs              Docker Container              HTML5/CSS3/JS
```

---

### 🔹 SLIDE 13 — Topic Tree MQTT

**Cây chủ đề MQTT cho 1 ngã tư**

| Topic           |      Hướng       |  QoS  | Chức năng            |
| --------------- | :--------------: | :---: | -------------------- |
| `.../state`     |  Edge→Dashboard  |   0   | Trạng thái pha đèn   |
| `.../telemetry` |  Edge→Dashboard  |   0   | RSSI, RAM, Uptime    |
| `.../cmd`       |  Dashboard→Edge  | **1** | **Lệnh điều khiển**  |
| `.../ack`       |  Edge→Dashboard  | **1** | **Xác nhận lệnh**    |
| `.../status`    | Broker→Dashboard |   1   | Online/Offline (LWT) |

---

### 🔹 SLIDE 14 — JSON Payload Schema

**Chuẩn hóa thông điệp JSON**

```json
// Lệnh điều khiển (cmd)
{
  "cmd_id": "a1b2c3d4-...",
  "type": "SET_MODE",
  "mode": "MANUAL",
  "ts_ms": 1709712000000
}

// Phản hồi (ack)
{
  "cmd_id": "a1b2c3d4-...",
  "ok": true,
  "error": null
}
```

---

### 🔹 SLIDE 15 — Chống lệnh trùng (Idempotency)

**Vấn đề:** QoS 1 có thể gửi lại lệnh → ESP32 nhận 2 lần

**Giải pháp:** Mỗi lệnh có `cmd_id` (UUID) duy nhất

- ESP32 lưu danh sách `cmd_id` đã xử lý
- Nếu trùng → trả ACK ngay, **KHÔNG đổi đèn lần nữa**
- → Đảm bảo an toàn cho hệ thống giao thông

---

### 🔹 SLIDE 16 — FSM: 4 Chế độ hoạt động

**Máy trạng thái hữu hạn — 4 Mode**

> _Chèn Hình 2.2: Sơ đồ FSM_

| Mode       | Chức năng            | Khi nào dùng          |
| ---------- | -------------------- | --------------------- |
| **AUTO**   | Chu kỳ 6 pha tự động | Hoạt động bình thường |
| **MANUAL** | Giữ 1 pha cố định    | Xe ưu tiên, tai nạn   |
| **BLINK**  | Vàng chớp tắt        | Cảnh báo nhường đường |
| **OFF**    | Tắt hết              | Thi công, cắt điện    |

---

### 🔹 SLIDE 17 — Chu kỳ 6 Pha đèn

**Vòng lặp đèn trong chế độ AUTO**

| Pha |   Đèn NS   |   Đèn EW   | Thời gian |
| :-: | :--------: | :--------: | :-------: |
|  0  |  🟢 Xanh   |   🔴 Đỏ    |    30s    |
|  1  |  🟡 Vàng   |   🔴 Đỏ    |    3s     |
|  2  | 🔴 ALL-RED | 🔴 ALL-RED |    4s     |
|  3  |   🔴 Đỏ    |  🟢 Xanh   |    30s    |
|  4  |   🔴 Đỏ    |  🟡 Vàng   |    3s     |
|  5  | 🔴 ALL-RED | 🔴 ALL-RED |    4s     |

> 🎤 _"Pha ALL-RED kéo dài 4 giây là thiết kế an toàn, đảm bảo phương tiện rời tâm giao lộ trước khi hướng đối diện bật xanh."_

---

### 🔹 SLIDE 18 — Dashboard Overview

**Giao diện giám sát thời gian thực**

> _Chèn Hình 3.1: Ảnh chụp Dashboard (Dark Theme)_

- 🎮 Control Panel: 4 nút Mode + Phase Selector
- 🚦 SVG Intersection: Mô phỏng ngã tư trực quan
- 📊 RTT Realtime Chart: Biểu đồ độ trễ sống
- 🔒 QoS Panel: Hiện mức QoS từng Topic
- 🔌 LWT Log: Lịch sử Online/Offline

---

### 🔹 SLIDE 19 — Dashboard UI Elements

**Các tính năng khoa học Dashboard**

| Tính năng | Mô tả                  |       Ý nghĩa NCKH       |
| --------- | ---------------------- | :----------------------: |
| RTT Chart | Canvas vẽ realtime     |  Đo hiệu năng trực tiếp  |
| QoS Panel | Hiện QoS/topic         |   Giải thích thiết kế    |
| LWT Log   | Online/Offline history | Chứng minh LWT hoạt động |
| ACK Log   | Lịch sử cmd→ack        |   Xác minh Idempotency   |

---

## PHẦN 4: THỬ NGHIỆM & ĐÁNH GIÁ (Slides 20–30) ⭐ TRỌNG TÂM

---

### 🔹 SLIDE 20 — Công cụ kiểm thử

**Mock ESP32 & Benchmark Tool**

- **Mock ESP32** (`mock_esp32.py`):
  - Giả lập 100% logic thiết bị thật
  - Telemetry thực tế (RSSI drift, Heap giảm dần)
  - Hỗ trợ `--speed 2x` cho demo nhanh
- **Benchmark** (`run_benchmark_report.py`):
  - Gửi tự động N lệnh với tần suất cố định
  - Thu thập RTT, tạo biểu đồ Histogram/ECDF
  - Xuất báo cáo Markdown + CSV

---

### 🔹 SLIDE 21 — Kịch bản Benchmark

**Thiết kế thử nghiệm tải**

| Thông số         | Giá trị                           |
| ---------------- | --------------------------------- |
| Số lệnh mỗi Case | 500                               |
| Số Case          | 5 (0B, 256B, 512B, 900B, 1200B)   |
| Tổng số lệnh     | **2500**                          |
| Tần suất         | 1 lệnh / 200ms                    |
| QoS              | QoS 1 (At-least-once)             |
| Broker           | Mosquitto 2.x (Docker, localhost) |

---

### 🔹 SLIDE 22 — Định nghĩa RTT

**Round-Trip Time (Độ trễ khứ hồi)**

```
RTT = t_ack_recv − t_cmd_send (milliseconds)
```

> _Chèn sơ đồ: Dashboard → Broker → ESP32 → Broker → Dashboard_

- `t_cmd_send`: Thời điểm Dashboard gửi lệnh
- `t_ack_recv`: Thời điểm Dashboard nhận ACK

---

### 🔹 SLIDE 23 — Kết quả Benchmark

**Bảng tổng hợp RTT — 2500 tín hiệu**

| Case |  Payload  | Recv  |   Loss   |  Mean  | **Std Dev** | P95  |
| :--: | :-------: | :---: | :------: | :----: | :---------: | :--: |
|  1   |    0B     |  500  |  **0%**  | 43.3ms |  **1.2ms**  | 45ms |
|  2   |   256B    |  500  |  **0%**  | 43.2ms |  **1.1ms**  | 45ms |
|  3   |   512B    |  500  |  **0%**  | 43.3ms |  **1.1ms**  | 45ms |
|  4   |   900B    |  500  |  **0%**  | 43.4ms |  **1.2ms**  | 45ms |
|  5   | **1200B** | **0** | **100%** |   —    |      —      |  —   |

> 🎤 _"RTT ổn định ~43ms bất kể payload. Std Dev chỉ 1.1ms chứng minh tính đồng nhất. Case 5 bị chặn 100% đúng thiết kế."_

---

### 🔹 SLIDE 24 — Histogram RTT

**Phân phối RTT**

> _Chèn Hình 4.1: Histogram từ `results/bench_.../plots/histogram_case_1.png`_

- Phân phối RTT tập trung quanh **43ms**
- Không có outlier đáng kể
- Đỉnh phân phối rõ ràng → MQTT xử lý ổn định

---

### 🔹 SLIDE 25 — ECDF Comparison

**Hàm phân phối tích lũy thực nghiệm**

> _Chèn Hình 4.2: ECDF từ `results/bench_.../plots/ecdf_comparison.png`_

- 50% lệnh hoàn thành trong **≤43ms**
- 95% lệnh hoàn thành trong **≤45ms**
- 4 đường ECDF gần như trùng nhau → **Payload không ảnh hưởng RTT**

---

### 🔹 SLIDE 26 — Comparison Chart

**So sánh RTT giữa các Case**

> _Chèn Hình 4.3: Comparison Chart từ `results/bench_.../plots/comparison_chart.png`_

- RTT chênh lệch giữa 0B và 900B chỉ **0.1ms** (0.2%)
- → MQTT header nhẹ, xử lý nhanh không phụ thuộc kích thước payload

---

### 🔹 SLIDE 27 — Oversize Rejection

**Bảo vệ hệ thống khỏi payload quá lớn**

- Case 5: Payload **1200 bytes** (>1KB)
- Kết quả: **500/500 lệnh bị chặn** → Loss 100%
- ESP32 tự động loại bỏ → không trả ACK
- → Chống tấn công DoS tràn bộ nhớ đệm ✅

> 🎤 _"Đây là cơ chế phòng thủ. Nếu hacker gửi payload lớn, thiết bị sẽ tự động bỏ qua mà không bị crash."_

---

### 🔹 SLIDE 28 — LWT Connection Log

**Kết quả thử nghiệm LWT**

| Kịch bản        | Thời gian phát hiện | Kết quả |
| --------------- | :-----------------: | :-----: |
| Kill Process    |        ~15s         | ✅ ĐẠT  |
| Ngắt mạng       |        ~15s         | ✅ ĐẠT  |
| Graceful Ctrl+C |         <1s         | ✅ ĐẠT  |

> _Chèn ảnh Dashboard hiện 🔴 OFFLINE trong Connection Log_

---

### 🔹 SLIDE 29 — So sánh với NC khác

**Đối chiếu kết quả**

| Nghiên cứu                  | Thiết bị       |     Mạng     |     RTT      |
| --------------------------- | -------------- | :----------: | :----------: |
| Kodali & Mahesh (2016)      | Raspberry Pi   |     WiFi     |   **52ms**   |
| Mishra & Muddinagiri (2020) | ESP8266        |      4G      | **85-120ms** |
| **Đề tài này**              | **Mock ESP32** | **Loopback** |  **43.3ms**  |

> 🎤 _"43ms của chúng tôi là protocol overhead thuần. Khi thêm WiFi, dự kiến RTT ~53-93ms, vẫn tốt hơn nghiên cứu qua 4G."_

---

### 🔹 SLIDE 30 — Tổng kết đánh giá

**Kết luận thử nghiệm**

| Tiêu chí             |  Kết quả  |     Đánh giá     |
| -------------------- | :-------: | :--------------: |
| RTT trung bình       |  43.3ms   |   ✅ Xuất sắc    |
| Std Dev              |   1.2ms   |  ✅ Rất ổn định  |
| Packet Loss (hợp lệ) |  **0%**   |   ✅ Hoàn hảo    |
| Oversize Rejection   | 100% chặn | ✅ Đúng thiết kế |
| LWT Detection        |   ~15s    |      ✅ Đạt      |

→ **MQTT đáp ứng hoàn toàn yêu cầu điều khiển đèn giao thông!**

---

## PHẦN 5: KẾT LUẬN & DEMO (Slides 31–35)

---

### 🔹 SLIDE 31 — Live Demo

**Demo hệ thống hoạt động**

- 🖥️ Mở Dashboard tại `http://localhost:1880/index.html`
- 🤖 Mock ESP32 chạy ở chế độ `--speed 2`
- 🎮 Demo gửi lệnh: AUTO → MANUAL → BLINK → OFF
- 📈 Giám khảo quan sát RTT Chart cập nhật realtime
- 🔌 Demo Kill Process → LWT OFFLINE hiện lên

> 🎤 _"Bây giờ chúng tôi sẽ demo trực tiếp hệ thống. Xin để ý biểu đồ RTT ở góc dưới cùng."_

---

### 🔹 SLIDE 32 — Đặc tính nổi bật

**Điểm khác biệt của đề tài**

1. 🧪 **Benchmark có data:** 2500 lệnh, biểu đồ Histogram/ECDF → Không phải demo suông
2. 🛡️ **Bảo mật:** Idempotency + Oversize Rejection + Auth
3. 📊 **Dashboard khoa học:** RTT Chart realtime, QoS Panel, LWT Log
4. 🧩 **Mô-đun hóa:** Mock ESP32 cho phép test không cần phần cứng

---

### 🔹 SLIDE 33 — Kết luận

**4 Thành tựu chính**

1. ✅ Xây dựng thành công kiến trúc **MQTT Broker + ESP32 + Dashboard**
2. ✅ RTT **43.3ms**, Std Dev **1.2ms**, Packet Loss **0%** trên 2000 gói
3. ✅ Idempotency với `cmd_id` chống lệnh trùng an toàn
4. ✅ LWT phát hiện offline trong **~15 giây**

---

### 🔹 SLIDE 34 — Hướng phát triển

**Kiến nghị mở rộng**

| Hướng               | Mô tả                                           |
| ------------------- | ----------------------------------------------- |
| 🏙️ **MQTT Cluster** | Broker Bridge cho hệ thống cấp quận/thành phố   |
| 🤖 **Camera AI**    | Đếm phương tiện → điều chỉnh chu kỳ đèn tự động |
| 🔐 **MQTTS + mTLS** | Mã hóa TLS cho từng cột đèn, chống hack         |
| 📡 **ESP32 thật**   | Đo RTT qua WiFi/4G thực tế (Giai đoạn 2)        |

---

### 🔹 SLIDE 35 — Cảm ơn

**CẢM ƠN HỘI ĐỒNG!**

> Đề tài: _Nghiên cứu ứng dụng IoT – MQTT trong giám sát và điều khiển từ xa hệ thống đèn tín hiệu giao thông_

📧 Email: <email>
📱 GitHub: https://github.com/Raindropdrops/NCKH-Traffic-Light

**XIN CHÂN THÀNH CẢM ƠN!**
