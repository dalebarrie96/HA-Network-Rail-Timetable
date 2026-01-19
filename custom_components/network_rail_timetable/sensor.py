from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import Entity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]

    async_add_entities([
        NextTrainSensor(entry.entry_id, coordinator)
    ], True)


class BaseNetworkRailEntity(Entity):
    def __init__(self, entry_id: str, coordinator):
        self.entry_id = entry_id
        self.coordinator = coordinator

    @property
    def available(self):
        return self.coordinator.last_update_success
    
    @property
    def extra_state_attributes(self):
        """All other train data as attributes"""
        return {
            "platform": self.coordinator.data.get("platform"),
            "origin": self.coordinator.data.get("origin"),
            "destination": self.coordinator.data.get("destination"),
            "status": self.coordinator.data.get("status"),
            "scheduled": self.coordinator.data.get("scheduled"),
            "estimated": self.coordinator.data.get("estimated"),
            "delayed": self.coordinator.data.get("delayed"),
            "cancelled": self.coordinator.data.get("cancelled"),
        }


class NextTrainSensor(SensorEntity, BaseNetworkRailEntity):
    _attr_should_poll = False

    def __init__(self, entry_id: str, coordinator):
        BaseNetworkRailEntity.__init__(self, entry_id, coordinator)
        self._attr_name = "Next Train"
        self._attr_unique_id = f"{entry_id}_next_train"

    @property
    def native_value(self):
        """Main state shows scheduled departure time"""
        scheduled = self.coordinator.data.get("scheduled")
        estimated = self.coordinator.data.get("estimated")
        
        if estimated and estimated.lower() != "on time":
            return estimated
        else:
            return scheduled
    
    @property
    def icon(self):
        """Train icon https://pictogrammers.com/library/mdi/icon/train/"""
        return "mdi:train"


    async def async_added_to_hass(self):
        self.async_on_remove(self.coordinator.async_add_listener(self.async_write_ha_state))