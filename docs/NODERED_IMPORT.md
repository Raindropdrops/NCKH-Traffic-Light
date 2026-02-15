# 📥 NODE-RED IMPORT GUIDE

> Hướng dẫn import flows.json và sử dụng Dashboard

---

## 1. Kiến Trúc Mount

```yaml
# docker-compose.yml
nodered:
  volumes:
    - ./docker/nodered/data:/data # ← Node-RED data dir
```

Node-RED đọc file `/data/flows.json` trong container.

### ⚠️ File Name Issue

Node-RED mặc định đọc `flows_<hostname>.json` (vd: `flows_nodered.json`). Trong container hostname = `nodered`, nên file thực tế là:

```
/data/flows_nodered.json    ← Node-RED reads this
/data/flows.json            ← Our source file
```

**Cách fix**: copy source vào đúng tên:

```powershell
docker cp node-red/flows.json nodered:/data/flows_nodered.json
docker compose restart nodered
```

Hoặc dùng settings.js để force `flows.json`:

```javascript
// /data/settings.js
module.exports = { flowFile: "flows.json" };
```

---

## 2. Import Flows

### Method A: Docker Copy (Recommended)

```powershell
# Step 1: Copy flows vào container
docker cp node-red/flows.json nodered:/data/flows_nodered.json

# Step 2: Restart Node-RED
docker compose restart nodered

# Step 3: Chờ 10s rồi mở Dashboard
Start-Sleep 10
Start-Process "http://localhost:1880/ui"
```

### Method B: UI Import

1. Mở http://localhost:1880
2. Menu (☰) → **Import**
3. Click **select a file to import** → chọn `node-red/flows.json`
4. Click **Import** → **Deploy** (nút đỏ)

---

## 3. URLs

| URL                      | Purpose                        |
| ------------------------ | ------------------------------ |
| http://localhost:1880    | Flow Editor                    |
| http://localhost:1880/ui | **Dashboard UI** ← mở khi demo |

---

## 4. Dashboard Groups

| Group                | Content                                     |
| -------------------- | ------------------------------------------- |
| 🎮 Control           | Mode dropdown + Send, Phase dropdown + Send |
| 🚦 Intersection View | SVG 4-hướng N/S/E/W với đèn R/Y/G           |
| 📊 Live Status       | Online/Offline, Mode, Phase, Uptime         |
| 📡 Telemetry         | RSSI, Heap free, Uptime                     |
| 📋 ACK Log           | 10 ACK gần nhất                             |

---

## 5. Verify Nhanh

```powershell
# 1. Check Node-RED running
docker compose ps

# 2. Check logs (no errors)
docker logs nodered --tail 10

# 3. Check MQTT connection
docker exec mosquitto mosquitto_sub -t "city/demo/intersection/001/state" -u demo -P demo_pass -C 1

# 4. Start mock ESP32
python logger/tools/mock_esp32.py --host 127.0.0.1

# 5. Mở browser → http://localhost:1880/ui
# → Dashboard phải hiện Intersection SVG + Status updates
```

---

## 6. Cài node-red-dashboard (nếu thiếu)

```powershell
docker exec nodered npm install node-red-dashboard
docker compose restart nodered
```

---

## 7. Troubleshoot

| Vấn đề           | Fix                                                                        |
| ---------------- | -------------------------------------------------------------------------- |
| Dashboard trắng  | Cài node-red-dashboard (step 6)                                            |
| MQTT disconnect  | Check broker: `docker logs mosquitto --tail 10`                            |
| Auth failed      | Verify user/pass: demo / demo_pass                                         |
| Flows not loaded | Copy lại: `docker cp node-red/flows.json nodered:/data/flows_nodered.json` |
