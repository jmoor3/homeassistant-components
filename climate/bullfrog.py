from datetime import timedelta
import logging
import voluptuous as vol


# Import the device class from the component that you want to support
from homeassistant.helpers.entity import Entity

# Import the device class from the component that you want to support
from homeassistant.const import (
    ATTR_ENTITY_ID, CONF_SCAN_INTERVAL,
    STATE_ON, ATTR_TEMPERATURE, TEMP_FAHRENHEIT)

from custom_components import bullfrog
from homeassistant.components.climate import (
    DOMAIN, STATE_COOL, STATE_HEAT, STATE_AUTO, STATE_IDLE, ClimateDevice,
    ATTR_TARGET_TEMP_LOW, ATTR_TARGET_TEMP_HIGH, SUPPORT_TARGET_TEMPERATURE,
    SUPPORT_AWAY_MODE, SUPPORT_HOLD_MODE, SUPPORT_OPERATION_MODE,
    SUPPORT_TARGET_HUMIDITY_LOW, SUPPORT_TARGET_HUMIDITY_HIGH,
    SUPPORT_AUX_HEAT, SUPPORT_TARGET_TEMPERATURE_HIGH, SUPPORT_FAN_MODE,
    SUPPORT_TARGET_TEMPERATURE_LOW, STATE_OFF)
import homeassistant.helpers.config_validation as cv
from homeassistant.util.temperature import convert as convert_temperature

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(seconds=1)

SUPPORT_FLAGS = (SUPPORT_TARGET_TEMPERATURE)

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the sensor platform."""
    spa_data = bullfrog.NETWORK
    add_devices([SpaTemp(spa_data)])

class SpaTemp(ClimateDevice):
    def __init__(self, data):
        """Initialize the sensor."""
        self._spa = data.spa

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'BullFrog Spa Temperature'

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return SUPPORT_FLAGS

    @property
    def current_temperature(self):
        """Return true if light is on."""
        return self._spa.get_current_temp()

    @property
    def target_temperature(self):
        return self._spa.get_set_temp()

    def set_temperature(self, **kwargs):
        _LOGGER.info("Setting Temperature")
        self._spa.send_config_request()
        self._spa.set_temperature(kwargs.get(ATTR_TEMPERATURE))

    @property
    def max_temp(self):
        """Return the maximum temperature."""
        return convert_temperature(104, TEMP_FAHRENHEIT, self.temperature_unit)

    @property
    def temperature_unit(self):
        """Return the unit of measurement used by the platform."""
        return TEMP_FAHRENHEIT

    @property
    def current_operation(self):
        """Return current operation ie. heat, cool, idle."""
        return "Set Temperature"

    def update(self):
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        self._spa.read_all_msg()

    def turn_off(self):
        pass

    def turn_on(self):
        pass


#spa = SpaClient(SpaClient.get_socket())
#SpaLight(spa)
