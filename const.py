DOMAIN = "network_rail_timetable"
PLATFORMS = ["sensor"]
UPDATE_INTERVAL_SECONDS = 60 # Update every 60 seconds
LIVE_DEPARTURE_BOARD_API_URL = "https://api1.raildata.org.uk/1010-live-departure-board-dep1_2/LDBWS/api/20220120/GetDepartureBoard/{crs_from}?numRows=1&filterCrs={crs_to}"

# Configuration constants
CONF_HOME_STATION = "home_station"
CONF_DESTINATION_STATION = "destination_station"