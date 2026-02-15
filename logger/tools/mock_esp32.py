#!/usr/bin/env python3
"""
Mock ESP32 Traffic Light Controller
Simulates ESP32 behavior for testing without hardware.

Features:
- Connects to MQTT broker with LWT (offline status)
- Publishes ONLINE status on connect
- Subscribes to cmd topic and responds with ack
- Publishes state periodically (1s interval)
- Idempotent command handling (deduplicates cmd_id)
- Optional ack delay for RTT testing

Usage:
    python mock_esp32.py --host localhost
    python mock_esp32.py --host 192.168.1.100 --ack_delay_ms 50
"""

import argparse
import json
import signal
import sys
import threading
import time
import uuid
from collections import deque

import paho.mqtt.client as mqtt


class MockESP32:
    def __init__(self, host: str, port: int, user: str, password: str,
                 city: str, intersection: str, ack_delay_ms: int = 0):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.ack_delay_ms = ack_delay_ms
        
        # Topics
        base = f"city/{city}/intersection/{intersection}"
        self.topic_state = f"{base}/state"
        self.topic_cmd = f"{base}/cmd"
        self.topic_ack = f"{base}/ack"
        self.topic_status = f"{base}/status"
        self.topic_telemetry = f"{base}/telemetry"
        
        # State
        self.mode = "AUTO"
        self.phase = 0
        self.phase_start = time.time()
        self.start_time = time.time()
        self.connected = False
        self.running = True
        self.blink_on = False
        
        # AUTO cycle timing (ms)
        self.phase_durations = [10000, 3000, 2000, 10000, 3000, 2000]  # NS_G, NS_Y, AR, EW_G, EW_Y, AR
        
        # Idempotency - cache last 32 cmd_ids
        self.cmd_id_cache = deque(maxlen=32)
        
        # MQTT client
        self.client = mqtt.Client(
            client_id=f"mock-esp32-{uuid.uuid4().hex[:8]}",
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2
        )
        self.client.username_pw_set(user, password)
        
        # LWT (Last Will Testament) - offline status
        lwt_payload = json.dumps({"online": False})
        self.client.will_set(self.topic_status, lwt_payload, qos=1, retain=True)
        
        # Callbacks
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_disconnect = self._on_disconnect
    
    def _on_connect(self, client, userdata, flags, rc, properties=None):
        if rc == 0:
            self.connected = True
            print(f"✅ Connected to MQTT broker: {self.host}:{self.port}")
            
            # Subscribe to cmd topic
            client.subscribe(self.topic_cmd, qos=1)
            print(f"📥 Subscribed to: {self.topic_cmd}")
            
            # Publish ONLINE status (retained)
            self._publish_status(online=True)
        else:
            print(f"❌ Connection failed with code: {rc}")
    
    def _on_message(self, client, userdata, msg):
        print(f"\n📨 Received: {msg.topic}")
        
        try:
            payload = json.loads(msg.payload.decode())
            print(f"   Payload: {json.dumps(payload, indent=2)}")
        except json.JSONDecodeError:
            print("   ❌ Invalid JSON")
            return
        
        # Check required field
        cmd_id = payload.get("cmd_id")
        if not cmd_id:
            print("   ❌ Missing cmd_id")
            self._publish_ack(None, ok=False, err="ERR_INVALID_CMD")
            return
        
        # Idempotency check
        if cmd_id in self.cmd_id_cache:
            print(f"   ⚠️ Duplicate cmd_id, acking without re-execution")
            self._publish_ack(cmd_id, ok=True)
            return
        
        # Process command
        self._handle_command(payload)
    
    def _on_disconnect(self, client, userdata, rc, properties=None):
        self.connected = False
        if rc != 0:
            print(f"⚠️ Unexpected disconnect: {rc}")
    
    def _handle_command(self, payload: dict):
        cmd_id = payload["cmd_id"]
        cmd_type = payload.get("type", "")
        
        ok = False
        err = None
        
        if cmd_type == "SET_MODE":
            mode = payload.get("mode", "")
            if mode in ["AUTO", "MANUAL", "BLINK", "OFF"]:
                self.mode = mode
                self.phase_start = time.time()
                ok = True
                print(f"   ✅ Mode changed to: {self.mode}")
            else:
                err = "ERR_INVALID_MODE"
                print(f"   ❌ Invalid mode: {mode}")
                
        elif cmd_type == "SET_PHASE":
            if self.mode != "MANUAL":
                err = "ERR_NOT_MANUAL_MODE"
                print(f"   ❌ SET_PHASE rejected: not in MANUAL mode")
            else:
                phase = payload.get("phase")
                if isinstance(phase, int) and 0 <= phase <= 5:
                    self.phase = phase
                    self.phase_start = time.time()
                    ok = True
                    print(f"   ✅ Phase set to: {self.phase}")
                else:
                    err = "ERR_INVALID_PHASE"
                    print(f"   ❌ Invalid phase: {phase}")
                    
        elif cmd_type == "EMERGENCY":
            self.mode = "BLINK"
            self.phase = 2  # ALL_RED
            self.phase_start = time.time()
            ok = True
            print(f"   ✅ EMERGENCY activated: BLINK mode")
            
        else:
            err = "ERR_UNKNOWN_TYPE"
            print(f"   ❌ Unknown command type: {cmd_type}")
        
        # Cache cmd_id
        self.cmd_id_cache.append(cmd_id)
        
        # Optional delay
        if self.ack_delay_ms > 0:
            time.sleep(self.ack_delay_ms / 1000.0)
        
        # Publish ack
        self._publish_ack(cmd_id, ok, err)
        
        # Publish updated state
        self._publish_state()
    
    def _publish_status(self, online: bool):
        payload = {
            "online": online,
            "ts_ms": int(time.time() * 1000)
        }
        self.client.publish(self.topic_status, json.dumps(payload), qos=1, retain=True)
        print(f"📤 Published status: online={online}")
    
    def _publish_ack(self, cmd_id: str, ok: bool, err: str = None):
        payload = {
            "cmd_id": cmd_id,
            "ok": ok,
            "err": err,
            "edge_recv_ts_ms": int(time.time() * 1000)
        }
        self.client.publish(self.topic_ack, json.dumps(payload), qos=1)
        status = "✅" if ok else "❌"
        print(f"📤 Published ack: {status} cmd_id={cmd_id[:8]}...")
    
    def _publish_state(self):
        payload = {
            "mode": self.mode,
            "phase": self.phase,
            "since_ms": int((time.time() - self.phase_start) * 1000),
            "uptime_s": int(time.time() - self.start_time),
            "ts_ms": int(time.time() * 1000)
        }
        self.client.publish(self.topic_state, json.dumps(payload), qos=0)
    
    def _publish_telemetry(self):
        """Publish simulated telemetry data."""
        import random
        payload = {
            "rssi_dbm": random.randint(-70, -40),
            "heap_free_kb": random.randint(180, 220),
            "uptime_s": int(time.time() - self.start_time),
            "ts_ms": int(time.time() * 1000)
        }
        self.client.publish(self.topic_telemetry, json.dumps(payload), qos=0)
    
    def _auto_cycle(self):
        """Cycle phases in AUTO mode."""
        elapsed_ms = (time.time() - self.phase_start) * 1000
        duration = self.phase_durations[self.phase]
        if elapsed_ms >= duration:
            self.phase = (self.phase + 1) % 6
            self.phase_start = time.time()
    
    def _state_loop(self):
        """Publish state every 1 second, telemetry every 5 seconds."""
        telemetry_counter = 0
        while self.running:
            if self.connected:
                # AUTO mode: cycle phases
                if self.mode == "AUTO":
                    self._auto_cycle()
                # BLINK mode: toggle phase between current and -1
                elif self.mode == "BLINK":
                    self.blink_on = not self.blink_on
                    self.phase = 2 if self.blink_on else -1  # ALL_RED or all off
                # OFF mode
                elif self.mode == "OFF":
                    self.phase = -1  # all off
                
                self._publish_state()
                
                telemetry_counter += 1
                if telemetry_counter >= 5:
                    self._publish_telemetry()
                    telemetry_counter = 0
            time.sleep(1.0)
    
    def run(self):
        """Start the mock ESP32."""
        print("\n" + "=" * 60)
        print("🤖 MOCK ESP32 TRAFFIC LIGHT CONTROLLER")
        print("=" * 60)
        print(f"  Host:       {self.host}:{self.port}")
        print(f"  User:       {self.user}")
        print(f"  Ack Delay:  {self.ack_delay_ms}ms")
        print("=" * 60)
        print(f"  Topics:")
        print(f"    state:  {self.topic_state}")
        print(f"    cmd:    {self.topic_cmd}")
        print(f"    ack:    {self.topic_ack}")
        print(f"    status: {self.topic_status}")
        print("=" * 60 + "\n")
        
        # Connect
        try:
            print(f"🔌 Connecting to {self.host}:{self.port}...")
            self.client.connect(self.host, self.port, keepalive=30)
            self.client.loop_start()
            
            # Wait for connection
            timeout = 5.0
            start = time.time()
            while not self.connected and (time.time() - start) < timeout:
                time.sleep(0.1)
            
            if not self.connected:
                print("❌ Connection timeout")
                return False
            
            # Start state publishing thread
            state_thread = threading.Thread(target=self._state_loop, daemon=True)
            state_thread.start()
            
            print("\n✅ Mock ESP32 running. Press Ctrl+C to stop.\n")
            
            # Run until interrupted
            while self.running:
                time.sleep(0.5)
            
            return True
            
        except KeyboardInterrupt:
            print("\n⚠️ Interrupted by user")
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            self.stop()
        
        return False
    
    def stop(self):
        """Stop the mock ESP32."""
        self.running = False
        
        if self.connected:
            # Publish offline status before disconnect
            self._publish_status(online=False)
            time.sleep(0.3)  # Allow message to be sent
        
        self.client.loop_stop()
        self.client.disconnect()
        print("👋 Mock ESP32 stopped")


def main():
    parser = argparse.ArgumentParser(
        description='Mock ESP32 Traffic Light Controller',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python mock_esp32.py --host localhost
  python mock_esp32.py --host 192.168.1.100 --user demo --password demo_pass
  python mock_esp32.py --host localhost --ack_delay_ms 50
        """
    )
    
    parser.add_argument('--host', default='localhost', help='MQTT broker host')
    parser.add_argument('--port', type=int, default=1883, help='MQTT broker port')
    parser.add_argument('--user', default='demo', help='MQTT username')
    parser.add_argument('--password', default='demo_pass', help='MQTT password')
    parser.add_argument('--city', default='demo', help='City ID')
    parser.add_argument('--intersection', default='001', help='Intersection ID')
    parser.add_argument('--ack_delay_ms', type=int, default=0, 
                        help='Delay before sending ack (ms) for RTT testing')
    
    args = parser.parse_args()
    
    # Handle SIGINT gracefully
    mock = MockESP32(
        host=args.host,
        port=args.port,
        user=args.user,
        password=args.password,
        city=args.city,
        intersection=args.intersection,
        ack_delay_ms=args.ack_delay_ms
    )
    
    def signal_handler(sig, frame):
        mock.stop()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    success = mock.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
