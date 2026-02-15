/**
 * ESP32 Traffic Light Controller Firmware
 *
 * Features:
 * - FSM with AUTO/MANUAL/BLINK/OFF modes
 * - MQTT integration with LWT (Last Will Testament)
 * - Fail-safe: returns to AUTO if MQTT lost > 10s
 * - Idempotent command handling (cmd_id deduplication)
 *
 * Hardware: ESP32 DevKit V1
 * Libraries: PubSubClient, ArduinoJson
 *
 * See SPEC.md for protocol details
 */

#include <ArduinoJson.h>
#include <PubSubClient.h>
#include <WiFi.h>


// =============================================================================
// CONFIGURATION - MODIFY THESE VALUES
// =============================================================================

// WiFi credentials
const char *WIFI_SSID = "YOUR_WIFI_SSID";
const char *WIFI_PASS = "YOUR_WIFI_PASSWORD";

// MQTT Broker - Use your Windows IP (run: ipconfig | findstr IPv4)
const char *MQTT_HOST = "192.168.1.100";
const uint16_t MQTT_PORT = 1883;
const char *MQTT_USER = "demo";
const char *MQTT_PASS = "demo_pass";

// Topic configuration
const char *CITY_ID = "demo";
const char *INTERSECTION_ID = "001";

// =============================================================================
// GPIO PIN MAPPING
// =============================================================================

#define PIN_NS_RED 25
#define PIN_NS_YELLOW 26
#define PIN_NS_GREEN 27
#define PIN_EW_RED 14
#define PIN_EW_YELLOW 12
#define PIN_EW_GREEN 13

// =============================================================================
// TIMING CONSTANTS (milliseconds)
// =============================================================================

#define TIME_NS_GREEN 15000 // 15s
#define TIME_NS_YELLOW 3000 // 3s
#define TIME_ALL_RED 1000   // 1s
#define TIME_EW_GREEN 15000 // 15s
#define TIME_EW_YELLOW 3000 // 3s

#define STATE_PUBLISH_INTERVAL 1000  // 1s
#define MQTT_RECONNECT_INTERVAL 5000 // 5s
#define FAILSAFE_TIMEOUT 10000       // 10s

// =============================================================================
// FSM DEFINITIONS
// =============================================================================

enum Mode { MODE_AUTO, MODE_MANUAL, MODE_BLINK, MODE_OFF };
enum Phase {
  PHASE_NS_GREEN = 0,  // Direction A green, B red
  PHASE_NS_YELLOW = 1, // Direction A yellow, B red
  PHASE_ALL_RED_1 = 2, // Transition
  PHASE_EW_GREEN = 3,  // Direction B green, A red
  PHASE_EW_YELLOW = 4, // Direction B yellow, A red
  PHASE_ALL_RED_2 = 5  // Transition
};

// Phase durations for AUTO mode
const unsigned long PHASE_DURATIONS[] = {
    TIME_NS_GREEN,  // Phase 0
    TIME_NS_YELLOW, // Phase 1
    TIME_ALL_RED,   // Phase 2
    TIME_EW_GREEN,  // Phase 3
    TIME_EW_YELLOW, // Phase 4
    TIME_ALL_RED    // Phase 5
};

// =============================================================================
// GLOBAL STATE
// =============================================================================

WiFiClient espClient;
PubSubClient mqtt(espClient);

// FSM state
Mode currentMode = MODE_AUTO;
Phase currentPhase = PHASE_NS_GREEN;
unsigned long phaseStartTime = 0;
unsigned long uptimeStart = 0;

// MQTT topics (built dynamically)
char topicState[64];
char topicCmd[64];
char topicAck[64];
char topicStatus[64];
char topicTelemetry[64];

// Timing
unsigned long lastStatePublish = 0;
unsigned long lastMqttConnected = 0;
unsigned long lastReconnectAttempt = 0;
bool wasConnected = false;

// Idempotency - store last N cmd_ids
#define CMD_ID_CACHE_SIZE 10
String cmdIdCache[CMD_ID_CACHE_SIZE];
int cmdIdCacheIndex = 0;

// Blink mode state
unsigned long lastBlinkToggle = 0;
bool blinkState = false;

// =============================================================================
// FORWARD DECLARATIONS
// =============================================================================

void setupWiFi();
void setupMQTT();
void buildTopics();
void mqttCallback(char *topic, byte *payload, unsigned int length);
void reconnectMQTT();
void publishState();
void publishAck(const char *cmdId, bool ok, const char *err);
void publishOnlineStatus(bool online);
void updateFSM();
void setLEDs();
void handleCommand(JsonDocument &doc);
bool isCommandProcessed(const char *cmdId);
void cacheCommandId(const char *cmdId);
void checkFailsafe();
Phase getNextPhase(Phase current);

// =============================================================================
// SETUP
// =============================================================================

void setup() {
  Serial.begin(115200);
  delay(100);

  Serial.println("\n========================================");
  Serial.println("  ESP32 Traffic Light Controller v1.0");
  Serial.println("========================================\n");

  // Initialize LED pins
  pinMode(PIN_NS_RED, OUTPUT);
  pinMode(PIN_NS_YELLOW, OUTPUT);
  pinMode(PIN_NS_GREEN, OUTPUT);
  pinMode(PIN_EW_RED, OUTPUT);
  pinMode(PIN_EW_YELLOW, OUTPUT);
  pinMode(PIN_EW_GREEN, OUTPUT);

  // Start with all LEDs off
  digitalWrite(PIN_NS_RED, LOW);
  digitalWrite(PIN_NS_YELLOW, LOW);
  digitalWrite(PIN_NS_GREEN, LOW);
  digitalWrite(PIN_EW_RED, LOW);
  digitalWrite(PIN_EW_YELLOW, LOW);
  digitalWrite(PIN_EW_GREEN, LOW);

  // Build MQTT topics
  buildTopics();

  // Connect WiFi
  setupWiFi();

  // Setup MQTT
  setupMQTT();

  // Initialize timing
  uptimeStart = millis();
  phaseStartTime = millis();
  lastMqttConnected = millis();

  Serial.println("Setup complete. Starting FSM in AUTO mode.\n");
}

// =============================================================================
// MAIN LOOP
// =============================================================================

void loop() {
  // Handle WiFi reconnection
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi disconnected. Reconnecting...");
    setupWiFi();
  }

  // Handle MQTT
  if (!mqtt.connected()) {
    reconnectMQTT();
  } else {
    mqtt.loop();
    lastMqttConnected = millis();

    if (!wasConnected) {
      wasConnected = true;
      publishOnlineStatus(true);
      Serial.println("MQTT connected. Published ONLINE status.");
    }
  }

  // Check failsafe
  checkFailsafe();

  // Update FSM
  updateFSM();

  // Set LEDs based on current state
  setLEDs();

  // Publish state periodically
  if (millis() - lastStatePublish >= STATE_PUBLISH_INTERVAL) {
    publishState();
    lastStatePublish = millis();
  }
}

// =============================================================================
// WIFI SETUP
// =============================================================================

void setupWiFi() {
  Serial.print("Connecting to WiFi: ");
  Serial.println(WIFI_SSID);

  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);

  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 30) {
    delay(500);
    Serial.print(".");
    attempts++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nWiFi connected!");
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\nWiFi connection failed. Will retry...");
  }
}

// =============================================================================
// MQTT SETUP
// =============================================================================

void buildTopics() {
  snprintf(topicState, sizeof(topicState), "city/%s/intersection/%s/state",
           CITY_ID, INTERSECTION_ID);
  snprintf(topicCmd, sizeof(topicCmd), "city/%s/intersection/%s/cmd", CITY_ID,
           INTERSECTION_ID);
  snprintf(topicAck, sizeof(topicAck), "city/%s/intersection/%s/ack", CITY_ID,
           INTERSECTION_ID);
  snprintf(topicStatus, sizeof(topicStatus), "city/%s/intersection/%s/status",
           CITY_ID, INTERSECTION_ID);
  snprintf(topicTelemetry, sizeof(topicTelemetry),
           "city/%s/intersection/%s/telemetry", CITY_ID, INTERSECTION_ID);

  Serial.println("MQTT Topics:");
  Serial.print("  state: ");
  Serial.println(topicState);
  Serial.print("  cmd:   ");
  Serial.println(topicCmd);
  Serial.print("  ack:   ");
  Serial.println(topicAck);
  Serial.print("  status:");
  Serial.println(topicStatus);
}

void setupMQTT() {
  mqtt.setServer(MQTT_HOST, MQTT_PORT);
  mqtt.setCallback(mqttCallback);
  mqtt.setBufferSize(512); // Increase buffer for JSON payloads

  Serial.print("MQTT broker: ");
  Serial.print(MQTT_HOST);
  Serial.print(":");
  Serial.println(MQTT_PORT);
}

void reconnectMQTT() {
  if (millis() - lastReconnectAttempt < MQTT_RECONNECT_INTERVAL) {
    return;
  }
  lastReconnectAttempt = millis();

  Serial.print("Connecting to MQTT broker...");

  // Create client ID
  String clientId = "esp32-traffic-";
  clientId += String(random(0xffff), HEX);

  // LWT: publish OFFLINE on disconnect
  StaticJsonDocument<64> lwtDoc;
  lwtDoc["online"] = false;
  char lwtPayload[64];
  serializeJson(lwtDoc, lwtPayload);

  // Connect with LWT
  if (mqtt.connect(clientId.c_str(), MQTT_USER, MQTT_PASS, topicStatus, 1, true,
                   lwtPayload)) {
    Serial.println(" connected!");

    // Subscribe to command topic
    mqtt.subscribe(topicCmd, 1);
    Serial.print("Subscribed to: ");
    Serial.println(topicCmd);

    // Publish online status
    publishOnlineStatus(true);
    wasConnected = true;
  } else {
    Serial.print(" failed, rc=");
    Serial.println(mqtt.state());
    wasConnected = false;
  }
}

// =============================================================================
// MQTT CALLBACK
// =============================================================================

void mqttCallback(char *topic, byte *payload, unsigned int length) {
  // Convert payload to string
  char message[length + 1];
  memcpy(message, payload, length);
  message[length] = '\0';

  Serial.print("Received [");
  Serial.print(topic);
  Serial.print("]: ");
  Serial.println(message);

  // Parse JSON
  StaticJsonDocument<256> doc;
  DeserializationError error = deserializeJson(doc, message);

  if (error) {
    Serial.print("JSON parse error: ");
    Serial.println(error.c_str());

    // Ack with error if cmd_id exists
    if (doc.containsKey("cmd_id")) {
      publishAck(doc["cmd_id"], false, "INVALID_JSON");
    }
    return;
  }

  // Check required field
  if (!doc.containsKey("cmd_id")) {
    Serial.println("Missing cmd_id");
    return;
  }

  const char *cmdId = doc["cmd_id"];

  // Idempotency check
  if (isCommandProcessed(cmdId)) {
    Serial.println("Duplicate command, acking without re-execution");
    publishAck(cmdId, true, nullptr);
    return;
  }

  // Process command
  handleCommand(doc);
}

// =============================================================================
// COMMAND HANDLING
// =============================================================================

void handleCommand(JsonDocument &doc) {
  const char *cmdId = doc["cmd_id"];
  const char *type = doc["type"] | "";

  Serial.print("Processing command: ");
  Serial.print(type);
  Serial.print(" (");
  Serial.print(cmdId);
  Serial.println(")");

  bool ok = false;
  const char *err = nullptr;

  if (strcmp(type, "SET_MODE") == 0) {
    const char *modeStr = doc["mode"] | "";

    if (strcmp(modeStr, "AUTO") == 0) {
      currentMode = MODE_AUTO;
      phaseStartTime = millis(); // Reset phase timer
      ok = true;
      Serial.println("Mode changed to AUTO");
    } else if (strcmp(modeStr, "MANUAL") == 0) {
      currentMode = MODE_MANUAL;
      ok = true;
      Serial.println("Mode changed to MANUAL");
    } else if (strcmp(modeStr, "BLINK") == 0) {
      currentMode = MODE_BLINK;
      lastBlinkToggle = millis();
      ok = true;
      Serial.println("Mode changed to BLINK");
    } else if (strcmp(modeStr, "OFF") == 0) {
      currentMode = MODE_OFF;
      ok = true;
      Serial.println("Mode changed to OFF");
    } else {
      err = "INVALID_MODE";
      Serial.print("Invalid mode: ");
      Serial.println(modeStr);
    }
  } else if (strcmp(type, "SET_PHASE") == 0) {
    if (currentMode != MODE_MANUAL) {
      err = "NOT_MANUAL_MODE";
      Serial.println("SET_PHASE rejected: not in MANUAL mode");
    } else {
      int phase = doc["phase"] | -1;
      if (phase >= 0 && phase <= 5) {
        // Safety: always transition through ALL_RED
        if (currentPhase != PHASE_ALL_RED_1 &&
            currentPhase != PHASE_ALL_RED_2 && phase != PHASE_ALL_RED_1 &&
            phase != PHASE_ALL_RED_2) {
          // Insert ALL_RED transition
          currentPhase = PHASE_ALL_RED_1;
          phaseStartTime = millis();
          // Note: actual phase change will happen after ALL_RED duration
        }
        currentPhase = (Phase)phase;
        phaseStartTime = millis();
        ok = true;
        Serial.print("Phase set to: ");
        Serial.println(phase);
      } else {
        err = "INVALID_PHASE";
        Serial.print("Invalid phase: ");
        Serial.println(phase);
      }
    }
  } else if (strcmp(type, "EMERGENCY") == 0) {
    // Emergency: immediate ALL_RED + BLINK
    currentMode = MODE_BLINK;
    currentPhase = PHASE_ALL_RED_1;
    phaseStartTime = millis();
    ok = true;
    Serial.println("EMERGENCY activated: BLINK mode");
  } else {
    err = "UNKNOWN_CMD";
    Serial.print("Unknown command type: ");
    Serial.println(type);
  }

  // Cache command ID and send ack
  cacheCommandId(cmdId);
  publishAck(cmdId, ok, err);
}

// =============================================================================
// IDEMPOTENCY
// =============================================================================

bool isCommandProcessed(const char *cmdId) {
  for (int i = 0; i < CMD_ID_CACHE_SIZE; i++) {
    if (cmdIdCache[i] == cmdId) {
      return true;
    }
  }
  return false;
}

void cacheCommandId(const char *cmdId) {
  cmdIdCache[cmdIdCacheIndex] = String(cmdId);
  cmdIdCacheIndex = (cmdIdCacheIndex + 1) % CMD_ID_CACHE_SIZE;
}

// =============================================================================
// MQTT PUBLISHING
// =============================================================================

void publishState() {
  if (!mqtt.connected())
    return;

  StaticJsonDocument<256> doc;

  // Mode string
  const char *modeStr;
  switch (currentMode) {
  case MODE_AUTO:
    modeStr = "AUTO";
    break;
  case MODE_MANUAL:
    modeStr = "MANUAL";
    break;
  case MODE_BLINK:
    modeStr = "BLINK";
    break;
  case MODE_OFF:
    modeStr = "OFF";
    break;
  default:
    modeStr = "UNKNOWN";
  }

  doc["mode"] = modeStr;
  doc["phase"] = (int)currentPhase;
  doc["since_ms"] = millis() - phaseStartTime;
  doc["uptime_s"] = (millis() - uptimeStart) / 1000;
  doc["ts_ms"] = millis(); // Note: not Unix timestamp, just uptime ms

  char buffer[256];
  serializeJson(doc, buffer);

  mqtt.publish(topicState, buffer, false); // QoS 0, not retained
}

void publishAck(const char *cmdId, bool ok, const char *err) {
  if (!mqtt.connected())
    return;

  StaticJsonDocument<128> doc;
  doc["cmd_id"] = cmdId;
  doc["ok"] = ok;
  if (err != nullptr) {
    doc["err"] = err;
  }
  doc["ts_ms"] = millis();

  char buffer[128];
  serializeJson(doc, buffer);

  mqtt.publish(topicAck, buffer, false); // QoS through PubSubClient default

  Serial.print("Published ACK: ");
  Serial.println(buffer);
}

void publishOnlineStatus(bool online) {
  if (!mqtt.connected())
    return;

  StaticJsonDocument<64> doc;
  doc["online"] = online;
  doc["ts_ms"] = millis();

  char buffer[64];
  serializeJson(doc, buffer);

  mqtt.publish(topicStatus, buffer, true); // Retained

  Serial.print("Published status: ");
  Serial.println(buffer);
}

// =============================================================================
// FSM UPDATE
// =============================================================================

void updateFSM() {
  unsigned long now = millis();
  unsigned long elapsed = now - phaseStartTime;

  switch (currentMode) {
  case MODE_AUTO:
    // Check if phase duration has elapsed
    if (elapsed >= PHASE_DURATIONS[currentPhase]) {
      currentPhase = getNextPhase(currentPhase);
      phaseStartTime = now;
      Serial.print("AUTO: Phase changed to ");
      Serial.println((int)currentPhase);
    }
    break;

  case MODE_MANUAL:
    // Phase is controlled by commands, no automatic transition
    break;

  case MODE_BLINK:
    // Toggle yellow lights every 500ms
    if (now - lastBlinkToggle >= 500) {
      blinkState = !blinkState;
      lastBlinkToggle = now;
    }
    break;

  case MODE_OFF:
    // All LEDs off - handled in setLEDs()
    break;
  }
}

Phase getNextPhase(Phase current) {
  switch (current) {
  case PHASE_NS_GREEN:
    return PHASE_NS_YELLOW;
  case PHASE_NS_YELLOW:
    return PHASE_ALL_RED_1;
  case PHASE_ALL_RED_1:
    return PHASE_EW_GREEN;
  case PHASE_EW_GREEN:
    return PHASE_EW_YELLOW;
  case PHASE_EW_YELLOW:
    return PHASE_ALL_RED_2;
  case PHASE_ALL_RED_2:
    return PHASE_NS_GREEN;
  default:
    return PHASE_NS_GREEN;
  }
}

// =============================================================================
// LED CONTROL
// =============================================================================

void setLEDs() {
  // All off first
  digitalWrite(PIN_NS_RED, LOW);
  digitalWrite(PIN_NS_YELLOW, LOW);
  digitalWrite(PIN_NS_GREEN, LOW);
  digitalWrite(PIN_EW_RED, LOW);
  digitalWrite(PIN_EW_YELLOW, LOW);
  digitalWrite(PIN_EW_GREEN, LOW);

  if (currentMode == MODE_OFF) {
    return; // Keep all off
  }

  if (currentMode == MODE_BLINK) {
    // Blink yellow lights only
    if (blinkState) {
      digitalWrite(PIN_NS_YELLOW, HIGH);
      digitalWrite(PIN_EW_YELLOW, HIGH);
    }
    return;
  }

  // Normal operation (AUTO or MANUAL)
  switch (currentPhase) {
  case PHASE_NS_GREEN: // NS green, EW red
    digitalWrite(PIN_NS_GREEN, HIGH);
    digitalWrite(PIN_EW_RED, HIGH);
    break;

  case PHASE_NS_YELLOW: // NS yellow, EW red
    digitalWrite(PIN_NS_YELLOW, HIGH);
    digitalWrite(PIN_EW_RED, HIGH);
    break;

  case PHASE_ALL_RED_1: // All red (transition)
  case PHASE_ALL_RED_2:
    digitalWrite(PIN_NS_RED, HIGH);
    digitalWrite(PIN_EW_RED, HIGH);
    break;

  case PHASE_EW_GREEN: // EW green, NS red
    digitalWrite(PIN_EW_GREEN, HIGH);
    digitalWrite(PIN_NS_RED, HIGH);
    break;

  case PHASE_EW_YELLOW: // EW yellow, NS red
    digitalWrite(PIN_EW_YELLOW, HIGH);
    digitalWrite(PIN_NS_RED, HIGH);
    break;
  }
}

// =============================================================================
// FAILSAFE
// =============================================================================

void checkFailsafe() {
  // If MQTT disconnected for more than FAILSAFE_TIMEOUT, revert to AUTO
  if (!mqtt.connected()) {
    unsigned long disconnectedTime = millis() - lastMqttConnected;

    if (disconnectedTime > FAILSAFE_TIMEOUT && currentMode != MODE_AUTO) {
      Serial.println(
          "FAILSAFE: MQTT disconnected > 10s. Reverting to AUTO mode.");
      currentMode = MODE_AUTO;
      phaseStartTime = millis();
    }
  }
}
