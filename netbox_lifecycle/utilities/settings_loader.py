"""
Resolves Cisco EoX plugin settings from the database (preferred) or from
PLUGINS_CONFIG (fallback).

Usage::

    from netbox_lifecycle.utilities.settings_loader import get_cisco_eox_settings
    cfg = get_cisco_eox_settings()
    if cfg is None:
        # not configured / not enabled
        ...
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

from netbox.plugins import get_plugin_config

logger = logging.getLogger(__name__)


@dataclass
class CiscoEoXConfig:
    """Resolved Cisco EoX configuration (from DB or PLUGINS_CONFIG)."""

    enabled: bool
    client_id: str
    client_secret: str
    sync_interval: int
    manufacturer_names: str

    @property
    def manufacturer_names_list(self) -> list[str]:
        return [n.strip() for n in self.manufacturer_names.split(',') if n.strip()]


def get_cisco_eox_settings() -> CiscoEoXConfig | None:
    """
    Return a :class:`CiscoEoXConfig` populated from the most authoritative
    source available:

    1. ``CiscoEoXSettings`` database record (pk=1) — if it exists, is enabled,
       and contains a ``client_id``.
    2. ``PLUGINS_CONFIG['netbox_lifecycle']`` keys prefixed with
       ``cisco_eox_*`` — if present.

    Returns ``None`` if no valid, enabled configuration is found.
    """
    # --- 1. Try database ---
    try:
        from netbox_lifecycle.models.cisco_eox import CiscoEoXSettings

        db_cfg = CiscoEoXSettings.objects.filter(pk=1).first()
        if db_cfg is not None and db_cfg.enabled and db_cfg.client_id:
            return CiscoEoXConfig(
                enabled=db_cfg.enabled,
                client_id=db_cfg.client_id,
                client_secret=db_cfg.client_secret,
                sync_interval=db_cfg.sync_interval,
                manufacturer_names=db_cfg.manufacturer_names,
            )
    except Exception as exc:
        # DB may not be available during migrations or tests
        logger.debug('Could not load CiscoEoXSettings from database: %s', exc)

    # --- 2. Fall back to PLUGINS_CONFIG ---
    try:
        enabled = get_plugin_config('netbox_lifecycle', 'cisco_eox_enabled')
        client_id = get_plugin_config('netbox_lifecycle', 'cisco_eox_client_id')
        client_secret = get_plugin_config('netbox_lifecycle', 'cisco_eox_client_secret')

        if enabled and client_id and client_secret:
            return CiscoEoXConfig(
                enabled=True,
                client_id=client_id,
                client_secret=client_secret,
                sync_interval=get_plugin_config(
                    'netbox_lifecycle', 'cisco_eox_sync_interval'
                ),
                manufacturer_names=get_plugin_config(
                    'netbox_lifecycle', 'cisco_eox_manufacturer_names'
                ),
            )
    except Exception as exc:
        logger.debug('Could not load Cisco EoX settings from PLUGINS_CONFIG: %s', exc)

    return None
