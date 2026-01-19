from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_API_KEY
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DOMAIN, PLATFORMS, UPDATE_INTERVAL_SECONDS, CONF_HOME_STATION, CONF_DESTINATION_STATION
from .live_departure_board_api import LiveDepartureBoardAPI

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Network Rail Timetable from a config entry."""
    token = entry.data.get(CONF_API_KEY)
    home = entry.data.get(CONF_HOME_STATION)
    destination = entry.data.get(CONF_DESTINATION_STATION)

    api = LiveDepartureBoardAPI(token)

    async def async_update_data():
        try:
            return await api.async_get_departure_board(home, destination)
        except Exception as err:
            raise UpdateFailed(err)

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=f"{DOMAIN}_{entry.entry_id}",
        update_method=async_update_data,
        update_interval=timedelta(seconds=UPDATE_INTERVAL_SECONDS),
    )

    # Do first refresh so we have data available
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "api": api,
        "coordinator": coordinator,
        "home": home,
        "destination": destination,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        data = hass.data.get(DOMAIN, {}).pop(entry.entry_id, None)
        if data is not None:
            api = data.get("api")
            try:
                await api.async_close()
            except Exception:
                _LOGGER.debug("Error closing API session", exc_info=True)
    return unload_ok