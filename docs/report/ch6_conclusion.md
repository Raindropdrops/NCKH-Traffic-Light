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
