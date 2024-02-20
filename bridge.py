import json
from paho.mqtt import client as mqtt

mqtt_clientid = 'dawon-ha-bridge'
mqtt_username = ''
mqtt_password = ''
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

        client.message_callback_add(mqtt_topic + "/+/homeassistant/status/json", on_message_sensor_value)
        client.message_callback_add("homeassistant/" + mqtt_ha_topic + "/+/set", on_message_control_value)
        print("register callback func succ !!!")

# for paho-mqtt latest version
#   client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id, clean_session=False)

# for paho-mqtt==1.6.1
    client = mqtt.Client(client_id, clean_session=False)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(host, int(port))
    return client

def on_message_sensor_value(client, userdata, msg):
    def publish_address(value):
        publish_data = { "Address": value }
        client.publish("homeassistant/sensor/" + device_name + "-address/state", json.dumps(publish_data), 0, False) 
 
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
        switch_func = { "/4/0/4"    : publish_address,
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

            ha_manufacture = device_name.split("-")[0] # DAWONDNS
            ha_device_mac = device_name.split("-")[1] # 000000000000

            ha_address_data = {
                "name": ha_device_mac + "_Address",
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
                "unique_id": ha_device_mac + "_Switch",
                "device": {
                    "identifiers": ha_device_mac,
                    "name": device_name,
                    "manufacturer": ha_manufacture,
                },
                "state_topic": "homeassistant/" + mqtt_ha_topic + "/" + device_name + "/state",
                "command_topic": "homeassistant/" + mqtt_ha_topic + "/" + device_name + "/set",
            }

            client.publish("homeassistant/sensor/" + device_name + "-address/config", json.dumps(ha_address_data), 2, True)
            client.publish("homeassistant/sensor/" + device_name + "-voltage/config", json.dumps(ha_voltage_data), 2, True)
            client.publish("homeassistant/sensor/" + device_name + "-power/config", json.dumps(ha_power_data), 2, True)
            client.publish("homeassistant/sensor/" + device_name + "-temperature/config", json.dumps(ha_temperature_data), 2, True)
            client.publish("homeassistant/switch/" + device_name + "/config", json.dumps(ha_switch_data), 2, True)
        else:
            pass 

    device_name = msg.topic.split("/")[1] # DAWONDNS-000000000000
    device_data = json.loads(msg.payload.decode())
    publish_discovery()

    for data in device_data["result"]:
        parse_value(data["type"], data["value"])

def on_message_control_value(client, userdata, msg):
    device_name = msg.topic.split("/")[2]
    if device_name in plug_list:
        print(f"Match device: {device_name}:" + msg.payload.decode())
        send_data = {
            "clientId": device_name,
            "result": [
                {"type": "/100/0/31", "value": "true" if msg.payload.decode() == "ON" else "false"}
            ]
        }

        client.publish(mqtt_topic + "/homeassistant/" + device_name + "/execute/json", json.dumps(send_data), 2, False)
    else:
        print(f"Not registered device: {device_name}")
        

if __name__ == "__main__":
    while True:
        client = connect_mqtt(mqtt_clientid, mqtt_username, mqtt_password, mqtt_host, mqtt_port)
        client.subscribe("#")
        client.loop_forever()
