# 🛡️ CHƯƠNG 5: CẨM NANG PHẢN BIỆN (Q&A CHEATSHEET HỘI ĐỒNG)

Bạn hãy đọc thuộc 6 câu tủ (hay bị hỏi xoáy) này. Nắm ý chính để cãi cứng tay. Hội đồng có thể hỏi "xoáy vặn" rất nhiều nhưng bản chất chỉ chung về 5 nhóm mục tiêu: Ổn định, Bảo mật, Độ nét hệ thống, Giới hạn mở rộng.

---

### Giám khảo 1 (Chuyên mạng): Dùng WiFi cho đèn giao thông à? Đứt mạng thì sao, xe tông nhau liên hoàn ngoài kia em đền à?
🔥 **Cách phản biện:** Bạn cười nhẹ.
- "Kính thưa thầy đội nhóm hoàn toàn lường trước việc mất mạng. Đèn giao thông của chúng em áp dụng nguyên lý **Edge-Computing Autonomous (Hoạt động tự chủ ở Rìa)**."
- "Mạng MQTT và Broker chỉ để Đổi Chế Độ khi khẩn cấp và Giám Sát. Máy tính lõi ESP32 (FSM State Machine) mang code tự chạy ở bên trong." 
- "Nếu đứt mạng Internet ngang chừng, WDT và Fallback sẽ kích hoạt. Ngã tư tự động thu hồi quyền điều khiển và tự bật lại chu kỳ chớp tắt auto cục bộ (Local Phase) 100% an toàn."

### Giám khảo 2 (Chuyên phần mềm): Em nói em code FSM (Cỗ máy trạng thái) cho ESP32. Nếu trên mạng bọn hacker gửi 1 lệnh bắt Ngã 4 đồng loạt xanh 4 phía thì sao? Hệ thống em nát không?
🔥 **Cách phản biện:** 
- "Dạ thưa thầy, Logic FSM của nhà em viết bằng code C có cấu trúc `switch-case` bị **Ràng buộc phần cứng cứng nhắc (Hard Constraints)**."
- "Dashboard dù có gửi payload `Phase: 99` hay Fake Lệnh 4 hướng xanh, khi trỏ lọt vào hàm `fsm_set_phase()`, phần cứng ESP32 sẽ block toàn bộ và đá bay payload do không có Phase nào vi phạm luật bảo toàn giao thông (Chỉ có pha NS đỏ-EW xanh, hoặc Vàng)." 
- Bổ sung: QoS 1 có Idempotency Cache lọc mất lệnh giả.

### Giám khảo 3 (Chứa nhiều lý luận): Cái "One-way Latency" của em phân tích trong báo cáo làm sao đo được bằng Python trên máy tính PC với con chip ở tít ngoài kia? Đồng hồ (Clock time) hai con lệch nhau thì em trừ đi bị số Âm à?
🔥 **Cách phản biện:** (Câu hỏi phân loại thủ khoa).
- "Thầy nhận xét rất Tinh tế ạ! Việc đồng hồ System Clock của máy PC và của con ESP32 bị lệch nhau là hiển nhiên. Cho nên thời điểm T_PC (1620002131) trừ cho T_ESP32 (3123) sẽ sai số kinh khủng."
- "Nhưng ở đây, chúng em không trừ Thời điểm thực tế. Chúng em cài đặt cho ESP32 chạy chế độ Đồng Bộ Hệ Thống (SNTP / NTP) bù đắp lại Epoch Time (Thời gian chuẩn toàn cầu) cho Clock của mình."
- "Vì vậy Timestamp nhúng vào Packet Payload Json đều là Mili-second Epoch. Nó triệt tiêu toàn bộ độ lệch địa phương của hai đồng hồ ạ."

### Giám khảo 4: Em cấu hình Broker Mosquitto là public vậy sao? Không ai bắt quyền truy cập thì hacker vào phá mất đèn chứ?
🔥 **Cách phản biện:** 
- "Dạ báo cáo thầy, Broker mặc định khi chạy Docker thì đóng toàn bộ kết nối nặc danh `allow_anonymous false`." 
- "Thiết bị cứng ESP và Giao diện Dashboard bắt buộc khởi tạo client với `username` và `password` được tụi em thiết lập mã hóa thông qua bộ sinh mã hash Password ở file `mosquitto.pw` tích phân trong phân hệ Docker Compose."
- "Tuy nhiên, em thừa nhận để lên Production thực tế ở đường phố, chúng ta phải mã hóa kênh truyền (MQTTS - Tức là TLS SSL port 8883) thì mới đảm bảo ko bị nghe lén mạng. Giới hạn mô hình Lab chi phí thấp nên em mới chạy port 1883 thô ạ."

### Giám khảo 5: Dashboard bằng HTML/JS thuần thế này thua đứt mấy bạn dùng React JS à?
🔥 **Cách phản biện:** 
- "Tùy bài toán thưa thầy. React JS yêu cầu bộ máy node_modules mấy chục ngàn tệp tin. DOM chậm chạm."
- "Nhiệm vụ của dự án này ở phần Web chỉ là làm Control Panel giám sát nhanh và kết nối Websocket 9001 realtime chớp nháy màu. Mã Vanilla JS được biên dịch và gắn CSS Native chạy trơn tru mượt mà ngay trên mọi chiếc IPAD, Iphone siêu nhỏ gọn, không cần load API 2 chiều nặng nề."
- "Thời gian Load trang tốn đúng... vài Milliseconds, độ trễ Rendering giao diện cực thấp nhằm bắt kịp tín hiệu thực từ ESP ạ."

---

*💪 Kết luận: Các bạn đã làm thật, code thật. Cứ tự tin bảo vệ, đập thẳng các luận điểm học thuyết này vào báo cáo và slide (rút gọn gạch đầu dòng).*
