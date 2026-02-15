# API Documentation

> **Status:** Placeholder - WP5.1
> **See:** SPEC.md for authoritative topic tree and payload schemas

## MQTT Topics

| Topic | Direction | QoS | Description |
|-------|-----------|-----|-------------|
| `city/demo/intersection/001/state` | ESP32 → Broker | 0 | Current state |
| `city/demo/intersection/001/cmd` | Broker → ESP32 | 1 | Commands |
| `city/demo/intersection/001/ack` | ESP32 → Broker | 1 | Acknowledgements |
| `city/demo/intersection/001/status` | ESP32 → Broker | 1 (retained) | LWT status |
| `city/demo/intersection/001/telemetry` | ESP32 → Broker | 0 | Metrics |

## Payload Examples

TODO: Add examples from SPEC.md Section 4
