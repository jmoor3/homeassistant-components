import logging

from datetime import timedelta

# Import the device class from the component that you want to support
from homeassistant.helpers.entity import Entity

from custom_components import bullfrog

# Import the device class from the component that you want to support
from homeassistant.components.light import ATTR_BRIGHTNESS, Light, PLATFORM_SCHEMA
from homeassistant.const import CONF_HOST, CONF_USERNAME, CONF_PASSWORD
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(seconds=1)


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the sensor platform."""
    spa_data = bullfrog.NETWORK
    add_devices([SpaLight(spa_data)])


class SpaLight(Light):
    """Representation of a Sensor."""

    def __init__(self, data):
        """Initialize the sensor."""
        self._spa = data.spa

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'BullFrog Spa Light'

    @property
    def device_state_attributes(self):
        """Return the state attributes of the device."""
        attrs = {}

        attrs["Current Temp"] = self._spa.get_current_temp()
        attrs["Time"] = self._spa.get_current_time()
        attrs["Set Temp"] = self._spa.get_set_temp()
        attrs["Pump 1"] = self._spa.get_pump1()
        attrs["Pump 2"] = self._spa.get_pump2()
        attrs["Temp Range"] = self._spa.get_temp_range()

        return attrs

    @property
    def is_on(self):
        """Return true if light is on."""
        return self._spa.get_light()

    def turn_on(self, **kwargs):
        """Instruct the light to turn on.

        You can skip the brightness part if your light does not support
        brightness control.
        """

        _LOGGER.info("Turning on Spa Light")
        _LOGGER.info("Spa light status %s", self._spa.get_light())
        self._spa.set_light(True)

    def turn_off(self, **kwargs):
        """Instruct the light to turn off."""

        _LOGGER.info("Turning off Spa Light")
        _LOGGER.info("Spa light status %s", self._spa.get_light())
        self._spa.set_light(False)

    def update(self):
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        self._spa.read_all_msg()


#spa = SpaClient(SpaClient.get_socket())
#SpaLight(spa)
