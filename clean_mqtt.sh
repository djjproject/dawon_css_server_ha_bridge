#!/bin/bash
mosquitto_pub -m "" -t homeassistant/switch/DAWONDNS-B540_W-2ef432510027/config
mosquitto_pub -m "" -t homeassistant/sensor/DAWONDNS-B540_W-2ef432510027-voltage/config
mosquitto_pub -m "" -t homeassistant/sensor/DAWONDNS-B540_W-2ef432510027-power/config
mosquitto_pub -m "" -t homeassistant/sensor/DAWONDNS-B540_W-2ef432510027-temperature/config
mosquitto_pub -m "" -t homeassistant/sensor/DAWONDNS-B540_W-2ef432510027-version/config
mosquitto_pub -m "" -t homeassistant/sensor/DAWONDNS-B540_W-2ef432510027-address/config
mosquitto_pub -m "" -t homeassistant/sensor/DAWONDNS-B5X-2ef432510027-version/state

