# ✅ DEMO CHECKLIST — Pre-Demo & Live Steps

> In ra giấy, tick từng bước trước khi lên demo

---

## A. Pre-Demo (T-5 phút)

| #   | Step                   | Command                                                                                                  | ✅  |
| --- | ---------------------- | -------------------------------------------------------------------------------------------------------- | --- |
| 1   | Bật Docker Desktop     | Click icon, chờ whale xanh                                                                               | ⬜  |
| 2   | Mở PowerShell tại repo | `cd "D:\Nam 2(D)\NCKH\traffic-mqtt-demo"`                                                                | ⬜  |
| 3   | Start containers       | `docker compose up -d`                                                                                   | ⬜  |
| 4   | Verify containers      | `docker compose ps` → 2 containers running                                                               | ⬜  |
| 5   | Verify MQTT port       | `Test-NetConnection localhost -Port 1883`                                                                | ⬜  |
| 6   | Start mock ESP32       | `Start-Process powershell -ArgumentList "-Command","python logger/tools/mock_esp32.py --host 127.0.0.1"` | ⬜  |
| 7   | Mở Dashboard           | Browser → `http://localhost:1880/ui`                                                                     | ⬜  |
| 8   | Check Status = ONLINE  | Dashboard "Status" group → 🟢 ONLINE                                                                     | ⬜  |

---

## B. Live Demo Steps

### Step 1: Show Dashboard

```
http://localhost:1880/ui
```

> Giới thiệu layout: Control | Intersection View | Status | Telemetry

### Step 2: SET_MODE MANUAL

- Dropdown → **MANUAL**
- Click **Send SET_MODE**
- Verify: ACK log shows ✅

### Step 3: SET_PHASE 3 (EW GREEN)

- Dropdown phase → **3: EW_GREEN**
- Click **Send SET_PHASE**
- Verify: Intersection SVG → E/W xanh, N/S đỏ

### Step 4: SET_MODE AUTO

- Dropdown → **AUTO**
- Click **Send SET_MODE**
- Verify: Phase auto-cycles on intersection view

### Step 5: Show Telemetry

> Chỉ RSSI, Heap, Uptime đang cập nhật mỗi 5s

---

## C. Plan B — Troubleshoot

| Vấn đề                | Lệnh fix                                                               |
| --------------------- | ---------------------------------------------------------------------- | ---------------------------- |
| Containers không chạy | `docker compose down; docker compose up -d`                            |
| Dashboard trắng       | `docker compose restart nodered; Start-Sleep 10` rồi refresh           |
| Mock ESP32 crash      | `python logger/tools/mock_esp32.py --host 127.0.0.1`                   |
| MQTT auth fail        | `docker exec mosquitto mosquitto_sub -t "#" -u demo -P demo_pass -C 1` |
| Port 1880 conflict    | `netstat -an                                                           | findstr 1880` → kill process |
| Port 1883 conflict    | `netstat -an                                                           | findstr 1883` → kill process |
| Node-RED logs         | `docker logs nodered --tail 20`                                        |
| Mosquitto logs        | `docker logs mosquitto --tail 20`                                      |

### Nuclear Option (restart everything)

```powershell
docker compose down
docker compose up -d
Start-Sleep 10
python logger/tools/mock_esp32.py --host 127.0.0.1
# Mở lại http://localhost:1880/ui
```

---

## D. Post-Demo

| #   | Step            | ✅                       |
| --- | --------------- | ------------------------ | --- |
| 1   | Stop mock ESP32 | Ctrl+C trong cửa sổ mock | ⬜  |
| 2   | Stop containers | `docker compose down`    | ⬜  |
