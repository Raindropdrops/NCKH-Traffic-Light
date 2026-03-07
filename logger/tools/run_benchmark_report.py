#!/usr/bin/env python3
"""
RTT Benchmark Report Generator - Traffic Light MQTT Demo
Runs multiple benchmark cases, analyzes results, generates plots and report.

Usage:
    python run_benchmark_report.py --host 127.0.0.1
    python run_benchmark_report.py --host 192.168.1.100 --cases "0,256,1024" --count 500
"""

import argparse
import csv
import json
import os
import subprocess
import sys
import time
import uuid
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Optional

import paho.mqtt.client as mqtt

# Optional imports for analysis and plotting
try:
    import numpy as np
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

try:
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False


# =============================================================================
# DATA STRUCTURES
# =============================================================================

def configure_console_output():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

@dataclass
class BenchmarkCase:
    name: str
    pad_bytes: int
    count: int
    interval_ms: int
    description: str
    expected_reject: bool = False


@dataclass
class CaseResult:
    case: BenchmarkCase
    csv_file: str
    sent: int
    received: int
    lost: int
    loss_rate: float
    mean: Optional[float]
    median: Optional[float]
    std: Optional[float]
    min_rtt: Optional[float]
    max_rtt: Optional[float]
    p50: Optional[float]
    p75: Optional[float]
    p90: Optional[float]
    p95: Optional[float]
    p99: Optional[float]
    outlier_count: int
    rtts: List[float]
    payload_bytes_min: int
    payload_bytes_max: int
    payload_bytes_mean: float
    status: str
    reason: str
    # One-Way Latencies
    mean_edge_lat: Optional[float]
    mean_ret_lat: Optional[float]


# =============================================================================
# MQTT BENCHMARK RUNNER
# =============================================================================

class RTTBenchmark:
    def __init__(self, host: str, port: int, user: str, password: str,
                 city: str = "demo", intersection: str = "001"):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        
        self.topic_cmd = f"city/{city}/intersection/{intersection}/cmd"
        self.topic_ack = f"city/{city}/intersection/{intersection}/ack"
        
        self.records = {}
        self.received_count = 0
        self.connected = False
        
        self.client = mqtt.Client(
            client_id=f"bench-{uuid.uuid4().hex[:8]}",
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2
        )
        self.client.username_pw_set(user, password)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
    
    def _on_connect(self, client, userdata, flags, rc, properties=None):
        if rc == 0:
            self.connected = True
            client.subscribe(self.topic_ack, qos=1)
    
    def _on_message(self, client, userdata, msg):
        t_recv = int(time.time() * 1000)
        try:
            payload = json.loads(msg.payload.decode())
            cmd_id = payload.get("cmd_id")
            if cmd_id and cmd_id in self.records:
                t_send = self.records[cmd_id]["t_send_ms"]
                self.records[cmd_id]["t_ack_recv_ms"] = t_recv
                self.records[cmd_id]["rtt_ms"] = t_recv - t_send
                
                # Check for one-way latency (only works if edge sends epoch ms, not uptime)
                edge_ts = payload.get("edge_recv_ts_ms", 0)
                if edge_ts > 1600000000000: # Valid Epoch MS
                    self.records[cmd_id]["edge_lat_ms"] = edge_ts - t_send
                    self.records[cmd_id]["ret_lat_ms"] = t_recv - edge_ts
                else:
                    self.records[cmd_id]["edge_lat_ms"] = None
                    self.records[cmd_id]["ret_lat_ms"] = None
                    
                self.received_count += 1
        except:
            pass
    
    def run(self, case: BenchmarkCase, output_csv: str) -> Optional[CaseResult]:
        """Run benchmark for a single case."""
        print(f"\n{'='*60}")
        print(f"📊 Running: {case.name}")
        print(f"   Payload: {case.pad_bytes} bytes, Count: {case.count}, Interval: {case.interval_ms}ms")
        print(f"{'='*60}")
        
        self.records = {}
        self.received_count = 0
        self.connected = False
        
        try:
            self.client.connect(self.host, self.port, keepalive=60)
            self.client.loop_start()
            
            # Wait for connection
            timeout = 5.0
            start = time.time()
            while not self.connected and (time.time() - start) < timeout:
                time.sleep(0.1)
            
            if not self.connected:
                print("❌ Connection failed")
                return None
            
            print(f"✅ Connected. Sending {case.count} commands...")
            
            # Send commands
            interval_s = case.interval_ms / 1000.0
            for i in range(case.count):
                cmd_id = str(uuid.uuid4())
                cmd = {
                    "cmd_id": cmd_id,
                    "type": "SET_MODE",
                    "mode": "AUTO",
                    "ts_ms": int(time.time() * 1000)
                }
                if case.pad_bytes > 0:
                    cmd["pad"] = "x" * case.pad_bytes
                
                payload_json = json.dumps(cmd)
                actual_payload_bytes = len(payload_json.encode('utf-8'))
                t_send = int(time.time() * 1000)
                self.records[cmd_id] = {
                    "cmd_id": cmd_id,
                    "t_send_ms": t_send,
                    "t_ack_recv_ms": None,
                    "rtt_ms": None,
                    "edge_lat_ms": None,
                    "ret_lat_ms": None,
                    "payload_size": len(payload_json),
                    "actual_payload_bytes": actual_payload_bytes,
                    "mode": "AUTO",
                    "phase": None,
                    "note": case.name
                }
                
                self.client.publish(self.topic_cmd, payload_json, qos=1)
                
                if (i + 1) % 100 == 0:
                    print(f"   Sent {i+1}/{case.count}...")
                
                if i < case.count - 1:
                    time.sleep(interval_s)
            
            # Wait for remaining acks
            print("⏳ Waiting for acks...")
            wait_start = time.time()
            while self.received_count < len(self.records) and (time.time() - wait_start) < 10.0:
                time.sleep(0.1)
            
            print(f"✅ Received {self.received_count}/{len(self.records)} acks")
            
        finally:
            self.client.loop_stop()
            self.client.disconnect()
        
        # Save CSV
        self._save_csv(output_csv)
        
        # Analyze results
        return self._analyze(case, output_csv)
    
    def _save_csv(self, filename: str):
        """Save results to CSV."""
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['cmd_id', 't_send_ms', 't_ack_recv_ms', 'rtt_ms', 'edge_lat_ms', 'ret_lat_ms',
                           'payload_size', 'actual_payload_bytes', 'mode', 'phase', 'note'])
            for r in self.records.values():
                writer.writerow([
                    r["cmd_id"], r["t_send_ms"], r["t_ack_recv_ms"] or '',
                    r["rtt_ms"] or '', r.get("edge_lat_ms", '') or '', r.get("ret_lat_ms", '') or '',
                    r["payload_size"], r.get("actual_payload_bytes", ''), r["mode"],
                    r["phase"] or '', r["note"]
                ])
        print(f"💾 Saved: {filename}")
    
    def _analyze(self, case: BenchmarkCase, csv_file: str) -> CaseResult:
        """Analyze benchmark results."""
        rtts = [r["rtt_ms"] for r in self.records.values() if r["rtt_ms"] is not None]
        payload_bytes = [r.get("actual_payload_bytes", 0) for r in self.records.values()]
        payload_min = min(payload_bytes) if payload_bytes else 0
        payload_max = max(payload_bytes) if payload_bytes else 0
        payload_mean = (sum(payload_bytes) / len(payload_bytes)) if payload_bytes else 0.0
        
        if not rtts:
            status = "PASS" if case.expected_reject else "FAIL"
            reason = "Expected reject/no-ack (oversize)" if case.expected_reject else "Timeout/no-ack"
            return CaseResult(
                case=case, csv_file=csv_file, sent=len(self.records),
                received=0, lost=len(self.records), loss_rate=100.0,
                mean=None, median=None, std=None, min_rtt=None, max_rtt=None,
                p50=None, p75=None, p90=None, p95=None, p99=None, outlier_count=0, rtts=[],
                payload_bytes_min=payload_min, payload_bytes_max=payload_max, payload_bytes_mean=payload_mean,
                status=status, reason=reason, mean_edge_lat=None, mean_ret_lat=None
            )
        
        rtts.sort()
        n = len(rtts)
        
        mean = sum(rtts) / n
        median = rtts[n // 2] if n % 2 == 1 else (rtts[n//2 - 1] + rtts[n//2]) / 2
        
        variance = sum((x - mean) ** 2 for x in rtts) / n
        std = variance ** 0.5
        
        def percentile(data, p):
            idx = int(len(data) * p)
            return data[min(idx, len(data) - 1)]
        
        p95 = percentile(rtts, 0.95)
        
        # Outlier rule: RTT > p95*2 OR RTT > median + 3*std
        outlier_threshold = min(p95 * 2, median + 3 * std)
        outlier_count = sum(1 for r in rtts if r > outlier_threshold)
        
        status = "PASS"
        reason = ""
        if case.expected_reject:
            status = "FAIL"
            reason = "Unexpected ack for oversize payload"
        elif ((len(self.records) - self.received_count) / len(self.records)) * 100 >= 1:
            status = "FAIL"
            reason = "Loss >= 1%"
        return CaseResult(
            case=case,
            csv_file=csv_file,
            sent=len(self.records),
            received=self.received_count,
            lost=len(self.records) - self.received_count,
            loss_rate=((len(self.records) - self.received_count) / len(self.records)) * 100,
            mean=mean,
            median=median,
            std=std,
            min_rtt=min(rtts),
            max_rtt=max(rtts),
            p50=percentile(rtts, 0.50),
            p75=percentile(rtts, 0.75),
            p90=percentile(rtts, 0.90),
            p95=p95,
            p99=percentile(rtts, 0.99),
            outlier_count=outlier_count,
            rtts=rtts,
            payload_bytes_min=payload_min,
            payload_bytes_max=payload_max,
            payload_bytes_mean=payload_mean,
            status=status,
            reason=reason
        )


# =============================================================================
# PLOTTING
# =============================================================================

def generate_plots(results: List[CaseResult], plots_dir: str):
    """Generate all plots."""
    if not HAS_MATPLOTLIB:
        print("⚠️ matplotlib not installed. Skipping plots.")
        return
    
    valid_results = [r for r in results if r.rtts]
    chart_results = [
        r for r in valid_results
        if r.p50 is not None and r.p95 is not None and r.max_rtt is not None
    ]
    os.makedirs(plots_dir, exist_ok=True)
    
    # 1. Histogram for each case
    for r in valid_results:
        if not r.rtts:
            continue
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(r.rtts, bins=50, edgecolor='black', alpha=0.7, color='steelblue')
        mean_val = r.mean if r.mean is not None else 0.0
        p95_val = r.p95 if r.p95 is not None else 0.0
        ax.axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_val:.1f}ms')
        ax.axvline(p95_val, color='orange', linestyle='--', linewidth=2, label=f'P95: {p95_val:.1f}ms')
        ax.set_xlabel('RTT (ms)')
        ax.set_ylabel('Frequency')
        ax.set_title(f'RTT Distribution - {r.case.name}\n(n={len(r.rtts)}, payload={r.case.pad_bytes}B)')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        filename = os.path.join(plots_dir, f"histogram_{r.case.name.lower().replace(' ', '_')}.png")
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        plt.close()
        print(f"📊 Saved: {filename}")
    
    # 2. Comparison bar chart
    if len(chart_results) > 1:
        fig, ax = plt.subplots(figsize=(12, 6))
        
        names = [r.case.name for r in chart_results]
        x = range(len(names))
        width = 0.25
        
        p50s = [float(r.p50) for r in chart_results]
        p95s = [float(r.p95) for r in chart_results]
        maxs = [float(r.max_rtt) for r in chart_results]
        
        bars1 = ax.bar([i - width for i in x], p50s, width, label='P50 (Median)', color='#2196F3')
        bars2 = ax.bar(x, p95s, width, label='P95', color='#FF9800')
        bars3 = ax.bar([i + width for i in x], maxs, width, label='Max', color='#f44336')
        
        ax.set_xlabel('Test Case')
        ax.set_ylabel('RTT (ms)')
        ax.set_title('RTT Comparison Across Test Cases')
        ax.set_xticks(x)
        ax.set_xticklabels(names)
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        
        # Add value labels
        for bars in [bars1, bars2, bars3]:
            for bar in bars:
                height = bar.get_height()
                ax.annotate(f'{height:.0f}',
                           xy=(bar.get_x() + bar.get_width() / 2, height),
                           xytext=(0, 3), textcoords="offset points",
                           ha='center', va='bottom', fontsize=8)
        
        filename = os.path.join(plots_dir, "comparison_chart.png")
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        plt.close()
        print(f"📊 Saved: {filename}")
    
    # 3. ECDF plot
    if len(valid_results) >= 2:
        fig, ax = plt.subplots(figsize=(10, 6))
        
        colors = ['#2196F3', '#4CAF50', '#FF9800', '#f44336']
        for i, r in enumerate(valid_results):
            if not r.rtts:
                continue
            sorted_rtts = sorted(r.rtts)
            ecdf = [(j + 1) / len(sorted_rtts) for j in range(len(sorted_rtts))]
            ax.plot(sorted_rtts, ecdf, label=f'{r.case.name} (n={len(r.rtts)})', 
                   color=colors[i % len(colors)], linewidth=2)
        
        ax.set_xlabel('RTT (ms)')
        ax.set_ylabel('Cumulative Probability')
        ax.set_title('Empirical CDF of RTT')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, 1.05)
        
        filename = os.path.join(plots_dir, "ecdf_comparison.png")
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        plt.close()
        print(f"📊 Saved: {filename}")


# =============================================================================
# REPORT GENERATION
# =============================================================================

def generate_summary_csv(results: List[CaseResult], output_file: str):
    """Generate summary CSV."""
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    def csv_metric(value: Optional[float]) -> str:
        return "NA" if value is None else f"{value:.2f}"

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['case', 'pad_bytes', 'count', 'interval_ms', 
                        'sent', 'received', 'lost', 'loss_rate',
                        'mean', 'median', 'std', 'min', 'max',
                        'p50', 'p75', 'p90', 'p95', 'p99', 'outliers',
                        'payload_bytes_min', 'payload_bytes_max', 'payload_bytes_mean',
                        'status', 'reason'])
        for r in results:
            writer.writerow([
                r.case.name, r.case.pad_bytes, r.case.count, r.case.interval_ms,
                r.sent, r.received, r.lost, f"{r.loss_rate:.2f}",
                csv_metric(r.mean), csv_metric(r.median), csv_metric(r.std),
                csv_metric(r.min_rtt), csv_metric(r.max_rtt),
                csv_metric(r.p50), csv_metric(r.p75), csv_metric(r.p90),
                csv_metric(r.p95), csv_metric(r.p99), r.outlier_count,
                r.payload_bytes_min, r.payload_bytes_max, f"{r.payload_bytes_mean:.2f}",
                r.status, r.reason
            ])
    print(f"💾 Saved: {output_file}")


def generate_report(results: List[CaseResult], output_file: str, plots_dir: str):
    """Generate Markdown report."""
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def md_metric(value: Optional[float]) -> str:
        return "N/A" if value is None else f"{value:.1f}"
    
    report = f"""# 📊 Báo Cáo Đo Độ Trễ RTT — MQTT Traffic Light Demo

> **Ngày tạo:** {timestamp}
> **Đề tài NCKH:** Giám sát và điều khiển đèn giao thông qua IoT–MQTT

---

## 1. Mục Tiêu

Đánh giá hiệu suất truyền thông MQTT giữa Dashboard (Node-RED) và Edge Device (ESP32/Mock) thông qua phép đo **Round-Trip Time (RTT)** từ lúc gửi command đến khi nhận acknowledgment.

## 2. Setup Thí Nghiệm

| Thành phần | Cấu hình |
|------------|----------|
| Broker | Mosquitto 2.x (Docker, localhost:1883) |
| Edge Device | mock_esp32.py (Python simulator) |
| QoS cmd/ack | QoS 1 (at-least-once) |
| Topic cmd | `city/demo/intersection/001/cmd` |
| Topic ack | `city/demo/intersection/001/ack` |

### Định nghĩa RTT

```
RTT = t_ack_recv - t_cmd_send (milliseconds)
```

- `t_cmd_send`: Thời điểm Dashboard publish command
- `t_ack_recv`: Thời điểm Dashboard nhận được ack từ Edge

## 3. Các Case Thí Nghiệm

| Case | Payload pad (bytes) | Actual payload bytes (avg) | Count | Interval (ms) | Mô tả |
|------|----------------------|----------------------------|-------|---------------|-------|
"""

    for r in results:
        report += f"| {r.case.name} | {r.case.pad_bytes} | {r.payload_bytes_mean:.1f} | {r.case.count} | {r.case.interval_ms} | {r.case.description} |\n"

    report += """
## 4. Kết Quả Tổng Hợp

| Case | Sent | Recv | Loss% | Mean (ms) | Median | P95 | P99 | Max | Status | Lý do |
|------|------|------|-------|-----------|--------|-----|-----|-----|--------|------|
"""

    for r in results:
        report += (
            f"| {r.case.name} | {r.sent} | {r.received} | {r.loss_rate:.1f}% | "
            f"{md_metric(r.mean)} | {md_metric(r.median)} | {md_metric(r.p95)} | {md_metric(r.p99)} | {md_metric(r.max_rtt)} | "
            f"{r.status} | {r.reason or '-'} |\n"
        )

    report += """
### Quy tắc phát hiện Outlier

```
outlier_threshold = min(P95 × 2, Median + 3×Std)
```

## 5. Biểu Đồ

"""

    # Add plot references
    for r in results:
        plot_name = f"histogram_{r.case.name.lower().replace(' ', '_')}.png"
        report += f"### {r.case.name}\n\n"
        report += f"![RTT Histogram - {r.case.name}](plots/{plot_name})\n\n"

    report += """### So sánh giữa các Case

![Comparison Chart](plots/comparison_chart.png)

### ECDF

![ECDF Comparison](plots/ecdf_comparison.png)

## 6. Nhận Xét

### Xu hướng theo Payload Size

"""

    # Analyze trend
    valid_results = [r for r in results if r.received > 0 and r.mean is not None]
    if len(valid_results) >= 2:
        r0 = valid_results[0]
        r_last = valid_results[-1]
        base_mean = float(r0.mean) if r0.mean is not None else 0.0
        last_mean = float(r_last.mean) if r_last.mean is not None else 0.0
        mean_increase = ((last_mean - base_mean) / base_mean) * 100 if base_mean > 0 else 0
        
        report += f"- Payload tăng từ {r0.case.pad_bytes}B → {r_last.case.pad_bytes}B\n"
        report += f"- RTT mean: {base_mean:.1f}ms → {last_mean:.1f}ms "
        
        if mean_increase > 10:
            report += f"(↑ {mean_increase:.1f}% — tăng đáng kể)\n"
        elif mean_increase > 0:
            report += f"(↑ {mean_increase:.1f}% — tăng nhẹ)\n"
        else:
            report += "(không đổi hoặc giảm)\n"
    else:
        report += "- Không đủ case có ack để kết luận xu hướng RTT theo payload\n"
    
    # Loss rate and oversize notes
    if any(r.loss_rate > 0 for r in results):
        report += f"- Có packet loss: {', '.join(f'{r.case.name}={r.loss_rate:.1f}%' for r in results if r.loss_rate > 0)}\n"
    else:
        report += "- Không có packet loss (0% loss rate)\n"
    
    oversize_cases = [r for r in results if r.case.expected_reject]
    if oversize_cases:
        for r in oversize_cases:
            report += f"- {r.case.name}: payload oversize → không đo RTT vì không có ack (expected)\n"
    no_ack_cases = [r for r in results if r.received == 0 and not r.case.expected_reject]
    if no_ack_cases:
        for r in no_ack_cases:
            report += f"- {r.case.name}: timeout/no-ack → không đủ dữ liệu RTT (FAIL)\n"

    report += """
### Hạn chế khi dùng Mock ESP32

> ⚠️ **Lưu ý quan trọng**

- Mock chạy trên cùng máy với Broker → RTT không phản ánh độ trễ mạng thực
- Không có độ trễ WiFi, xử lý phần cứng, interrupt...
- Kết quả chỉ đo overhead của MQTT protocol + JSON parse

**Kế hoạch:** Lặp lại thí nghiệm với ESP32 thật qua WiFi để có số liệu thực tế.

## 7. Gợi Ý Mở Rộng Đô Thị

| Giải pháp | Mô tả | Trade-off |
|-----------|-------|-----------|
| **Broker Bridge** | Mosquitto bridge giữa các khu vực | Tăng độ trễ inter-region, giảm tải broker trung tâm |
| **Broker Cluster** | Multiple broker với load balancing | Phức tạp hóa infrastructure, cần sticky sessions |
| **QoS Trade-off** | QoS 0 cho state (high-freq), QoS 1 cho cmd/ack | Mất state acceptable, mất cmd không acceptable |
| **TLS/mTLS** | Encryption + mutual authentication | Thêm ~5-20ms handshake, tăng CPU |

## 8. Raw Data

"""

    for r in results:
        report += f"- [{r.case.name}](raw/{os.path.basename(r.csv_file)})\n"

    report += """
---

> 📝 Báo cáo được tạo tự động bởi `run_benchmark_report.py`
"""

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"📝 Saved: {output_file}")


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='RTT Benchmark Report Generator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_benchmark_report.py --host 127.0.0.1
  python run_benchmark_report.py --host 192.168.1.100 --cases "0,256,1024" --count 500
        """
    )
    
    parser.add_argument('--host', default='127.0.0.1', help='MQTT broker host')
    parser.add_argument('--port', type=int, default=1883, help='MQTT broker port')
    parser.add_argument('--user', default='demo', help='MQTT username')
    parser.add_argument('--password', default='demo_pass', help='MQTT password')
    parser.add_argument('--count', type=int, default=500, help='Commands per case')
    parser.add_argument('--interval_ms', type=int, default=200, help='Interval between commands (ms)')
    parser.add_argument('--cases', default='0,256,512,900', help='Comma-separated pad_bytes values (latency cases)')
    parser.add_argument('--oversize', type=int, default=1200, help='Oversize pad_bytes for edge-case (<=0 to skip)')
    parser.add_argument('--outdir', default=None, help='Output directory')
    
    args = parser.parse_args()
    configure_console_output()
    
    # Parse cases
    try:
        pad_bytes_list = [int(x.strip()) for x in args.cases.split(',')]
    except ValueError:
        print("❌ Invalid --cases format. Use comma-separated integers.")
        sys.exit(1)
    
    # Create output directory
    if args.outdir:
        outdir = args.outdir
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        outdir = f"results/bench_{timestamp}"
    
    raw_dir = os.path.join(outdir, "raw")
    plots_dir = os.path.join(outdir, "plots")
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(plots_dir, exist_ok=True)
    
    print("\n" + "=" * 70)
    print("🚀 RTT BENCHMARK REPORT GENERATOR")
    print("=" * 70)
    print(f"  Host: {args.host}:{args.port}")
    print(f"  Cases: {pad_bytes_list}")
    print(f"  Count: {args.count}, Interval: {args.interval_ms}ms")
    print(f"  Output: {outdir}")
    print("=" * 70)
    
    # Define cases
    cases = []
    for i, pad in enumerate(pad_bytes_list):
        case_name = f"Case {i+1}"
        desc = "Baseline" if pad == 0 else f"Payload +{pad}B (<=1KB expected)"
        cases.append(BenchmarkCase(
            name=case_name,
            pad_bytes=pad,
            count=args.count,
            interval_ms=args.interval_ms,
            description=desc,
            expected_reject=False
        ))
    if args.oversize and args.oversize > 0:
        case_name = f"Case {len(cases) + 1}"
        cases.append(BenchmarkCase(
            name=case_name,
            pad_bytes=args.oversize,
            count=args.count,
            interval_ms=args.interval_ms,
            description=f"Oversize payload +{args.oversize}B (expected reject/no-ack)",
            expected_reject=True
        ))
    
    # Run benchmarks
    benchmark = RTTBenchmark(args.host, args.port, args.user, args.password)
    results = []
    
    for case in cases:
        csv_file = os.path.join(raw_dir, f"case_{case.pad_bytes}b.csv")
        result = benchmark.run(case, csv_file)
        if result:
            results.append(result)
        else:
            print(f"⚠️ Case {case.name} failed, skipping...")
        
        # Brief pause between cases
        time.sleep(1)
    
    if not results:
        print("❌ All cases failed. Check broker/edge connectivity.")
        sys.exit(1)
    
    # Generate outputs
    print("\n" + "=" * 70)
    print("📊 GENERATING REPORTS")
    print("=" * 70)
    
    generate_summary_csv(results, os.path.join(outdir, "summary.csv"))
    generate_plots(results, plots_dir)
    generate_report(results, os.path.join(outdir, "report.md"), plots_dir)
    
    # Print summary
    print("\n" + "=" * 70)
    print("✅ BENCHMARK COMPLETE")
    print("=" * 70)
    print(f"  Output directory: {outdir}")
    print(f"  Raw CSV files:    {len(results)}")
    print(f"  Summary:          {outdir}/summary.csv")
    print(f"  Report:           {outdir}/report.md")
    print(f"  Plots:            {plots_dir}/")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
