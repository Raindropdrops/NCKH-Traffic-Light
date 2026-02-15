# 📜 SCRIPTS GUIDE

> Hướng dẫn sử dụng scripts demo

---

## Scripts Overview

| Script          | Purpose         | Command                   |
| --------------- | --------------- | ------------------------- |
| `demo_up.ps1`   | Start full demo | `.\scripts\demo_up.ps1`   |
| `demo_down.ps1` | Stop demo       | `.\scripts\demo_down.ps1` |
| `smoke.ps1`     | Run smoke test  | `.\scripts\smoke.ps1`     |

---

## 1. demo_up.ps1

**Chạy 1-click khởi động demo:**

```powershell
cd "D:\Nam 2(D)\NCKH\traffic-mqtt-demo"
.\scripts\demo_up.ps1
```

**Tự động thực hiện:**

1. `docker compose up -d`
2. Chờ services ready
3. Copy flows.json vào Node-RED
4. Start mock_esp32 (cửa sổ mới)
5. Mở browser → http://localhost:1880/ui

---

## 2. demo_down.ps1

**Tắt toàn bộ:**

```powershell
.\scripts\demo_down.ps1
```

**Tự động:**

1. Stop mock_esp32 processes
2. `docker compose down`

---

## 3. smoke.ps1

**Chạy test nhanh:**

```powershell
.\scripts\smoke.ps1
```

**Pre-checks:** Docker running, MQTT port 1883 accessible.

---

## Lỗi Thường Gặp

| Lỗi                                                    | Nguyên nhân                | Fix                                                                    |
| ------------------------------------------------------ | -------------------------- | ---------------------------------------------------------------------- |
| "cannot be loaded because running scripts is disabled" | PowerShell ExecutionPolicy | `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` |
| "docker compose up failed"                             | Docker Desktop chưa bật    | Start Docker Desktop, chờ 20s                                          |
| "mock_esp32.py not found"                              | Sai path                   | Ensure `logger/tools/mock_esp32.py` exists                             |
| "MQTT port not accessible"                             | Mosquitto chưa chạy        | `docker compose up -d`, chờ 10s                                        |
