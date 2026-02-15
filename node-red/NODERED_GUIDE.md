# 🔴 NODE-RED DASHBOARD GUIDE

> Hướng dẫn import và sử dụng Node-RED Dashboard cho Traffic Light MQTT Demo

---

## 1. Khởi Động

### 1.1 Start Docker Services

```powershell
cd "D:\Nam 2(D)\NCKH\traffic-mqtt-demo"
docker compose up -d
```

### 1.2 Verify Services Running

```powershell
docker compose ps
# Expected: mosquitto (0.0.0.0:1883), nodered (0.0.0.0:1880)
```

---

## 2. Truy Cập Node-RED

| URL                      | Purpose                   |
| ------------------------ | ------------------------- |
| http://localhost:1880    | Flow Editor (development) |
| http://localhost:1880/ui | Dashboard UI (end user)   |

---

## 3. Import Flows

### 3.1 Method A: Copy from File

1. Mở file `node-red/flows.json`
2. Copy toàn bộ nội dung (Ctrl+A, Ctrl+C)
3. Mở http://localhost:1880
4. Menu (☰) → **Import**
5. Paste vào Clipboard tab
6. Click **Import**
7. Click **Deploy** (nút đỏ góc trên phải)

### 3.2 Method B: Docker Copy

```powershell
# Copy flows.json vào container
docker cp node-red/flows.json nodered:/data/flows.json

# Restart Node-RED để load flows
docker compose restart nodered
```

### 3.3 Method C: File Upload

1. Mở http://localhost:1880
2. Menu (☰) → **Import**
3. Click **select a file to import**
4. Chọn `node-red/flows.json`
5. Click **Import**
6. Click **Deploy**

---

## 4. Dashboard Layout

```
┌─────────────────────────────────────────────────────────────┐
│                    Traffic Control                          │
├──────────────────────────────┬──────────────────────────────┤
│  🎮 Control                  │  📊 Status                    │
│  ┌──────────┐ ┌──────────┐  │  Connection: 🟢 ONLINE        │
│  │ 🔄 AUTO  │ │ ✋ MANUAL │  │  Mode: AUTO                   │
│  └──────────┘ └──────────┘  │  Phase: 0: NS_GREEN           │
│  ┌──────────┐ ┌──────────┐  │  Uptime: 1234s                │
│  │ 🟢 NS GO │ │ 🟢 EW GO │  │                               │
│  └──────────┘ └──────────┘  ├──────────────────────────────┤
│  ┌──────────────────┐ [SET] │  📡 Telemetry                  │
│  │ 0: NS_GREEN    ▼ │       │  📶 RSSI: -45 dBm              │
│  └──────────────────┘       │  💾 Heap: 180 KB               │
│                             │  ⏱️ Uptime: 1234s              │
├─────────────────────────────┴──────────────────────────────┤
│  📋 ACK Log                                                  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ Time     │ CMD ID     │ OK │ Error                    │  │
│  │ 15:30:01 │ a1b2c3... │ ✅ │ -                        │  │
│  │ 15:29:55 │ d4e5f6... │ ✅ │ -                        │  │
│  │ 15:29:48 │ g7h8i9... │ ❌ │ ERR_PHASE_REJECTED       │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Control Buttons

| Button               | Action             | MQTT Message                              |
| -------------------- | ------------------ | ----------------------------------------- |
| 🔄 AUTO              | Set AUTO mode      | `{"type":"SET_MODE","mode":"AUTO",...}`   |
| ✋ MANUAL            | Set MANUAL mode    | `{"type":"SET_MODE","mode":"MANUAL",...}` |
| 🟢 NS GO             | NS Green (Phase 0) | `{"type":"SET_PHASE","phase":0,...}`      |
| 🟢 EW GO             | EW Green (Phase 3) | `{"type":"SET_PHASE","phase":3,...}`      |
| Phase Dropdown + SET | Custom phase       | `{"type":"SET_PHASE","phase":N,...}`      |

---

## 6. MQTT Configuration

Default broker config (trong flows.json):

| Setting  | Value                        |
| -------- | ---------------------------- |
| Host     | `mosquitto` (Docker network) |
| Port     | `1883`                       |
| Username | `demo`                       |
| Password | `demo_pass`                  |

### Sửa Broker

1. Double-click bất kỳ MQTT node (màu tím)
2. Click ✏️ cạnh **Server**
3. Sửa host/port/credentials
4. Click **Update** → **Done** → **Deploy**

---

## 7. Troubleshoot

| Vấn đề                   | Nguyên nhân         | Giải pháp                              |
| ------------------------ | ------------------- | -------------------------------------- |
| Dashboard trống          | Flows chưa import   | Import lại flows.json                  |
| MQTT không kết nối       | Sai credentials     | Check Security tab trong broker config |
| "Connection refused"     | Mosquitto chưa chạy | `docker compose up -d`                 |
| Node-RED không load      | Container lỗi       | `docker compose restart nodered`       |
| Dashboard không cập nhật | ESP32/mock offline  | Check status topic                     |

### Xem Logs

```powershell
# Node-RED logs
docker logs nodered --tail 50 -f

# Mosquitto logs
docker logs mosquitto --tail 50 -f
```

### Test MQTT Manually

```powershell
# Subscribe all topics
docker exec -it mosquitto mosquitto_sub -t "city/demo/intersection/001/#" -u demo -P demo_pass -v
```

---

## 8. Test với Mock ESP32

```powershell
# Terminal 1: Start mock
cd logger/tools
python mock_esp32.py --host 127.0.0.1

# Terminal 2: Verify dashboard updates
# Mở http://localhost:1880/ui
# Click các nút control
# Verify ACK log hiện entries
```

---

## 9. Cài Node-RED Dashboard (nếu cần)

Nếu thiếu `node-red-dashboard`:

```powershell
# Vào container
docker exec -it nodered bash

# Cài dashboard
npm install node-red-dashboard

# Exit và restart
exit
docker compose restart nodered
```

---

> 📚 See also: [ARCHITECTURE_OVERVIEW.md](../docs/ARCHITECTURE_OVERVIEW.md) | [SPEC.md](../SPEC.md)
