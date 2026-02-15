#!/usr/bin/env python3
"""
Smoke Test - Traffic Light MQTT Demo
Verifies end-to-end system connectivity and command processing.

Usage:
    python smoke_test.py --host 192.168.1.100
    python smoke_test.py --host localhost --timeout 10
    
Exit codes:
    0 = All tests passed
    1 = One or more tests failed
    2 = Connection error
"""

import argparse
import json
import sys
import time
import uuid
from dataclasses import dataclass
from typing import Optional

import paho.mqtt.client as mqtt


@dataclass
class TestResult:
    name: str
    passed: bool
    message: str
    rtt_ms: Optional[float] = None


class SmokeTest:
    def __init__(self, host: str, port: int, user: str, password: str,
                 city: str, intersection: str, timeout: float):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.timeout = timeout
        
        # Topics
        self.topic_cmd = f"city/{city}/intersection/{intersection}/cmd"
        self.topic_ack = f"city/{city}/intersection/{intersection}/ack"
        self.topic_status = f"city/{city}/intersection/{intersection}/status"
        
        # State
        self.connected = False
        self.received_ack = None
        self.received_status = None
        self.waiting_for_cmd_id = None
        
        # Results
        self.results: list[TestResult] = []
        
        # MQTT client
        self.client = mqtt.Client(
            client_id=f"smoke-test-{uuid.uuid4().hex[:8]}",
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2
        )
        self.client.username_pw_set(user, password)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_disconnect = self._on_disconnect
    
    def _on_connect(self, client, userdata, flags, rc, properties=None):
        if rc == 0:
            self.connected = True
            client.subscribe(self.topic_ack, qos=1)
            client.subscribe(self.topic_status, qos=1)
        else:
            self.connected = False
    
    def _on_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode())
            
            if msg.topic == self.topic_ack:
                if payload.get("cmd_id") == self.waiting_for_cmd_id:
                    self.received_ack = payload
            elif msg.topic == self.topic_status:
                self.received_status = payload
                
        except json.JSONDecodeError:
            pass
    
    def _on_disconnect(self, client, userdata, disconnect_flags, rc, properties=None):
        self.connected = False
    
    def _send_command(self, cmd_type: str, **kwargs) -> tuple[bool, Optional[dict], float]:
        """Send command and wait for ack. Returns (success, ack_payload, rtt_ms)."""
        cmd_id = str(uuid.uuid4())
        self.waiting_for_cmd_id = cmd_id
        self.received_ack = None
        
        cmd = {
            "cmd_id": cmd_id,
            "type": cmd_type,
            "ts_ms": int(time.time() * 1000),
            **kwargs
        }
        
        t_send = time.time()
        self.client.publish(self.topic_cmd, json.dumps(cmd), qos=1)
        
        # Wait for ack
        deadline = time.time() + self.timeout
        while self.received_ack is None and time.time() < deadline:
            time.sleep(0.05)
        
        if self.received_ack:
            rtt_ms = (time.time() - t_send) * 1000
            return True, self.received_ack, rtt_ms
        else:
            return False, None, 0
    
    def test_broker_connection(self) -> TestResult:
        """Test 1: Verify broker is reachable."""
        print("  🔌 Testing broker connection...", end=" ", flush=True)
        
        try:
            self.client.connect(self.host, self.port, keepalive=10)
            self.client.loop_start()
            
            # Wait for connection
            deadline = time.time() + self.timeout
            while not self.connected and time.time() < deadline:
                time.sleep(0.1)
            
            if self.connected:
                print("✅ PASS")
                return TestResult("Broker Connection", True, f"Connected to {self.host}:{self.port}")
            else:
                print("❌ FAIL")
                return TestResult("Broker Connection", False, "Connection timeout")
                
        except Exception as e:
            print("❌ FAIL")
            return TestResult("Broker Connection", False, str(e))
    
    def test_set_mode_manual(self) -> TestResult:
        """Test 2: Send SET_MODE MANUAL command."""
        print("  📤 Testing SET_MODE MANUAL...", end=" ", flush=True)
        
        success, ack, rtt = self._send_command("SET_MODE", mode="MANUAL")
        
        if success and ack.get("ok"):
            print(f"✅ PASS (RTT: {rtt:.1f}ms)")
            return TestResult("SET_MODE MANUAL", True, f"Ack received, ok=true", rtt)
        elif success and not ack.get("ok"):
            print(f"❌ FAIL (err: {ack.get('err')})")
            return TestResult("SET_MODE MANUAL", False, f"Ack received, ok=false, err={ack.get('err')}")
        else:
            print("❌ FAIL (timeout)")
            return TestResult("SET_MODE MANUAL", False, "No ack received within timeout")
    
    def test_set_phase_ns_green(self) -> TestResult:
        """Test 3: Send SET_PHASE NS_GREEN command."""
        print("  📤 Testing SET_PHASE 0 (NS_GREEN)...", end=" ", flush=True)
        
        success, ack, rtt = self._send_command("SET_PHASE", phase=0)
        
        if success and ack.get("ok"):
            print(f"✅ PASS (RTT: {rtt:.1f}ms)")
            return TestResult("SET_PHASE NS_GREEN", True, f"Ack received, ok=true", rtt)
        elif success and not ack.get("ok"):
            print(f"❌ FAIL (err: {ack.get('err')})")
            return TestResult("SET_PHASE NS_GREEN", False, f"Ack received, ok=false, err={ack.get('err')}")
        else:
            print("❌ FAIL (timeout)")
            return TestResult("SET_PHASE NS_GREEN", False, "No ack received within timeout")
    
    def test_set_mode_auto(self) -> TestResult:
        """Test 4: Return to AUTO mode (cleanup)."""
        print("  📤 Testing SET_MODE AUTO (cleanup)...", end=" ", flush=True)
        
        success, ack, rtt = self._send_command("SET_MODE", mode="AUTO")
        
        if success and ack.get("ok"):
            print(f"✅ PASS (RTT: {rtt:.1f}ms)")
            return TestResult("SET_MODE AUTO", True, f"Ack received, ok=true", rtt)
        elif success and not ack.get("ok"):
            print(f"⚠️ WARN (err: {ack.get('err')})")
            return TestResult("SET_MODE AUTO", True, f"Cleanup - err={ack.get('err')}")
        else:
            print("⚠️ WARN (timeout)")
            return TestResult("SET_MODE AUTO", True, "Cleanup - no ack (non-critical)")
    
    def run_all(self) -> bool:
        """Run all smoke tests. Returns True if all passed."""
        print("\n" + "=" * 60)
        print("🧪 SMOKE TEST - Traffic Light MQTT Demo")
        print("=" * 60)
        print(f"  Host: {self.host}:{self.port}")
        print(f"  User: {self.user}")
        print(f"  Timeout: {self.timeout}s")
        print("=" * 60 + "\n")
        
        # Test 1: Connection
        result = self.test_broker_connection()
        self.results.append(result)
        
        if not result.passed:
            self._print_summary()
            return False
        
        # Wait a moment for subscriptions
        time.sleep(0.5)
        
        # Test 2: SET_MODE MANUAL
        result = self.test_set_mode_manual()
        self.results.append(result)
        
        # Test 3: SET_PHASE NS_GREEN (only if MANUAL succeeded)
        if result.passed:
            time.sleep(0.2)
            result = self.test_set_phase_ns_green()
            self.results.append(result)
        
        # Test 4: Return to AUTO (cleanup)
        time.sleep(0.2)
        result = self.test_set_mode_auto()
        self.results.append(result)
        
        # Cleanup
        self.client.loop_stop()
        self.client.disconnect()
        
        # Summary
        self._print_summary()
        
        # Check critical tests (first 3)
        critical_passed = all(r.passed for r in self.results[:3])
        return critical_passed
    
    def _print_summary(self):
        """Print test summary."""
        print("\n" + "=" * 60)
        print("📋 SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for r in self.results if r.passed)
        total = len(self.results)
        
        for r in self.results:
            status = "✅" if r.passed else "❌"
            rtt_str = f" ({r.rtt_ms:.1f}ms)" if r.rtt_ms else ""
            print(f"  {status} {r.name}{rtt_str}")
            if not r.passed:
                print(f"      → {r.message}")
        
        print()
        if passed == total:
            print("🎉 ALL TESTS PASSED")
        else:
            print(f"⚠️ {passed}/{total} TESTS PASSED")
        print("=" * 60 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description='Smoke test for Traffic Light MQTT Demo',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exit codes:
  0 = All critical tests passed
  1 = One or more critical tests failed
  2 = Connection/setup error

Examples:
  python smoke_test.py --host 192.168.1.100
  python smoke_test.py --host localhost --timeout 10
        """
    )
    
    parser.add_argument('--host', default='localhost', help='MQTT broker host')
    parser.add_argument('--port', type=int, default=1883, help='MQTT broker port')
    parser.add_argument('--user', default='demo', help='MQTT username')
    parser.add_argument('--password', default='demo_pass', help='MQTT password')
    parser.add_argument('--city', default='demo', help='City ID')
    parser.add_argument('--intersection', default='001', help='Intersection ID')
    parser.add_argument('--timeout', type=float, default=5.0, help='Timeout per test (seconds)')
    
    args = parser.parse_args()
    
    try:
        test = SmokeTest(
            host=args.host,
            port=args.port,
            user=args.user,
            password=args.password,
            city=args.city,
            intersection=args.intersection,
            timeout=args.timeout
        )
        
        success = test.run_all()
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n⚠️ Interrupted by user")
        sys.exit(2)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(2)


if __name__ == "__main__":
    main()
