# Danh mục những từ viết tắt

| Từ viết tắt | Ý nghĩa                                                             |
| :---------: | ------------------------------------------------------------------- |
|     ACK     | Acknowledgment — Bản tin xác nhận                                   |
|     ACL     | Access Control List — Danh sách kiểm soát truy cập                  |
|    CoAP     | Constrained Application Protocol                                    |
|     DoS     | Denial of Service — Tấn công từ chối dịch vụ                        |
|    ECDF     | Empirical Cumulative Distribution Function                          |
|    ESP32    | Vi điều khiển Espressif Systems 32-bit                              |
|     FSM     | Finite State Machine — Máy trạng thái hữu hạn                       |
|    GPIO     | General Purpose Input/Output                                        |
|     IoT     | Internet of Things — Internet vạn vật                               |
|     ITS     | Intelligent Transportation Systems — Hệ thống giao thông thông minh |
|    JSON     | JavaScript Object Notation                                          |
|     LWT     | Last Will and Testament — Di chúc cuối cùng (MQTT)                  |
|     M2M     | Machine-to-Machine — Liên lạc máy-máy                               |
|    MQTT     | Message Queuing Telemetry Transport                                 |
|    mTLS     | Mutual Transport Layer Security — Bảo mật tầng vận chuyển 2 chiều   |
|     QoS     | Quality of Service — Chất lượng dịch vụ                             |
|    RSSI     | Received Signal Strength Indicator — Cường độ tín hiệu thu          |
|     RTT     | Round-Trip Time — Thời gian khứ hồi                                 |
|     SVG     | Scalable Vector Graphics                                            |
|     TCP     | Transmission Control Protocol                                       |
|     TLS     | Transport Layer Security — Bảo mật tầng vận chuyển                  |
|     UDP     | User Datagram Protocol                                              |
|    UUID     | Universally Unique Identifier — Mã định danh duy nhất toàn cầu      |

---

# Các Phần Mở Đầu

## 5. Mở đầu

Sự bùng nổ của Internet of Things (IoT) đã mở ra những hướng đi mới trong việc quản lý và vận hành thông minh cơ sở hạ tầng đô thị [1]. Trong đó, hệ thống giao thông tín hiệu đóng vai trò xương sống trong việc duy trì trật tự và an toàn công cộng. Phương thức điều khiển đèn giao thông truyền thống hiện nay phần lớn dựa trên các bộ định thời (timer-based) được thiết lập sẵn, thiếu khả năng giám sát từ xa và khó khăn trong việc thay đổi chu kỳ linh hoạt [2]. Điều này đặt ra yêu cầu cấp thiết về một giải pháp quản lý tập trung, có độ trễ thấp và độ tin cậy cao. Đề tài "Nghiên cứu ứng dụng IoT - MQTT trong giám sát và điều khiển từ xa hệ thống đèn tín hiệu giao thông" được thực hiện nhằm mục đích giải quyết vấn đề này.

## 6. Tổng quan tình hình nghiên cứu thuộc lĩnh vực

### Tình hình trong nước

Tại Việt Nam, hệ thống điều khiển đèn tín hiệu giao thông tập trung SCATS (Sydney Coordinated Adaptive Traffic System) đã được thí điểm triển khai tại TP. Hồ Chí Minh từ năm 2014 trên một số tuyến đường chính [2]. Tại Hà Nội, hệ thống UTC (Urban Traffic Control) của Siemens đã được lắp đặt cho khoảng 100 nút giao thông từ năm 2017 [3]. Tuy nhiên, cả hai hệ thống trên đều sử dụng hạ tầng mạng cáp quang tốn kém và giao thức truyền thông đóng (proprietary). Việc giám sát thiết bị ở các điểm nút giao thông nhỏ lẻ vẫn còn hạn chế do chi phí triển khai cao.

### Tình hình thế giới

Trên thế giới, kiến trúc IoT với các giao thức nhẹ như MQTT hoặc CoAP đã trở thành tiêu chuẩn công nghiệp cho liên lạc máy-máy (M2M) [4]. Năm 2019, C. S. Nandy và cộng sự đã đề xuất mô hình "IoT Based Smart Traffic Control System" sử dụng vi điều khiển Arduino kết hợp cảm biến hồng ngoại đếm phương tiện, tuy nhiên nghiên cứu này không đo lường hiệu năng định lượng của giao thức truyền thông [5]. Nghiên cứu của A. Al-Fuqaha và cộng sự (2015) đã khảo sát toàn diện các giao thức IoT và kết luận MQTT là lựa chọn tối ưu cho các ứng dụng yêu cầu push notification thời gian thực [6].

### Khoảng trống nghiên cứu

Qua khảo sát, nhóm nhận thấy phần lớn các nghiên cứu tập trung vào kiến trúc hệ thống hoặc thuật toán AI đếm xe, mà chưa đi sâu vào việc **đo lường định lượng hiệu năng truyền thông MQTT** (độ trễ RTT, tỷ lệ mất gói tin, cơ chế phát hiện offline) trong bài toán điều khiển đèn giao thông.

## 7. Lý do lựa chọn đề tài

Giao thức MQTT (Message Queuing Telemetry Transport) được đánh giá là đặc biệt phù hợp cho mạng IoT băng thông thấp và không ổn định nhờ dung lượng header cực nhỏ (chỉ 2 bytes) và cơ chế QoS linh hoạt [1][4]. Dù vậy, ứng dụng thực tế và việc đo đạc hiệu năng định lượng của MQTT trong bài toán đặc thù như điều khiển đèn giao thông tại Việt Nam vẫn chưa được nghiên cứu toàn diện. Do đó, việc thực nghiệm đo lường độ trễ (RTT) và tính ổn định của MQTT là lý do chính để nhóm lựa chọn đề tài này, làm tiền đề cho hệ thống giao thông thông minh.

## 8. Mục tiêu, nội dung, phương pháp nghiên cứu

**Mục tiêu:**

- Xây dựng thành công mô hình hệ thống giám sát và điều khiển tín hiệu đèn giao thông từ xa thông qua giao thức MQTT.
- Đánh giá hiệu quả, đo lường độ trễ mạng (Round-Trip Time) và tỷ lệ mất gói tin (Packet Loss).
- Xây dựng giao diện Dashboard thời gian thực hiện đại, hiển thị giám sát và cung cấp cơ chế điều khiển khẩn cấp.

**Nội dung nghiên cứu:**

- Nghiên cứu kiến trúc IoT, giao thức MQTT, và các chuẩn thông điệp (Payload).
- Cấu hình MQTT Broker (Mosquitto) với tính năng bảo mật và WebSocket.
- Lập trình firmware cho vi điều khiển (ESP32) hoạt động như một thiết bị biên (Edge worker).
- Phát triển phần mềm Dashboard hiển thị trực quan.

**Phương pháp nghiên cứu:**

- **Nghiên cứu lý thuyết:** Tham khảo tiêu chuẩn MQTT v5.0 của quy chuẩn OASIS [1].
- **Nghiên cứu thực nghiệm:** Thiết kế kịch bản Benchmark gồm 500 lệnh điều khiển × 5 mức kích cỡ payload (0B, 256B, 512B, 900B, 1200B) với tần suất 1 lệnh mỗi 200ms. Thu thập dữ liệu về độ trễ, lưu trữ thành tệp CSV, viết mã Python vẽ biểu đồ phân phối (Histogram) và hàm phân phối tích lũy thực nghiệm (ECDF).

## 9. Đối tượng và phạm vi nghiên cứu

- **Đối tượng nghiên cứu:**
  - Giao thức truyền thông MQTT và các cơ chế QoS (0, 1).
  - Vi điều khiển ESP32 và công nghệ web thời gian thực (WebSocket).
- **Phạm vi nghiên cứu:**
  - Đề tài giới hạn mô phỏng và thực nghiệm ở quy mô một nút giao thông (intersection) dạng ngã tư tiêu chuẩn gồm 4 hướng đi.
  - **Giai đoạn 1:** Thử nghiệm độ trễ trong môi trường mạng nội bộ (loopback) với thiết bị mô phỏng Mock ESP32.
  - **Giai đoạn 2:** Thử nghiệm với thiết bị ESP32 vật lý qua mạng WiFi thực tế (dự kiến cập nhật).


---

# Chương 1. Cơ sở lý thuyết về IoT và giao thức MQTT

Chi tiết trong chương này tập trung làm rõ các nền tảng công nghệ lõi tạo nên hệ thống, đặc biệt là kiến trúc truyền thông MQTT [1]. Việc hiểu rõ cơ chế nội tại của MQTT là cơ sở để giải thích các quyết định thiết kế ở các chương sau.

## 1.1 Tổng quan về Internet of Things (IoT) trong Giao thông

Internet vạn vật (IoT) trong giao thông, hay ITS (Intelligent Transportation Systems), đề cập đến việc tích hợp các cảm biến, vi điều khiển tính toán và công nghệ truyền thông vào cơ sở hạ tầng giao thông [6].

Yêu cầu cốt lõi của một hệ thống IoT giao thông:

1. **Độ trễ thấp (Low Latency):** Tính năng an toàn (như thao tác khẩn cấp đổi đèn ALL-RED) yêu cầu lệnh phải được phản hồi tính bằng mili-giây [5].
2. **Khả năng chịu lỗi (Fault Tolerance):** Mạng không dây thường xuyên bị nhiễu. Hệ thống phải biết khi nào mất kết nối để có cơ chế tự động xử lý an toàn cục bộ.
3. **Tiết kiệm tài nguyên:** Các tủ điều khiển ngoài đường phố có năng lực xử lý (CPU) và kết nối mạng hạn chế (thường dùng mạng di động 3G/4G) [4].

## 1.2 Giao thức MQTT (Message Queuing Telemetry Transport)

MQTT là một giao thức truyền thông mạng mở, nhẹ (lightweight), tuân theo mô hình xuất bản/đăng ký (publish/subscribe), được chuẩn hóa bởi OASIS [1]. Giao thức được thiết kế đặc biệt cho các thiết bị bị giới hạn tài nguyên và các mạng có băng thông thấp, độ trễ cao.

### 1.2.1 Mô hình Publish/Subscribe và Broker

> _Hình 1.1: Mô hình kiến trúc Publish/Subscribe của MQTT (Minh họa — chèn hình vào báo cáo Word)_

Khác với giao thức HTTP hoạt động theo mô hình Client/Server (Request/Response) đồng bộ, MQTT sử dụng kiến trúc bất đồng bộ [1][4]:

- **Broker (Máy chủ trung gian):** Đóng vai trò làm bưu điện, nhận mọi tin nhắn (message) và phân phối lại cho các đối tượng quan tâm.
- **Publisher (Người gửi):** Thiết bị gửi dữ liệu lên Broker với một nhãn dán cụ thể gọi là `Topic`.
- **Subscriber (Người nhận):** Cài đặt lắng nghe các `Topic`. Bất cứ khi nào có tin nhắn mới thuộc Topic đó, Broker sẽ lập tức đẩy (push) dữ liệu xuống.

Nhờ mô hình này, Dashboard điều khiển đèn và vi điều khiển ESP32 không cần biết địa chỉ IP của nhau, giúp hệ thống dễ dàng mở rộng [4].

### 1.2.2 Các mức độ đảm bảo phản hồi - Quality of Service (QoS)

MQTT cung cấp 3 mức độ ưu tiên xác nhận gói tin, cho phép lập trình viên đánh đổi giữa tốc độ và độ tin cậy [1]:

- **QoS 0 (At most once / Fire-and-forget):** Gửi 1 lần duy nhất, không cần phản hồi. Phù hợp cho dữ liệu telemetry liên tục vì nếu mất 1 bản tin, bản tin ở giây tiếp theo sẽ bù đắp.
- **QoS 1 (At least once):** Đảm bảo bản tin tới đích ít nhất 1 lần. Người nhận phải trả về gói ACK. Bắt buộc dùng cho lệnh điều khiển đổi pha đèn giao thông.
- **QoS 2 (Exactly once):** Đảm bảo nhận đúng và chỉ 1 lần. Triển khai phức tạp qua tiến trình bắt tay 4 bước.

Trong đề tài này, nhóm thiết kế kết hợp linh hoạt cả QoS 0 và QoS 1 tùy theo nội dung bản tin (được trình bày chi tiết tại Chương 2).

### 1.2.3 Cơ chế Last Will and Testament (LWT) và Retained Messages

- **LWT (Di chúc cuối cùng):** Khi thiết bị kết nối tới Broker, nó "gửi gắm" một bản tin LWT. Nếu thiết bị bị sập nguồn đột ngột, Broker sẽ thay mặt thiết bị công bố bản tin này cho Dashboard biết [1][7]. Điều này giải quyết bài toán giám sát trạng thái (Online/Offline) một cách chủ động.
- **Retained Messages:** Broker lưu giữ lại (retain) bản tin cuối cùng của một Topic. Dashboard mới kết nối sẽ lập tức nhận được trạng thái hiện thời mà không cần polling [7].

## 1.3 Bảng so sánh MQTT so với các giao thức khác

Bảng 1.1 so sánh MQTT với các giao thức truyền thông IoT phổ biến khác [4][6].

_Bảng 1.1: So sánh giao thức MQTT, HTTP/REST và CoAP_

| Tiêu chí                 | MQTT                   | HTTP / REST                  | CoAP                         |
| :----------------------- | :--------------------- | :--------------------------- | :--------------------------- |
| **Kiến trúc**            | Publish / Subscribe    | Request / Response (Đồng bộ) | Client / Server              |
| **Kích thước Header**    | Rất nhỏ (2 Bytes)      | Lớn (Vài trăm Bytes)         | Nhỏ (4 Bytes)                |
| **Giao thức mạng**       | TCP/IP (Có WebSockets) | TCP                          | UDP                          |
| **Tiêu tốn băng thông**  | Cực kỳ thấp            | Rất cao (Do overhead)        | Thấp                         |
| **Hỗ trợ realtime push** | Rất tốt (Push)         | Kém (Phải Polling)           | Khá tốt                      |
| **Ứng dụng chính**       | IoT, Smart City        | Web Services, CRUD           | Cảm biến năng lượng cực thấp |

Có thể thấy giao thức MQTT cân bằng hoàn hảo giữa độ tin cậy mạng truyền thông với tính năng push tức thời, là lựa chọn lý tưởng nhất cho hệ thống điều khiển đèn tín hiệu giao thông.

## 1.4 Vi điều khiển ESP32

Node vi điều khiển ESP32 của hãng Espressif Systems được ứng dụng trong nghiên cứu này do vi xử lý lõi kép mạnh mẽ (lên tới 240MHz) cùng chip Wi-Fi/Bluetooth tích hợp sẵn [8]. ESP32 đi kèm với framework chính thức ESP-IDF sử dụng hệ điều hành thời gian thực FreeRTOS, giúp linh kiện chạy đa luồng đồng thời: một luồng giữ tín hiệu điều khiển đèn theo chu kì cứng (Hardware Timer), một luồng riêng biệt xử lý các gói tin MQTT.


---

# Chương 2. Thiết kế Kiến trúc Hệ thống Điều khiển

Hệ thống điều khiển đèn giao thông dựa trên chuẩn MQTT theo mô hình Client-Broker-Client được nhóm thiết kế nhằm khắc phục điểm yếu của điều khiển vòng từ truyền thống [2], cung cấp khả năng giám sát liên tục và phản hồi linh hoạt.

## 2.1 Sơ đồ khối tổng thể của hệ thống

> _Hình 2.1: Sơ đồ khối tổng thể hệ thống (Edge Device ↔ MQTT Broker ↔ Web Dashboard) — chèn hình vào Word_

Hệ thống được chia làm 3 thành phần chính (End-to-end Architecture):

1. **MQTT Broker (Core):** Là máy chủ trung tâm nhận dữ liệu, xử lý phân quyền. Cài đặt trên Docker sử dụng mã nguồn mở Eclipse Mosquitto [9].
2. **Edge Device (ESP32 Controller):** Lắp đặt trực tiếp tại các tủ điều khiển ngã tư. Đọc cảm biến cứng, điều khiển rơ-le đèn, gửi trạng thái về Broker, và lắng nghe lệnh ghi đè (Override Command).
3. **Web Dashboard (HTML/WebSocket):** Trung tâm giám sát. Hiển thị UI trực quan trên web trình duyệt cho người trực ban, vẽ biểu đồ trạng thái thời gian thực.

## 2.2 Thiết kế Topic Tree MQTT

Thay vì giao tiếp theo địa chỉ IP, giao thức MQTT dùng các Topic String [1]. Hệ thống sử dụng Prefix chung: `city/demo/intersection/001/` định danh duy nhất ngã tư thứ 001.

_Bảng 2.1: Thiết kế Topic Tree MQTT_

| Topic Path     | Chiều dữ liệu        | QoS | Chức năng                                                |
| -------------- | -------------------- | --- | -------------------------------------------------------- |
| `../state`     | Edge → Dashboard     | 0   | Phát trạng thái pha đèn, chu kỳ liên tục (Retained=True) |
| `../telemetry` | Edge → Dashboard     | 0   | Phát định kì thông số RSSI mạng, RAM, thời gian sống     |
| `../cmd`       | Dashboard → Edge     | 1   | Lệnh điều khiển khẩn cấp, yêu cầu báo nhận               |
| `../ack`       | Edge → Dashboard     | 1   | Phản hồi xác nhận lệnh `cmd_id` đã thực thi              |
| `../status`    | (Broker) → Dashboard | 1   | Bản tin LWT (Online / Offline) retain trên Server        |

## 2.3 Tiêu chuẩn hóa thông điệp (JSON Payload Schema)

Tất cả gói tin được đóng gói theo chuẩn JSON nhằm đảm bảo khả năng mở rộng đa ngôn ngữ (Python, C++, JavaScript).

Lệnh điều khiển mạng đôi khi có hiện tượng lặp (do cơ chế QoS 1 thử gửi lại). Để giải quyết triệt để, mã JSON chèn thêm trường duy nhất `cmd_id` (UUID). Nếu vi điều khiển nhận lại một mã lệnh đã thực thi, nó sẽ trả về ACK ngay lập tức nhưng không thay đổi ngắt cứng (Hardware Interrupt) — gọi là tính "Idempotent" [10].

## 2.4 Máy trạng thái điều khiển đèn (FSM)

> _Hình 2.2: Sơ đồ máy trạng thái hữu hạn (FSM) cho 4 chế độ và 6 pha đèn — chèn hình vào Word_

Cụm đèn (Bắc-Nam gọi là NS, Đông-Tây gọi là EW) vận hành theo máy trạng thái hữu hạn, bao gồm 4 chế độ (Mode):

- **AUTO:** Tự động đếm vòng chu kì 6 Pha đèn chuẩn mực.
- **MANUAL:** Dừng cấp đông (Freeze) ở một Pha đèn cụ thể và giữ vô thời hạn. Dùng trong tình huống xe ưu tiên hoặc sự cố.
- **BLINK:** Đèn Vàng chớp tắt liên tục 2 hướng nhằm cảnh báo nhường đường.
- **OFF:** Tắt toàn bộ rơ-le đèn khi thi công hoặc cắt điện diện rộng.

_Bảng 2.2: Chi tiết 6 Pha trong chế độ AUTO_

| Pha | Tên       | Đèn NS  | Đèn EW  | Thời gian mặc định |
| :-: | --------- | :-----: | :-----: | :----------------: |
|  0  | NS_GREEN  | 🟢 Xanh |  🔴 Đỏ  |        30s         |
|  1  | NS_YELLOW | 🟡 Vàng |  🔴 Đỏ  |         3s         |
|  2  | ALL_RED   |  🔴 Đỏ  |  🔴 Đỏ  |         4s         |
|  3  | EW_GREEN  |  🔴 Đỏ  | 🟢 Xanh |        30s         |
|  4  | EW_YELLOW |  🔴 Đỏ  | 🟡 Vàng |         3s         |
|  5  | ALL_RED   |  🔴 Đỏ  |  🔴 Đỏ  |         4s         |

Pha ALL_RED (Pha 2 và 5) kéo dài 4 giây được bổ sung nhằm đảm bảo toàn bộ phương tiện thoát khỏi tâm giao lộ trước khi hướng đối diện bật xanh.


---

# Chương 3. Nội dung Triển khai xây dựng

## 3.1 Xây dựng hệ thống Broker Mosquitto

Hệ thống sử dụng Docker Compose cài đặt Eclipse Mosquitto [9] trên Linux/Windows cho độ đồng nhất mã nguồn cao trên mọi hệ sinh thái thực thi.

Tập cấu hình chính `mosquitto.conf`:

- **Port 1883:** Lắng nghe giao tiếp giao thức gốc MQTT cho vi điều khiển.
- **Port 9001:** Lắng nghe WebSocket cho phép giao tiếp xuyên trình duyệt, phục vụ Dashboard giám sát.
- **Authentication:** Kích hoạt file mật khẩu `passwordfile` chặn truy cập trái phép [9].

## 3.2 Lập trình Firmware vi điều khiển ESP32

Firmware xây dựng trên nền tảng C/C++ của nhà sản xuất (ESP-IDF v5.5) [8] thay vì Framework Arduino nhằm tận dụng trọn vẹn sức mạnh đa luồng FreeRTOS.

Thành phần chia làm 4 luồng xử lý đồng thời (FreeRTOS Tasks):

1. **MQTT Task Network:** Khởi tạo mạng WiFi, xử lý vòng lặp Reconnect. Duy trì tín hiệu Keep Alive. Khai báo bản tin "Offline" cho LWT ngay trước khi kết nối [1][7].
2. **Command Handler:** Parsing JSON điều khiển bằng thư viện cJSON. Lọc `cmd_id` trùng lặp và kích hoạt rơ-le thay đổi Phase. Nếu JSON kích thước lớn hơn 1024 Bytes, hệ thống tự động loại bỏ để phòng thủ tấn công DoS tràn bộ nhớ đệm [10].
3. **GPIO LED Control:** Cấp dòng tải 3.3V điều khiển Relay kích các chân GPIO cho 6 đèn.
4. **Telemetry Publisher:** Mỗi 5 giây đọc Free Heap Memory, thời gian sống Uptime, độ nhiễu mạng RSSI và gửi lên QoS 0 về Dashboard.

## 3.3 Phát triển giao diện Dashboard điều khiển

> _Hình 3.1: Ảnh chụp màn hình Dashboard giám sát đèn giao thông (Dark Theme) — chèn ảnh vào Word_

Hệ thống sử dụng nền tảng HTML5/CSS3/JavaScript thuần, kết nối theo phương thức WebSocket. Màn hình Dark Theme được chia thành các khu vực chức năng:

- **Control Panel:** 4 nút chế độ (AUTO, MANUAL, BLINK, OFF) và bộ chọn Phase kèm nút SET PHASE.
- **Intersection SVG:** Mô phỏng đồ họa ngã tư thời gian thực với hiệu ứng glow trên đèn đang sáng.
- **Live Status:** Hiển thị Mode, Phase, Uptime hiện tại.
- **Telemetry Panel:** Hiển thị RSSI, Heap Free, Device Uptime.
- **ACK Log:** Lịch sử các lệnh đã gửi và xác nhận.

Ba tính năng khoa học then chốt được bổ sung nhằm phục vụ mục tiêu đánh giá hiệu năng MQTT:

- **Biểu đồ RTT Realtime (Canvas Chart):** Tính toán và biểu diễn RTT ngay trên Dashboard mỗi khi gửi lệnh và nhận ACK. Hiển thị Mean, Last, Min, Max và số lượng mẫu.
- **QoS Indicator Panel:** Hiện rõ mức QoS đang dùng cho từng topic MQTT, giúp giải thích thiết kế.
- **Connection Log (LWT):** Ghi lại lịch sử sự kiện Online/Offline với timestamp.

## 3.4 Xây dựng công cụ kiểm thử Mock ESP32 và Benchmark

> _Hình 3.2: Kiến trúc quy trình kiểm thử tự động (Mock ESP32 → Broker → Benchmark Script) — vẽ sơ đồ_

Do phần cứng ESP32 có rủi ro can nhiễu kết nối WiFi khi thử nghiệm số lượng gói lớn [8], nhóm đã lập trình thiết bị mô phỏng "Mock ESP32" bằng Python. Công cụ này giả lập 100% logic xử lý thiết bị thật bao gồm: vòng tuần hoàn đèn, trả về ACK, publish trạng thái, và telemetry giả lập thực tế (RSSI drift -1dBm/5 phút, Heap giảm dần). Mock ESP32 cho phép thiết lập tăng tốc quá trình đèn (`--speed 2x`) dùng cho demo.

Công cụ Benchmark `run_benchmark_report.py` gửi tự động lệnh điều khiển theo tần suất cố định và thu thập RTT, tự động tạo biểu đồ Histogram, ECDF và báo cáo Markdown.


---

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


---

# 11. Kết luận và kiến nghị

## a) Phần Kết luận

Đề tài "Nghiên cứu ứng dụng IoT - MQTT trong giám sát và điều khiển từ xa hệ thống đèn tín hiệu giao thông" đã hoàn thành các mục tiêu đề ra ban đầu:

1. Xây dựng thành công kiến trúc phần mềm tích hợp MQTT Broker (Mosquitto) [9] với thiết bị điều khiển vi mạch thông minh biên (ESP32) [8] và giao diện giám sát Dashboard thời gian thực.
2. Xây dựng bộ công cụ kiểm thử tự động (Mock ESP32 + Benchmark), cung cấp bằng chứng định lượng về hiệu năng: RTT trung bình **43.3 ms** (Std Dev chỉ **1.2 ms**), Packet Loss **0%** trên 2000 gói tin hợp lệ.
3. Giải quyết bài toán chống lệnh điều khiển trùng lặp thông qua trường `cmd_id` (Idempotency) [10] và bảo vệ bộ nhớ đệm khỏi payload vượt ngưỡng 1KB.
4. Khai thác thành công cơ chế LWT [1][7] phát hiện thiết bị offline trong ~15 giây, phục vụ giám sát trạng thái mạng lưới đèn.

## b) Phần Kiến nghị

- **Nghiên cứu tiếp theo:** Triển khai hệ thống cho quy mô quận cần ứng dụng "MQTT Broker Bridge" và "Cluster" nhằm chia tải, tránh Single Point of Failure [4].
- **Phát triển thuật toán thích nghi:** Tích hợp Camera AI đếm lưu lượng phương tiện để điều chỉnh chu kỳ đèn theo thời gian thực [5].
- **Về Bảo mật:** Chuyển sang MQTTS (MQTT over SSL/TLS) với mTLS cấp chứng chỉ cho từng cột đèn, chống hacker chiếm quyền điều khiển [4].

# 12. Tài liệu tham khảo

[1] OASIS, _MQTT Version 5.0 Standard_, 2019. [Online]. Available: https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html

[2] Sở GTVT TP. Hồ Chí Minh, _Báo cáo triển khai hệ thống SCATS_, 2017.

[3] Sở GTVT Hà Nội, _Dự án Hệ thống UTC (Urban Traffic Control) Siemens_, 2017.

[4] A. Al-Fuqaha, M. Guizani, M. Mohammadi, M. Aledhari, and M. Ayyash, "Internet of Things: A Survey on Enabling Technologies, Protocols, and Applications," _IEEE Communications Surveys & Tutorials_, vol. 17, no. 4, pp. 2347–2376, 2015.

[5] C. S. Nandy, B. K. Patra, and A. B. Saha, "IoT Based Smart Traffic Control System," _2019 International Conference on Vision Towards Emerging Trends in Communication and Networking (ViTECoN)_, Vellore, India, 2019, pp. 1–5.

[6] M. B. Yassein, M. Q. Shatnawi, and D. Al-Zoubi, "Application Layer Protocols for the Internet of Things: A Survey," _2016 International Conference on Engineering & MIS (ICEMIS)_, Agadir, Morocco, 2016, pp. 1–4.

[7] HiveMQ, _MQTT Essentials – Last Will and Testament_, 2023. [Online]. Available: https://www.hivemq.com/mqtt-essentials/

[8] Espressif Systems, _ESP-IDF Programming Guide v5.5_, 2024. [Online]. Available: https://docs.espressif.com/projects/esp-idf/

[9] Eclipse Foundation, _Eclipse Mosquitto – An Open Source MQTT Broker_, 2024. [Online]. Available: https://mosquitto.org/documentation/

[10] M. Fowler, "Idempotency Key," _martinfowler.com_, 2020. [Online]. Available: https://martinfowler.com/articles/patterns-of-distributed-systems/idempotent-receiver.html

[11] R. K. Kodali and S. R. Mahesh, "A Low Cost Implementation of MQTT using ESP8266," _2016 2nd International Conference on Contemporary Computing and Informatics (IC3I)_, Noida, India, 2016, pp. 404–408.

[12] D. Mishra and S. P. Muddinagiri, "IoT Based Smart Traffic Signal Control System with Performance Evaluation using MQTT," _International Journal of Engineering Research & Technology_, vol. 9, no. 1, pp. 205–210, 2020.

# 13. Phụ lục

- Phụ lục A: Sơ đồ nối dây phần cứng ESP32 (Nếu có thiết bị thật).
- Phụ lục B: Mã nguồn đại diện (Mock ESP32, Benchmark Script).
- Phụ lục C: Ảnh chụp Dashboard và biểu đồ RTT Benchmark.
