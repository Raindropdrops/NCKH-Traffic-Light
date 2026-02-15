idf_component_register(
    SRCS 
        "app_main.c"
        "wifi_manager.c"
        "mqtt_handler.c"
        "fsm_controller.c"
        "gpio_lights.c"
    INCLUDE_DIRS "."
    REQUIRES 
        nvs_flash
        esp_wifi
        esp_event
        esp_timer
)

