/**
 * @file gpio_lights.c
 * @brief GPIO control for 4 traffic light modules (N, S, E, W)
 */

#include "gpio_lights.h"
#include "driver/gpio.h"
#include "esp_log.h"
#include "sdkconfig.h"

static const char *TAG = "GPIO_LIGHTS";

// Pin definitions from Kconfig
#define PIN_N_RED CONFIG_PIN_NORTH_RED
#define PIN_N_YELLOW CONFIG_PIN_NORTH_YELLOW
#define PIN_N_GREEN CONFIG_PIN_NORTH_GREEN

#define PIN_S_RED CONFIG_PIN_SOUTH_RED
#define PIN_S_YELLOW CONFIG_PIN_SOUTH_YELLOW
#define PIN_S_GREEN CONFIG_PIN_SOUTH_GREEN

#define PIN_E_RED CONFIG_PIN_EAST_RED
#define PIN_E_YELLOW CONFIG_PIN_EAST_YELLOW
#define PIN_E_GREEN CONFIG_PIN_EAST_GREEN

#define PIN_W_RED CONFIG_PIN_WEST_RED
#define PIN_W_YELLOW CONFIG_PIN_WEST_YELLOW
#define PIN_W_GREEN CONFIG_PIN_WEST_GREEN

// All pins array for initialization
static const int ALL_PINS[] = {
    PIN_N_RED, PIN_N_YELLOW, PIN_N_GREEN, PIN_S_RED, PIN_S_YELLOW, PIN_S_GREEN,
    PIN_E_RED, PIN_E_YELLOW, PIN_E_GREEN, PIN_W_RED, PIN_W_YELLOW, PIN_W_GREEN};
#define NUM_PINS (sizeof(ALL_PINS) / sizeof(ALL_PINS[0]))

// Yellow toggle state for blink mode
static bool yellow_state = false;

void gpio_lights_init(void) {
  ESP_LOGI(TAG, "Initializing GPIO pins for 4 LED modules");

  gpio_config_t io_conf = {
      .mode = GPIO_MODE_OUTPUT,
      .pull_up_en = GPIO_PULLUP_DISABLE,
      .pull_down_en = GPIO_PULLDOWN_DISABLE,
      .intr_type = GPIO_INTR_DISABLE,
  };

  for (int i = 0; i < NUM_PINS; i++) {
    io_conf.pin_bit_mask = (1ULL << ALL_PINS[i]);
    gpio_config(&io_conf);
    gpio_set_level(ALL_PINS[i], 0); // Start OFF
  }

  ESP_LOGI(
      TAG,
      "GPIO init complete: N(%d,%d,%d) S(%d,%d,%d) E(%d,%d,%d) W(%d,%d,%d)",
      PIN_N_RED, PIN_N_YELLOW, PIN_N_GREEN, PIN_S_RED, PIN_S_YELLOW,
      PIN_S_GREEN, PIN_E_RED, PIN_E_YELLOW, PIN_E_GREEN, PIN_W_RED,
      PIN_W_YELLOW, PIN_W_GREEN);
}

void gpio_lights_set(int direction, bool red, bool yellow, bool green) {
  int r_pin, y_pin, g_pin;

  switch (direction) {
  case 0: // North
    r_pin = PIN_N_RED;
    y_pin = PIN_N_YELLOW;
    g_pin = PIN_N_GREEN;
    break;
  case 1: // South
    r_pin = PIN_S_RED;
    y_pin = PIN_S_YELLOW;
    g_pin = PIN_S_GREEN;
    break;
  case 2: // East
    r_pin = PIN_E_RED;
    y_pin = PIN_E_YELLOW;
    g_pin = PIN_E_GREEN;
    break;
  case 3: // West
    r_pin = PIN_W_RED;
    y_pin = PIN_W_YELLOW;
    g_pin = PIN_W_GREEN;
    break;
  default:
    return;
  }

  gpio_set_level(r_pin, red ? 1 : 0);
  gpio_set_level(y_pin, yellow ? 1 : 0);
  gpio_set_level(g_pin, green ? 1 : 0);
}

void gpio_lights_set_ns(bool red, bool yellow, bool green) {
  gpio_lights_set(0, red, yellow, green); // North
  gpio_lights_set(1, red, yellow, green); // South (mirrored)
}

void gpio_lights_set_ew(bool red, bool yellow, bool green) {
  gpio_lights_set(2, red, yellow, green); // East
  gpio_lights_set(3, red, yellow, green); // West (mirrored)
}

void gpio_lights_all_off(void) {
  for (int i = 0; i < NUM_PINS; i++) {
    gpio_set_level(ALL_PINS[i], 0);
  }
}

void gpio_lights_all_red(void) {
  gpio_lights_set_ns(true, false, false);
  gpio_lights_set_ew(true, false, false);
}

void gpio_lights_toggle_yellow(void) {
  yellow_state = !yellow_state;

  // All directions: only yellow toggles, others off
  gpio_set_level(PIN_N_RED, 0);
  gpio_set_level(PIN_N_YELLOW, yellow_state ? 1 : 0);
  gpio_set_level(PIN_N_GREEN, 0);

  gpio_set_level(PIN_S_RED, 0);
  gpio_set_level(PIN_S_YELLOW, yellow_state ? 1 : 0);
  gpio_set_level(PIN_S_GREEN, 0);

  gpio_set_level(PIN_E_RED, 0);
  gpio_set_level(PIN_E_YELLOW, yellow_state ? 1 : 0);
  gpio_set_level(PIN_E_GREEN, 0);

  gpio_set_level(PIN_W_RED, 0);
  gpio_set_level(PIN_W_YELLOW, yellow_state ? 1 : 0);
  gpio_set_level(PIN_W_GREEN, 0);
}
