# Hass.io custom components - my_bwa

## Needed python module

The 'crc8' module is automatically installed when first used of this custom component on Hass.io.

## Balboa Hot Tub

Copy the files from the directories into your homeassistant directory.

```
custom_components/my_bwa/__init__.py
custom_components/my_bwa/climate.py
custom_components/my_bwa/light.py
custom_components/my_bwa/spaclient.py
custom_components/my_bwa/switch.py
```

congifuration.yaml file entry:
```
my_bwa:
     #scan_interval: 1   # Poll the device every x seconds instead of the default 30 seconds
     #nb_pump: 3         # Spa pump count (1, 2 or 3)
     #nb_toggle: 1       # Number of toggles to action the pumps (1 or 2)
     spa_ip: 192.168.0.150
```     
     
TODOs:
- Make the code to use the parameters scan_interval, nb_pump, nb_toggle
- Find the right place for spaclient and factor out the data into a separate class
- Support more functionality like toggling heating mode
- Make states of various components into enums, support cycling through states better
