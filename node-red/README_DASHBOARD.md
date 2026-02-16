# Node-RED Dashboard PRO — Setup & Usage

## 🚀 Quick Start

```bash
docker compose up -d --build
```

Wait ~60 seconds for Node-RED to install packages and start.

## 🔗 Access Dashboard

Open **[http://localhost:1880/ui](http://localhost:1880/ui)**

## 🧪 Verification (Mock Data)

Run the mock ESP32 to feed live data into the dashboard:

```bash
# In a new terminal
python mock_esp32.py --host localhost
```

## 🛠 Features (PRO Edition)

1.  **Animated Intersection Map**: SVG-based map with glowing traffic lights.
2.  **Split Layout**:
    - **Left**: Large visualization.
    - **Right**: Controls, Logs, & Charts.
3.  **Real-time Charts**:
    - **RTT**: Measures latency (Command -> ACK).
    - **RSSI/Heap**: Live telemetry signals.
4.  **Countdown Ring**: Visual pulse indicating active phase.

## ⚠️ Troubleshooting "White UI"

If the dashboard is blank:

1.  Ensure `node-red-dashboard` is installed:
    ```bash
    docker exec -it nodered npm install node-red-dashboard
    docker restart nodered
    ```
    _(Note: The provided Dockerfile handles this automatically)_
2.  Check logs:
    ```bash
    docker logs -f nodered
    ```
