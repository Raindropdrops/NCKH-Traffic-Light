# 🔬 Experiment Plan — RTT Benchmark Study

> Traffic Light MQTT Demo — Research Methodology

---

## 1. RTT Definition and Measurement Method

### 1.1 Round-Trip Time (RTT) Definition

**RTT** (Round-Trip Time) is the time elapsed from when a command is sent from the logger to the MQTT broker until the acknowledgment (ack) is received back.

```
RTT = t_ack_received - t_command_sent (milliseconds)
```

### 1.2 Measurement Architecture

```
┌─────────────┐      cmd (QoS 1)      ┌───────────┐      cmd        ┌─────────┐
│   Logger    │ ───────────────────▶  │  Mosquitto │ ──────────────▶ │  ESP32  │
│  (Python)   │                       │   Broker   │                 │         │
│             │ ◀─────────────────── │            │ ◀────────────── │         │
└─────────────┘      ack (QoS 1)      └───────────┘      ack        └─────────┘
       │                                                                   │
       │                                                                   │
       ▼                                                                   ▼
   t_send_ms                                                          t_ack_ms
   (recorded)                                                        (recorded)
```

### 1.3 Measured Components

| Segment | Description |
|---------|-------------|
| Logger → Broker | Python MQTT publish latency |
| Broker → ESP32 | WiFi transmission + broker routing |
| ESP32 processing | JSON parsing + command execution |
| ESP32 → Broker | WiFi transmission |
| Broker → Logger | Python MQTT receive latency |

### 1.4 Payload Schema

**Command (cmd):**

```json
{
  "cmd_id": "uuid-v4",
  "type": "SET_MODE",
  "mode": "AUTO",
  "ts_ms": 1234567890,
  "pad": "xxx..." (optional padding)
}
```

**Acknowledgment (ack):**

```json
{
  "cmd_id": "uuid-v4",
  "ok": true,
  "ts_ms": 1234567890
}
```

---

## 2. Experiment Cases

### 2.1 Case Definitions

| Case | pad_bytes | count | interval_ms | Purpose |
|------|-----------|-------|-------------|---------|
| **Case 1** | 0 | 500 | 200 | Baseline (minimal payload) |
| **Case 2** | 256 | 500 | 200 | Medium payload impact |
| **Case 3** | 1024 | 500 | 200 | Large payload impact |

### 2.2 Optional Extended Cases

| Case | Network | pad_bytes | count | Purpose |
|------|---------|-----------|-------|---------|
| **Case 4** | WiFi 2.4GHz | 0 | 500 | WiFi baseline |
| **Case 5** | 4G Hotspot | 0 | 500 | Mobile network latency |
| **Case 6** | WiFi 5GHz | 0 | 500 | 5GHz comparison |

---

## 3. Execution Instructions

### 3.1 Prerequisites

- Docker running with Mosquitto + Node-RED
- ESP32 connected and publishing state
- Python venv activated with requirements installed

### 3.2 Individual Case Commands

```powershell
cd logger/tools

# Case 1: Baseline (no padding)
python logger.py --host <BROKER_IP> --count 500 --interval_ms 200 --mode AUTO --pad_bytes 0 --out ../results/results_case1.csv

# Case 2: Medium payload (256 bytes padding)
python logger.py --host <BROKER_IP> --count 500 --interval_ms 200 --mode AUTO --pad_bytes 256 --out ../results/results_case2.csv

# Case 3: Large payload (1024 bytes padding)
python logger.py --host <BROKER_IP> --count 500 --interval_ms 200 --mode AUTO --pad_bytes 1024 --out ../results/results_case3.csv
```

### 3.3 Automated Execution

```powershell
# Run all cases with one command
python run_experiments.py --host <BROKER_IP>

# With custom output directory
python run_experiments.py --host 192.168.1.100 --output-dir ../results/run_20260208
```

---

## 4. Data Validity Criteria

### 4.1 Minimum Requirements

| Criterion | Threshold | Rationale |
|-----------|-----------|-----------|
| Completion rate | ≥ 95% | At least 475/500 acks received |
| Outlier filtering | RTT < 5000ms | Exclude network anomalies |
| Data integrity | All fields present | cmd_id, t_send_ms, t_ack_recv_ms |

### 4.2 Exclusion Criteria

- Lost commands (no ack received within 5s)
- RTT > 5000ms (network anomaly)
- Duplicate cmd_id (should not occur)

---

## 5. Results Template

### 5.1 Per-Case Results

| Metric | Case 1 (0B) | Case 2 (256B) | Case 3 (1024B) |
|--------|-------------|---------------|----------------|
| Sent | | | |
| Received | | | |
| Lost | | | |
| Loss Rate (%) | | | |
| Min (ms) | | | |
| Mean (ms) | | | |
| Median (ms) | | | |
| P95 (ms) | | | |
| P99 (ms) | | | |
| Max (ms) | | | |

### 5.2 Statistical Comparison

| Comparison | Δ Mean (ms) | Δ P95 (ms) | Significance |
|------------|-------------|------------|--------------|
| Case 2 vs Case 1 | | | |
| Case 3 vs Case 1 | | | |
| Case 3 vs Case 2 | | | |

---

## 6. Expected Outcomes

### 6.1 Hypothesis

1. **H1:** Payload size correlates positively with RTT
2. **H2:** P95 RTT increases more than mean as payload grows
3. **H3:** Loss rate remains constant across payload sizes

### 6.2 Acceptance Criteria

| Metric | Target | Rationale |
|--------|--------|-----------|
| Mean RTT | < 200ms | Real-time control requirement |
| P95 RTT | < 500ms | Worst-case acceptable |
| Loss Rate | < 1% | Reliable delivery |

---

## 7. Directory Structure

```
logger/
├── tools/
│   ├── logger.py           # Benchmark tool
│   ├── analyze_results.py  # Analysis tool
│   └── run_experiments.py  # Experiment runner
├── results/
│   ├── results_case1.csv   # Case 1 raw data
│   ├── results_case2.csv   # Case 2 raw data
│   ├── results_case3.csv   # Case 3 raw data
│   ├── summary.csv         # Aggregated statistics
│   └── histograms/         # Generated plots
│       ├── case1_histogram.png
│       ├── case2_histogram.png
│       └── case3_histogram.png
└── requirements.txt
```

---

## 8. Reporting

### 8.1 Output Files

| File | Format | Content |
|------|--------|---------|
| `results_caseN.csv` | CSV | Raw RTT measurements |
| `summary.csv` | CSV | Aggregated statistics per case |
| `summary.md` | Markdown | Human-readable report |
| `*_histogram.png` | PNG | RTT distribution plots |

### 8.2 Report Template

Generated `summary.md` will include:

1. Experiment metadata (date, host, ESP32 info)
2. Per-case statistics table
3. Comparison analysis
4. Embedded histograms
5. Conclusion (pass/fail against targets)

---

## 9. References

- [SPEC.md](../SPEC.md) — Protocol specification
- [RUNBOOK.md](../RUNBOOK.md) — Setup and execution guide
- [QA_CHECKLIST.md](../QA_CHECKLIST.md) — Verification checklist
