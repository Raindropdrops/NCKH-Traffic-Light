/**
 * @file mqtt_handler.c
 * @brief MQTT client handler - cmd/ack/state/status/telemetry per SPEC.md
 *
 * Topic tree (LOCKED):
 *   city/{city}/intersection/{id}/cmd      - Subscribe QoS1
 *   city/{city}/intersection/{id}/ack      - Publish QoS1
 *   city/{city}/intersection/{id}/state    - Publish QoS0
 *   city/{city}/intersection/{id}/status   - Publish QoS1 retained (LWT)
 *   city/{city}/intersection/{id}/telemetry - Publish QoS0
 */

#include "mqtt_handler.h"
#include "cJSON.h"
#include "esp_log.h"
#include "esp_timer.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "fsm_controller.h"
#include "mqtt_client.h"
#include "sdkconfig.h"
#include "wifi_manager.h"
#include <stdio.h>
#include <string.h>


static const char *TAG = "MQTT";

// Topic buffer size
#define TOPIC_LEN 128

// Topics
static char topic_cmd[TOPIC_LEN];
static char topic_ack[TOPIC_LEN];
static char topic_state[TOPIC_LEN];
static char topic_status[TOPIC_LEN];
static char topic_telemetry[TOPIC_LEN];

// MQTT client handle
static esp_mqtt_client_handle_t mqtt_client = NULL;
static bool is_connected = false;
static int64_t last_activity_ms = 0;

// Idempotency cache (32 cmd_ids)
#define CMD_ID_CACHE_SIZE 32
#define CMD_ID_MAX_LEN 64
static char cmd_id_cache[CMD_ID_CACHE_SIZE][CMD_ID_MAX_LEN];
static int cmd_id_cache_idx = 0;

// Uptime
static int64_t boot_time_ms = 0;

static int64_t get_timestamp_ms(void) { return esp_timer_get_time() / 1000; }

static int64_t get_uptime_s(void) {
  return (get_timestamp_ms() - boot_time_ms) / 1000;
}

static bool is_cmd_id_cached(const char *cmd_id) {
  for (int i = 0; i < CMD_ID_CACHE_SIZE; i++) {
    if (strcmp(cmd_id_cache[i], cmd_id) == 0) {
      return true;
    }
  }
  return false;
}

static void cache_cmd_id(const char *cmd_id) {
  strncpy(cmd_id_cache[cmd_id_cache_idx], cmd_id, CMD_ID_MAX_LEN - 1);
  cmd_id_cache[cmd_id_cache_idx][CMD_ID_MAX_LEN - 1] = '\0';
  cmd_id_cache_idx = (cmd_id_cache_idx + 1) % CMD_ID_CACHE_SIZE;
}

static void publish_ack(const char *cmd_id, bool ok, const char *err) {
  cJSON *root = cJSON_CreateObject();
  cJSON_AddStringToObject(root, "cmd_id", cmd_id);
  cJSON_AddBoolToObject(root, "ok", ok);
  if (err) {
    cJSON_AddStringToObject(root, "err", err);
  } else {
    cJSON_AddNullToObject(root, "err");
  }
  cJSON_AddNumberToObject(root, "edge_recv_ts_ms", (double)get_timestamp_ms());

  char *json_str = cJSON_PrintUnformatted(root);
  if (json_str) {
    esp_mqtt_client_publish(mqtt_client, topic_ack, json_str, 0, 1, 0);
    ESP_LOGI(TAG, "ACK: %s", json_str);
    free(json_str);
  }
  cJSON_Delete(root);
}

static void publish_status(bool online) {
  cJSON *root = cJSON_CreateObject();
  cJSON_AddBoolToObject(root, "online", online);
  cJSON_AddNumberToObject(root, "ts_ms", (double)get_timestamp_ms());

  char *json_str = cJSON_PrintUnformatted(root);
  if (json_str) {
    esp_mqtt_client_publish(mqtt_client, topic_status, json_str, 0, 1,
                            1); // QoS1, retained
    ESP_LOGI(TAG, "STATUS: %s", json_str);
    free(json_str);
  }
  cJSON_Delete(root);
}

static void handle_command(const char *payload, int len) {
  cJSON *root = cJSON_ParseWithLength(payload, len);
  if (!root) {
    ESP_LOGW(TAG, "Invalid JSON command");
    return;
  }

  // Required fields
  cJSON *cmd_id_j = cJSON_GetObjectItem(root, "cmd_id");
  cJSON *type_j = cJSON_GetObjectItem(root, "type");

  if (!cJSON_IsString(cmd_id_j) || !cJSON_IsString(type_j)) {
    ESP_LOGW(TAG, "Missing cmd_id or type");
    cJSON_Delete(root);
    return;
  }

  const char *cmd_id = cmd_id_j->valuestring;
  const char *type = type_j->valuestring;

  ESP_LOGI(TAG, "CMD: id=%s, type=%s", cmd_id, type);

  // Idempotency check
  if (is_cmd_id_cached(cmd_id)) {
    ESP_LOGI(TAG, "Duplicate cmd_id, sending cached ack");
    publish_ack(cmd_id, true, NULL);
    cJSON_Delete(root);
    return;
  }

  bool ok = false;
  const char *err = NULL;

  if (strcmp(type, "SET_MODE") == 0) {
    cJSON *mode_j = cJSON_GetObjectItem(root, "mode");
    if (cJSON_IsString(mode_j)) {
      traffic_mode_t mode = fsm_string_to_mode(mode_j->valuestring);
      ok = fsm_set_mode(mode);
      if (!ok) {
        err = "ERR_INVALID_MODE";
      }
    } else {
      err = "ERR_MISSING_MODE";
    }
  } else if (strcmp(type, "SET_PHASE") == 0) {
    cJSON *phase_j = cJSON_GetObjectItem(root, "phase");
    if (cJSON_IsNumber(phase_j)) {
      int phase = (int)phase_j->valuedouble;
      ok = fsm_set_phase(phase);
      if (!ok) {
        err = "ERR_PHASE_REJECTED";
      }
    } else {
      err = "ERR_MISSING_PHASE";
    }
  } else if (strcmp(type, "EMERGENCY") == 0) {
    // Emergency: all red
    fsm_set_mode(MODE_MANUAL);
    fsm_set_phase(2); // ALL_RED
    ok = true;
  } else {
    err = "ERR_UNKNOWN_TYPE";
  }

  if (ok) {
    cache_cmd_id(cmd_id);
  }

  publish_ack(cmd_id, ok, err);
  cJSON_Delete(root);
}

static void mqtt_event_handler(void *handler_args, esp_event_base_t base,
                               int32_t event_id, void *event_data) {
  esp_mqtt_event_handle_t event = event_data;

  switch ((esp_mqtt_event_id_t)event_id) {
  case MQTT_EVENT_CONNECTED:
    ESP_LOGI(TAG, "MQTT connected to broker");
    is_connected = true;
    last_activity_ms = get_timestamp_ms();

    // Subscribe to cmd topic
    esp_mqtt_client_subscribe(mqtt_client, topic_cmd, 1);

    // Publish online status
    publish_status(true);
    break;

  case MQTT_EVENT_DISCONNECTED:
    ESP_LOGW(TAG, "MQTT disconnected");
    is_connected = false;
    break;

  case MQTT_EVENT_SUBSCRIBED:
    ESP_LOGI(TAG, "Subscribed to: %s", topic_cmd);
    break;

  case MQTT_EVENT_DATA:
    last_activity_ms = get_timestamp_ms();
    if (strncmp(event->topic, topic_cmd, event->topic_len) == 0) {
      handle_command(event->data, event->data_len);
    }
    break;

  case MQTT_EVENT_ERROR:
    ESP_LOGE(TAG, "MQTT error");
    break;

  default:
    break;
  }
}

void mqtt_init(void) {
  boot_time_ms = get_timestamp_ms();

  // Build topic strings
  snprintf(topic_cmd, TOPIC_LEN, "city/%s/intersection/%s/cmd",
           CONFIG_MQTT_CITY_ID, CONFIG_MQTT_INTERSECTION_ID);
  snprintf(topic_ack, TOPIC_LEN, "city/%s/intersection/%s/ack",
           CONFIG_MQTT_CITY_ID, CONFIG_MQTT_INTERSECTION_ID);
  snprintf(topic_state, TOPIC_LEN, "city/%s/intersection/%s/state",
           CONFIG_MQTT_CITY_ID, CONFIG_MQTT_INTERSECTION_ID);
  snprintf(topic_status, TOPIC_LEN, "city/%s/intersection/%s/status",
           CONFIG_MQTT_CITY_ID, CONFIG_MQTT_INTERSECTION_ID);
  snprintf(topic_telemetry, TOPIC_LEN, "city/%s/intersection/%s/telemetry",
           CONFIG_MQTT_CITY_ID, CONFIG_MQTT_INTERSECTION_ID);

  // Clear cmd_id cache
  memset(cmd_id_cache, 0, sizeof(cmd_id_cache));

  ESP_LOGI(TAG, "Topics: cmd=%s, ack=%s, state=%s", topic_cmd, topic_ack,
           topic_state);
}

void mqtt_start(void) {
  // Build LWT message
  cJSON *lwt = cJSON_CreateObject();
  cJSON_AddBoolToObject(lwt, "online", false);
  cJSON_AddNumberToObject(lwt, "ts_ms", 0);
  char *lwt_str = cJSON_PrintUnformatted(lwt);

  // Build broker URI
  char uri[128];
  snprintf(uri, sizeof(uri), "mqtt://%s:%d", CONFIG_MQTT_BROKER_HOST,
           CONFIG_MQTT_BROKER_PORT);

  esp_mqtt_client_config_t mqtt_cfg = {
      .broker.address.uri = uri,
      .credentials.username = CONFIG_MQTT_USERNAME,
      .credentials.authentication.password = CONFIG_MQTT_PASSWORD,
      .session.last_will.topic = topic_status,
      .session.last_will.msg = lwt_str,
      .session.last_will.qos = 1,
      .session.last_will.retain = 1,
  };

  mqtt_client = esp_mqtt_client_init(&mqtt_cfg);
  esp_mqtt_client_register_event(mqtt_client, ESP_EVENT_ANY_ID,
                                 mqtt_event_handler, NULL);
  esp_mqtt_client_start(mqtt_client);

  cJSON_Delete(lwt);
  free(lwt_str);

  ESP_LOGI(TAG, "MQTT client started, connecting to %s", uri);
}

bool mqtt_is_connected(void) { return is_connected; }

uint32_t mqtt_get_offline_duration_ms(void) {
  if (is_connected) {
    return 0;
  }
  return (uint32_t)(get_timestamp_ms() - last_activity_ms);
}

void mqtt_publish_state(void) {
  if (!is_connected)
    return;

  cJSON *root = cJSON_CreateObject();
  cJSON_AddStringToObject(root, "mode", fsm_mode_to_string(fsm_get_mode()));
  cJSON_AddNumberToObject(root, "phase", fsm_get_phase());
  cJSON_AddNumberToObject(root, "ts_ms", (double)get_timestamp_ms());
  cJSON_AddNumberToObject(root, "uptime_s", (double)get_uptime_s());

  char *json_str = cJSON_PrintUnformatted(root);
  if (json_str) {
    esp_mqtt_client_publish(mqtt_client, topic_state, json_str, 0, 0,
                            0); // QoS0
    free(json_str);
  }
  cJSON_Delete(root);
}

void mqtt_publish_telemetry(void) {
  if (!is_connected)
    return;

  cJSON *root = cJSON_CreateObject();
  cJSON_AddNumberToObject(root, "rssi_dbm", wifi_get_rssi());
  cJSON_AddNumberToObject(root, "heap_free_kb",
                          (double)(esp_get_free_heap_size() / 1024));
  cJSON_AddNumberToObject(root, "uptime_s", (double)get_uptime_s());
  cJSON_AddNumberToObject(root, "ts_ms", (double)get_timestamp_ms());

  char *json_str = cJSON_PrintUnformatted(root);
  if (json_str) {
    esp_mqtt_client_publish(mqtt_client, topic_telemetry, json_str, 0, 0,
                            0); // QoS0
    free(json_str);
  }
  cJSON_Delete(root);
}
