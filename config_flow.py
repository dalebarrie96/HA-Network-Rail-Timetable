import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_API_KEY
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.selector import (
    TextSelector,
    TextSelectorConfig,
    TextSelectorType,
)
from .const import DOMAIN, CONF_HOME_STATION, CONF_DESTINATION_STATION

STEP_USER_DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_API_KEY): TextSelector(
        TextSelectorConfig(type=TextSelectorType.PASSWORD)
    ),
    vol.Required(CONF_HOME_STATION): str,
    vol.Required(CONF_DESTINATION_STATION): str,
})

class NetworkRailConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 0
    MINOR_VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        errors = {}
        
        if user_input is None:
            return self.async_show_form(step_id="user", data_schema=STEP_USER_DATA_SCHEMA)

        # Validate station codes are uppercase and exactly 3 characters
        home_station = user_input[CONF_HOME_STATION].strip()
        dest_station = user_input[CONF_DESTINATION_STATION].strip()
        
        if not home_station.isupper() or len(home_station) != 3  or not home_station.isalpha():
            errors[CONF_HOME_STATION] = "Station code must be 3 uppercase letters (e.g., VIC)"
        
        if not dest_station.isupper() or len(dest_station) != 3 or not dest_station.isalpha():
            errors[CONF_DESTINATION_STATION] = "Station code must be 3 uppercase letters (e.g., VIC)"
        
        if errors:
            return self.async_show_form(
                step_id="user", 
                data_schema=STEP_USER_DATA_SCHEMA,
                errors=errors
            )

        # Store validated data
        validated_data = {
            CONF_API_KEY: user_input[CONF_API_KEY],
            CONF_HOME_STATION: home_station,
            CONF_DESTINATION_STATION: dest_station,
        }

        title = f"Network Rail Timetable Config: {home_station} → {dest_station}"
        return self.async_create_entry(title=title, data=validated_data)