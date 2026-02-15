/**
 * Configuration Header for ESP32 Traffic Light Controller
 *
 * Copy this file to config.h and modify the values.
 * config.h is gitignored to prevent credential leaks.
 */

#ifndef CONFIG_H
#define CONFIG_H

// =============================================================================
// WiFi Configuration
// =============================================================================
#define WIFI_SSID "YOUR_WIFI_SSID"
#define WIFI_PASS "YOUR_WIFI_PASSWORD"

// =============================================================================
// MQTT Broker Configuration
// Get your Windows IP by running: ipconfig | findstr IPv4
// =============================================================================
#define MQTT_HOST "192.168.1.100"
#define MQTT_PORT 1883
#define MQTT_USER "demo"
#define MQTT_PASS "demo_pass"

// =============================================================================
// Topic Configuration
// =============================================================================
#define CITY_ID "demo"
#define INTERSECTION_ID "001"

// =============================================================================
// GPIO Pin Mapping
// Modify if your wiring is different
// =============================================================================
#define PIN_NS_RED 25
#define PIN_NS_YELLOW 26
#define PIN_NS_GREEN 27
#define PIN_EW_RED 14
#define PIN_EW_YELLOW 12
#define PIN_EW_GREEN 13

// =============================================================================
// Timing Configuration (milliseconds)
// =============================================================================
#define TIME_NS_GREEN 15000 // North-South green duration
#define TIME_NS_YELLOW 3000 // North-South yellow duration
#define TIME_ALL_RED 1000   // All-red transition duration
#define TIME_EW_GREEN 15000 // East-West green duration
#define TIME_EW_YELLOW 3000 // East-West yellow duration

#define STATE_PUBLISH_INTERVAL 1000  // State publish frequency
#define MQTT_RECONNECT_INTERVAL 5000 // MQTT reconnect attempt interval
#define FAILSAFE_TIMEOUT 10000       // Time before failsafe activates

#endif // CONFIG_H
