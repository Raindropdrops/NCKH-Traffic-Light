/**
 * @file mqtt_handler.h
 * @brief MQTT client handler with LWT, cmd/ack/state/status/telemetry
 */

#pragma once

#include <stdbool.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief Initialize MQTT client (does not connect)
 */
void mqtt_init(void);

/**
 * @brief Start MQTT client (connect to broker)
 */
void mqtt_start(void);

/**
 * @brief Check if MQTT is connected
 */
bool mqtt_is_connected(void);

/**
 * @brief Get time since last MQTT activity (ms)
 */
uint32_t mqtt_get_offline_duration_ms(void);

/**
 * @brief Publish state message
 */
void mqtt_publish_state(void);

/**
 * @brief Publish telemetry message
 */
void mqtt_publish_telemetry(void);

#ifdef __cplusplus
}
#endif
