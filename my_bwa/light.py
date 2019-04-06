import logging

# Import the device class from the component that you want to support
from custom_components import my_bwa
from homeassistant.components.light import Light
from datetime import timedelta

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(seconds=1)

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the sensor platform."""
    spa_data = my_bwa.NETWORK
    add_devices([SpaLight(spa_data)])

class SpaLight(Light):
    """Representation of a Sensor."""
    def __init__(self, data):
        """Initialize the sensor."""
        self._spa = data.spa

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'Spa Light'

    @property
    def is_on(self):
        """Return true if light is on."""
        return self._spa.get_light()

    def turn_on(self, **kwargs):
        """Instruct the light to turn on."""
        _LOGGER.info("Turning on Spa Light")
        _LOGGER.info("Spa Light status %s", self._spa.get_light())
        self._spa.set_light(True)

    def turn_off(self, **kwargs):
        """Instruct the light to turn off."""
        _LOGGER.info("Turning off Spa Light")
        _LOGGER.info("Spa Light status %s", self._spa.get_light())
        self._spa.set_light(False)

    def update(self):
        """Fetch new state data for the sensor."""
        self._spa.read_all_msg()