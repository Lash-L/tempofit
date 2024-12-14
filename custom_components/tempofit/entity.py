from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .coordinator import TempoSensorCoordinator
from .tempo_api import Tempo
from homeassistant.helpers.entity import Entity


class TempoEntity(CoordinatorEntity[TempoSensorCoordinator]):
    """Representation of a base Tempo Entity."""

    _attr_has_entity_name = True

    def __init__(self, unique_id: str, coordinator: TempoSensorCoordinator) -> None:
        """Initialize the Tempo Device."""
        self._attr_unique_id = unique_id
        self.coordinator = coordinator
        super().__init__(coordinator=coordinator)
