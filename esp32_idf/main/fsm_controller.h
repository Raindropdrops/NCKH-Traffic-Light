/**
 * @file fsm_controller.h
 * @brief Traffic light FSM controller
 */

#pragma once

#include <stdbool.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef enum {
  MODE_AUTO = 0,
  MODE_MANUAL,
  MODE_BLINK,
  MODE_OFF
} traffic_mode_t;

/**
 * @brief Initialize FSM controller
 */
void fsm_init(void);

/**
 * @brief Start FSM task
 */
void fsm_start(void);

/**
 * @brief Set operating mode
 * @return true if mode changed successfully
 */
bool fsm_set_mode(traffic_mode_t mode);

/**
 * @brief Set phase (only in MANUAL mode)
 * @param phase 0-5
 * @return true if phase set successfully
 */
bool fsm_set_phase(int phase);

/**
 * @brief Get current mode
 */
traffic_mode_t fsm_get_mode(void);

/**
 * @brief Get current phase
 */
int fsm_get_phase(void);

/**
 * @brief Get mode as string
 */
const char *fsm_mode_to_string(traffic_mode_t mode);

/**
 * @brief Parse mode from string
 * @return MODE_AUTO if invalid
 */
traffic_mode_t fsm_string_to_mode(const char *str);

#ifdef __cplusplus
}
#endif
