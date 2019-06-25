# Hass.io custom component - my_bwa

## Needed python module

The ```crc8``` module is automatically installed when first used of this custom component on Hass.io.

## Balboa Hot Tub

Copy the files from the directories into your homeassistant directory.

```
custom_components/my_bwa/__init__.py
custom_components/my_bwa/climate.py
custom_components/my_bwa/light.py
custom_components/my_bwa/manifest.json
custom_components/my_bwa/spaclient.py
custom_components/my_bwa/switch.py
```

congifuration.yaml file entry:
```
my_bwa:
     spa_ip: 192.168.2.150 # Spa IP-adress, Required
     nb_toggle: 1          # 1 or 2 toggle to action the pumps (default = 1), Optional
     scan_interval: 1      # Poll the devices every x seconds (default = 1), Optional
```     
     
TODOs:
- Create a ```const.py``` file
- Introduce asynchronous programming in this custom component
- Add the programming capacity of the filter cycles
- Add the time synchronization function
- Bring more information to the user in case of connect/receive/send issues
