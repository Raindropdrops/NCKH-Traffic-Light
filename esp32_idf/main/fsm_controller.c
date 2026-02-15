/**
 * @file fsm_controller.c
 * @brief Traffic light FSM controller - AUTO/MANUAL/BLINK/OFF modes
 *
 * Phase definitions (LOCKED):
 *   0: NS_GREEN  - NS=Green, EW=Red
 *   1: NS_YELLOW - NS=Yellow, EW=Red
 *   2: ALL_RED   - All Red (transition)
 *   3: EW_GREEN  - NS=Red, EW=Green
 *   4: EW_YELLOW - NS=Red, EW=Yellow
 *   5: ALL_RED   - All Red (transition)
 */

#include "fsm_controller.h"
#include "esp_log.h"
#include "freertos/FreeRTOS.h"
#include "freertos/semphr.h"
#include "freertos/task.h"
#include "gpio_lights.h"
#include "sdkconfig.h"
#include <string.h>


static const char *TAG = "FSM";

// Timing from Kconfig
#define GREEN_MS CONFIG_PHASE_GREEN_MS
#define YELLOW_MS CONFIG_PHASE_YELLOW_MS
#define ALL_RED_MS CONFIG_PHASE_ALL_RED_MS
#define BLINK_MS 500 // 1Hz blink

// Phase durations (ms)
static const int PHASE_DURATIONS[6] = {
    GREEN_MS,   // Phase 0: NS_GREEN
    YELLOW_MS,  // Phase 1: NS_YELLOW
    ALL_RED_MS, // Phase 2: ALL_RED
    GREEN_MS,   // Phase 3: EW_GREEN
    YELLOW_MS,  // Phase 4: EW_YELLOW
    ALL_RED_MS  // Phase 5: ALL_RED
};

// FSM state
static traffic_mode_t current_mode = MODE_AUTO;
static int current_phase = 0;
static SemaphoreHandle_t fsm_mutex = NULL;
static TaskHandle_t fsm_task_handle = NULL;

/**
 * @brief Apply phase to LEDs
 * Safety: NS_GREEN and EW_GREEN never simultaneous
 */
static void apply_phase(int phase) {
  switch (phase) {
  case 0:                                   // NS_GREEN
    gpio_lights_set_ns(false, false, true); // NS = Green
    gpio_lights_set_ew(true, false, false); // EW = Red
    break;
  case 1:                                   // NS_YELLOW
    gpio_lights_set_ns(false, true, false); // NS = Yellow
    gpio_lights_set_ew(true, false, false); // EW = Red
    break;
  case 2: // ALL_RED (before EW)
  case 5: // ALL_RED (before NS)
    gpio_lights_all_red();
    break;
  case 3:                                   // EW_GREEN
    gpio_lights_set_ns(true, false, false); // NS = Red
    gpio_lights_set_ew(false, false, true); // EW = Green
    break;
  case 4:                                   // EW_YELLOW
    gpio_lights_set_ns(true, false, false); // NS = Red
    gpio_lights_set_ew(false, true, false); // EW = Yellow
    break;
  default:
    gpio_lights_all_red(); // Safety fallback
    break;
  }
}

/**
 * @brief FSM task - handles mode execution
 */
static void fsm_task(void *arg) {
  TickType_t last_change = xTaskGetTickCount();

  while (1) {
    xSemaphoreTake(fsm_mutex, portMAX_DELAY);
    traffic_mode_t mode = current_mode;
    int phase = current_phase;
    xSemaphoreGive(fsm_mutex);

    switch (mode) {
    case MODE_AUTO: {
      // Check if phase duration elapsed
      int duration_ms = PHASE_DURATIONS[phase];
      if ((xTaskGetTickCount() - last_change) * portTICK_PERIOD_MS >=
          duration_ms) {
        xSemaphoreTake(fsm_mutex, portMAX_DELAY);
        current_phase = (current_phase + 1) % 6;
        phase = current_phase;
        xSemaphoreGive(fsm_mutex);

        last_change = xTaskGetTickCount();
        ESP_LOGI(TAG, "AUTO: Phase -> %d", phase);
      }
      apply_phase(phase);
      break;
    }

    case MODE_MANUAL:
      apply_phase(phase);
      break;

    case MODE_BLINK:
      gpio_lights_toggle_yellow();
      vTaskDelay(pdMS_TO_TICKS(BLINK_MS));
      continue; // Skip normal delay

    case MODE_OFF:
      gpio_lights_all_off();
      break;
    }

    vTaskDelay(pdMS_TO_TICKS(50)); // 50ms loop
  }
}

void fsm_init(void) {
  fsm_mutex = xSemaphoreCreateMutex();
  configASSERT(fsm_mutex != NULL);

  gpio_lights_init();
  gpio_lights_all_red(); // Start safe

  ESP_LOGI(TAG, "FSM initialized. Default mode=AUTO, phase=0");
}

void fsm_start(void) {
  xTaskCreate(fsm_task, "fsm_task", 4096, NULL, 5, &fsm_task_handle);
  ESP_LOGI(TAG, "FSM task started");
}

bool fsm_set_mode(traffic_mode_t mode) {
  if (mode < MODE_AUTO || mode > MODE_OFF) {
    return false;
  }

  xSemaphoreTake(fsm_mutex, portMAX_DELAY);
  traffic_mode_t old_mode = current_mode;
  current_mode = mode;

  // Reset phase on mode change to AUTO
  if (mode == MODE_AUTO && old_mode != MODE_AUTO) {
    current_phase = 0;
  }
  xSemaphoreGive(fsm_mutex);

  ESP_LOGI(TAG, "Mode changed: %s -> %s", fsm_mode_to_string(old_mode),
           fsm_mode_to_string(mode));
  return true;
}

bool fsm_set_phase(int phase) {
  if (phase < 0 || phase > 5) {
    ESP_LOGW(TAG, "Invalid phase: %d (must be 0-5)", phase);
    return false;
  }

  xSemaphoreTake(fsm_mutex, portMAX_DELAY);
  if (current_mode != MODE_MANUAL) {
    xSemaphoreGive(fsm_mutex);
    ESP_LOGW(TAG, "SET_PHASE rejected: not in MANUAL mode");
    return false;
  }
  current_phase = phase;
  xSemaphoreGive(fsm_mutex);

  ESP_LOGI(TAG, "Phase set to: %d", phase);
  return true;
}

traffic_mode_t fsm_get_mode(void) {
  xSemaphoreTake(fsm_mutex, portMAX_DELAY);
  traffic_mode_t mode = current_mode;
  xSemaphoreGive(fsm_mutex);
  return mode;
}

int fsm_get_phase(void) {
  xSemaphoreTake(fsm_mutex, portMAX_DELAY);
  int phase = current_phase;
  xSemaphoreGive(fsm_mutex);
  return phase;
}

const char *fsm_mode_to_string(traffic_mode_t mode) {
  switch (mode) {
  case MODE_AUTO:
    return "AUTO";
  case MODE_MANUAL:
    return "MANUAL";
  case MODE_BLINK:
    return "BLINK";
  case MODE_OFF:
    return "OFF";
  default:
    return "UNKNOWN";
  }
}

traffic_mode_t fsm_string_to_mode(const char *str) {
  if (!str)
    return MODE_AUTO;
  if (strcmp(str, "AUTO") == 0)
    return MODE_AUTO;
  if (strcmp(str, "MANUAL") == 0)
    return MODE_MANUAL;
  if (strcmp(str, "BLINK") == 0)
    return MODE_BLINK;
  if (strcmp(str, "OFF") == 0)
    return MODE_OFF;
  return MODE_AUTO; // Default fallback
}
