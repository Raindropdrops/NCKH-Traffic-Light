# Chương 1. Cơ sở lý thuyết về IoT và giao thức MQTT

Chi tiết trong chương này tập trung làm rõ các nền tảng công nghệ lõi tạo nên hệ thống, đặc biệt là kiến trúc truyền thông MQTT. Việc hiểu rõ cơ chế nội tại của MQTT là cơ sở để giải thích các quyết định thiết kế ở các chương sau.

## 1.1 Tổng quan về Internet of Things (IoT) trong Giao thông

Internet vạn vật (IoT) trong giao thông, hay ITS (Intelligent Transportation Systems), đề cập đến việc tích hợp các cảm biến, vi điều khiển tính toán và công nghệ truyền thông vào cơ sở hạ tầng giao thông.

Yêu cầu cốt lõi của một hệ thống IoT giao thông:

1. **Độ trễ thấp (Low Latency):** Tính năng an toàn (như thao tác khẩn cấp đổi đèn ALL-RED) yêu cầu lệnh phải được phản hồi tính bằng mili-giây.
2. **Khả năng chịu lỗi (Fault Tolerance):** Mạng không dây thường xuyên bị nhiễu. Hệ thống phải biết khi nào mất kết nối để có cơ chế tự động xử lý an toàn cục bộ.
3. **Tiết kiệm tài nguyên:** Các tủ điều khiển ngoài đường phố có năng lực xử lý (CPU) và kết nối mạng hạn chế (thường dùng mạng di động 3G/4G/4G-LTE).

## 1.2 Giao thức MQTT (Message Queuing Telemetry Transport)

MQTT là một giao thức truyền thông mạng mở, nhẹ (lightweight), tuân theo mô hình xuất bản/đăng ký (publish/subscribe). MQTT chuẩn hóa quy định bởi OASIS, đặc biệt thiết kế cho các thiết bị bị giới hạn tài nguyên và các mạng có băng thông thấp, độ trễ cao, hay không đáng tin cậy.

### 1.2.1 Mô hình Publish/Subscribe và Broker

Khác với giao thức HTTP hoạt động theo mô hình Client/Server (Request/Response) đồng bộ, MQTT sử dụng kiến trúc bất đồng bộ:

- **Broker (Máy chủ trung gian):** Đóng vai trò làm bưu điện, nhận mọi tin nhắn (message) và phân phối lại cho các đối tượng quan tâm.
- **Publisher (Người gửi):** Thiết bị gửi dữ liệu lên Broker với một nhãn dán cụ thể gọi là `Topic`.
- **Subscriber (Người nhận):** Cài đặt lắng nghe các `Topic`. Bất cứ khi nào có tin nhắn mới thuộc Topic đó, Broker sẽ lập tức đẩy (push) dữ liệu xuống.

Nhờ mô hình này, Dashboard điều khiển đèn và vi điều khiển ESP32 không cần biết địa chỉ IP của nhau, giúp hệ thống dễ dàng mở rộng, đồng thời giải quyết được yêu cầu băng thông hẹp của ITS.

### 1.2.2 Các mức độ đảm bảo phản hồi - Quality of Service (QoS)

MQTT cung cấp 3 mức độ ưu tiên xác nhận gói tin, cho phép lập trình viên đánh đổi giữa tốc độ và độ tin cậy:

- **QoS 0 (At most once / Fire-and-forget):** Gửi 1 lần duy nhất, không cần phản hồi. Phù hợp cho dữ liệu telemetry liên tục như nhiệt độ, tình trạng RAM, vì nếu mất 1 bản tin, bản tin ở giây tiếp theo sẽ bù đắp. Tốc độ cực nhanh.
- **QoS 1 (At least once):** Đảm bảo bản tin tới đích ít nhất 1 lần. Người nhận phải trả về gói tin xác nhận (ACK). Dùng cho mạng không ổn định, nơi tin nhắn có thể bị gửi lại. Bắt buộc dùng cho lệnh điều khiển đổi pha đèn giao thông, vì việc bỏ sót lệnh là không thể chấp nhận được.
- **QoS 2 (Exactly once):** Đảm bảo nhận đúng và chỉ 1 lần. Triển khai phức tạp qua tiến trình bắt tay 4 bước.

Trong đề tài này, nhóm thiết kế kết hợp linh hoạt cả QoS 0 và QoS 1 tùy theo nội dung bản tin (Được trình bày chi tiết tại Phần thiết kế kiến trúc Chương 2).

### 1.2.3 Cơ chế Last Will and Testament (LWT) và Retained Messages

- **LWT (Di chúc cuối cùng):** Khi thiết bị (Edge) kết nối tới Broker, nó "gửi gắm" một bản tin LWT. Nếu thiết bị bị sập nguồn đột ngột hoặc rớt mạng mà không kịp ngắt kết nối đúng cách, Broker sẽ thay mặt thiết bị công bố bản tin này cho Dashboard biết. Điều này giải quyết bài toán giám sát trạng thái (Online/Offline) của thiết bị viễn thông một cách chủ động.
- **Retained Messages:** Broker có khả năng lưu giữ lại (retain) bản tin cuối cùng của một Topic. Bất kỳ một Dashboard mới nào vừa mở lên cũng lập tức nhận được bản tin Retained, giúp đồng bộ hóa trạng thái hiện thời ngay lập tức mà không cần phải gọi lệnh lấy dữ liệu (polling).

## 1.3 Bảng so sánh MQTT so với các giao thức khác

Để làm sáng tỏ tính ưu việt của MQTT với bài toán, dưới đây là bảng so sánh tham chiếu.

| Tiêu chí                                  | MQTT                            | HTTP / REST                         | CoAP                         |
| :---------------------------------------- | :------------------------------ | :---------------------------------- | :--------------------------- |
| **Kiến trúc**                             | Publish / Subscribe             | Request / Response (Đồng bộ)        | Client / Server (Request)    |
| **Kích thước Header**                     | Rất nhỏ (2 Bytes)               | Lớn (Vài trăm Bytes)                | Nhỏ (4 Bytes)                |
| **Giao thức mạng**                        | TCP/IP (Có thể dùng WebSockets) | TCP (chiếm dụng tài nguyên)         | UDP (không tin cậy)          |
| **Tiêu tốn pin / băng thông**             | Cực kỳ thấp                     | Rất cao (Do overhead)               | Khá mThấp                    |
| **Hỗ trợ thời gian thực (Realtime push)** | Cực kì tốt (Push)               | Rất kém (Phải Polling/Long-polling) | Khá tốt                      |
| **Ứng dụng chính**                        | IoT, Smart City                 | Web Services, CRUD                  | Cảm biến năng lượng cực thấp |

Có thể thấy giao thức MQTT (chạy trên TCP nền tảng) cân bằng hoàn hảo giữa độ tin cậy mạng truyền thông với tính năng push tức thời, là lựa chọn lý tưởng nhất cho hệ thống điểu khiển đèn tín hiệu giao thông so với cơ chế lấy-cấp (Polling) của HTTP truyền thống.

## 1.4 Vi điều khiển ESP32

Node vi điều khiển ESP32 của hãng Espressif Systems được ứng dụng trong nghiên cứu này do vi xử lý lõi kép mạnh mẽ (lên tới 240MHz) cùng chip Wi-Fi/Bluetooth tích hợp sẵn. ESP32 đi kèm với framework chính thức là ESP-IDF (IoT Development Framework) sử dụng hệ điều hành thời gian thực FreeRTOS, giúp linh kiện có thể chạy đa luồng đồng thời: một luồng giữ tín hiệu điều khiển đèn theo chu kì cứng (Hardware Timer), một luồng riêng biệt xử lý các gói tin MQTT mạng lưới.
