/**
 * @file wifi_manager.h
 * @brief WiFi connection manager with auto-reconnect
 */

#pragma once

#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief Initialize and connect to WiFi
 * Blocks until connected or max retries reached
 * @return true if connected successfully
 */
bool wifi_init_sta(void);

/**
 * @brief Check if WiFi is connected
 */
bool wifi_is_connected(void);

/**
 * @brief Get WiFi RSSI
 * @return RSSI in dBm, or 0 if not connected
 */
int wifi_get_rssi(void);

#ifdef __cplusplus
}
#endif
