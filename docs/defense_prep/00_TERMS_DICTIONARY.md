# 📖 TỪ ĐIỂN THUẬT NGỮ "BÌNH DÂN HỌC VỤ" (DÀNH CHO NGƯỜI MỚI BẮT ĐẦU)

> **Mục tiêu:** Giúp bạn hiểu bản chất gốc rễ của các từ khóa Tiếng Anh xuất hiện trong dự án bằng những ví dụ "đời thường" nhất (như gửi bưu điện, shipper, nhà hàng), từ đó bạn có thể tự tin chém gió mà không sợ bị hỏi vặn lại.

---

## 🛑 1. NHÓM TỪ VỰNG VỀ MẠNG & GIAO TIẾP (MQTT)

### **MQTT (Message Queuing Telemetry Transport)**
- **Dịch thô:** Giao thức truyền tải tin nhắn đo lường từ xa.
- **Hiểu đơn giản:** Nó giống như **Zalo** hoặc **Messenger** dành cho máy móc. Thay vì máy móc (Đèn giao thông) gọi điện thoại cho máy tính (Tốn tiền, lúc gọi được lúc không), thì chúng gửi tin nhắn nhỏ gọn qua mạng. Bản chất MQTT sinh ra để chạy trên các thiết bị yếu, mạng chập chờn (như sóng 3G ở ngã tư).

### **Broker (Máy chủ trung gian)**
- **Dịch thô:** Người môi giới.
- **Hiểu đơn giản:** Chỗ này chính là **Bưu điện** (Phần mềm Mosquitto đang chạy trên máy tính bạn). Đèn giao thông không gửi tin nhắn trực tiếp thẳng vào màn hình Dashboard. Nó gửi tin ra "Bưu điện". Sau đó "Bưu điện" mới phân phát tin nhắn đó đến các máy tính/điện thoại đang mở mạng lưới.

### **Publish & Subscribe (Pub/Sub)**
- **Dịch thô:** Phát hành & Đăng ký theo dõi.
- **Hiểu đơn giản:** Giống hệt **Youtube**.
  - **Publish (Đăng video/Gửi tin):** Cây đèn giao thông quay được cảnh đèn chuyển sang Đỏ liền *Publish* (Đăng tải) màu Đỏ đó lên tường.
  - **Subscribe (Đăng ký/Hóng tin):** Trang web Dashboard bấm *Subscribe* (Theo dõi) cái cây đèn đó. Hễ cây đèn Đăng bài (Publish), ngay lập tức Bưu điện (Broker) sẽ báo Notification đẩy cái màu Đỏ về cho màn hình Dashboard nảy lên.

### **Topic (Chủ đề)**
- **Dịch thô:** Chủ đề.
- **Hiểu đơn giản:** Nó là cái **Địa chỉ nhà**. Khi gửi bưu kiện, bạn phải ghi gửi đi đâu đúng không? Cây đèn khi gửi trạng thái màu Đỏ, nó không ném bừa lên mạng, nó bảo: "Hãy gửi tới địa chỉ `city/hanoi/intersection/001/state`". Web nào muốn nhận đúng cái màu Đỏ của chốt này, thì phải Hóng (Subscribe) đúng cái địa chỉ `city/hanoi/intersection/001/state`.

### **QoS - Quality of Service (Đảm bảo chuyển phát)**
- **Hiểu đơn giản:** Khi bạn thuê Shipper gửi đồ, bạn chọn gói cước nào?
  - **QoS 0 (Gửi thư thường):** Giao xong quăng ở cửa rồi đi luôn. Mất ráng chịu. Dùng cho việc báo cáo "Màu đèn", vì mất giây này thì giây sau có tin khác tới.
  - **QoS 1 (Gửi thư bảo đảm):** Shipper giao xong phải đứng đợi người nhận ký tên (gọi là gói ACK). Nếu chưa thấy ký tên, shipper gọi điện giao đi giao lại tới khi đưa được tận tay. Dùng cho các "Lệnh đổi màu khẩn cấp" từ Web xuống Đèn.

### **LWT - Last Will and Testament (Di chúc thư)**
- **Hiểu đơn giản:** Một tờ **Giấy uỷ quyền/Di chúc**. Trước khi đi làm nhiệm vụ, cây đèn giao thông để lại Bưu điện (Broker) một lá thư: "Nếu tui mà mất tích (Đứt mạng) quá 30 giây, nhờ Bưu điện bóc thư này ra và thông báo cho cả làng là tui ĐÃ CHẾT (Offline)". Nhờ vậy Dashboard biết để báo trạng thái mất kết nối màu Đỏ.

---

## 🧠 2. NHÓM TỪ VỰNG VỀ CODE & THIẾT BỊ (ESP32)

### **Firmware (Phần mềm vi điều khiển)**
- **Hiểu đơn giản:** Là linh hồn phần mềm bạn viết (bằng C++) nạp chết vào trong con chip ESP32 để điều khiển cái đèn. Nó tựa tựa như hệ điều hành Windows của máy tính, nhưng chỉ chuyên trị một việc rẽ nhánh đèn LED.

### **FSM - Finite State Machine (Cỗ máy trạng thái)**
- **Hiểu đơn giản:** Đây là cái **Bản đồ luồng hoạt động**. Đèn giao thông không thể nhảy từ Xanh phát sang Đỏ luôn được. Nó bắt buộc phải đi theo "Trạng thái": Xanh -> Vàng -> Tất cả cùng Đỏ (Vùng an toàn) -> Xanh hướng kia. FSM chính là khối code chặn đứng mọi lệnh vớ vẩn (ví dụ cấm không cho Xanh 4 hướng cùng lúc).

### **WDT - Task Watchdog Timer (Chó canh cổng)**
- **Hiểu đơn giản:** Con chip điện tử đôi khi máy tính nó bị **"Treo/Đơ"** (Giống bị đứng máy win). Bạn lập trình một "Cái chuông báo thức" (Chó canh) đếm ngược 30 giây. Luồng code (FSM) chạy 1 vòng xong phải đập tay vô cái chuông báo "Tao còn sống" (gọi là Feed the dog / Cho chó ăn). Nếu 30 giây mà code đơ, không đập tay chuông, Chó bảo: "Thằng này chết rồi", lập tức nó đá đít (Hard Reset) khởi động lại cái cây đèn giao thông. Mạch tự cứu sống chính nó.

### **FreeRTOS (Hệ điều hành thời gian thực)**
- **Hiểu đơn giản:** Bình thường code chạy từ trên xuống dưới (Single-thread). FreeRTOS cho phép ESP32 có **"Thuật phân thân"** (Multi-threading). Cùng một mili-giây, cái Tay Trái thì tập trung chớp tắt đèn giao thông, Tay Phải thì đứng cãi nhau với wifi/MQTT. Mạng có bị đứng (wifi xoay vòng vòng), Tay Trái chuyển đèn vẫn diễn ra bình thường. Arduino thường không làm được trò này mượt mà.

### **Idempotency Cache (Bộ nhớ đệm chống lệnh ma)**
- **Hiểu đơn giản:** Bạn là phục vụ quán cafe. Bàn số 1 gọi "Cho 1 ly đen đá". Bạn chốt bill (Lưu vào 1 tờ giấy note Cache ghi: Mã Bill: 1234). 1 giây sau WiFi lắc lag nảy sinh lỗi, bàn số 1 vô tình gửi lại câu "Cho 1 ly đen đá" (vẫn mã 1234). Bác check tờ giấy thấy mã 1234 hồi nãy pha rồi. Bác từ chối không pha ly thứ 2 nhưng vẫn vui vẻ bảo "Dạ có ngay". Chống thiết bị chớp nháy loạn xạ do bị gửi trùng lệnh.

---

## 📈 3. NHÓM TỪ VỰNG VỀ ĐO LƯỜNG (BENCHMARK)

### **RTT - Round Trip Time (Tổng thời gian đi & về)**
- **Hiểu đơn giản:** Bạn gửi tin nhắn "Anh yêu em" cho crush. Bạn lấy điện thoại canh giờ. Từ lúc bấm nút Send, chông chênh đến bao lâu thì chữ "Em cũng yêu anh" (ACK) quay về màn hình của bạn? Thời gian một vòng khép kín đó gọi là RTT. RTT càng nhỏ mạng càng xịn.

### **Latency (Độ trễ đi đường)**
- **One-way Latency (Trễ một chiều):** Việc đi và về tốn 100ms. Thầy giáo sẽ hỏi: Do lúc mầy gửi đi bị tắc đường? Hay do con ESP chạy tính toán quá lâu mất 80ms, lúc về tốn có 20ms?
Bóc tách **One-way Latency** ra giúp bạn trả lời: Dạ thưa thầy, gửi lệnh đi (Upload/Edge Latency) mất 25ms, Về (Download/Ret_Latency) mất 50ms, Chạy code tính toán (như FSM) mất 25ms. Đây là con số rất đẳng cấp trong nghiên cứu.

---

## 🐳 4. NHÓM DEVOPS (VẬN HÀNH)

### **Docker & Docker Compose**
- **Hiểu đơn giản:** Bạn muốn nuôi cá cảnh (Máy chủ Broker MQTT). Bạn phải mua hồ, mua bơm nước, sỏi đá, cân bằng pH... Rất phiền.
Docker đóng gói cái "hồ cá" đó thành 1 cái container (Hộp) chuẩn chỉnh. Bê cái thùng này đi đâu (Laptop Window của bạn hư, qua máy Macbook khác), chỉ cần gõ 1 câu thần chú (`docker compose up -d`) là bụp! Nước, sỏi, con cá (Mosquitto) bung ra sống khỏe mạch liền, hoạt động y hệt 100% không cần setup lại từ đầu. Chống được chứng bệnh "Máy tớ chạy được mà quăng qua máy cậu báo lỗi từa lưa".
