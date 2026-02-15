# 📦 ESP-IDF Traffic Light Controller

> ESP32 DevKit V1 firmware using ESP-IDF framework

---

## Prerequisites

| Tool                        | Version  |
| --------------------------- | -------- |
| ESP-IDF                     | 5.0+     |
| Python                      | 3.8+     |
| VS Code + ESP-IDF Extension | Optional |

---

## Windows Setup (ESP-IDF)

### 1. Install ESP-IDF

```powershell
# Download ESP-IDF installer from Espressif
# https://docs.espressif.com/projects/esp-idf/en/latest/esp32/get-started/windows-setup.html

# Or use the offline installer:
# https://dl.espressif.com/dl/esp-idf/
```

### 2. Open ESP-IDF Terminal

```powershell
# From Start Menu: "ESP-IDF 5.x CMD"
# Or run:
C:\Espressif\frameworks\esp-idf-v5.x\export.bat
```

---

## Build & Flash

### 1. Navigate to Project

```powershell
cd "D:\Nam 2(D)\NCKH\traffic-mqtt-demo\esp32_idf"
```

### 2. Configure (menuconfig)

```powershell
idf.py menuconfig
```

Navigate to **Traffic Light Configuration**:

- **WiFi Settings**: SSID, Password
- **MQTT Settings**: Broker host/port, username/password
- **GPIO Pin Configuration**: Adjust if needed
- **Timing Configuration**: Green/Yellow/AllRed durations

### 3. Build

```powershell
idf.py build
```

### 4. Flash

```powershell
idf.py -p COM3 flash
```

### 5. Monitor

```powershell
idf.py -p COM3 monitor
```

### 6. Build + Flash + Monitor (Combined)

```powershell
idf.py -p COM3 flash monitor
```

---

## Configuration Options (menuconfig)

| Category | Option        | Default       |
| -------- | ------------- | ------------- |
| WiFi     | SSID          | YourSSID      |
| WiFi     | Password      | YourPassword  |
| MQTT     | Broker Host   | 192.168.1.100 |
| MQTT     | Port          | 1883          |
| MQTT     | Username      | demo          |
| MQTT     | Password      | demo_pass     |
| Timing   | Green phase   | 8000ms        |
| Timing   | Yellow phase  | 3000ms        |
| Timing   | All-red phase | 2000ms        |

---

## Test MQTT (Docker)

### Subscribe to all topics

```powershell
docker exec -it mosquitto mosquitto_sub -t "city/demo/intersection/001/#" -u demo -P demo_pass -v
```

### Send SET_MODE command

```powershell
docker exec -it mosquitto mosquitto_pub -t "city/demo/intersection/001/cmd" -u demo -P demo_pass -m '{"cmd_id":"test-001","type":"SET_MODE","mode":"MANUAL","ts_ms":1234567890}'
```

### Send SET_PHASE command

```powershell
docker exec -it mosquitto mosquitto_pub -t "city/demo/intersection/001/cmd" -u demo -P demo_pass -m '{"cmd_id":"test-002","type":"SET_PHASE","phase":3,"ts_ms":1234567890}'
```

---

## Smoke Test

```powershell
cd logger/tools
python smoke_test.py --host 127.0.0.1
# Expected: Exit code 0 (PASS)
```

---

## Project Structure

```
esp32_idf/
├── CMakeLists.txt
├── main/
│   ├── CMakeLists.txt
│   ├── Kconfig.projbuild
│   ├── app_main.c
│   ├── wifi_manager.c/.h
│   ├── mqtt_handler.c/.h
│   ├── fsm_controller.c/.h
│   └── gpio_lights.c/.h
└── README_ESP_IDF.md
```

---

## Troubleshoot

| Issue               | Solution                             |
| ------------------- | ------------------------------------ |
| Build fails         | Run `idf.py fullclean` then rebuild  |
| COM port not found  | Check Device Manager, install driver |
| WiFi not connecting | Verify SSID/password in menuconfig   |
| MQTT not connecting | Check broker IP, firewall            |

---

> 📚 See also: [WIRING.md](../docs/WIRING.md) | [SPEC.md](../SPEC.md)
