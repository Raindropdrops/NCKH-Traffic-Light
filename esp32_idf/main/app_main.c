/**
 * @file app_main.c
 * @brief Traffic Light MQTT Controller - ESP-IDF
 *
 * Main application entry point. Initializes WiFi, MQTT, FSM.
 * Publishes state every 1s, telemetry every 5s.
 * Fallback to AUTO mode if MQTT offline > 10s.
 */

#include "esp_log.h"
#include "esp_timer.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "sdkconfig.h"
#include <stdio.h>


#include "fsm_controller.h"
#include "mqtt_handler.h"
#include "wifi_manager.h"


static const char *TAG = "MAIN";

#define STATE_INTERVAL_MS CONFIG_STATE_PUBLISH_INTERVAL_MS
#define TELEMETRY_INTERVAL_MS CONFIG_TELEMETRY_INTERVAL_MS
#define OFFLINE_TIMEOUT_MS CONFIG_MQTT_OFFLINE_TIMEOUT_MS

/**
 * @brief Publisher task - state and telemetry
 */
static void publisher_task(void *arg) {
  int64_t last_state_ms = 0;
  int64_t last_telemetry_ms = 0;
  bool fallback_mode_active = false;

  while (1) {
    int64_t now_ms = esp_timer_get_time() / 1000;

    // Check MQTT offline timeout -> fallback to AUTO
    if (!mqtt_is_connected()) {
      uint32_t offline_ms = mqtt_get_offline_duration_ms();
      if (offline_ms > OFFLINE_TIMEOUT_MS && !fallback_mode_active) {
        ESP_LOGW(TAG, "MQTT offline > %dms, fallback to AUTO",
                 OFFLINE_TIMEOUT_MS);
        fsm_set_mode(MODE_AUTO);
        fallback_mode_active = true;
      }
    } else {
      fallback_mode_active = false;
    }

    // Publish state every 1s
    if (now_ms - last_state_ms >= STATE_INTERVAL_MS) {
      mqtt_publish_state();
      last_state_ms = now_ms;
    }

    // Publish telemetry every 5s
    if (now_ms - last_telemetry_ms >= TELEMETRY_INTERVAL_MS) {
      mqtt_publish_telemetry();
      last_telemetry_ms = now_ms;
    }

    vTaskDelay(pdMS_TO_TICKS(100));
  }
}

void app_main(void) {
  ESP_LOGI(TAG, "=================================");
  ESP_LOGI(TAG, "Traffic Light MQTT Controller");
  ESP_LOGI(TAG, "ESP-IDF version: %s", esp_get_idf_version());
  ESP_LOGI(TAG, "=================================");

  // 1. Initialize FSM (also inits GPIO)
  fsm_init();

  // 2. Connect to WiFi
  ESP_LOGI(TAG, "Connecting to WiFi...");
  if (!wifi_init_sta()) {
    ESP_LOGE(TAG, "WiFi failed, running in offline AUTO mode");
    fsm_start();
    // Continue without MQTT
    while (1) {
      vTaskDelay(pdMS_TO_TICKS(1000));
    }
  }

  // 3. Initialize and start MQTT
  ESP_LOGI(TAG, "Starting MQTT...");
  mqtt_init();
  mqtt_start();

  // 4. Start FSM task
  fsm_start();

  // 5. Start publisher task
  xTaskCreate(publisher_task, "publisher", 4096, NULL, 4, NULL);

  ESP_LOGI(TAG, "System initialized. Running...");
}
