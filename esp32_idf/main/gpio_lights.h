/**
 * @file gpio_lights.h
 * @brief GPIO control for 4 traffic light modules (N, S, E, W)
 */

#pragma once

#include <stdbool.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief Initialize all GPIO pins for LED modules
 */
void gpio_lights_init(void);

/**
 * @brief Set individual LED state
 * @param direction 0=North, 1=South, 2=East, 3=West
 * @param red true=on
 * @param yellow true=on
 * @param green true=on
 */
void gpio_lights_set(int direction, bool red, bool yellow, bool green);

/**
 * @brief Set NS direction (North + South mirrored)
 */
void gpio_lights_set_ns(bool red, bool yellow, bool green);

/**
 * @brief Set EW direction (East + West mirrored)
 */
void gpio_lights_set_ew(bool red, bool yellow, bool green);

/**
 * @brief Turn all LEDs off
 */
void gpio_lights_all_off(void);

/**
 * @brief Set all directions to RED
 */
void gpio_lights_all_red(void);

/**
 * @brief Toggle yellow LEDs for blink mode
 */
void gpio_lights_toggle_yellow(void);

#ifdef __cplusplus
}
#endif
