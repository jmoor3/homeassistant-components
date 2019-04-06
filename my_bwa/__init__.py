import logging

import voluptuous as vol
import homeassistant.helpers.config_validation as cv

# Import the device class from the component that you want to support
from .spaclient import SpaClient
from homeassistant.helpers import discovery
from homeassistant.const import CONF_SCAN_INTERVAL
from datetime import timedelta

_CONFIGURING = {}
_LOGGER = logging.getLogger(__name__)

DOMAIN = 'my_bwa'

SCAN_INTERVAL = timedelta(seconds=10)

NETWORK = None

CONF_HOST_IP = "spa_ip"

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_HOST_IP): cv.string,
        vol.Optional(CONF_SCAN_INTERVAL, default=1): cv.positive_int,
    })
}, extra=vol.ALLOW_EXTRA)

def setup_spa(hass, config):
    """Set up the Balboa Spa."""
    conf = config[DOMAIN]

    discovery.load_platform(hass, 'climate', DOMAIN, conf, config)
    discovery.load_platform(hass, 'light', DOMAIN, conf, config)
    discovery.load_platform(hass, 'switch', DOMAIN, conf, config)

class SpaData(object):
    """Get the latest data and update the states."""
    def __init__(self, host_ip):
        self.spa = SpaClient(SpaClient.get_socket(host_ip))

    def update(self):
        """Fetch new state data for the sensor."""
        self.spa.read_all_msg()
        _LOGGER.info("Spa data updated successfully")

def setup(hass, config):
    """Set up the Spa."""
    global NETWORK

    conf = config[DOMAIN]
    host_ip = conf[CONF_HOST_IP]
    NETWORK = SpaData(host_ip)

    setup_spa(hass, config)

    return True