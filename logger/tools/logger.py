#!/usr/bin/env python3
"""
RTT Benchmark Logger - Traffic Light MQTT Demo
Sends commands and measures round-trip time to acknowledgment.

Usage:
    python logger.py --host 192.168.1.100 --count 100 --mode AUTO --out results.csv
    python logger.py --host 192.168.1.100 --count 500 --phase 0 --interval_ms 100
    python logger.py --host localhost --count 1000 --mode AUTO --pad_bytes 100
"""

import argparse
import csv
import json
import sys
import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Dict, Optional

import paho.mqtt.client as mqtt

# =============================================================================
# DATA STRUCTURES
# =============================================================================

@dataclass
class CommandRecord:
    cmd_id: str
    t_send_ms: int
    t_ack_recv_ms: Optional[int] = None
    rtt_ms: Optional[float] = None
    mode: Optional[str] = None
    phase: Optional[int] = None
    payload_size: int = 0
    actual_payload_bytes: int = 0
    note: str = ""


@dataclass
class BenchmarkState:
    records: Dict[str, CommandRecord] = field(default_factory=dict)
    sent_count: int = 0
    received_count: int = 0
    connected: bool = False
    done: bool = False
    lock: threading.Lock = field(default_factory=threading.Lock)


# =============================================================================
# MQTT CALLBACKS
# =============================================================================

def on_connect(client, userdata, flags, rc, properties=None):
    state: BenchmarkState = userdata['state']
    args = userdata['args']
    
    if rc == 0:
        print(f"✅ Connected to MQTT broker: {args.host}:{args.port}")
        state.connected = True
        
        # Subscribe to ack topic
        ack_topic = f"city/{args.city}/intersection/{args.intersection}/ack"
        client.subscribe(ack_topic, qos=1)
        print(f"📥 Subscribed to: {ack_topic}")
    else:
        print(f"❌ Connection failed with code: {rc}")
        state.connected = False


def on_message(client, userdata, msg):
    state: BenchmarkState = userdata['state']
    t_recv = int(time.time() * 1000)
    
    try:
        payload = json.loads(msg.payload.decode())
        cmd_id = payload.get("cmd_id")
        
        if cmd_id and cmd_id in state.records:
            with state.lock:
                record = state.records[cmd_id]
                record.t_ack_recv_ms = t_recv
                record.rtt_ms = t_recv - record.t_send_ms
                state.received_count += 1
                
                # Log progress every 50 acks
                if state.received_count % 50 == 0:
                    print(f"   Received {state.received_count} acks...")
                    
    except json.JSONDecodeError:
        pass


def on_disconnect(client, userdata, rc, properties=None):
    state: BenchmarkState = userdata['state']
    state.connected = False
    if rc != 0:
        print(f"⚠️ Unexpected disconnect: {rc}")


# =============================================================================
# BENCHMARK LOGIC
# =============================================================================

def build_command(args, pad_bytes: int = 0) -> dict:
    """Build command payload based on args."""
    cmd = {
        "cmd_id": str(uuid.uuid4()),
        "ts_ms": int(time.time() * 1000)
    }
    
    if args.mode:
        cmd["type"] = "SET_MODE"
        cmd["mode"] = args.mode
    elif args.phase is not None:
        cmd["type"] = "SET_PHASE"
        cmd["phase"] = args.phase
    else:
        cmd["type"] = "SET_MODE"
        cmd["mode"] = "AUTO"
    
    # Add padding if requested (for payload size testing)
    if pad_bytes > 0:
        cmd["pad"] = "x" * pad_bytes
    
    return cmd


def run_benchmark(client: mqtt.Client, state: BenchmarkState, args):
    """Run the benchmark sending commands."""
    cmd_topic = f"city/{args.city}/intersection/{args.intersection}/cmd"
    interval_s = args.interval_ms / 1000.0
    
    print(f"\n🚀 Starting benchmark: {args.count} commands, {args.interval_ms}ms interval")
    print(f"📤 Publishing to: {cmd_topic}\n")
    
    for i in range(args.count):
        if not state.connected:
            print("❌ Lost connection, stopping benchmark")
            break
        
        cmd = build_command(args, args.pad_bytes)
        cmd_id = cmd["cmd_id"]
        payload = json.dumps(cmd)
        actual_payload_bytes = len(payload.encode('utf-8'))
        t_send = int(time.time() * 1000)
        
        # Record command
        with state.lock:
            state.records[cmd_id] = CommandRecord(
                cmd_id=cmd_id,
                t_send_ms=t_send,
                mode=cmd.get("mode"),
                phase=cmd.get("phase"),
                payload_size=len(payload),
                actual_payload_bytes=actual_payload_bytes,
                note=cmd["type"]
            )
            state.sent_count += 1
        
        # Publish
        result = client.publish(cmd_topic, payload, qos=1)
        
        # Log progress every 100 commands
        if (i + 1) % 100 == 0:
            print(f"   Sent {i + 1}/{args.count} commands...")
        
        # Wait for interval
        if i < args.count - 1:
            time.sleep(interval_s)
    
    print(f"\n✅ Sent {state.sent_count} commands")
    
    # Wait for remaining acks (with timeout)
    print("⏳ Waiting for remaining acks (max 5s)...")
    wait_start = time.time()
    while state.received_count < state.sent_count and (time.time() - wait_start) < 5.0:
        time.sleep(0.1)
    
    state.done = True


def calculate_statistics(state: BenchmarkState) -> dict:
    """Calculate benchmark statistics."""
    rtts = [r.rtt_ms for r in state.records.values() if r.rtt_ms is not None]
    
    if not rtts:
        return {
            "sent": state.sent_count,
            "received": 0,
            "lost": state.sent_count,
            "loss_rate": 100.0,
            "mean": None,
            "median": None,
            "p95": None,
            "max": None,
            "min": None
        }
    
    rtts.sort()
    n = len(rtts)
    
    return {
        "sent": state.sent_count,
        "received": state.received_count,
        "lost": state.sent_count - state.received_count,
        "loss_rate": ((state.sent_count - state.received_count) / state.sent_count) * 100,
        "mean": sum(rtts) / n,
        "median": rtts[n // 2] if n % 2 == 1 else (rtts[n//2 - 1] + rtts[n//2]) / 2,
        "p95": rtts[int(n * 0.95)] if n > 0 else None,
        "max": max(rtts),
        "min": min(rtts)
    }


def save_csv(state: BenchmarkState, filename: str):
    """Save results to CSV file."""
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['cmd_id', 't_send_ms', 't_ack_recv_ms', 'rtt_ms', 
                        'mode', 'phase', 'payload_size', 'actual_payload_bytes', 'note'])
        
        for record in state.records.values():
            writer.writerow([
                record.cmd_id,
                record.t_send_ms,
                record.t_ack_recv_ms or '',
                record.rtt_ms or '',
                record.mode or '',
                record.phase if record.phase is not None else '',
                record.payload_size,
                record.actual_payload_bytes,
                record.note
            ])
    
    print(f"💾 Results saved to: {filename}")


def print_statistics(stats: dict):
    """Print benchmark statistics."""
    print("\n" + "=" * 50)
    print("📊 BENCHMARK RESULTS")
    print("=" * 50)
    print(f"  Sent:       {stats['sent']}")
    print(f"  Received:   {stats['received']}")
    print(f"  Lost:       {stats['lost']}")
    print(f"  Loss Rate:  {stats['loss_rate']:.2f}%")
    print()
    
    if stats['mean'] is not None:
        print("  RTT Statistics (ms):")
        print(f"    Min:      {stats['min']:.2f}")
        print(f"    Mean:     {stats['mean']:.2f}")
        print(f"    Median:   {stats['median']:.2f}")
        print(f"    P95:      {stats['p95']:.2f}")
        print(f"    Max:      {stats['max']:.2f}")
    else:
        print("  ❌ No RTT data (no acks received)")
    
    print("=" * 50 + "\n")


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='RTT Benchmark Logger for Traffic Light MQTT Demo',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python logger.py --host 192.168.1.100 --count 100 --mode AUTO
  python logger.py --host localhost --count 500 --phase 0 --interval_ms 50
  python logger.py --host 192.168.1.100 --count 1000 --mode MANUAL --pad_bytes 100
        """
    )
    
    # Connection args
    parser.add_argument('--host', default='localhost', help='MQTT broker host')
    parser.add_argument('--port', type=int, default=1883, help='MQTT broker port')
    parser.add_argument('--user', default='demo', help='MQTT username')
    parser.add_argument('--password', default='demo_pass', help='MQTT password')
    
    # Topic args
    parser.add_argument('--city', default='demo', help='City ID for topic')
    parser.add_argument('--intersection', default='001', help='Intersection ID for topic')
    
    # Benchmark args
    parser.add_argument('--count', type=int, default=100, help='Number of commands to send')
    parser.add_argument('--interval_ms', type=int, default=100, help='Interval between commands (ms)')
    
    # Command args (mutually exclusive)
    parser.add_argument('--mode', choices=['AUTO', 'MANUAL', 'BLINK', 'OFF'], 
                        help='Send SET_MODE command')
    parser.add_argument('--phase', type=int, choices=[0, 1, 2, 3, 4, 5],
                        help='Send SET_PHASE command (0=NS_GREEN, 3=EW_GREEN, 2=ALL_RED)')
    
    # Payload args
    parser.add_argument('--pad_bytes', type=int, default=0, 
                        help='Add padding bytes to payload')
    
    # Output args
    parser.add_argument('--out', default='results.csv', help='Output CSV filename')
    
    args = parser.parse_args()
    
    # Print configuration
    print("\n" + "=" * 50)
    print("🚦 RTT BENCHMARK LOGGER")
    print("=" * 50)
    print(f"  Host:       {args.host}:{args.port}")
    print(f"  User:       {args.user}")
    print(f"  City:       {args.city}")
    print(f"  Intersect:  {args.intersection}")
    print(f"  Count:      {args.count}")
    print(f"  Interval:   {args.interval_ms}ms")
    if args.mode:
        print(f"  Command:    SET_MODE {args.mode}")
    elif args.phase is not None:
        print(f"  Command:    SET_PHASE {args.phase}")
    else:
        print(f"  Command:    SET_MODE AUTO (default)")
    if args.pad_bytes > 0:
        print(f"  Padding:    {args.pad_bytes} bytes")
    print(f"  Output:     {args.out}")
    print("=" * 50 + "\n")
    
    # Initialize state
    state = BenchmarkState()
    userdata = {'state': state, 'args': args}
    
    # Create MQTT client
    client = mqtt.Client(
        client_id=f"rtt-logger-{uuid.uuid4().hex[:8]}",
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        userdata=userdata
    )
    client.username_pw_set(args.user, args.password)
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    
    # Connect
    try:
        print(f"🔌 Connecting to {args.host}:{args.port}...")
        client.connect(args.host, args.port, keepalive=60)
        client.loop_start()
        
        # Wait for connection
        timeout = 5.0
        start = time.time()
        while not state.connected and (time.time() - start) < timeout:
            time.sleep(0.1)
        
        if not state.connected:
            print("❌ Connection timeout")
            sys.exit(1)
        
        # Run benchmark
        run_benchmark(client, state, args)
        
        # Calculate and print statistics
        stats = calculate_statistics(state)
        print_statistics(stats)
        
        # Save CSV
        save_csv(state, args.out)
        
    except KeyboardInterrupt:
        print("\n⚠️ Interrupted by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    finally:
        client.loop_stop()
        client.disconnect()
        print("👋 Disconnected from broker")


if __name__ == "__main__":
    main()
