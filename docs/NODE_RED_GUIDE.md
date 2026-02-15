# 🔴 NODE-RED GUIDE — Hướng Dẫn Thực Hành

> Cách chỉnh sửa và debug Node-RED Dashboard cho traffic-mqtt-demo

---

## 1. Truy Cập Node-RED

### 1.1 Mở Dashboard UI (End User)

```
http://localhost:1880/ui
```

### 1.2 Mở Flow Editor (Developer)

```
http://localhost:1880
```

---

## 2. Import/Export Flows

### 2.1 Export Flows (Backup)

1. Flow Editor → Menu (☰) → **Export**
2. Chọn **all flows** hoặc tab cụ thể
3. Copy JSON hoặc **Download**
4. Lưu vào `node-red/flows.json`

### 2.2 Import Flows

1. Flow Editor → Menu (☰) → **Import**
2. Paste JSON hoặc **select a file**
3. Click **Import**
4. **Deploy** để áp dụng

### 2.3 Backup Command

```powershell
# Copy từ Docker volume
docker cp nodered:/data/flows.json ./node-red/flows.json
```

---

## 3. Cấu Hình MQTT Broker

### 3.1 Tìm MQTT Node

1. Flow Editor → double-click bất kỳ node **mqtt in** hoặc **mqtt out**
2. Click biểu tượng ✏️ bên cạnh **Server**

### 3.2 Chỉnh Connection

| Field     | Value               | Note                |
| --------- | ------------------- | ------------------- |
| Server    | `mosquitto`         | Docker network name |
| Port      | `1883`              | Default MQTT        |
| Client ID | `nodered-dashboard` | Unique ID           |

### 3.3 Chỉnh Security

Tab **Security**:

| Field    | Value       |
| -------- | ----------- |
| Username | `demo`      |
| Password | `demo_pass` |

**⚠️ Sau khi sửa:** Click **Update** → **Deploy**

---

## 4. Chỉnh Topics

### 4.1 Subscribe Topics (mqtt in)

Double-click node `mqtt in` → chỉnh **Topic**:

| Topic                               | Purpose                  |
| ----------------------------------- | ------------------------ |
| `city/demo/intersection/001/state`  | LED state updates        |
| `city/demo/intersection/001/status` | Online/Offline           |
| `city/demo/intersection/001/ack`    | Command acknowledgements |

### 4.2 Publish Topics (mqtt out)

Double-click node `mqtt out` → chỉnh **Topic**:

| Topic                            | Purpose       |
| -------------------------------- | ------------- |
| `city/demo/intersection/001/cmd` | Send commands |

---

## 5. Chỉnh UI Dashboard

### 5.1 Dashboard Layout

1. Flow Editor → sidebar → **dashboard** tab (icon 📊)
2. **Layout**: Kéo thả tabs và groups
3. **Theme**: Chọn màu sắc

### 5.2 Mode Dropdown

1. Tìm node **ui_dropdown** trong flow
2. Double-click → chỉnh **Options**:

```
AUTO
MANUAL
BLINK
OFF
```

### 5.3 Phase Buttons

1. Tìm các node **ui_button**
2. Chỉnh **Label** và **Payload**:

| Button   | Payload                          |
| -------- | -------------------------------- |
| NS_GREEN | `{"type":"SET_PHASE","phase":0}` |
| EW_GREEN | `{"type":"SET_PHASE","phase":1}` |
| ALL_RED  | `{"type":"SET_PHASE","phase":2}` |

---

## 6. Deploy Changes

### 6.1 Deploy Options

| Option             | Khi nào dùng                |
| ------------------ | --------------------------- |
| **Full**           | Thay đổi lớn (nodes, flows) |
| **Modified Flows** | Chỉ sửa flow hiện tại       |
| **Modified Nodes** | Chỉ sửa 1-2 nodes           |

### 6.2 Deploy Button

1. Click **Deploy** (góc trên phải)
2. Chọn loại deploy từ dropdown ▼

---

## 7. Debug & Troubleshoot

### 7.1 Debug Node

1. Kéo **debug** node vào flow
2. Connect từ output của node cần debug
3. Deploy → xem output trong **Debug** tab (sidebar)

### 7.2 Test MQTT Subscription

```powershell
# Trong terminal
docker exec -it mosquitto mosquitto_sub -t "city/demo/intersection/001/#" -u demo -P demo_pass -v
```

### 7.3 Test MQTT Publish

```powershell
# Gửi command test
docker exec -it mosquitto mosquitto_pub -t "city/demo/intersection/001/cmd" -u demo -P demo_pass -m '{"cmd_id":"test-123","type":"SET_MODE","mode":"MANUAL","ts_ms":1234567890}'
```

### 7.4 Xem Node-RED Logs

```powershell
docker logs nodered --tail 100 -f
```

---

## 8. Common Issues

| Vấn đề               | Nguyên nhân         | Giải pháp              |
| -------------------- | ------------------- | ---------------------- |
| Dashboard không load | Node-RED chưa start | `docker compose up -d` |
| MQTT không connect   | Sai credentials     | Check Security tab     |
| Command không gửi    | Sai topic           | Check mqtt out node    |
| Không nhận state     | ESP32 offline       | Check status topic     |

---

## 9. Files Liên Quan

| File                              | Mục đích          |
| --------------------------------- | ----------------- |
| `docker/nodered/data/flows.json`  | Flow definitions  |
| `docker/nodered/data/settings.js` | Node-RED settings |
| `node-red/flows.json`             | Backup flows      |

---

> 📚 Xem thêm: [ARCHITECTURE_OVERVIEW.md](ARCHITECTURE_OVERVIEW.md) | [SPEC.md](../SPEC.md)
