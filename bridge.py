import time
import json
from paho.mqtt import client as mqtt

#mqtt_client_id = 'DAWONDNS-habridge0000'
#mqtt_username = 'DAWONDNS-habridge-habridge0000'
#mqtt_password = 'djjproject'
mqtt_clientid = 'habridge'
mqtt_host = '127.0.0.1'
mqtt_port = '1883'
mqtt_topic = 'dawon'
mqtt_ha_topic = 'dawon-switch'


plug_list = []

def connect_mqtt(client_id, username, password, host, port):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print(f"Connect OK. {host}:{port}")
        else:
            print(f"Connect Failed. {host}:{port}")

    client = mqtt.Client(client_id, clean_session=False)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(host, int(port))
    return client

def on_message_sensor_value(client, userdata, msg):
    def publish_version(value):
        publish_data = { "Version": value }
        client.publish("homeassistant/sensor/" + device_name + "-version/state", json.dumps(publish_data), 0, True) 

    def publish_address(value):
        publish_data = { "Address": value }
        client.publish("homeassistant/sensor/" + device_name + "-address/state", json.dumps(publish_data), 0, True) 
 
    def publish_voltage(value):
        publish_data = { "Voltage": value }
        client.publish("homeassistant/sensor/" + device_name + "-voltage/state", json.dumps(publish_data), 0, False) 
 
    def publish_power(value):
        publish_data = { "Power": value }
        client.publish("homeassistant/sensor/" + device_name + "-power/state", json.dumps(publish_data), 0, False) 
 
    def publish_temperature(value):
        publish_data = { "Temperature": value }
        client.publish("homeassistant/sensor/" + device_name + "-temperature/state", json.dumps(publish_data), 0, False) 
 
    def publish_state(value):
        client.publish("homeassistant/" + mqtt_ha_topic + "/" + device_name + "/state", "ON" if value == "true" else "OFF" , 0, False) 
 
    def parse_value(data_type, value):
        switch_func = { "/3/0/3"    : publish_version,
                        "/4/0/4"    : publish_address,
                        "/100/0/1"  : publish_voltage,
                        "/100/0/11" : publish_power,
                        "/100/0/4"  : publish_temperature,
                        "/100/0/31" : publish_state }
        try:
            switch_func[data_type](value)
        except Exception as e:
            pass

    def publish_discovery():
        if not device_name in plug_list:
            plug_list.append(device_name)
            print(f"Register {device_name}.")

            ha_manufacture = device_name.split("-")[0]
            ha_device_mac = device_name.split("-")[2]
            ha_version_data = {
                "name": ha_device_mac + "_Version",
                #"object_id": ha_device_mac + "_Version",
                "unique_id": ha_device_mac + "_Version",
                "device": {
                    "identifiers": ha_device_mac,
                    "name": device_name,
                    "manufacturer": ha_manufacture,
                },
                "state_topic": "homeassistant/sensor/" + device_name + "-version/state",
                "value_template": "{{ value_json.Version }}",
            }

            ha_address_data = {
                "name": ha_device_mac + "_Address",
                #"object_id": ha_device_mac + "_Address",
                "unique_id": ha_device_mac + "_Address",
                "device": {
                    "identifiers": ha_device_mac,
                    "name": device_name,
                    "manufacturer": ha_manufacture,
                },
                "state_topic": "homeassistant/sensor/" + device_name + "-address/state",
                "value_template": "{{ value_json.Address }}",
            }

            ha_voltage_data = {
                "device_class": "voltage",
                "name": ha_device_mac + "_Voltage",
                #"object_id": ha_device_mac + "_Voltage",
                "unique_id": ha_device_mac + "_Voltage",
                "device": {
                    "identifiers": ha_device_mac,
                    "name": device_name,
                    "manufacturer": ha_manufacture,
                },
                "state_topic": "homeassistant/sensor/" + device_name + "-voltage/state",
                "value_template": "{{ value_json.Voltage }}",
                "unit_of_measurement": "V",
            }

            ha_power_data = {
                "device_class": "power",
                "name": ha_device_mac + "_Power",
                #"object_id": ha_device_mac + "_Power",
                "unique_id": ha_device_mac + "_Power",
                "device": {
                    "identifiers": ha_device_mac,
                    "name": device_name,
                    "manufacturer": ha_manufacture,
                },
                "state_topic": "homeassistant/sensor/" + device_name + "-power/state",
                "value_template": "{{ value_json.Power }}",
                "unit_of_measurement": "W",
            }

            ha_temperature_data = {
                "device_class": "temperature",
                "name": ha_device_mac + "_Temperature",
                #"object_id":  ha_device_mac + "_Switch",
                "unique_id":  ha_device_mac + "_Switch",
                "device": {
                    "identifiers": ha_device_mac,
                    "name": device_name,
                    "manufacturer": ha_manufacture,
                },
                "state_topic": "homeassistant/sensor/" + device_name + "-temperature/state",
                "value_template": "{{ value_json.Temperature }}",
                "unit_of_measurement": "°C",
            }

            ha_switch_data = {
                "device_class": "switch",
                "name": ha_device_mac + "_Switch",
                #"object_id": ha_device_mac + "_Switch",
                "unique_id": ha_device_mac + "_Switch",
                "device": {
                    "identifiers": ha_device_mac,
                    "name": device_name,
                    "manufacturer": ha_manufacture,
                },
                "state_topic": "homeassistant/" + mqtt_ha_topic + "/" + device_name + "/state",
                "command_topic": "homeassistant/" + mqtt_ha_topic + "/" + device_name + "/set",
            }

            client.publish("homeassistant/sensor/" + device_name + "-version/config", json.dumps(ha_version_data), 2, True)
            client.publish("homeassistant/sensor/" + device_name + "-address/config", json.dumps(ha_address_data), 2, True)
            client.publish("homeassistant/sensor/" + device_name + "-voltage/config", json.dumps(ha_voltage_data), 2, True)
            client.publish("homeassistant/sensor/" + device_name + "-power/config", json.dumps(ha_power_data), 2, True)
            client.publish("homeassistant/sensor/" + device_name + "-temperature/config", json.dumps(ha_temperature_data), 2, True)
            client.publish("homeassistant/switch/" + device_name + "/config", json.dumps(ha_switch_data), 2, True)
        else:
            pass
            

    device_name = msg.topic.split("/")[1]
    device_data = json.loads(msg.payload.decode())
    publish_discovery()

    for data in device_data["msg"]["e"]:
        parse_value(data["n"], data["sv"])

def on_message_control_value(client, userdata, msg):
    device_name = msg.topic.split("/")[2]
    if device_name in plug_list:
        print(f"Match device: {device_name}:" + msg.payload.decode())
        time_tick = int(time.time())
        send_data = {
            "sid": "2",
            "msg": {
                "o": "e",
                "e": [
                    {"n": "/100/0/31", "sv": "true" if msg.payload.decode() == "ON" else "false", "ti": time_tick}
                ]
            }
        }

        client.publish(mqtt_topic + "/iot-server/" + device_name + "/execute/json", json.dumps(send_data), 2, False)
    else:
        print(f"Not registered device: {device_name}")
        


if __name__ == "__main__":
    mqtt_ret = -1
    while True:
        client = connect_mqtt(mqtt_clientid, "", "", mqtt_host, mqtt_port)
        client.message_callback_add(mqtt_topic + "/+/iot-server/notify/json", on_message_sensor_value)
        client.message_callback_add("homeassistant/" + mqtt_ha_topic + "/+/set", on_message_control_value)
        client.subscribe("#")
        client.loop_forever()
