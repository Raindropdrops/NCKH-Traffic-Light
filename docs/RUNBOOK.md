# Traffic Light MQTT Demo - Runbook

## 1. Start System (PRO Dashboard)

```powershell
docker compose up -d --build
```

_Wait ~30s for Node-RED to initialize._

## 2. Open Dashboard

Browser: **[http://localhost:1880/ui](http://localhost:1880/ui)**
_You should see the Traffic Control Center with the modern dark theme._

## 3. Start Simulation (Mock ESP32)

Open a new terminal:

```powershell
python mock_esp32.py --host localhost
```

_The dashboard specific indicators (Online status, RSSI, Phase) should update immediately._

## 4. Operational Checks

1.  **Map Animation**: Verify the SVG traffic light changes phase (Green -> Yellow -> Red).
2.  **Control**:
    - Click **MANUAL** in dashboard.
    - Click **EW Green**.
    - Verify Map updates to EW Green / NS Red.
    - Verify **RTT Chart** shows a data point (latency).
3.  **Telemetry**: Verify RSSI/Heap charts are drawing lines.

## 5. Stop System

```powershell
# Stop simulation
Ctrl+C

# Stop containers
docker compose down
```
