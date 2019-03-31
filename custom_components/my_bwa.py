import logging
import os
from datetime import timedelta
import voluptuous as vol

from custom_components.spaclient import SpaClient
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers import discovery
from homeassistant.const import (CONF_API_KEY, CONF_SCAN_INTERVAL)
from homeassistant.util import Throttle
from homeassistant.util.json import save_json

_CONFIGURING = {}
_LOGGER = logging.getLogger(__name__)

DOMAIN = 'my_bwa'

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=1)
SCAN_INTERVAL = timedelta(seconds=1)

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
    # scan_interval = conf[CONF_SCAN_INTERVAL]

    discovery.load_platform(hass, 'climate', DOMAIN, conf, config)
    discovery.load_platform(hass, 'light', DOMAIN, conf, config)
    discovery.load_platform(hass, 'switch', DOMAIN, conf, config)

class SpaData(object):
    """Get the latest data and update the states."""
    def __init__(self, host_ip):
        self.spa = SpaClient(SpaClient.get_socket(host_ip))

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        """Fetch new state data for the sensor."""
        self.spa.read_all_msg()
        _LOGGER.info("Spa data updated successfully")

def setup(hass, config):
    """Set up the Spa."""
    # pylint: disable=global-statement, import-error
    global NETWORK

    conf = config[DOMAIN]
    host_ip = conf[CONF_HOST_IP]
    NETWORK = SpaData(host_ip)

    setup_spa(hass, config)

    return True