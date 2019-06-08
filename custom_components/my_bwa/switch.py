import logging

# Import the device class from the component that you want to support
from custom_components import my_bwa
from homeassistant.components.switch import SwitchDevice
from datetime import timedelta

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(seconds=1)

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the sensor platform."""
    spa_data = my_bwa.NETWORK
    add_devices([SpaPump(1, spa_data), SpaPump(2, spa_data), SpaPump(3, spa_data)])

class SpaPump(SwitchDevice):
    """Representation of a Sensor."""
    def __init__(self, pump_num, data):
        """Initialize the sensor."""
        self._spa = data.spa
        self._pump_num = pump_num

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'Spa Pump ' + str(self._pump_num)

    @property
    def device_state_attributes(self):
        """Return the state attributes of the device."""
        attrs = {}

        attrs["Current Temp"] = self._spa.get_current_temp()
        attrs["Time"] = self._spa.get_current_time()
        attrs["Set Temp"] = self._spa.get_set_temp()
        attrs["Pump 1"] = self._spa.get_pump(1)
        attrs["Pump 2"] = self._spa.get_pump(2)
        attrs["Pump 3"] = self._spa.get_pump(3)
        attrs["Temp Range"] = self._spa.get_temp_range()

        return attrs

    @property
    def is_on(self):
        """Return true if switch is on."""
        return self._spa.get_pump(self._pump_num) != "Off"

    def turn_on(self, **kwargs):
        """Instruct the switch to turn on."""
        _LOGGER.info("Spa Pump %s status %s", self._pump_num, self._spa.get_pump(self._pump_num))
        _LOGGER.info("Turning on Spa Pump %s", self._pump_num)
        self._spa.set_pump(self._pump_num, "High")

    def turn_off(self, **kwargs):
        """Instruct the switch to turn off."""
        _LOGGER.info("Spa Pump %s status %s", self._pump_num, self._spa.get_pump(self._pump_num))
        if self._spa.get_pump(self._pump_num) == "Low":
            _LOGGER.info("Turning on Spa Pump %s", self._pump_num)
        if self._spa.get_pump(self._pump_num) == "High":
            _LOGGER.info("Turning off Spa Pump %s", self._pump_num)
        self._spa.set_pump(self._pump_num, "Off")

    def update(self):
        """Fetch new state data for the sensor."""
        self._spa.read_all_msg()