# ESP-IDF Traffic Light Controller
# Minimum IDF version: 5.0

cmake_minimum_required(VERSION 3.16)

set(EXTRA_COMPONENT_DIRS 
    $ENV{IDF_PATH}/components
)

include($ENV{IDF_PATH}/tools/cmake/project.cmake)
project(traffic_light_mqtt)
