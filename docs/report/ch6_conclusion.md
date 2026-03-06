# 11. Kết luận và kiến nghị

## a) Phần Kết luận

Đề tài "Nghiên cứu ứng dụng IoT - MQTT trong giám sát và điều khiển từ xa hệ thống đèn tín hiệu giao thông" đã đi đúng định hướng và hoàn thành các mục tiêu đề ra ban đầu.

1. Xây dựng thành công kiến trúc phần mềm tích hợp MQTT (Broker Mosquitto) với thiết bị điều khiển vi mạch thông minh biên (ESP32) và màn hình trung tâm (Web Dashboard).
2. Xây dựng bộ công cụ kiểm thử tự động, cung cấp bằng chứng định lượng sắc bén về hiệu năng của MQTT: Duy trì độ trễ siêu thấp ~43ms và tỉ lệ Packet Loss 0% kể cả khi bị nhồi nhét kích thước bản tin lớn.
3. Giải quyết được bài toán bảo vệ hệ thống khỏi các lệnh điều khiển lặp lặp thông qua trường định danh thông điệp `cmd_id` (Idempotency).
4. Khai thác thành công các lợi điểm của MQTT (QoS 0/1, Bản tin LWT) làm cơ sở đánh giá tình trạng bảo trì mạng lưới đèn.

Đây là một khuôn mẫu tiền đề vững chắc cho khái niệm "Giao thông thông minh" (Intelligent Transportation Systems) bằng chứng thực tiễn. Đề tài mở ra tiềm năng ứng dụng không chỉ cho hệ thống đèn tín hiệu mà còn cho các hệ thống cảnh báo và phát hiện xe cứu thương, cứu hỏa trong đô thị khẩn cấp.

## b) Phần Kiến nghị

- **Nghiên cứu tiếp theo:** Để triển khai hệ thống cho một quận, cần ứng dụng thêm cấu trúc "MQTT Broker Bridge" (Cây cầu nối) và "Cluster" (Cụm máy chủ) nhằm chia tải và tránh điểm lỗi duy nhất (Single Point of Failure).
- **Phát triển thuật toán thích nghi:** Thay thế chế độ vòng tuần hoàn cố định (AUTO Fixed-Timer) bằng hệ AI đếm lưu lượng phương tiện đi qua giao lộ bằng Camera AI, sau đó ra quyết định tăng/giảm số giây đèn Đỏ. Đề tài kiến nghị tích hợp mạch điện Edge AI phụ trợ kết nối vào vi điều khiển.
- **Về Bảo mật:** Chuyển đổi mã hóa giao thức MQTT sang MQTTS (MQTT over SSL/TLS) sử dụng chuẩn chứng thực 2 chiều mTLS (Mutual TLS) cấp thẻ căn cước (Certificate) cho từng cột đèn, chống hoàn toàn nguy cơ hacker chiếm quyền đổi đèn.

# 12. Tài liệu tham khảo

1. OASIS, _MQTT Version 5.0 Standard_, 2018. [Online]. Available: https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html
2. Espressif Systems, _ESP-IDF Programming Guide_, 2024. [Online]. Available: https://docs.espressif.com/projects/esp-idf/
3. HiveMQ, _MQTT Essentials - A Comprehensive Guide to MQTT_, 2023. [Online]. Available: https://www.hivemq.com/mqtt-essentials/
4. Eclipse Foundation, _Mosquitto Documentation_, 2024. [Online]. Available: https://mosquitto.org/documentation/
5. C. S. Nandy et al., "IoT Based Smart Traffic Control System," _2019 International Conference on Vision Towards Emerging Trends in Communication and Networking (ViTECoN)_, Vallore, India, 2019.

# 13. Phụ lục

- Sơ đồ mạch Node-RED luồng Socket.
- Scripts Python chạy Mock Test.
- Ảnh chụp kiểm thử Dashboard trên Web.
