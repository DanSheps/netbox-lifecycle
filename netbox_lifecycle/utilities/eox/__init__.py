"""
EoX driver registry. Add a new vendor by implementing a BaseEoXDriver
subclass under ``drivers/`` and registering it in DRIVERS.
"""

from netbox_lifecycle.choices.eox import DriverChoices

from .base import BaseEoXDriver, EoXAPIError
from .drivers import CiscoEoXDriver

__all__ = ('BaseEoXDriver', 'EoXAPIError', 'DRIVERS', 'get_driver')


DRIVERS: dict[str, type[BaseEoXDriver]] = {
    DriverChoices.CISCO: CiscoEoXDriver,
}


def get_driver(name: str) -> type[BaseEoXDriver]:
    try:
        return DRIVERS[name]
    except KeyError as exc:
        raise EoXAPIError(f'Unknown EoX driver: {name!r}') from exc
