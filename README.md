# homeassistant-components

## Mitsubishi MQTT AC Split Duct

https://github.com/SwiCago/HeatPump

custom_components/climate/mitsubishi_mqtt.py

## Needed python modules

Make sure the CRC8 module is installed by running the following command on your homeassistant server: 

```
pip install crc8
```

## Balboa Hot Tub

**Use this fork, it is more up to date and has better functionality support - https://github.com/plmilord/Hass.io-custom-component-SpaClient**

Adds Balboa Hot Tub support. Copy the files from the directories into your homeassistant directory.

```
custom_components/bullfrog.py
custom_components/climate/bullfrog.py
custom_components/light/bullfrog.py
custom_components/switch/bullfrog.py
custom_components/spaclient.py
```

groups.yaml file entry:
```
spa:
    name: Spa
    entities:
      - light.bullfrog_spa_light
      - climate.bullfrog_spa_temperature
      - switch.bullfrog_spa_pump
```
congifuration.yaml file entry:
```
bullfrog:
     scan_interval: 1 # Not used yet
     spa_ip: 192.168.0.150
```     
     
TODOs:
- Find the right place for spaclient and factor out the data into a separate class
- Support more functionality like toggling heating mode
- Make states of various components into enums, support cycling through states better
