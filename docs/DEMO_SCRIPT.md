# 🎬 DEMO SCRIPT — Traffic Light MQTT (2–3 phút)

> Kịch bản trình bày demo NCKH — Không cần ESP32 thật

---

## Mở đầu (30s)

**Lời thoại:**

> "Xin chào thầy/cô và các bạn. Đề tài của nhóm em là **Hệ thống giám sát và điều khiển đèn giao thông qua giao thức MQTT**."
>
> "Vấn đề: hệ thống đèn giao thông truyền thống thường cố định, khó giám sát từ xa, thiếu phản hồi khi lỗi. Giải pháp của chúng em dùng **MQTT — giao thức IoT lightweight** — để điều khiển real-time, có xác nhận lệnh, và phát hiện offline tự động."

---

## Kiến trúc (30s)

**Lời thoại:**

> "Kiến trúc hệ thống gồm 3 thành phần chính:"
>
> "**1. Mosquitto MQTT Broker** — trung tâm chuyển tiếp message, chạy trong Docker."
> "**2. Node-RED Dashboard** — giao diện điều khiển trực quan, cũng chạy trong Docker."
> "**3. ESP32** — vi điều khiển tại ngã tư, điều khiển đèn LED. Hôm nay em dùng **mock simulator** thay thế."

```
  Dashboard (Node-RED)  ←→  MQTT Broker (Mosquitto)  ←→  ESP32/Mock
       :1880                      :1883                   (simulator)
```

> "Tất cả giao tiếp qua 5 MQTT topics: **cmd, ack, state, status, telemetry**."

---

## Demo thao tác (60–90s)

### Bước 1: Khởi động hệ thống

**Lời thoại:**

> "Em khởi động hệ thống bằng 1 lệnh Docker Compose..."

```powershell
docker compose up -d
```

> "...và chạy mock ESP32 để giả lập thiết bị tại ngã tư."

```powershell
python logger/tools/mock_esp32.py --host 127.0.0.1
```

### Bước 2: Mở Dashboard

**Lời thoại:**

> "Mở Dashboard tại localhost:1880/ui. Mời thầy/cô quan sát ngã tư ảo ở góc phải."

→ Mở browser: `http://localhost:1880/ui`

### Bước 3: Demo SET_MODE

**Lời thoại:**

> "Hiện tại đang ở chế độ AUTO — đèn tự chuyển phase. Em chuyển sang **MANUAL** để điều khiển thủ công..."
>
> "Lệnh SET_MODE gửi qua topic `/cmd` với QoS 1 — đảm bảo broker nhận được. ESP32 trả lại **ACK** xác nhận."

→ Dashboard: chọn MANUAL → Send

### Bước 4: Demo SET_PHASE

**Lời thoại:**

> "Giờ em set phase 3 — hướng Đông-Tây xanh, Nam-Bắc đỏ. Quan sát ngã tư trên dashboard..."

→ Dashboard: chọn Phase 3 → Send

> "Ngay lập tức, 4 hướng cập nhật. ACK log bên dưới hiện cmd_id và kết quả OK."

### Bước 5: Demo Status (LWT)

**Lời thoại:**

> "Nếu ESP32 mất kết nối — ví dụ mất WiFi — broker tự động gửi **Last Will Testament** báo OFFLINE. Khi kết nối lại, ESP32 publish ONLINE. Đây là cơ chế phát hiện lỗi quan trọng."

---

## Chốt / Kết luận (30s)

**Lời thoại:**

> "Tóm lại, hệ thống đảm bảo 3 yếu tố quan trọng:"
>
> "**1. Tin cậy**: QoS 1 đảm bảo lệnh được nhận, ACK xác nhận xử lý."
> "**2. An toàn**: Safety rule không bao giờ cho 2 hướng cùng xanh."
> "**3. Giám sát**: Phát hiện offline qua LWT, đo RTT dưới 100ms."
>
> "Cảm ơn thầy/cô, nhóm em sẵn sàng trả lời câu hỏi."

---

## Câu hỏi thường gặp (chuẩn bị sẵn)

| Câu hỏi                | Trả lời ngắn                                                    |
| ---------------------- | --------------------------------------------------------------- |
| Tại sao chọn MQTT?     | Lightweight, QoS levels, LWT, pub/sub phù hợp IoT               |
| QoS 0 vs 1 khác gì?    | QoS 0 = fire-and-forget, QoS 1 = at-least-once delivery         |
| LWT hoạt động thế nào? | Broker giữ "di chúc", khi client mất kết nối → tự publish       |
| RTT bao nhiêu?         | ~50-100ms qua WiFi, ~10-30ms qua LAN                            |
| Nếu duplicate cmd?     | Idempotency cache 32 cmd_id, trùng → ack ok, không thực thi lại |
