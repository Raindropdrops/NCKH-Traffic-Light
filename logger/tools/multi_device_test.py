#!/usr/bin/env python3
"""
Multi-Device Stress Test for Traffic Light MQTT Demo
Runs two instance of mock_esp32.py simultaneously and sends concurrent benchmarks.
"""
import subprocess
import time
import sys
import threading
from run_benchmark_report import RTTBenchmark, BenchmarkCase

def run_mock(intersection, speed):
    print(f"Starting MOCK ESP32 for intersection {intersection}...")
    return subprocess.Popen(
        ["python", "mock_esp32.py", "--host", "127.0.0.1", "--intersection", intersection, "--speed", str(speed)],
        cwd="."
    )

def run_bench(intersection, cases_prefix):
    print(f"\n--- Running Benchmark for intersection {intersection} ---")
    bench = RTTBenchmark("127.0.0.1", 1883, "demo", "demo_pass", "demo", intersection)
    if bench.client:
        case = BenchmarkCase(f"{cases_prefix}_load", 256, 100, 50, f"Concurrent load {intersection}")
        bench.run(case, f"results/multi_{intersection}.csv")

def main():
    print("Multi-Device Stress Test Started")
    p1 = run_mock("001", 1.0)
    p2 = run_mock("002", 1.0)
    
    time.sleep(2) # wait for connect
    
    t1 = threading.Thread(target=run_bench, args=("001", "dev1"))
    t2 = threading.Thread(target=run_bench, args=("002", "dev2"))
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()
    
    print("\nBenchmark finished. Terminating mock instances...")
    p1.terminate()
    p2.terminate()
    p1.wait()
    p2.wait()
    print("Stress test complete.")

if __name__ == "__main__":
    main()
