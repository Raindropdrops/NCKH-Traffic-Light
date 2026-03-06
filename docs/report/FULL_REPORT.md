# CÃ¡c Pháº§n Má»Ÿ Äáº§u

## 5. Má»Ÿ Ä‘áº§u

Sá»± bÃ¹ng ná»• cá»§a Internet of Things (IoT) Ä‘Ã£ má»Ÿ ra nhá»¯ng hÆ°á»›ng Ä‘i má»›i trong viá»‡c quáº£n lÃ½ vÃ  váº­n hÃ nh thÃ´ng minh cÆ¡ sá»Ÿ háº¡ táº§ng Ä‘Ã´ thá»‹. Trong Ä‘Ã³, há»‡ thá»‘ng giao thÃ´ng tÃ­n hiá»‡u Ä‘Ã³ng vai trÃ² xÆ°Æ¡ng sá»‘ng trong viá»‡c duy trÃ¬ tráº­t tá»± vÃ  an toÃ n cÃ´ng cá»™ng. PhÆ°Æ¡ng thá»©c Ä‘iá»u khiá»ƒn Ä‘Ã¨n giao thÃ´ng truyá»n thá»‘ng hiá»‡n nay pháº§n lá»›n dá»±a trÃªn cÃ¡c bá»™ Ä‘á»‹nh thá»i (timer-based) Ä‘Æ°á»£c thiáº¿t láº­p sáºµn, thiáº¿u kháº£ nÄƒng giÃ¡m sÃ¡t tá»« xa vÃ  khÃ³ khÄƒn trong viá»‡c thay Ä‘á»•i chu ká»³ linh hoáº¡t. Äiá»u nÃ y Ä‘áº·t ra yÃªu cáº§u cáº¥p thiáº¿t vá» má»™t giáº£i phÃ¡p quáº£n lÃ½ táº­p trung, cÃ³ Ä‘á»™ trá»… tháº¥p vÃ  Ä‘á»™ tin cáº­y cao. Äá» tÃ i "NghiÃªn cá»©u á»©ng dá»¥ng IoT - MQTT trong giÃ¡m sÃ¡t vÃ  Ä‘iá»u khiá»ƒn tá»« xa há»‡ thá»‘ng Ä‘Ã¨n tÃ­n hiá»‡u giao thÃ´ng" Ä‘Æ°á»£c thá»±c hiá»‡n nháº±m má»¥c Ä‘Ã­ch giáº£i quyáº¿t váº¥n Ä‘á» nÃ y.

## 6. Tá»•ng quan tÃ¬nh hÃ¬nh nghiÃªn cá»©u thuá»™c lÄ©nh vá»±c

### TÃ¬nh hÃ¬nh trong nÆ°á»›c

Táº¡i Viá»‡t Nam, cÃ¡c thÃ nh phá»‘ lá»›n nhÆ° HÃ  Ná»™i vÃ  TP.HCM Ä‘ang bÆ°á»›c Ä‘áº§u thá»­ nghiá»‡m cÃ¡c há»‡ thá»‘ng giao thÃ´ng thÃ´ng minh (ITS). Tuy nhiÃªn, háº§u háº¿t cÃ¡c há»‡ thá»‘ng hiá»‡n táº¡i Ä‘á»u sá»­ dá»¥ng háº¡ táº§ng máº¡ng cÃ¡p quang tá»‘n kÃ©m vÃ  cÃ¡c giao thá»©c truyá»n thÃ´ng Ä‘á»™c quyá»n tÄ©nh. Viá»‡c giÃ¡m sÃ¡t thiáº¿t bá»‹ á»Ÿ cÃ¡c Ä‘iá»ƒm nÃºt giao thÃ´ng nhá» váº«n cÃ²n háº¡n cháº¿ do chi phÃ­ káº¿t ná»‘i cao.

### TÃ¬nh hÃ¬nh tháº¿ giá»›i

TrÃªn tháº¿ giá»›i, kiáº¿n trÃºc IoT vá»›i cÃ¡c giao thá»©c nháº¹ nhÆ° MQTT hoáº·c CoAP Ä‘Ã£ trá»Ÿ thÃ nh tiÃªu chuáº©n cÃ´ng nghiá»‡p cho liÃªn láº¡c mÃ¡y-mÃ¡y (M2M). CÃ¡c quá»‘c gia phÃ¡t triá»ƒn sá»­ dá»¥ng vi Ä‘iá»u khiá»ƒn biÃªn (Edge devices) káº¿t ná»‘i khÃ´ng dÃ¢y Ä‘á»ƒ gá»­i dá»¯ liá»‡u giao thÃ´ng theo thá»i gian thá»±c vá» mÃ¡y chá»§ trung tÃ¢m (Cloud), cho phÃ©p thuáº­t toÃ¡n AI phÃ¢n luá»“ng giao thÃ´ng Ä‘á»™ng.

## 7. LÃ½ do lá»±a chá»n Ä‘á» tÃ i

Giao thá»©c MQTT (Message Queuing Telemetry Transport) Ä‘Æ°á»£c Ä‘Ã¡nh giÃ¡ lÃ  Ä‘áº·c biá»‡t phÃ¹ há»£p cho máº¡ng IoT bÄƒng thÃ´ng tháº¥p vÃ  khÃ´ng á»•n Ä‘á»‹nh do dung lÆ°á»£ng header cá»±c nhá» (chá»‰ 2 bytes) vÃ  cÆ¡ cháº¿ QoS (Quality of Service) linh hoáº¡t. DÃ¹ váº­y, á»©ng dá»¥ng thá»±c táº¿ vÃ  viá»‡c Ä‘o Ä‘áº¡c hiá»‡u nÄƒng Ä‘á»‹nh lÆ°á»£ng cá»§a MQTT trong bÃ i toÃ¡n Ä‘áº·c thÃ¹ nhÆ° Ä‘iá»u khiá»ƒn Ä‘Ã¨n giao thÃ´ng táº¡i Viá»‡t Nam váº«n chÆ°a Ä‘Æ°á»£c nghiÃªn cá»©u toÃ n diá»‡n. Do Ä‘Ã³, viá»‡c thá»±c nghiá»‡m Ä‘o lÆ°á»ng Ä‘á»™ trá»… (RTT) vÃ  tÃ­nh á»•n Ä‘á»‹nh cá»§a MQTT lÃ  lÃ½ do chÃ­nh Ä‘á»ƒ nhÃ³m lá»±a chá»n Ä‘á» tÃ i nÃ y, lÃ m tiá»n Ä‘á» cho há»‡ thá»‘ng giao thÃ´ng thÃ´ng minh.

## 8. Má»¥c tiÃªu, ná»™i dung, phÆ°Æ¡ng phÃ¡p nghiÃªn cá»©u

**Má»¥c tiÃªu:**

- XÃ¢y dá»±ng thÃ nh cÃ´ng mÃ´ hÃ¬nh há»‡ thá»‘ng giÃ¡m sÃ¡t vÃ  Ä‘iá»u khiá»ƒn tÃ­n hiá»‡u Ä‘Ã¨n giao thÃ´ng tá»« xa thÃ´ng qua giao thá»©c MQTT.
- ÄÃ¡nh giÃ¡ hiá»‡u quáº£, Ä‘o lÆ°á»ng Ä‘á»™ trá»… máº¡ng (Round-Trip Time) vÃ  tá»· lá»‡ máº¥t gÃ³i tin (Packet Loss).
- XÃ¢y dá»±ng giao diá»‡n Dashboard thá»i gian thá»±c hiá»‡n Ä‘áº¡i, hiá»ƒn thá»‹ giÃ¡m sÃ¡t vÃ  cung cáº¥p cÆ¡ cháº¿ Ä‘iá»u khiá»ƒn kháº©n cáº¥p.

**Ná»™i dung nghiÃªn cá»©u:**

- NghiÃªn cá»©u kiáº¿n trÃºc IoT, giao thá»©c MQTT, vÃ  cÃ¡c chuáº©n thÃ´ng Ä‘iá»‡p (Payload).
- Cáº¥u hÃ¬nh MQTT Broker (Mosquitto) vá»›i tÃ­nh nÄƒng báº£o máº­t vÃ  WebSocket.
- Láº­p trÃ¬nh firmware cho vi Ä‘iá»u khiá»ƒn (ESP32) hoáº¡t Ä‘á»™ng nhÆ° má»™t thiáº¿t bá»‹ biÃªn (Edge worker).
- PhÃ¡t triá»ƒn pháº§n má»m Dashboard hiá»ƒn thá»‹.

**PhÆ°Æ¡ng phÃ¡p nghiÃªn cá»©u:**

- **NghiÃªn cá»©u lÃ½ thuyáº¿t:** Tham kháº£o tiÃªu chuáº©n MQTT v5.0 cá»§a quy chuáº©n OASIS.
- **NghiÃªn cá»©u thá»±c nghiá»‡m:** Thiáº¿t káº¿ ká»‹ch báº£n Benchmark, gá»­i hÃ ng nghÃ¬n gÃ³i tin tá»± Ä‘á»™ng Ä‘á»ƒ thu tháº­p dá»¯ liá»‡u vá» Ä‘á»™ trá»…, lÆ°u trá»¯ thÃ nh tá»‡p CSV, vÃ  viáº¿t mÃ£ Python váº½ biá»ƒu Ä‘á»“ xÃ¡c suáº¥t (ECDF, Histogram).

## 9. Äá»‘i tÆ°á»£ng vÃ  pháº¡m vi nghiÃªn cá»©u

- **Äá»‘i tÆ°á»£ng nghiÃªn cá»©u:**
  - Giao thá»©c truyá»n thÃ´ng MQTT vÃ  cÃ¡c cÆ¡ cháº¿ QoS (0, 1).
  - Vi Ä‘iá»u khiá»ƒn ESP32 vÃ  cÃ´ng nghá»‡ web thá»i gian thá»±c (WebSocket).
- **Pháº¡m vi nghiÃªn cá»©u:**
  - Äá» tÃ i giá»›i háº¡n mÃ´ phá»ng vÃ  thá»±c nghiá»‡m á»Ÿ quy mÃ´ má»™t nÃºt giao thÃ´ng (intersection) dáº¡ng ngÃ£ tÆ° tiÃªu chuáº©n gá»“m 4 hÆ°á»›ng Ä‘i.
  - Thá»­ nghiá»‡m Ä‘á»™ trá»… thá»±c hiá»‡n trong mÃ´i trÆ°á»ng máº¡ng giáº£ láº­p (Mock) vÃ  máº¡ng cá»¥c bá»™ (LAN/WiFi).
# ChÆ°Æ¡ng 1. CÆ¡ sá»Ÿ lÃ½ thuyáº¿t vá» IoT vÃ  giao thá»©c MQTT

Chi tiáº¿t trong chÆ°Æ¡ng nÃ y táº­p trung lÃ m rÃµ cÃ¡c ná»n táº£ng cÃ´ng nghá»‡ lÃµi táº¡o nÃªn há»‡ thá»‘ng, Ä‘áº·c biá»‡t lÃ  kiáº¿n trÃºc truyá»n thÃ´ng MQTT. Viá»‡c hiá»ƒu rÃµ cÆ¡ cháº¿ ná»™i táº¡i cá»§a MQTT lÃ  cÆ¡ sá»Ÿ Ä‘á»ƒ giáº£i thÃ­ch cÃ¡c quyáº¿t Ä‘á»‹nh thiáº¿t káº¿ á»Ÿ cÃ¡c chÆ°Æ¡ng sau.

## 1.1 Tá»•ng quan vá» Internet of Things (IoT) trong Giao thÃ´ng

Internet váº¡n váº­t (IoT) trong giao thÃ´ng, hay ITS (Intelligent Transportation Systems), Ä‘á» cáº­p Ä‘áº¿n viá»‡c tÃ­ch há»£p cÃ¡c cáº£m biáº¿n, vi Ä‘iá»u khiá»ƒn tÃ­nh toÃ¡n vÃ  cÃ´ng nghá»‡ truyá»n thÃ´ng vÃ o cÆ¡ sá»Ÿ háº¡ táº§ng giao thÃ´ng.

YÃªu cáº§u cá»‘t lÃµi cá»§a má»™t há»‡ thá»‘ng IoT giao thÃ´ng:

1. **Äá»™ trá»… tháº¥p (Low Latency):** TÃ­nh nÄƒng an toÃ n (nhÆ° thao tÃ¡c kháº©n cáº¥p Ä‘á»•i Ä‘Ã¨n ALL-RED) yÃªu cáº§u lá»‡nh pháº£i Ä‘Æ°á»£c pháº£n há»“i tÃ­nh báº±ng mili-giÃ¢y.
2. **Kháº£ nÄƒng chá»‹u lá»—i (Fault Tolerance):** Máº¡ng khÃ´ng dÃ¢y thÆ°á»ng xuyÃªn bá»‹ nhiá»…u. Há»‡ thá»‘ng pháº£i biáº¿t khi nÃ o máº¥t káº¿t ná»‘i Ä‘á»ƒ cÃ³ cÆ¡ cháº¿ tá»± Ä‘á»™ng xá»­ lÃ½ an toÃ n cá»¥c bá»™.
3. **Tiáº¿t kiá»‡m tÃ i nguyÃªn:** CÃ¡c tá»§ Ä‘iá»u khiá»ƒn ngoÃ i Ä‘Æ°á»ng phá»‘ cÃ³ nÄƒng lá»±c xá»­ lÃ½ (CPU) vÃ  káº¿t ná»‘i máº¡ng háº¡n cháº¿ (thÆ°á»ng dÃ¹ng máº¡ng di Ä‘á»™ng 3G/4G/4G-LTE).

## 1.2 Giao thá»©c MQTT (Message Queuing Telemetry Transport)

MQTT lÃ  má»™t giao thá»©c truyá»n thÃ´ng máº¡ng má»Ÿ, nháº¹ (lightweight), tuÃ¢n theo mÃ´ hÃ¬nh xuáº¥t báº£n/Ä‘Äƒng kÃ½ (publish/subscribe). MQTT chuáº©n hÃ³a quy Ä‘á»‹nh bá»Ÿi OASIS, Ä‘áº·c biá»‡t thiáº¿t káº¿ cho cÃ¡c thiáº¿t bá»‹ bá»‹ giá»›i háº¡n tÃ i nguyÃªn vÃ  cÃ¡c máº¡ng cÃ³ bÄƒng thÃ´ng tháº¥p, Ä‘á»™ trá»… cao, hay khÃ´ng Ä‘Ã¡ng tin cáº­y.

### 1.2.1 MÃ´ hÃ¬nh Publish/Subscribe vÃ  Broker

KhÃ¡c vá»›i giao thá»©c HTTP hoáº¡t Ä‘á»™ng theo mÃ´ hÃ¬nh Client/Server (Request/Response) Ä‘á»“ng bá»™, MQTT sá»­ dá»¥ng kiáº¿n trÃºc báº¥t Ä‘á»“ng bá»™:

- **Broker (MÃ¡y chá»§ trung gian):** ÄÃ³ng vai trÃ² lÃ m bÆ°u Ä‘iá»‡n, nháº­n má»i tin nháº¯n (message) vÃ  phÃ¢n phá»‘i láº¡i cho cÃ¡c Ä‘á»‘i tÆ°á»£ng quan tÃ¢m.
- **Publisher (NgÆ°á»i gá»­i):** Thiáº¿t bá»‹ gá»­i dá»¯ liá»‡u lÃªn Broker vá»›i má»™t nhÃ£n dÃ¡n cá»¥ thá»ƒ gá»i lÃ  `Topic`.
- **Subscriber (NgÆ°á»i nháº­n):** CÃ i Ä‘áº·t láº¯ng nghe cÃ¡c `Topic`. Báº¥t cá»© khi nÃ o cÃ³ tin nháº¯n má»›i thuá»™c Topic Ä‘Ã³, Broker sáº½ láº­p tá»©c Ä‘áº©y (push) dá»¯ liá»‡u xuá»‘ng.

Nhá» mÃ´ hÃ¬nh nÃ y, Dashboard Ä‘iá»u khiá»ƒn Ä‘Ã¨n vÃ  vi Ä‘iá»u khiá»ƒn ESP32 khÃ´ng cáº§n biáº¿t Ä‘á»‹a chá»‰ IP cá»§a nhau, giÃºp há»‡ thá»‘ng dá»… dÃ ng má»Ÿ rá»™ng, Ä‘á»“ng thá»i giáº£i quyáº¿t Ä‘Æ°á»£c yÃªu cáº§u bÄƒng thÃ´ng háº¹p cá»§a ITS.

### 1.2.2 CÃ¡c má»©c Ä‘á»™ Ä‘áº£m báº£o pháº£n há»“i - Quality of Service (QoS)

MQTT cung cáº¥p 3 má»©c Ä‘á»™ Æ°u tiÃªn xÃ¡c nháº­n gÃ³i tin, cho phÃ©p láº­p trÃ¬nh viÃªn Ä‘Ã¡nh Ä‘á»•i giá»¯a tá»‘c Ä‘á»™ vÃ  Ä‘á»™ tin cáº­y:

- **QoS 0 (At most once / Fire-and-forget):** Gá»­i 1 láº§n duy nháº¥t, khÃ´ng cáº§n pháº£n há»“i. PhÃ¹ há»£p cho dá»¯ liá»‡u telemetry liÃªn tá»¥c nhÆ° nhiá»‡t Ä‘á»™, tÃ¬nh tráº¡ng RAM, vÃ¬ náº¿u máº¥t 1 báº£n tin, báº£n tin á»Ÿ giÃ¢y tiáº¿p theo sáº½ bÃ¹ Ä‘áº¯p. Tá»‘c Ä‘á»™ cá»±c nhanh.
- **QoS 1 (At least once):** Äáº£m báº£o báº£n tin tá»›i Ä‘Ã­ch Ã­t nháº¥t 1 láº§n. NgÆ°á»i nháº­n pháº£i tráº£ vá» gÃ³i tin xÃ¡c nháº­n (ACK). DÃ¹ng cho máº¡ng khÃ´ng á»•n Ä‘á»‹nh, nÆ¡i tin nháº¯n cÃ³ thá»ƒ bá»‹ gá»­i láº¡i. Báº¯t buá»™c dÃ¹ng cho lá»‡nh Ä‘iá»u khiá»ƒn Ä‘á»•i pha Ä‘Ã¨n giao thÃ´ng, vÃ¬ viá»‡c bá» sÃ³t lá»‡nh lÃ  khÃ´ng thá»ƒ cháº¥p nháº­n Ä‘Æ°á»£c.
- **QoS 2 (Exactly once):** Äáº£m báº£o nháº­n Ä‘Ãºng vÃ  chá»‰ 1 láº§n. Triá»ƒn khai phá»©c táº¡p qua tiáº¿n trÃ¬nh báº¯t tay 4 bÆ°á»›c.

Trong Ä‘á» tÃ i nÃ y, nhÃ³m thiáº¿t káº¿ káº¿t há»£p linh hoáº¡t cáº£ QoS 0 vÃ  QoS 1 tÃ¹y theo ná»™i dung báº£n tin (ÄÆ°á»£c trÃ¬nh bÃ y chi tiáº¿t táº¡i Pháº§n thiáº¿t káº¿ kiáº¿n trÃºc ChÆ°Æ¡ng 2).

### 1.2.3 CÆ¡ cháº¿ Last Will and Testament (LWT) vÃ  Retained Messages

- **LWT (Di chÃºc cuá»‘i cÃ¹ng):** Khi thiáº¿t bá»‹ (Edge) káº¿t ná»‘i tá»›i Broker, nÃ³ "gá»­i gáº¯m" má»™t báº£n tin LWT. Náº¿u thiáº¿t bá»‹ bá»‹ sáº­p nguá»“n Ä‘á»™t ngá»™t hoáº·c rá»›t máº¡ng mÃ  khÃ´ng ká»‹p ngáº¯t káº¿t ná»‘i Ä‘Ãºng cÃ¡ch, Broker sáº½ thay máº·t thiáº¿t bá»‹ cÃ´ng bá»‘ báº£n tin nÃ y cho Dashboard biáº¿t. Äiá»u nÃ y giáº£i quyáº¿t bÃ i toÃ¡n giÃ¡m sÃ¡t tráº¡ng thÃ¡i (Online/Offline) cá»§a thiáº¿t bá»‹ viá»…n thÃ´ng má»™t cÃ¡ch chá»§ Ä‘á»™ng.
- **Retained Messages:** Broker cÃ³ kháº£ nÄƒng lÆ°u giá»¯ láº¡i (retain) báº£n tin cuá»‘i cÃ¹ng cá»§a má»™t Topic. Báº¥t ká»³ má»™t Dashboard má»›i nÃ o vá»«a má»Ÿ lÃªn cÅ©ng láº­p tá»©c nháº­n Ä‘Æ°á»£c báº£n tin Retained, giÃºp Ä‘á»“ng bá»™ hÃ³a tráº¡ng thÃ¡i hiá»‡n thá»i ngay láº­p tá»©c mÃ  khÃ´ng cáº§n pháº£i gá»i lá»‡nh láº¥y dá»¯ liá»‡u (polling).

## 1.3 Báº£ng so sÃ¡nh MQTT so vá»›i cÃ¡c giao thá»©c khÃ¡c

Äá»ƒ lÃ m sÃ¡ng tá» tÃ­nh Æ°u viá»‡t cá»§a MQTT vá»›i bÃ i toÃ¡n, dÆ°á»›i Ä‘Ã¢y lÃ  báº£ng so sÃ¡nh tham chiáº¿u.

| TiÃªu chÃ­                                  | MQTT                            | HTTP / REST                         | CoAP                         |
| :---------------------------------------- | :------------------------------ | :---------------------------------- | :--------------------------- |
| **Kiáº¿n trÃºc**                             | Publish / Subscribe             | Request / Response (Äá»“ng bá»™)        | Client / Server (Request)    |
| **KÃ­ch thÆ°á»›c Header**                     | Ráº¥t nhá» (2 Bytes)               | Lá»›n (VÃ i trÄƒm Bytes)                | Nhá» (4 Bytes)                |
| **Giao thá»©c máº¡ng**                        | TCP/IP (CÃ³ thá»ƒ dÃ¹ng WebSockets) | TCP (chiáº¿m dá»¥ng tÃ i nguyÃªn)         | UDP (khÃ´ng tin cáº­y)          |
| **TiÃªu tá»‘n pin / bÄƒng thÃ´ng**             | Cá»±c ká»³ tháº¥p                     | Ráº¥t cao (Do overhead)               | KhÃ¡ mTháº¥p                    |
| **Há»— trá»£ thá»i gian thá»±c (Realtime push)** | Cá»±c kÃ¬ tá»‘t (Push)               | Ráº¥t kÃ©m (Pháº£i Polling/Long-polling) | KhÃ¡ tá»‘t                      |
| **á»¨ng dá»¥ng chÃ­nh**                        | IoT, Smart City                 | Web Services, CRUD                  | Cáº£m biáº¿n nÄƒng lÆ°á»£ng cá»±c tháº¥p |

CÃ³ thá»ƒ tháº¥y giao thá»©c MQTT (cháº¡y trÃªn TCP ná»n táº£ng) cÃ¢n báº±ng hoÃ n háº£o giá»¯a Ä‘á»™ tin cáº­y máº¡ng truyá»n thÃ´ng vá»›i tÃ­nh nÄƒng push tá»©c thá»i, lÃ  lá»±a chá»n lÃ½ tÆ°á»Ÿng nháº¥t cho há»‡ thá»‘ng Ä‘iá»ƒu khiá»ƒn Ä‘Ã¨n tÃ­n hiá»‡u giao thÃ´ng so vá»›i cÆ¡ cháº¿ láº¥y-cáº¥p (Polling) cá»§a HTTP truyá»n thá»‘ng.

## 1.4 Vi Ä‘iá»u khiá»ƒn ESP32

Node vi Ä‘iá»u khiá»ƒn ESP32 cá»§a hÃ£ng Espressif Systems Ä‘Æ°á»£c á»©ng dá»¥ng trong nghiÃªn cá»©u nÃ y do vi xá»­ lÃ½ lÃµi kÃ©p máº¡nh máº½ (lÃªn tá»›i 240MHz) cÃ¹ng chip Wi-Fi/Bluetooth tÃ­ch há»£p sáºµn. ESP32 Ä‘i kÃ¨m vá»›i framework chÃ­nh thá»©c lÃ  ESP-IDF (IoT Development Framework) sá»­ dá»¥ng há»‡ Ä‘iá»u hÃ nh thá»i gian thá»±c FreeRTOS, giÃºp linh kiá»‡n cÃ³ thá»ƒ cháº¡y Ä‘a luá»“ng Ä‘á»“ng thá»i: má»™t luá»“ng giá»¯ tÃ­n hiá»‡u Ä‘iá»u khiá»ƒn Ä‘Ã¨n theo chu kÃ¬ cá»©ng (Hardware Timer), má»™t luá»“ng riÃªng biá»‡t xá»­ lÃ½ cÃ¡c gÃ³i tin MQTT máº¡ng lÆ°á»›i.
# ChÆ°Æ¡ng 2. Thiáº¿t káº¿ Kiáº¿n trÃºc Há»‡ thá»‘ng Äiá»u khiá»ƒn

Há»‡ thá»‘ng Ä‘iá»u khiá»ƒn Ä‘Ã¨n giao thÃ´ng dá»±a trÃªn chuáº©n MQTT theo mÃ´ hÃ¬nh Client-Broker-Client Ä‘Æ°á»£c nhÃ³m thiáº¿t káº¿ nháº±m kháº¯c phá»¥c Ä‘iá»ƒm yáº¿u cá»§a Ä‘iá»u khiá»ƒn vÃ²ng tá»« truyá»n thá»‘ng, cung cáº¥p kháº£ nÄƒng phÃ¡t hiá»‡n liÃªn tá»¥c luá»“ng giao thÃ´ng vÃ  pháº£n há»“i linh hoáº¡t.

## 2.1 SÆ¡ Ä‘á»“ khá»‘i tá»•ng thá»ƒ cá»§a há»‡ thá»‘ng

Há»‡ thá»‘ng Ä‘Æ°á»£c chia lÃ m 3 thÃ nh pháº§n chÃ­nh tuyáº¿n tÃ­nh yáº¿u cáº§u (End-to-end Architecture).

1. **MQTT Broker (Core):** LÃ  mÃ¡y chá»§ trung tÃ¢m nháº­n dá»¯ liá»‡u, xá»­ lÃ½ phÃ¢n quyá»n. CÃ i Ä‘áº·t trÃªn Docker sá»­ dá»¥ng mÃ£ nguá»“n má»Ÿ Eclipse Mosquitto.
2. **Edge Device (ESP32 Controller):** Láº¯p Ä‘áº·t trá»±c tiáº¿p táº¡i cÃ¡c tá»§ Ä‘iá»u khiá»ƒn ngÃ£ tÆ°. Äá»c cáº£m biáº¿n cá»©ng, Ä‘iá»u khiá»ƒn rÆ¡-le Ä‘Ã¨n, gá»­i tráº¡ng thÃ¡i vá» Broker, vÃ  láº¯ng nghe lá»‡nh ghi Ä‘Ã¨ (Override Command).
3. **Web Dashboard (Node-RED/HTML):** Trung tÃ¢m giÃ¡m sÃ¡t thÃ nh phá»‘. Hiá»ƒn thá»‹ UI trá»±c quan trÃªn web trÃ¬nh duyá»‡t cho ngÆ°á»i trá»±c ban, váº½ biá»ƒu Ä‘á»“ tráº¡ng thÃ¡i thá»i gian thá»±c.

## 2.2 Thiáº¿t káº¿ Topic Tree MQTT

Thay vÃ¬ giao tiáº¿p theo Ä‘á»‹a chá»‰ IP khÃ³ dá»± Ä‘oÃ¡n, giao thá»©c MQTT dÃ¹ng cÃ¡c Topic String. Há»‡ thá»‘ng sá»­ dá»¥ng Prefix chung: `city/demo/intersection/001/` Ä‘á»‹nh danh duy nháº¥t ngÃ£ tÆ° thá»© 001.

| Topic Path     | Chiá»u dá»¯ liá»‡u        | QoS | Chá»©c nÄƒng (Ã nghÄ©a)                                      |
| -------------- | -------------------- | --- | -------------------------------------------------------- |
| `../state`     | Edge â†’ Dashboard     | 0   | PhÃ¡t tráº¡ng thÃ¡i pha Ä‘Ã¨n, chu ká»³ liÃªn tá»¥c (Retained=True) |
| `../telemetry` | Edge â†’ Dashboard     | 0   | PhÃ¡t Ä‘á»‹nh kÃ¬ thÃ´ng sá»‘ RSSI máº¡ng, RAM, thá»i gian sá»‘ng     |
| `../cmd`       | Dashboard â†’ Edge     | 1   | Lá»‡nh Ä‘iá»u khiá»ƒn kháº©n cáº¥p, yÃªu cáº§u bÃ¡o nháº­n               |
| `../ack`       | Edge â†’ Dashboard     | 1   | Pháº£n há»“i xÃ¡c nháº­n lá»‡nh `cmd_id` Ä‘Ã£ thá»±c thi              |
| `../status`    | (Broker) â†’ Dashboard | 1   | Báº£n tin LWT (Online / Offline) giá»¯ láº¡i trÃªn Server       |

## 2.3 TiÃªu chuáº©n hÃ³a thÃ´ng Ä‘iá»‡p (JSON Payload Schema)

Nháº±m Ä‘áº£m báº£o kháº£ nÄƒng má»Ÿ rá»™ng thuáº­t toÃ¡n Ä‘a ngÃ´n ngá»¯ (Python, C++, JS), táº¥t cáº£ gÃ³i tin Ä‘Æ°á»£c Ä‘Ã³ng gÃ³i theo Ä‘á»‹nh dáº¡ng chuáº©n JSON.

Äáº·c biá»‡t lÆ°u Ã½, lá»‡nh Ä‘iá»u khiá»ƒn máº¡ng Ä‘Ã´i khi cÃ³ hiá»‡n tÆ°á»£ng láº·p (do cÆ¡ cháº¿ QoS 1 thá»­ gá»­i láº¡i). Äá»ƒ giáº£i quyáº¿t triá»‡t Ä‘á»ƒ tÃ­nh cháº¥t nÃ y, mÃ£ JSON chÃ¨n thÃªm trÆ°á»ng duy nháº¥t `cmd_id` (UUID). Náº¿u vi Ä‘iá»u khiá»ƒn nháº­n láº¡i má»™t mÃ£ lá»‡nh Ä‘Ã£ thá»±c thi, nÃ³ sáº½ tráº£ vá» ACK ngay láº­p tá»©c nhÆ°ng khÃ´ng thay Ä‘á»•i ngáº¯t cá»©ng (Hardware Interrupt), gá»i lÃ  tÃ­nh "Idempotent" (Ká»¹ thuáº­t thÆ°á»ng dÃ¹ng trong DevOps ngÃ¢n hÃ ng).

## 2.4 MÃ¡y tráº¡ng thÃ¡i Ä‘iá»u khiá»ƒn Ä‘Ã¨n (FSM)

Cá»¥m Ä‘Ã¨n (Báº¯c-Nam gá»i lÃ  NS, ÄÃ´ng-TÃ¢y gá»i lÃ  EW) váº­n hÃ nh theo mÃ¡y tráº¡ng thÃ¡i há»¯u háº¡n, bao gá»“m 4 cháº¿ Ä‘á»™ (Mode):

- **AUTO:** Tá»± Ä‘á»™ng Ä‘áº¿m vÃ²ng chu kÃ¬ 6 Pha Ä‘Ã¨n chuáº©n má»±c.
- **MANUAL:** Dá»«ng cáº¥p Ä‘Ã´ng (Freeze) á»Ÿ má»™t Pha Ä‘Ã¨n cá»¥ thá»ƒ vÃ  giá»¯ vÃ´ thá»i háº¡n. Lá»‡nh nÃ y Ä‘Æ°á»£c gá»­i trong tÃ¬nh huá»‘ng cÃ³ xe Æ°u tiÃªn, sá»± cá»‘ tai náº¡n tÄ©nh.
- **BLINK:** ÄÃ¨n VÃ ng chá»›p táº¯t liÃªn tá»¥c 2 hÆ°á»›ng nháº±m cáº£nh bÃ¡o nhÆ°á»ng Ä‘Æ°á»ng.
- **OFF:** Táº¯t toÃ n bá»™ rÆ¡ le Ä‘Ã¨n khi thi cÃ´ng hoáº·c cáº¯t Ä‘iá»‡n ngÃ£ tÆ° diá»‡n rá»™ng.

Táº¡i mÃ´ hÃ¬nh AUTO, 6 Pha Ä‘Æ°á»£c quy Ä‘á»‹nh theo tá»· lá»‡ thá»i gian vÃ ng. (1-NS_GREEN, 2-NS_YELLOW, 3-ALL_RED_CLEAR, 4-EW_GREEN, 5-EW_YELLOW, 6-ALL_RED_CLEAR). Bá»‘n giÃ¢y ALL_RED_CLEAR Ä‘Æ°á»£c bá»• sung kÄ© lÆ°á»¡ng nháº±m Ä‘áº£m báº£o toÃ n bá»™ phÆ°Æ¡ng tiá»‡n thoÃ¡t khá»i tÃ¢m giao lá»™, háº¡n cháº¿ nguy cÆ¡ va cháº¡m.
# ChÆ°Æ¡ng 3. Ná»™i dung Triá»ƒn khai xÃ¢y dá»±ng

## 3.1 XÃ¢y dá»±ng há»‡ thá»‘ng Broker Mosquitto

MÃ´i trÆ°á»ng Broker lÃ  khá»‘i Ã³c xÆ°Æ¡ng sá»‘ng. Há»‡ thá»‘ng sá»­ dá»¥ng Docker Compose cÃ i Ä‘áº·t trÃªn Linux/Windows cho Ä‘á»™ Ä‘á»“ng nháº¥t mÃ£ nguá»“n cá»±c cao trÃªn má»i há»‡ sinh thÃ¡i thá»±c thi (Write once run everywhere).

Táº­p cáº¥u hÃ¬nh chÃ­nh `mosquitto.conf`:

- **Port 1883:** Láº¯ng nghe giao tiáº¿p giao thá»©c gá»‘c MQTT, giao tiáº¿p vi Ä‘iá»u khiá»ƒn.
- **Port 9001:** Láº¯ng nghe Websocket - má»™t tÃ­nh nÄƒng Ä‘Æ°á»£c kÃ­ch hoáº¡t bá»• sung cho phÃ©p giao tiáº¿p xuyÃªn trÃ¬nh duyá»‡t, phá»¥c vá»¥ Dashboard giÃ¡m sÃ¡t.
- **Authentication:** KÃ­ch hoáº¡t mÃ£ hoÃ¡ TLS cÆ¡ báº£n vÃ  file máº­t kháº©u `passwordfile` cháº·n trÃ¡i phÃ©p truy cáº­p (ACL) trÃ¡i luá»“ng.

## 3.2 Láº­p trÃ¬nh Firmware vi Ä‘iá»u khiá»ƒn ESP32

Firmware xÃ¢y dá»±ng dá»±a vÃ o ná»n táº£ng C/C++ trá»±c tiáº¿p cá»§a nhÃ  sáº£n xuáº¥t (ESP-IDF phiÃªn báº£n cao cáº¥p v5.5) thay vÃ¬ Framework Arduino Ä‘Æ¡n giáº£n nháº±m táº­n dá»¥ng trá»n váº¹n sá»©c máº¡nh vi tÃ­nh luá»“ng.

ThÃ nh pháº§n há»‡ thá»‘ng chia lÃ m 4 luá»“ng xá»­ lÃ½ Ä‘á»“ng dáº¡ng (FreeRTOS Tasks):

1. **MQTT Task Network:** Khá»Ÿi táº¡o máº¡ng Wifi, xá»­ lÃ½ vÃ²ng láº·p Reconnect tÄ©nh. Duy trÃ¬ tÃ­n hiá»‡u Keep Alive. Khai bÃ¡o chuá»—i báº£n tin "Offline" cho LWT ngay trÆ°á»›c khi thá»±c thi káº¿t ná»‘i.
2. **Command Handler:** Parsing file JSON Ä‘iá»u khiá»ƒn báº±ng thÆ° viá»‡n cJSON. Cáº¥p phÃ¡t cÆ¡ cháº¿ lá»c `cmd_id` vÃ  kÃ­ch hoáº¡t rÆ¡_le thay Ä‘á»•i Phase. Náº¿u JSON kÃ­ch thÆ°á»›c lá»›n hÆ¡n 1024 Bytes, há»‡ thá»‘ng tá»± Ä‘á»™ng loáº¡i bá» phÃ²ng thá»§ táº¥n cÃ´ng DoS trÃ n bá»™ nhá»› Ä‘á»‡m.
3. **GPIO LED Control:** Cáº¥p dÃ²ng táº£i 3.3v Ä‘iá»u khiáº¿n Relay kÃ­ch cÃ¡c chÃ¢n GPIO cho 6 Ä‘Ã¨n.
4. **Telemetry Publisher:** Má»—i 5s Ä‘á»c Free Heap Mem, thá»i gian sá»‘ng Uptime, Ä‘á»™ nhiá»…u máº¡ng gá»­i lÃªn QoS 0 vá» Dashboard Ä‘Ã¡nh giÃ¡.

## 3.3 PhÃ¡t triá»ƒn giao diá»‡n pháº§n má»m Dashboard Ä‘iá»u khiá»ƒn

Há»‡ thá»‘ng sá»­ dá»¥ng ná»n táº£ng HTML5/CSS3 cho tráº£i nghiá»‡m tá»‘c Ä‘á»™ (Performatic Interface), káº¿t ná»‘i theo phÆ°Æ¡ng thá»©c WebSocket. MÃ n hÃ¬nh Dark Theme Ä‘Æ°á»£c chia ra cÃ¡c khu vá»±c quáº£n lÃ½ chuyÃªn nghiá»‡p: Cá»¥m Ä‘iá»u khiá»ƒn kháº©n cáº¥p Control Mode; NgÃ£ tÆ° Ä‘á»“ há»a SVG thá»ƒ hiá»‡n sá»‘ng Ä‘á»™ng quÃ¡ trÃ¬nh luÃ¢n chuyá»ƒn chu ká»³ mÃ u; Live Status thÃ´ng sá»‘ mÃ¡y láº».

Hai tÃ­nh nÄƒng khoa há»c then chá»‘t Ä‘Æ°á»£c bá»• sung:

- **Biá»ƒu Ä‘á»“ thá»i gian thá»±c RTT (Realtime Chart):** TÃ­nh toÃ¡n vÃ  biá»ƒu diá»…n ngay láº­p tá»©c trÃªn há»‡ tá»a Ä‘á»™ thá»i gian (Canvas) tá»‘c Ä‘á»™ khá»© há»“i máº¡ng tÃ­nh tá»« milliseconds lá»‡nh gá»­i (cmd) gá»­i Ä‘i so vá»›i thá»i gian nháº­n xÃ¡c thá»±c (ack).
- **QoS Level Panels / Event LWT:** Lá»‹ch sá»­ ghi log tá»± Ä‘á»™ng ngáº¯t thiáº¿t bá»‹ cho giÃ¡m thá»‹.

## 3.4 Ká»‹ch báº£n mÃ´ phá»ng kiá»ƒm thá»­ vá»›i Mock ESP32

Do pháº§n cá»©ng ESP32 cÃ³ rá»§i ro vá» can nhiá»…u káº¿t ná»‘i sÃ³ng Wifi khi thá»­ nghiá»‡m Ä‘o Ä‘áº¡c á»Ÿ sá»‘ lÆ°á»£ng gÃ³i siÃªu lá»›n (Load testing). NhÃ³m Ä‘Ã£ láº­p trÃ¬nh thiáº¿t bá»‹ mÃ´ phá»ng linh kiá»‡n áº£o "Mock ESP32" báº±ng mÃ£ nguá»“n Python. CÃ´ng cá»¥ nÃ y xá»­ lÃ½ giáº£ láº­p 100% giá»‘ng thiáº¿t bá»‹ tháº­t vá» logic xá»­ lÃ½, vÃ²ng tuáº§n hoÃ n Ä‘Ã¨n, tráº£ vá» ACK vÃ  Publish tráº¡ng thÃ¡i. Mock ESP32 cho phÃ©p thiáº¿t láº­p Ä‘á»™ trá»… nhÃ¢n táº¡o vÃ  tÃ¹y biáº¿n tÄƒng tá»‘c quÃ¡ trÃ¬nh Ä‘Ã¨n `Speed=2x` dÃ¹ng cho demo. Khá»‘i lÆ°á»£ng gÃ³i benchmark 2000 Requests gá»­i liÃªn tiáº¿p Ä‘Ã£ Ä‘Æ°á»£c cÃ´ng cá»¥ mÃ´ phá»ng gá»“ng gÃ¡nh xuáº¥t sáº¯c lÃ m ná»n táº£ng kiá»ƒm thá»­ cho pháº§n Ä‘Ã¡nh giÃ¡ táº¡i ChÆ°Æ¡ng 4.
# ChÆ°Æ¡ng 4. Thá»­ nghiá»‡m káº¿t quáº£ vÃ  ÄÃ¡nh giÃ¡

ChÆ°Æ¡ng nÃ y trÃ¬nh bÃ y cÃ¡c ká»‹ch báº£n thá»­ nghiá»‡m táº£i (Load Testing), Ä‘o lÆ°á»ng Ä‘á»™ trá»… máº¡ng (Round-Trip Time - RTT) vÃ  Ä‘Ã¡nh giÃ¡ Ä‘á»™ tin cáº­y cá»§a há»‡ thá»‘ng dá»±a trÃªn dá»¯ liá»‡u thu tháº­p tá»« cÃ´ng cá»¥ Benchmark mÃ´ phá»ng (Mock ESP32).

## 4.1 MÃ´i trÆ°á»ng vÃ  CÃ´ng cá»¥ Thá»­ nghiá»‡m

Há»‡ thá»‘ng thá»­ nghiá»‡m Ä‘Æ°á»£c thiáº¿t láº­p trÃªn mÃ´i trÆ°á»ng máº¡ng vÃ²ng cá»¥c bá»™ (loopback) Ä‘á»ƒ Ä‘Ã¡nh giÃ¡ kháº£ nÄƒng xá»­ lÃ½ nguyÃªn báº£n cá»§a lÃµi MQTT Broker vÃ  Node-RED Dashboard:

- **Broker:** Mosquitto 2.x (Docker, localhost:1883)
- **Thiáº¿t bá»‹ áº£o (Edge Device):** MÃ£ nguá»“n mÃ´ phá»ng `mock_esp32.py`
- **CÃ´ng cá»¥ sinh táº£i:** MÃ£ lá»‡nh tá»± Ä‘á»™ng `run_benchmark_report.py`
- **Má»©c QoS:** QoS 1 (At-least-once) cho luá»“ng Gá»­i lá»‡nh `cmd` vÃ  Nháº­n pháº£n há»“i `ack`.

## 4.2 Äá»‹nh nghÄ©a vÃ  Ká»‹ch báº£n Test Äá»™ trá»… RTT

Trong bÃ i toÃ¡n giÃ¡m sÃ¡t, Ä‘á»™ trá»… RTT Ä‘Æ°á»£c Ä‘á»‹nh nghÄ©a lÃ  khoáº£ng thá»i gian tá»« lÃºc Dashboard phÃ¡t Ä‘i má»™t lá»‡nh Ä‘iá»u khiá»ƒn (báº¥m nÃºt) cho tá»›i khi nháº­n láº¡i xÃ¡c nháº­n thiáº¿t bá»‹ Ä‘Ã£ chuyá»ƒn pha Ä‘Ã¨n thÃ nh cÃ´ng.

$$\text{RTT} = t_{\text{ack\_recv}} - t_{\text{cmd\_send}}$$

- **Ká»‹ch báº£n:** Gá»­i tá»± Ä‘á»™ng 500 tÃ­n hiá»‡u Ä‘iá»u khiá»ƒn liÃªn tiáº¿p, vá»›i cÆ°á»ng Ä‘á»™ 1 lá»‡nh má»—i 200 mili-giÃ¢y.
- **Biáº¿n Ä‘á»™c láº­p:** TÄƒng dáº§n kÃ­ch thÆ°á»›c gÃ³i tin Ä‘iá»u khiá»ƒn (Payload pad) tá»« 0 Bytes lÃªn 1200 Bytes nháº±m thá»­ táº£i vÃ  kiá»ƒm tra giá»›i háº¡n báº£o máº­t há»‡ thá»‘ng.

## 4.3 PhÃ¢n tÃ­ch Káº¿t quáº£ Thá»­ nghiá»‡m

DÆ°á»›i Ä‘Ã¢y lÃ  báº£ng tá»•ng há»£p káº¿t quáº£ Ä‘o Ä‘áº¡c tá»« 2500 tÃ­n hiá»‡u thá»­ nghiá»‡m phÃ¢n bá»• Ä‘á»u trÃªn 5 Case kÃ­ch cá»¡ gÃ³i tin:

| Case | Payload pad | Giá»›i háº¡n  | Sá»‘ lá»‡nh | Nháº­n  | RTT Mean | Median  |   P95   | Packet Loss |        ÄÃ¡nh giÃ¡        |
| :--: | :---------: | :-------: | :-----: | :---: | :------: | :-----: | :-----: | :---------: | :--------------------: |
|  1   |     0 B     |   â‰¤ 1KB   |   500   |  500  | 43.3 ms  | 43.0 ms | 45.0 ms |     0%      |          PASS          |
|  2   |    256 B    |   â‰¤ 1KB   |   500   |  500  | 43.2 ms  | 43.0 ms | 45.0 ms |     0%      |          PASS          |
|  3   |    512 B    |   â‰¤ 1KB   |   500   |  500  | 43.3 ms  | 43.0 ms | 45.0 ms |     0%      |          PASS          |
|  4   |    900 B    |   â‰¤ 1KB   |   500   |  500  | 43.4 ms  | 43.0 ms | 45.0 ms |     0%      |          PASS          |
|  5   | **1200 B**  | **> 1KB** | **500** | **0** |  **â€”**   |  **â€”**  |  **â€”**  |  **100%**   | **PASS (Bá»‹ loáº¡i trá»«)** |

### 4.3.1 ÄÃ¡nh giÃ¡ TÃ­nh kiÃªn Ä‘á»‹nh (Consistency) cá»§a Ä‘á»™ trá»…

XuyÃªn suá»‘t cÃ¡c Case tá»« 1 Ä‘áº¿n 4, khi lÆ°á»£ng dá»¯ liá»‡u táº£i (Payload) nhá»“i thÃªm tÄƒng tá»« 0 Ä‘áº¿n 900 Bytes, Ä‘á»™ trá»… trung bÃ¬nh (Mean) duy trÃ¬ má»©c á»•n Ä‘á»‹nh tá»‹nh tiáº¿n ráº¥t nhá», giao Ä‘á»™ng tá»« **43.2 ms Ä‘áº¿n 43.4 ms**. Chá»‰ sá»‘ phÃ¢n vá»‹ P95 Ä‘áº¡t **45.0 ms** (nghÄ©a lÃ  95% sá»‘ lÆ°á»£ng gÃ³i tin Ä‘á»u máº¥t chÆ°a tá»›i 45ms Ä‘á»ƒ hoÃ n táº¥t má»™t cháº·ng khá»© há»“i hoÃ n chá»‰nh).

CÃ³ thá»ƒ Ä‘Ã¡nh giÃ¡ MQTT thá»ƒ hiá»‡n tÃ­nh hiá»‡u quáº£ bÄƒng thÃ´ng vÆ°á»£t trá»™i, gáº§n nhÆ° khÃ´ng gÃ¢y quÃ¡ táº£i cho bá»™ xá»­ lÃ½ cá»§a Broker khi dá»¯ liá»‡u phÃ¬nh to.

### 4.3.2 ÄÃ¡nh giÃ¡ TÃ­nh Ä‘á»™ tin cáº­y vÃ  Báº£o máº­t (Packet Loss vÃ  Rejection)

- **Packet Loss:** XuyÃªn suá»‘t 2000 gÃ³i tin ná»™i bá»™ á»Ÿ giá»›i háº¡n kÃ­ch thÆ°á»›c cho phÃ©p, tá»· lá»‡ Packet Loss Ä‘áº¡t má»©c tuyá»‡t Ä‘á»‘i 0% nhá» cÆ¡ cháº¿ QoS 1 cá»§a MQTT tá»± Ä‘á»™ng thá»­ gá»­i láº¡i (Retry) khi phÃ¡t hiá»‡n máº¥t mÃ¡t tÃ­n hiá»‡u.
- **Oversize Rejection (Táº¡i Case 5):** Khi nhá»“i kÃ­ch thÆ°á»›c báº£n tin vÆ°á»£t qua ngÆ°á»¡ng chá»‹u Ä‘á»±ng thiáº¿t káº¿ (1024 Bytes), thiáº¿t bá»‹ Mock ESP32 Ä‘Ã£ hoáº¡t Ä‘á»™ng chÃ­nh xÃ¡c theo ká»‹ch báº£n chá»‘ng táº¥n cÃ´ng tá»« chá»‘i dá»‹ch vá»¥ (DoS): Tá»± Ä‘á»™ng cÃ´ láº­p, huá»· bá» tÃ­n hiá»‡u vi pháº¡m vÃ  khÃ´ng tráº£ vá» ACK. Äiá»u nÃ y dáº«n tá»›i 500 lá»‡nh gá»­i Ä‘i tháº¥t báº¡i (Loss 100%), chá»©ng minh mÃ´ hÃ¬nh hoáº¡t Ä‘á»™ng phÃ²ng vá»‡ Ä‘Ãºng thiáº¿t káº¿.

## 4.4 Giá»›i háº¡n cá»§a Thá»­ nghiá»‡m (Mock vs Physical Device)

Cáº§n lÃ m rÃµ, cÃ¡c dá»¯ liá»‡u RTT ~43ms trÃªn chá»‰ pháº£n Ã¡nh "Overhead" cá»§a riÃªng giao thá»©c TCP/MQTT vÃ  quÃ¡ trÃ¬nh Parse chuá»—i JSON táº¡i trung tÃ¢m.

á»ž mÃ´i trÆ°á»ng ngÃ£ tÆ° thá»±c táº¿ khi thay Mock ESP32 báº±ng máº¡ch ESP32 váº­t lÃ½, Ä‘á»™ trá»… RTT sáº½ bá»‹ cá»™ng dá»“n thÃªm:

1. Äá»™ trá»… váº­t lÃ½ sÃ³ng WiFi/4G (Biáº¿n thiÃªn tá»« 10ms - 200ms).
2. Thá»i gian chá»‘t Interrupt chuyá»ƒn Ä‘á»•i vi máº¡ch RÆ¡-le Ä‘iá»‡n (VÃ i ms).
3. Äá»™ trá»… do sá»¥t nguá»“n, nhiá»…u Ä‘iá»‡n tá»«.

Dá»¯ liá»‡u mÃ´ phá»ng nÃ y Ä‘Ã³ng vai trÃ² chá»©ng minh tÃ­nh kháº£ thi cá»§a giao thá»©c vá» phÃ­a pháº§n má»m. Viá»‡c thá»­ nghiá»‡m vá»›i thiáº¿t bá»‹ pháº§n cá»©ng tháº­t sáº½ Ä‘Æ°á»£c thá»±c nghiá»‡m vÃ  cáº­p nháº­t sá»‘ liá»‡u á»Ÿ tiáº¿n trÃ¬nh káº¿ tiáº¿p cá»§a Ä‘á» tÃ i.

## 4.5 XÃ¡c nháº­n tÃ­nh nÄƒng Last Will And Testament (LWT)

Trong quÃ¡ trÃ¬nh giáº£ láº­p ngáº¯t Ä‘iá»‡n ngá»™t ngá»™t (Kill Process Mock), Broker Mosquitto Ä‘Ã£ thÃ nh cÃ´ng báº¯t lá»—i rá»›t máº¡ng ngang hÃ ng vÃ  thay máº·t thiáº¿t bá»‹ phÃ¡t tÃ­n hiá»‡u Offline vá» Dashboard. TÃ­nh nÄƒng nÃ y cho phÃ©p Ä‘iá»u phá»‘i viÃªn giao thÃ´ng nháº­n diá»‡n ngay láº­p tá»©c trá»¥ Ä‘Ã¨n nÃ o Ä‘ang máº¥t tÃ­n hiá»‡u Ä‘á»ƒ phá»‘i há»£p cá»­ cáº£nh sÃ¡t giao thÃ´ng ra thay tháº¿. ÄÃ¡nh giÃ¡ tÃ­nh nÄƒng nÃ y: Äáº T.
# 11. Káº¿t luáº­n vÃ  kiáº¿n nghá»‹

## a) Pháº§n Káº¿t luáº­n

Äá» tÃ i "NghiÃªn cá»©u á»©ng dá»¥ng IoT - MQTT trong giÃ¡m sÃ¡t vÃ  Ä‘iá»u khiá»ƒn tá»« xa há»‡ thá»‘ng Ä‘Ã¨n tÃ­n hiá»‡u giao thÃ´ng" Ä‘Ã£ Ä‘i Ä‘Ãºng Ä‘á»‹nh hÆ°á»›ng vÃ  hoÃ n thÃ nh cÃ¡c má»¥c tiÃªu Ä‘á» ra ban Ä‘áº§u.

1. XÃ¢y dá»±ng thÃ nh cÃ´ng kiáº¿n trÃºc pháº§n má»m tÃ­ch há»£p MQTT (Broker Mosquitto) vá»›i thiáº¿t bá»‹ Ä‘iá»u khiá»ƒn vi máº¡ch thÃ´ng minh biÃªn (ESP32) vÃ  mÃ n hÃ¬nh trung tÃ¢m (Web Dashboard).
2. XÃ¢y dá»±ng bá»™ cÃ´ng cá»¥ kiá»ƒm thá»­ tá»± Ä‘á»™ng, cung cáº¥p báº±ng chá»©ng Ä‘á»‹nh lÆ°á»£ng sáº¯c bÃ©n vá» hiá»‡u nÄƒng cá»§a MQTT: Duy trÃ¬ Ä‘á»™ trá»… siÃªu tháº¥p ~43ms vÃ  tá»‰ lá»‡ Packet Loss 0% ká»ƒ cáº£ khi bá»‹ nhá»“i nhÃ©t kÃ­ch thÆ°á»›c báº£n tin lá»›n.
3. Giáº£i quyáº¿t Ä‘Æ°á»£c bÃ i toÃ¡n báº£o vá»‡ há»‡ thá»‘ng khá»i cÃ¡c lá»‡nh Ä‘iá»u khiá»ƒn láº·p láº·p thÃ´ng qua trÆ°á»ng Ä‘á»‹nh danh thÃ´ng Ä‘iá»‡p `cmd_id` (Idempotency).
4. Khai thÃ¡c thÃ nh cÃ´ng cÃ¡c lá»£i Ä‘iá»ƒm cá»§a MQTT (QoS 0/1, Báº£n tin LWT) lÃ m cÆ¡ sá»Ÿ Ä‘Ã¡nh giÃ¡ tÃ¬nh tráº¡ng báº£o trÃ¬ máº¡ng lÆ°á»›i Ä‘Ã¨n.

ÄÃ¢y lÃ  má»™t khuÃ´n máº«u tiá»n Ä‘á» vá»¯ng cháº¯c cho khÃ¡i niá»‡m "Giao thÃ´ng thÃ´ng minh" (Intelligent Transportation Systems) báº±ng chá»©ng thá»±c tiá»…n. Äá» tÃ i má»Ÿ ra tiá»m nÄƒng á»©ng dá»¥ng khÃ´ng chá»‰ cho há»‡ thá»‘ng Ä‘Ã¨n tÃ­n hiá»‡u mÃ  cÃ²n cho cÃ¡c há»‡ thá»‘ng cáº£nh bÃ¡o vÃ  phÃ¡t hiá»‡n xe cá»©u thÆ°Æ¡ng, cá»©u há»a trong Ä‘Ã´ thá»‹ kháº©n cáº¥p.

## b) Pháº§n Kiáº¿n nghá»‹

- **NghiÃªn cá»©u tiáº¿p theo:** Äá»ƒ triá»ƒn khai há»‡ thá»‘ng cho má»™t quáº­n, cáº§n á»©ng dá»¥ng thÃªm cáº¥u trÃºc "MQTT Broker Bridge" (CÃ¢y cáº§u ná»‘i) vÃ  "Cluster" (Cá»¥m mÃ¡y chá»§) nháº±m chia táº£i vÃ  trÃ¡nh Ä‘iá»ƒm lá»—i duy nháº¥t (Single Point of Failure).
- **PhÃ¡t triá»ƒn thuáº­t toÃ¡n thÃ­ch nghi:** Thay tháº¿ cháº¿ Ä‘á»™ vÃ²ng tuáº§n hoÃ n cá»‘ Ä‘á»‹nh (AUTO Fixed-Timer) báº±ng há»‡ AI Ä‘áº¿m lÆ°u lÆ°á»£ng phÆ°Æ¡ng tiá»‡n Ä‘i qua giao lá»™ báº±ng Camera AI, sau Ä‘Ã³ ra quyáº¿t Ä‘á»‹nh tÄƒng/giáº£m sá»‘ giÃ¢y Ä‘Ã¨n Äá». Äá» tÃ i kiáº¿n nghá»‹ tÃ­ch há»£p máº¡ch Ä‘iá»‡n Edge AI phá»¥ trá»£ káº¿t ná»‘i vÃ o vi Ä‘iá»u khiá»ƒn.
- **Vá» Báº£o máº­t:** Chuyá»ƒn Ä‘á»•i mÃ£ hÃ³a giao thá»©c MQTT sang MQTTS (MQTT over SSL/TLS) sá»­ dá»¥ng chuáº©n chá»©ng thá»±c 2 chiá»u mTLS (Mutual TLS) cáº¥p tháº» cÄƒn cÆ°á»›c (Certificate) cho tá»«ng cá»™t Ä‘Ã¨n, chá»‘ng hoÃ n toÃ n nguy cÆ¡ hacker chiáº¿m quyá»n Ä‘á»•i Ä‘Ã¨n.

# 12. TÃ i liá»‡u tham kháº£o

1. OASIS, _MQTT Version 5.0 Standard_, 2018. [Online]. Available: https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html
2. Espressif Systems, _ESP-IDF Programming Guide_, 2024. [Online]. Available: https://docs.espressif.com/projects/esp-idf/
3. HiveMQ, _MQTT Essentials - A Comprehensive Guide to MQTT_, 2023. [Online]. Available: https://www.hivemq.com/mqtt-essentials/
4. Eclipse Foundation, _Mosquitto Documentation_, 2024. [Online]. Available: https://mosquitto.org/documentation/
5. C. S. Nandy et al., "IoT Based Smart Traffic Control System," _2019 International Conference on Vision Towards Emerging Trends in Communication and Networking (ViTECoN)_, Vallore, India, 2019.

# 13. Phá»¥ lá»¥c

- SÆ¡ Ä‘á»“ máº¡ch Node-RED luá»“ng Socket.
- Scripts Python cháº¡y Mock Test.
- áº¢nh chá»¥p kiá»ƒm thá»­ Dashboard trÃªn Web.

