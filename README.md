# CSS PowerManagerServer to HomeAssistant Bridge
## How to install?
### 0. depends
```
python3 / paho-mqtt
```
### 1. add dummy plug for connecting CSS PowerMangerServer
```
# Settigns --> Device Mangement --> Add Device
ID : habridge0000
Devie Name : habridge
Model : habridge
Topic : dwd
Passsowrd : {you_like}
```
![image](https://blog.kakaocdn.net/dn/qKs0A/btrJSnqGuSg/2KO9LSjrb2pd8sXWNSDoF1/img.png)
### 2. associate macvlan to host network
```
# pysical ethernet : vmbr0
# host network : 192.168.0.0/24
# simulate network-if name : macvlan-shim
# powermangger server on 192.168.0.200 (macvlan docker network)
root@debian:~# ip link add macvlan-shim link vmbr0 type macvlan mode bridge
root@debian:~# ip addr add 192.168.0.234/24 dev macvlan-shim
root@debian:~# ip link set macvlan-shim up
root@debian:~# ip route add 192.168.0.200 dev macvlan-shim
```
```
root@debian:~# ifconfig
macvlan-shim: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.0.234  netmask 255.255.255.0  broadcast 0.0.0.0
        inet6 fe80::58df:ecff:fedd:5dfc  prefixlen 64  scopeid 0x20<link>
        ether 5a:df:ec:dd:5d:fc  txqueuelen 1000  (Ethernet)
        RX packets 1411692  bytes 362519143 (345.7 MiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 1318236  bytes 105173290 (100.3 MiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```
### 3. connect CSS PowerManager MQTT with HomeAssistant MQTT
```
root@debian:~# cat /etc/mosquitto/mosquitto.conf
# powermanager MQTT
connection dawon-bridge
address 192.168.0.200:1803
topic # both 0 dawon/ dwd.v1/
clientid DAWONDNS-habridge0000
remote_username DAWONDNS-habridge-habridge0000
remote_password {password you like}
cleansession true
try_private false
```
### 4. installing bridge service
```
mkdir -p /opt/dawon-bridge
cd /opt/dawon-brige
git clone https://github.com/djjproject/dawon_css_server_ha_bridge .
cp dawon-bridge.service /etc/systemd/system
systemctl enable dawon-bridge
```
```
# configure dawon bridge
root@debian:/opt/dawon-bridge# vi bridge.py
mqtt_clientid = 'habridge'
mqtt_username = ''
mqtt_password = ''
mqtt_host = '127.0.0.1'
mqtt_port = '1883'
mqtt_topic = 'dawon'
```
```
# run service
root@debian:/opt/dawon-bridge# systemctl start dawon-bridge
root@debian:/opt/dawon-bridge# systemctl status dawon-bridge
● dawon-bridge.service - Dawon Plug CSS HomeAssistant Bridge
   Loaded: loaded (/etc/systemd/system/dawon-bridge.service; enabled; vendor preset: enabled)
   Active: active (running) since Wed 2022-08-17 13:34:16 KST; 1min 8s ago
 Main PID: 8567 (python3)
    Tasks: 1 (limit: 4915)
   Memory: 8.7M
   CGroup: /system.slice/dawon-bridge.service
           └─8567 /usr/bin/python3 /opt/dawon-bridge/bridge.py

Aug 17 13:34:16 debian systemd[1]: Started Dawon Plug CSS HomeAssistant Bridge.
```
## Screenshot
![image](https://blog.kakaocdn.net/dn/bAzVDu/btrJWnQCcTq/usUS6tDCjVPkqUQbW07pH1/img.png)
![image](https://blog.kakaocdn.net/dn/bEBVqu/btrJV7AEbFY/O5ksZNwrt7tq5XrUUTkjuk/img.gif)
## MQTT HomeAssistant DATA
### 1. Discovery
```
homeassistant/sensor/DAWONDNS-B5X-6ac63ad2ae04-version/config {"name": "6ac63ad2ae04_Version", "unique_id": "6ac63ad2ae04_Version", "device": {"identifiers": "6ac63ad2ae04", "name": "DAWONDNS-B5X-6ac63ad2ae04", "manufacturer": "DAWONDNS"}, "state_topic": "homeassistant/sensor/DAWONDNS-B5X-6ac63ad2ae04-version/state", "value_template": "{{ value_json.Version }}"}
homeassistant/sensor/DAWONDNS-B5X-6ac63ad2ae04-address/config {"name": "6ac63ad2ae04_Address", "unique_id": "6ac63ad2ae04_Address", "device": {"identifiers": "6ac63ad2ae04", "name": "DAWONDNS-B5X-6ac63ad2ae04", "manufacturer": "DAWONDNS"}, "state_topic": "homeassistant/sensor/DAWONDNS-B5X-6ac63ad2ae04-address/state", "value_template": "{{ value_json.Address }}"}
homeassistant/sensor/DAWONDNS-B5X-6ac63ad2ae04-voltage/config {"device_class": "voltage", "name": "6ac63ad2ae04_Voltage", "unique_id": "6ac63ad2ae04_Voltage", "device": {"identifiers": "6ac63ad2ae04", "name": "DAWONDNS-B5X-6ac63ad2ae04", "manufacturer": "DAWONDNS"}, "state_topic": "homeassistant/sensor/DAWONDNS-B5X-6ac63ad2ae04-voltage/state", "value_template": "{{ value_json.Voltage }}", "unit_of_measurement": "V"}
homeassistant/sensor/DAWONDNS-B5X-6ac63ad2ae04-power/config {"device_class": "power", "name": "6ac63ad2ae04_Power", "unique_id": "6ac63ad2ae04_Power", "device": {"identifiers": "6ac63ad2ae04", "name": "DAWONDNS-B5X-6ac63ad2ae04", "manufacturer": "DAWONDNS"}, "state_topic": "homeassistant/sensor/DAWONDNS-B5X-6ac63ad2ae04-power/state", "value_template": "{{ value_json.Power }}", "unit_of_measurement": "W"}
homeassistant/sensor/DAWONDNS-B5X-6ac63ad2ae04-temperature/config {"device_class": "temperature", "name": "6ac63ad2ae04_Temperature", "unique_id": "6ac63ad2ae04_Switch", "device": {"identifiers": "6ac63ad2ae04", "name": "DAWONDNS-B5X-6ac63ad2ae04", "manufacturer": "DAWONDNS"}, "state_topic": "homeassistant/sensor/DAWONDNS-B5X-6ac63ad2ae04-temperature/state", "value_template": "{{ value_json.Temperature }}", "unit_of_measurement": "\u00b0C"}
homeassistant/switch/DAWONDNS-B5X-6ac63ad2ae04/config {"device_class": "switch", "name": "6ac63ad2ae04_Switch", "unique_id": "6ac63ad2ae04_Switch", "device": {"identifiers": "6ac63ad2ae04", "name": "DAWONDNS-B5X-6ac63ad2ae04", "manufacturer": "DAWONDNS"}, "state_topic": "homeassistant/dawon-switch/DAWONDNS-B5X-6ac63ad2ae04/state", "command_topic": "homeassistant/dawon-switch/DAWONDNS-B5X-6ac63ad2ae04/set"}
```
### 2. Sensor Value
#### from PowerManagerServer
```
{
"sid":"2",
"msg":{
"o":"n",
"e":[
{
"n":"/100/0/31",
"sv":"false",
"ti":"1660793324"
},
{
"n":"/100/0/1",
"sv":"227.00",
"ti":"1660793324"
},
{
"n":"/100/0/11",
"sv":"0.00",
"ti":"1660793324"
},
{
"n":"/100/0/4",
"sv":"40.67",
"ti":"1660793324"
}
]
}
}
{
"sid":"2",
"msg":{
"o":"n",
"e":[
{
"n":"/3/0/3",
"sv":"1.01.34",
"ti":"1660793324"
},
{
"n":"/4/0/4",
"sv":"192.168.1.4",
"ti":"1660793324"
}
]
}
}
```
#### to HomeAssistant
```
homeassistant/dawon-switch/DAWONDNS-B5X-2ef432510027/state OFF
homeassistant/sensor/DAWONDNS-B5X-2ef432510027-voltage/state {"Voltage": "227.00"}
homeassistant/sensor/DAWONDNS-B5X-2ef432510027-power/state {"Power": "0.00"}
homeassistant/sensor/DAWONDNS-B5X-2ef432510027-temperature/state {"Temperature": "40.67"}
homeassistant/sensor/DAWONDNS-B5X-2ef432510027-version/state {"Version": "1.01.34"}
homeassistant/sensor/DAWONDNS-B5X-2ef432510027-address/state {"Address": "192.168.1.4"}
```
### 3. HomeAssistant Control
#### from HomeAssistant
```
homeassistant/dawon-switch/DAWONDNS-B5X-2ef432510027/set ON
homeassistant/dawon-switch/DAWONDNS-B5X-2ef432510027/set OFF
```
#### to PowerManagerServer
```
dawon/iot-server/DAWONDNS-B5X-2ef432510027/execute/json {"sid": "2", "msg": {"o": "e", "e": [{"n": "/100/0/31", "sv": "true", "ti": 1660794416}]}}
dawon/iot-server/DAWONDNS-B5X-2ef432510027/execute/json {"sid": "2", "msg": {"o": "e", "e": [{"n": "/100/0/31", "sv": "false", "ti": 1660794420}]}}
```
