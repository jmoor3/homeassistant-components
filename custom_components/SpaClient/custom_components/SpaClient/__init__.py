import logging

import voluptuous as vol
import homeassistant.helpers.config_validation as cv

# Import the device class from the component that you want to support
from .spaclient import SpaClient
from homeassistant.helpers import discovery
from homeassistant.const import CONF_SCAN_INTERVAL
from datetime import timedelta

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'SpaClient'
ATTR_HOST_IP = 'spa_ip'
ATTR_NB_TOGGLE = 'nb_toggle'

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(ATTR_HOST_IP): cv.string,
        vol.Optional(ATTR_NB_TOGGLE, default=1): cv.positive_int,
        vol.Optional(CONF_SCAN_INTERVAL, default=1): cv.positive_int,
    })
}, extra=vol.ALLOW_EXTRA)

def setup(hass, config):
    """Set up the Spa."""
    global NETWORK
    global NB_TOGGLE
    global INTERVAL

    conf = config[DOMAIN]
    host_ip = conf[ATTR_HOST_IP]
    NETWORK = SpaData(host_ip)
    NB_TOGGLE = conf[ATTR_NB_TOGGLE]
    INTERVAL = timedelta(seconds=conf[CONF_SCAN_INTERVAL])

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
