import logging

import voluptuous as vol
import homeassistant.helpers.config_validation as cv

# Import the device class from the component that you want to support
from .spaclient import SpaClient
from homeassistant.helpers import discovery
from homeassistant.const import CONF_SCAN_INTERVAL
from datetime import timedelta

# Home Assistant depends on 3rd party packages for API specific code.
REQUIREMENTS = ['crc8==0.0.5']

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(seconds=1)

DOMAIN = 'my_bwa'
CONF_HOST_IP = "spa_ip"

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_HOST_IP): cv.string,
        vol.Optional(CONF_SCAN_INTERVAL, default=1): cv.positive_int,
    })
}, extra=vol.ALLOW_EXTRA)

def setup(hass, config):
    """Set up the Spa."""
    global NETWORK

    conf = config[DOMAIN]
    host_ip = conf[CONF_HOST_IP]
    NETWORK = SpaData(host_ip)

    setup_spa(hass, config)

    return True

class SpaData(object):
    """Get the latest data and update the states."""
    def __init__(self, host_ip):
        self.spa = SpaClient(SpaClient.get_socket(host_ip))

def setup_spa(hass, config):
    """Set up the Balboa Spa."""
    conf = config[DOMAIN]

    discovery.load_platform(hass, 'climate', DOMAIN, conf, config)
    discovery.load_platform(hass, 'light', DOMAIN, conf, config)
    discovery.load_platform(hass, 'switch', DOMAIN, conf, config)