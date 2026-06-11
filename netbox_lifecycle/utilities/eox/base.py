"""
Abstract base class and shared exception for EoX (End-of-Life/Sale/Support)
API drivers. Each vendor-specific driver subclass implements the lookup
methods against its own API.
"""

from abc import ABC, abstractmethod


class EoXAPIError(Exception):
    """Raised for authentication failures or vendor API-level errors."""


class BaseEoXDriver(ABC):
    """
    Interface a driver must implement so the sync job can query EoX records
    by serial number and by product/part number, then translate the vendor's
    record format into HardwareLifecycle field values.
    """

    def __init__(self, client_id: str, client_secret: str, base_url: str):
        if not client_id or not client_secret:
            raise EoXAPIError('client_id and client_secret must be non-empty.')
        self._client_id = client_id
        self._client_secret = client_secret
        self._base_url = base_url.rstrip('/')

    @abstractmethod
    def get_eox_by_serial(self, serial_numbers: list[str]) -> list[dict]:
        """Return raw EoX records for a list of serial numbers."""

    @abstractmethod
    def get_eox_by_product_id(self, product_ids: list[str]) -> list[dict]:
        """Return raw EoX records for a list of product/part numbers."""

    @staticmethod
    @abstractmethod
    def parse_eox_record(record: dict) -> dict:
        """
        Translate a raw vendor record into a dict whose keys match
        HardwareLifecycle field names. Values that are absent or null in
        the vendor record must be returned as ``None`` so the sync job can
        skip them rather than blanking existing data.
        """
