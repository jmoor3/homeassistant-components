# Hass.io custom component - SpaClient

## What you need

- A Hot Tub Equipped with a Balboa BP System
- bwa™ Wi-Fi Module (50350)
- Reference : http://www.balboawatergroup.com/bwa

## SpaClient custom component setup

1-Copy these project files into your Home Assistant ```/config``` directory.

```
custom_components/SpaClient/__init__.py
custom_components/SpaClient/climate.py
custom_components/SpaClient/light.py
custom_components/SpaClient/manifest.json
custom_components/SpaClient/spaclient.py
custom_components/SpaClient/switch.py
```

2-Edit congifuration.yaml file entry:
```
SpaClient:
     spa_ip: 192.168.2.150 # Spa IP-adress, Required
     nb_toggle: 1          # 1 or 2 toggle to action the pumps (default = 1), Optional
     scan_interval: 1      # Poll the devices every x seconds (default = 1), Optional
```     

3-Restart your Hass.io. Wait few minutes (10-20 min.)... While the system installing the ```crc8``` module!

4-Restart your Hass.io. Enjoy!

## Needed python module

The ```crc8``` module is automatically installed when first used of this custom component on Hass.io.

## TODOs

- Create a ```const.py``` file
- Add the programming capacity of the filter cycles
- Add the time synchronization function
- Bring more information to the user in case of connect/receive/send issues
