"""Handles HTTP functions."""

from __future__ import annotations

import logging
from pathlib import Path

from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import CUSTOM_PATH, DOMAIN, SUB_DIRS, URL_BASE

_LOGGER = logging.getLogger(__name__)


class HTTPManager:
    """Manage HTTP paths."""

    def __init__(self, hass: HomeAssistant, config: ConfigEntry) -> None:
        """Initialise."""
        self.hass = hass
        self.config = config

    async def async_setup(self) -> bool:
        """Set up the HTTP Manager."""
        await self.create_url_paths()
        return True

    async def async_unload(self) -> bool:
        """Unload the HTTP Manager."""
        # Currently nothing to unload
        return True

    async def _async_register_path(self, url: str, path: str):
        """Register resource path if not already registered."""
        try:
            await self.hass.http.async_register_static_paths(
                [StaticPathConfig(url, path, False)]
            )
            _LOGGER.debug("Registered resource path from %s", path)
        except RuntimeError:
            # Runtime error - likley this is already registered.
            _LOGGER.debug("Resource path already registered")

    async def create_url_paths(self):
        """Create viewassist url paths."""

        # Create config/view_assist path if it doesn't exist
        vaca_dir = self.hass.config.path(DOMAIN)
        Path(vaca_dir).mkdir(exist_ok=True)

        # Create out list of standard sub dirs
        for sub_dir in SUB_DIRS:
            Path(vaca_dir, CUSTOM_PATH, sub_dir).mkdir(exist_ok=True)

        await self._async_register_path(f"/{URL_BASE}", vaca_dir)
