# Chương 3: Thiết Kế Hệ Thống

## 3.1 Kiến trúc tổng quan

Hệ thống gồm 4 thành phần chính kết nối qua giao thức MQTT:

```
┌─────────────┐      MQTT       ┌──────────────┐      MQTT      ┌──────────────────┐
│   ESP32     │ ◄────────────► │  Mosquitto   │ ◄────────────► │   Dashboard      │
│  (Edge)     │    QoS 0/1     │  (Broker)    │    WebSocket   │   (Browser)      │
│  12 LED     │                │  port:1883   │    port:9001   │                  │
└─────────────┘                └──────────────┘                └──────────────────┘
                                       ▲
                                       │ MQTT Subscribe
                                ┌──────┴──────┐
                                │   Python    │
                                │   Logger    │
                                │  (*.jsonl)  │
                                └─────────────┘
```

| Thành phần        | Vai trò                                           | Công nghệ                   |
| ----------------- | ------------------------------------------------- | --------------------------- |
| **ESP32**         | Bộ điều khiển biên, xuất tín hiệu LED, FSM cục bộ | ESP-IDF 5.5 / C             |
| **Mosquitto**     | MQTT broker trung gian, quản lý message routing   | Docker, port 1883 + 9001    |
| **Dashboard**     | Giám sát trạng thái, gửi lệnh điều khiển từ xa    | HTML/CSS/JS, MQTT WebSocket |
| **Python Logger** | Ghi log telemetry, benchmark RTT                  | Python 3.11+, paho-mqtt     |

### Luồng dữ liệu chính

1. **Điều khiển**: Dashboard → `cmd` → Broker → ESP32 → thực thi → `ack` → Dashboard
2. **Giám sát**: ESP32 → `state` (1 msg/s) → Broker → Dashboard (cập nhật giao diện)
3. **Telemetry**: ESP32 → `telemetry` (1 msg/5s) → Broker → Dashboard (hiển thị RSSI, heap)
4. **Trạng thái**: ESP32 → `status` (retained, LWT) → Broker → Dashboard (online/offline)

## 3.2 MQTT Topic Tree

Hệ thống sử dụng cấu trúc topic phân cấp, hỗ trợ mở rộng multi-intersection:

```
city/{city_id}/intersection/{intersection_id}/
├── cmd          ← Dashboard gửi lệnh
├── ack          → ESP32 xác nhận lệnh
├── state        → Trạng thái đèn (mode, phase, uptime)
├── status       → Online/Offline (LWT, Retained)
└── telemetry    → Số liệu hệ thống (RSSI, heap, uptime)
```

### Chi tiết QoS và Retained

| Topic           | Hướng             | QoS | Retained | Tần suất     | Lý do                                         |
| --------------- | ----------------- | :-: | :------: | ------------ | --------------------------------------------- |
| `.../cmd`       | Dashboard → ESP32 |  1  |    ❌    | Theo nhu cầu | Mất lệnh = mất an toàn                        |
| `.../ack`       | ESP32 → Dashboard |  1  |    ❌    | Theo cmd     | Cần biết ESP32 đã nhận lệnh                   |
| `.../state`     | ESP32 → Dashboard |  0  |    ❌    | 1 msg/s      | Mất 1 msg không sao, msg tiếp theo đến sau 1s |
| `.../status`    | ESP32 → Broker    |  1  |    ✅    | Khi thay đổi | Dashboard mới mở cần biết trạng thái ngay     |
| `.../telemetry` | ESP32 → Dashboard |  0  |    ❌    | 1 msg/5s     | Dữ liệu bổ sung, không critical               |

## 3.3 Payload Schema (JSON)

### 3.3.1 Command (`cmd`)

```json
{
  "cmd_id": "a1b2c3d4-uuid-format",
  "type": "SET_MODE | SET_PHASE",
  "mode": "AUTO | MANUAL | BLINK | OFF",
  "phase": 0,
  "ts_ms": 1709712000000
}
```

### 3.3.2 Acknowledgment (`ack`)

```json
{
  "cmd_id": "a1b2c3d4-uuid-format",
  "ok": true,
  "err": null,
  "edge_recv_ts_ms": 1709712000050
}
```

**Idempotency**: ESP32 cache 32 `cmd_id` gần nhất. Nếu nhận cmd trùng `cmd_id`, bỏ qua (tránh thực thi lệnh 2 lần do QoS 1 gửi lại).

### 3.3.3 State (`state`)

```json
{
  "mode": "AUTO",
  "phase": 0,
  "since_ms": 5000,
  "uptime_s": 3600,
  "ts_ms": 1709712000000
}
```

### 3.3.4 Telemetry (`telemetry`)

```json
{
  "rssi_dbm": -55,
  "heap_free_kb": 215.0,
  "uptime_s": 3600,
  "ts_ms": 1709712000000
}
```

### 3.3.5 Status (`status`)

```json
{
  "online": true,
  "ts_ms": 1709712000000
}
```

## 3.4 Finite State Machine (FSM)

### 3.4.1 Các chế độ hoạt động (Mode)

| Mode       | Mô tả    | Hành vi                                                                                  |
| ---------- | -------- | ---------------------------------------------------------------------------------------- |
| **AUTO**   | Tự động  | Cycle 6 phase liên tục (NS_GREEN → NS_YELLOW → ALL_RED → EW_GREEN → EW_YELLOW → ALL_RED) |
| **MANUAL** | Thủ công | Giữ phase hiện tại, chờ lệnh SET_PHASE từ dashboard                                      |
| **BLINK**  | Nháy     | Tất cả đỏ nháy (ALL_RED ↔ tắt, chu kỳ 1s)                                                |
| **OFF**    | Tắt      | Tất cả đèn tắt                                                                           |

### 3.4.2 Chu kỳ phase (AUTO mode)

```
Phase 0: NS_GREEN   (10s) → N/S xanh, E/W đỏ
Phase 1: NS_YELLOW  ( 3s) → N/S vàng, E/W đỏ
Phase 2: ALL_RED    ( 2s) → Tất cả đỏ (guard)
Phase 3: EW_GREEN   (10s) → E/W xanh, N/S đỏ
Phase 4: EW_YELLOW  ( 3s) → E/W vàng, N/S đỏ
Phase 5: ALL_RED    ( 2s) → Tất cả đỏ (guard)
→ Quay lại Phase 0
```

Tổng chu kỳ: **30 giây** (10 + 3 + 2 + 10 + 3 + 2).

### 3.4.3 Quy tắc an toàn (Safety Rules)

1. **Không bao giờ 2 hướng cùng xanh**: N/S và E/W luôn đối nghịch.
2. **ALL_RED guard**: Giữa mỗi lần chuyển hướng luôn có 2 giây tất cả đỏ.
3. **Fallback**: Nếu MQTT mất kết nối > 10 giây, ESP32 tự chuyển về AUTO mode.

## 3.5 Sơ đồ phần cứng

### GPIO Pin Mapping

| GPIO | LED       |  Hướng   | Màu     |
| :--: | --------- | :------: | ------- |
|  13  | NS Red    | Bắc/Nam  | 🔴 Đỏ   |
|  12  | NS Yellow | Bắc/Nam  | 🟡 Vàng |
|  14  | NS Green  | Bắc/Nam  | 🟢 Xanh |
|  27  | EW Red    | Đông/Tây | 🔴 Đỏ   |
|  26  | EW Yellow | Đông/Tây | 🟡 Vàng |
|  25  | EW Green  | Đông/Tây | 🟢 Xanh |

> **Ghi chú**: Mỗi GPIO điều khiển 2 LED cùng lúc (N+S hoặc E+W) vì 2 hướng đối diện luôn cùng trạng thái.

### Sơ đồ kết nối

```
ESP32 DevKit V1
├── GPIO 13 ──► 220Ω ──► LED Đỏ (N) + LED Đỏ (S)
├── GPIO 12 ──► 220Ω ──► LED Vàng (N) + LED Vàng (S)
├── GPIO 14 ──► 220Ω ──► LED Xanh (N) + LED Xanh (S)
├── GPIO 27 ──► 220Ω ──► LED Đỏ (E) + LED Đỏ (E)
├── GPIO 26 ──► 220Ω ──► LED Vàng (E) + LED Vàng (W)
├── GPIO 25 ──► 220Ω ──► LED Xanh (E) + LED Xanh (W)
├── 3.3V ──► Cấp nguồn
└── GND ──► Ground chung
```
