# 🔧 HƯỚNG DẪN PHẦN CỨNG — Đèn Giao Thông IoT-MQTT

> Tài liệu này hướng dẫn chi tiết từ mua linh kiện → nối dây → nạp code → chạy thật.

---

## 1. TỔNG QUAN FIRMWARE ĐÃ CÓ

✅ **Code ESP32 đã viết hoàn chỉnh** tại `esp32_idf/main/`, gồm 5 module:

| File                 | Chức năng                                                      | Trạng thái |
| -------------------- | -------------------------------------------------------------- | :--------: |
| `app_main.c`         | Khởi tạo WiFi → MQTT → FSM → Publisher task                    |  ✅ Xong   |
| `wifi_manager.c/h`   | Kết nối WiFi (có retry 10 lần)                                 |  ✅ Xong   |
| `mqtt_handler.c/h`   | MQTT connect, publish state/telemetry, subscribe cmd, ACK, LWT |  ✅ Xong   |
| `fsm_controller.c/h` | Máy trạng thái 4 Mode × 6 Phase, Idempotency `cmd_id`          |  ✅ Xong   |
| `gpio_lights.c/h`    | Điều khiển 12 chân GPIO (4 hướng × 3 màu), toggle blink        |  ✅ Xong   |

**Bạn KHÔNG cần viết thêm code.** Chỉ cần mua linh kiện, nối dây, cấu hình WiFi/MQTT, rồi nạp.

---

## 2. DANH SÁCH LINH KIỆN CẦN MUA

### Linh kiện bắt buộc

|  #  | Linh kiện                                |   Số lượng    | Giá ước tính | Ghi chú                   |
| :-: | ---------------------------------------- | :-----------: | :----------: | ------------------------- |
|  1  | **ESP32 DevKit V1** (30-pin hoặc 38-pin) |       1       |   75.000đ    | Dùng chip ESP32-WROOM-32  |
|  2  | **LED 5mm** Đỏ                           |       4       |    2.000đ    | 4 hướng × 1 đèn đỏ        |
|  3  | **LED 5mm** Vàng                         |       4       |    2.000đ    | 4 hướng × 1 đèn vàng      |
|  4  | **LED 5mm** Xanh lá                      |       4       |    2.000đ    | 4 hướng × 1 đèn xanh      |
|  5  | **Điện trở 220Ω**                        |      12       |    3.000đ    | 1 điện trở / 1 LED        |
|  6  | **Breadboard** 830 lỗ                    |      1-2      |   25.000đ    | Cắm thử nghiệm, không hàn |
|  7  | **Dây cắm breadboard** (Jumper wires)    | 1 bộ (40 sợi) |   15.000đ    | Loại Male-Male            |
|  8  | **Cáp Micro-USB**                        |       1       |   10.000đ    | Nạp code + cấp nguồn      |

### Linh kiện nâng cao (tùy chọn)

|  #  | Linh kiện                                             | Khi nào cần                       |
| :-: | ----------------------------------------------------- | --------------------------------- |
|  9  | Module Traffic Light LED 3-in-1 (có sẵn Đỏ-Vàng-Xanh) | Thay 12 LED rời, gọn hơn          |
| 10  | Mô hình ngã tư in 3D / Bìa carton                     | Trình bày đẹp trước hội đồng      |
| 11  | Nguồn 5V/2A (Adapter USB)                             | Nếu cần chạy độc lập không laptop |

**💰 Tổng chi phí ước tính: ~130.000 – 200.000 VNĐ**

---

## 3. SƠ ĐỒ NỐI DÂY (Wiring Diagram)

### Bảng chân GPIO đã cấu hình trong firmware

Firmware dùng `Kconfig` nên các chân GPIO **có thể thay đổi** qua `idf.py menuconfig` mà không cần sửa code. Dưới đây là giá trị mặc định:

```
                    ESP32 DevKit V1
                   ┌───────────────┐
                   │               │
    NORTH RED  ←── │ GPIO 25       │
    NORTH YEL  ←── │ GPIO 26       │
    NORTH GRN  ←── │ GPIO 27       │
                   │               │
    SOUTH RED  ←── │ GPIO 16       │
    SOUTH YEL  ←── │ GPIO 17       │
    SOUTH GRN  ←── │ GPIO 22       │
                   │               │
    EAST  RED  ←── │ GPIO 32       │
    EAST  YEL  ←── │ GPIO 33       │
    EAST  GRN  ←── │ GPIO 21       │
                   │               │
    WEST  RED  ←── │ GPIO 19       │
    WEST  YEL  ←── │ GPIO 18       │
    WEST  GRN  ←── │ GPIO 23       │
                   │               │
           GND ─── │ GND           │
                   └───────────────┘
```

### Cách nối 1 LED (áp dụng lặp lại cho cả 12 LED)

```
ESP32 GPIO Pin ──→ Điện trở 220Ω ──→ Chân dài LED (Anode +) ──→ Chân ngắn LED (Cathode -) ──→ GND ESP32
```

### Bảng nối dây đầy đủ

|    Hướng     |   Màu   |  GPIO   | Điện trở |           LED           |
| :----------: | :-----: | :-----: | :------: | :---------------------: |
| **Bắc (N)**  |  🔴 Đỏ  | GPIO 25 |   220Ω   |         LED Đỏ          |
| **Bắc (N)**  | 🟡 Vàng | GPIO 26 |   220Ω   |        LED Vàng         |
| **Bắc (N)**  | 🟢 Xanh | GPIO 27 |   220Ω   |        LED Xanh         |
| **Nam (S)**  |  🔴 Đỏ  | GPIO 16 |   220Ω   |         LED Đỏ          |
| **Nam (S)**  | 🟡 Vàng | GPIO 17 |   220Ω   |        LED Vàng         |
| **Nam (S)**  | 🟢 Xanh | GPIO 22 |   220Ω   |        LED Xanh         |
| **Đông (E)** |  🔴 Đỏ  | GPIO 32 |   220Ω   |         LED Đỏ          |
| **Đông (E)** | 🟡 Vàng | GPIO 33 |   220Ω   |        LED Vàng         |
| **Đông (E)** | 🟢 Xanh | GPIO 21 |   220Ω   |        LED Xanh         |
| **Tây (W)**  |  🔴 Đỏ  | GPIO 19 |   220Ω   |         LED Đỏ          |
| **Tây (W)**  | 🟡 Vàng | GPIO 18 |   220Ω   |        LED Vàng         |
| **Tây (W)**  | 🟢 Xanh | GPIO 23 |   220Ω   |        LED Xanh         |
|      —       |    —    | **GND** |    —     | Tất cả chân Cathode (-) |

> ⚠️ **Lưu ý:** Tất cả LED dùng chung 1 chân GND của ESP32. Nếu dùng breadboard, kéo 1 đường GND dài rồi nối tất cả chân ngắn LED vào đó.

---

## 4. CÀI ĐẶT MÔI TRƯỜNG PHÁT TRIỂN

### Bước 1: Cài ESP-IDF v5.5

```powershell
# Trên Windows — tải installer chính thức
# Link: https://docs.espressif.com/projects/esp-idf/en/stable/esp32/get-started/windows-setup.html

# Hoặc dùng CLI:
mkdir C:\esp
cd C:\esp
git clone --recursive https://github.com/espressif/esp-idf.git -b v5.3
cd esp-idf
.\install.bat esp32
```

### Bước 2: Mở ESP-IDF PowerShell

```powershell
# Chạy file export (mở mỗi lần cần build)
C:\esp\esp-idf\export.ps1
```

### Bước 3: Di chuyển vào folder dự án ESP32

```powershell
cd "d:\Nam 2(D)\NCKH\traffic-mqtt-demo\esp32_idf"
```

---

## 5. CẤU HÌNH (Menuconfig)

### Bước 4: Mở giao diện cấu hình

```powershell
idf.py menuconfig
```

Trong menu **"Traffic Light Configuration"**, cấu hình:

#### WiFi Settings

| Tham số       | Giá trị cần nhập     |
| ------------- | -------------------- |
| WiFi SSID     | **Tên WiFi nhà bạn** |
| WiFi Password | **Mật khẩu WiFi**    |
| Maximum retry | 10 (giữ mặc định)    |

#### MQTT Settings

| Tham số          | Giá trị cần nhập                                     |
| ---------------- | ---------------------------------------------------- |
| MQTT Broker Host | **IP máy tính chạy Docker** (ví dụ: `192.168.1.100`) |
| MQTT Broker Port | 1883                                                 |
| MQTT Username    | `demo`                                               |
| MQTT Password    | `demo_pass`                                          |
| City ID          | `demo`                                               |
| Intersection ID  | `001`                                                |

#### GPIO Pin Configuration

- Giữ mặc định nếu nối dây theo bảng trên
- Nếu bạn đổi chân: sửa trong menu này, **KHÔNG cần sửa code**

#### Timing Configuration

| Tham số         | Giá trị | Ý nghĩa                             |
| --------------- | :-----: | ----------------------------------- |
| Green phase     | 8000ms  | 8 giây đèn xanh (rút ngắn cho demo) |
| Yellow phase    | 3000ms  | 3 giây đèn vàng                     |
| All-red phase   | 2000ms  | 2 giây tất cả đỏ                    |
| Offline timeout | 10000ms | 10s mất MQTT → tự về AUTO           |

> 💡 **Mẹo demo:** Để thời gian Green ngắn (5000ms) để đèn nhảy nhanh hơn trước hội đồng.

---

## 6. BUILD VÀ NẠP CODE

### Bước 5: Build firmware

```powershell
idf.py build
```

Lần đầu build sẽ mất 3-5 phút. Các lần sau nhanh hơn (~30 giây).

### Bước 6: Cắm ESP32 qua USB và tìm cổng COM

```powershell
# Kiểm tra cổng COM trong Device Manager
# Thường là COM3 hoặc COM4
# Nếu không thấy: cài driver CP2102 hoặc CH340
```

### Bước 7: Nạp (Flash) code vào ESP32

```powershell
idf.py -p COM3 flash
```

### Bước 8: Mở Serial Monitor xem log

```powershell
idf.py -p COM3 monitor
```

Bạn sẽ thấy log kiểu:

```
I (1234) MAIN: =================================
I (1235) MAIN: Traffic Light MQTT Controller
I (1236) MAIN: ESP-IDF version: v5.3
I (1237) MAIN: =================================
I (2000) WIFI: Connecting to WiFi...
I (3500) WIFI: Connected! IP: 192.168.1.50
I (4000) MQTT: Connecting to mqtt://192.168.1.100:1883
I (4500) MQTT: Connected to broker
I (4600) FSM: Starting in AUTO mode
I (5000) GPIO_LIGHTS: GPIO init complete: N(25,26,27) S(16,17,22) ...
```

> Nhấn `Ctrl+]` để thoát monitor.

---

## 7. KIỂM TRA HOẠT ĐỘNG

### Checklist sau khi nạp code

|  #  | Kiểm tra                                    | Kết quả mong đợi  |
| :-: | ------------------------------------------- | :---------------: |
|  1  | Serial Monitor hiện "Connected!"            |    ✅ WiFi OK     |
|  2  | Serial Monitor hiện "Connected to broker"   |    ✅ MQTT OK     |
|  3  | LED chạy vòng tự động (Xanh→Vàng→Đỏ)        |     ✅ FSM OK     |
|  4  | Mở Dashboard → thấy trạng thái thay đổi     | ✅ State Topic OK |
|  5  | Bấm MANUAL trên Dashboard → LED giữ cố định |     ✅ CMD OK     |
|  6  | Kill ESP32 → Dashboard hiện OFFLINE         |     ✅ LWT OK     |

### So sánh Mock vs ESP32 thật

| Tiêu chí    | Mock ESP32 (Python)  |          ESP32 thật           |
| ----------- | :------------------: | :---------------------------: |
| Kiến trúc   |     Chạy trên PC     |    Chạy trên vi điều khiển    |
| Kết nối     | Loopback (localhost) |           WiFi thật           |
| LED         |       Không có       |         12 LED vật lý         |
| RTT dự kiến |        ~43ms         | ~53-93ms (thêm WiFi overhead) |
| Dùng khi    |  Dev/Test/Benchmark  |      Demo trước hội đồng      |

---

## 8. LƯU Ý QUAN TRỌNG

### Tìm IP máy chạy Docker (Broker)

```powershell
ipconfig
# Tìm dòng "IPv4 Address" của WiFi adapter
# Ví dụ: 192.168.1.100
```

### ESP32 và Máy tính phải cùng mạng WiFi

- ESP32 kết nối WiFi nhà
- Máy tính chạy Docker Mosquitto cũng trên cùng mạng WiFi
- Nếu khác mạng → ESP32 không kết nối được Broker

### Nếu ESP32 không kết nối WiFi

1. Kiểm tra SSID và mật khẩu trong menuconfig
2. Đảm bảo WiFi là băng tần **2.4GHz** (ESP32 KHÔNG hỗ trợ 5GHz)
3. Thử restart ESP32 (bấm nút EN trên board)

### Nếu MQTT không kết nối

1. Kiểm tra IP Broker trong menuconfig
2. Đảm bảo Docker Mosquitto đang chạy: `docker ps`
3. Kiểm tra firewall Windows không chặn port 1883

---

## 9. CHẠY BENCHMARK VỚI ESP32 THẬT

Sau khi ESP32 hoạt động ổn, chạy benchmark thật:

```powershell
cd "d:\Nam 2(D)\NCKH\traffic-mqtt-demo"
python logger/tools/run_benchmark_report.py --host 192.168.1.100 --count 500
```

So sánh RTT mới với RTT Mock (43ms) để có dữ liệu thực tế bổ sung vào báo cáo.
