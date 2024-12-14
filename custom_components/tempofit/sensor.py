import asyncio
import logging
import aiohttp
from typing import Any

from homeassistant import config_entries
from homeassistant.config_entries import ConfigEntry, OptionsFlow
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType
from homeassistant.components.sensor import SensorEntity
import voluptuous as vol
from .coordinator import TempoSensorCoordinator
from .entity import TempoEntity


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Roborock vacuum sensors."""
    coordinator = config_entry.runtime_data
    async_add_entities(
        TempoSensorEntity(
            coordinator,
            exercise,
        )
        for exercise in coordinator.data["me"]
    )
    async_add_entities(
        [
            TempoSensorAllTimeActiveMinutes(coordinator),
            TempoSensorAllTimeCaloriedBurned(coordinator),
            TempoSensorAllTimeWeightLifted(coordinator),
            TempoSensorAllTimeWorkoutCount(coordinator),
        ]
    )


class TempoSensorEntity(TempoEntity, SensorEntity):
    """Representation of a Roborock sensor."""

    def __init__(
        self,
        coordinator: TempoSensorCoordinator,
        exercise: str,
    ) -> None:
        """Initialize the entity."""
        super().__init__(
            f"{exercise}_{coordinator.id}",
            coordinator,
        )
        self._name = f"{exercise} Weight"
        self._exercise = exercise

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def native_value(self):
        """Return the current weight."""
        if self.coordinator.data:
            return self.coordinator.data["me"].get(self._exercise)
        return None


class TempoSensorAllTimeWorkoutCount(TempoEntity, SensorEntity):
    """Representation of a Roborock sensor."""

    def __init__(
        self,
        coordinator: TempoSensorCoordinator,
    ) -> None:
        """Initialize the entity."""
        self._name = f"All Workout Count"
        super().__init__(
            f"{self._name}_{coordinator.id}",
            coordinator,
        )

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def native_value(self):
        """Return the current weight."""
        if self.coordinator.data:
            return self.coordinator.data["all_time"].numWorkouts
        return None


class TempoSensorAllTimeWeightLifted(TempoEntity, SensorEntity):
    """Representation of a Roborock sensor."""

    def __init__(
        self,
        coordinator: TempoSensorCoordinator,
    ) -> None:
        """Initialize the entity."""
        self._name = f"All Weighted Lifted"
        super().__init__(
            f"{self._name}_{coordinator.id}",
            coordinator,
        )

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def native_value(self):
        """Return the current weight."""
        if self.coordinator.data:
            return self.coordinator.data["all_time"].weightLifted
        return None


class TempoSensorAllTimeCaloriedBurned(TempoEntity, SensorEntity):
    """Representation of a Roborock sensor."""

    def __init__(
        self,
        coordinator: TempoSensorCoordinator,
    ) -> None:
        """Initialize the entity."""
        self._name = f"All calories burned"

        super().__init__(
            f"{self._name}_{coordinator.id}",
            coordinator,
        )

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def native_value(self):
        """Return the current weight."""
        if self.coordinator.data:
            return self.coordinator.data["all_time"].caloriesBurned
        return None


class TempoSensorAllTimeActiveMinutes(TempoEntity, SensorEntity):
    """Representation of a Roborock sensor."""

    def __init__(
        self,
        coordinator: TempoSensorCoordinator,
    ) -> None:
        """Initialize the entity."""
        self._name = f"All Active Minutes"
        super().__init__(
            f"{self._name}_{coordinator.id}",
            coordinator,
        )

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def native_value(self):
        """Return the current weight."""
        if self.coordinator.data:
            return self.coordinator.data["all_time"].activeMinutes
        return None
