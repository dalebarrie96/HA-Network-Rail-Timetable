import aiohttp
from typing import Optional
from .const import LIVE_DEPARTURE_BOARD_API_URL, API_TIMEOUT_SECONDS

class LiveDepartureBoardAPI:
    def __init__(self, token: str, session: Optional[aiohttp.ClientSession] = None):
        self.token = token
        self._external_session = session is not None
        self._session = session or aiohttp.ClientSession()

    async def async_close(self):
        if not self._external_session:
            await self._session.close()

    async def async_get_departure_board(self, crs_from: str, crs_to: str):
        url = LIVE_DEPARTURE_BOARD_API_URL.format(crs_from=crs_from, crs_to=crs_to)
        
        headers = {
            "x-apikey": self.token,
            "Accept": "application/json"
        }

        async with self._session.get(url, headers=headers, timeout=API_TIMEOUT_SECONDS) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise Exception(f"Live Departure Board API returned HTTP {resp.status}: {text[:200]}")
            
            data = await resp.json()

        return self._parse_departure_board_response(data)

    def _parse_departure_board_response(self, data: dict):
        # Parse JSON response and extract the first train service
        train_services = data.get('trainServices', [])
        
        if not train_services:
            # No services available
            return {
                'scheduled': None,
                'estimated': None,
                'platform': None,
                'origin': None,
                'destination': None,
                'status': 'No services',
                'delayed': False,
                'cancelled': False
            }
        
        # Get the first service
        service = train_services[0]
        
        # Extract relevant information
        scheduled = service.get('std')  # Scheduled Time of Departure
        estimated = service.get('etd')  # Estimated Time of Departure
        platform = service.get('platform')
        is_cancelled = service.get('isCancelled', False)
        
        # Get origin name
        origin_name = None
        origins = service.get('origin', [])
        if origins:
            origin_name = origins[0].get('locationName')

        # Get destination name
        dest_name = None
        destinations = service.get('destination', [])
        if destinations:
            dest_name = destinations[0].get('locationName')

        # Determine delay status and overall status
        is_delayed = False
        
        if is_cancelled:
            status = 'Cancelled'
            is_delayed = True
        elif estimated and estimated.lower() == 'on time':
            status = 'On time'
            is_delayed = False
        elif estimated and scheduled and estimated != scheduled:
            # Estimated time differs from scheduled - train is delayed
            status = 'Delayed'
            is_delayed = True
        else:
            status = 'Unknown'
            is_delayed = False
        
        return {
            'scheduled': scheduled,
            'estimated': estimated,
            'platform': platform,
            'origin': origin_name,
            'destination': dest_name,
            'status': status,
            'delayed': is_delayed,
            'cancelled': is_cancelled
        }