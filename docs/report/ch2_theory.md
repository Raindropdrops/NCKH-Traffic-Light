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
