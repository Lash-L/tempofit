import asyncio
from datetime import timedelta
import logging

import aiohttp
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .tempo_api import Tempo
from .const import DOMAIN
from datetime import datetime

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(hours=4)


class TempoSensorCoordinator(DataUpdateCoordinator[dict]):
    """Coordinator to manage sensor data."""

    def __init__(self, hass: HomeAssistant, tempo: Tempo):
        self.hass = hass
        self.tempo = tempo
        super().__init__(
            hass=hass, logger=_LOGGER, update_interval=SCAN_INTERVAL, name=DOMAIN
        )

    @property
    def id(self):
        return self.tempo.username

    async def _async_update_data(
        self,
    ) -> dict:
        data = {}
        try:
            await self.tempo.refresh()
            data["me"] = await self.tempo.me()
            data["all_time"] = await self.tempo.get_stats(
                datetime(year=2000, day=1, month=1), datetime.now()
            )
        except (aiohttp.ClientResponseError, asyncio.TimeoutError) as ex:
            raise UpdateFailed("Error refreshing data") from ex
        return data
