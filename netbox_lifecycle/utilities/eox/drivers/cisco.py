"""
Cisco EoX (End-of-Life) API driver.

Authentication: OAuth 2.0 client_credentials grant.

API documentation:
  https://developer.cisco.com/docs/support-apis/eox/
"""

import logging
from datetime import date

import requests
from django.core.cache import cache

from ..base import BaseEoXDriver, EoXAPIError

logger = logging.getLogger(__name__)

TOKEN_URL = 'https://id.cisco.com/oauth2/default/v1/token'
TOKEN_CACHE_KEY = 'netbox_lifecycle__cisco_eox_token'
# Sentinel date Cisco returns when no specific date exists
_CISCO_NULL_DATE = 'Y-Y-Y-Y'


class CiscoEoXDriver(BaseEoXDriver):
    """
    Thin wrapper around the Cisco EoX REST API v5.

    Usage::

        driver = CiscoEoXDriver(client_id='…', client_secret='…',
            base_url='https://apix.cisco.com/supporttools/eox/rest/5')
        records = driver.get_eox_by_product_id(['WS-C3750X-48P-S'])
        for r in records:
            parsed = driver.parse_eox_record(r)
    """

    # ------------------------------------------------------------------
    # Authentication
    # ------------------------------------------------------------------

    def _get_token(self) -> str:
        """
        Return a valid Bearer token, fetching a new one if the cached token
        has expired. Tokens are cached for 58 minutes (Cisco tokens expire
        after ~60 minutes).
        """
        token = cache.get(TOKEN_CACHE_KEY)
        if token:
            return token

        try:
            response = requests.post(
                TOKEN_URL,
                data={
                    'grant_type': 'client_credentials',
                    'client_id': self._client_id,
                    'client_secret': self._client_secret,
                },
                timeout=30,
            )
        except requests.RequestException as exc:
            raise EoXAPIError(f'Cisco OAuth token request failed: {exc}') from exc

        if response.status_code != 200:
            raise EoXAPIError(
                f'Cisco OAuth token request failed ({response.status_code}): '
                f'{response.text[:300]}'
            )

        payload = response.json()
        token = payload.get('access_token')
        if not token:
            raise EoXAPIError(f'Cisco OAuth response missing access_token: {payload}')

        # Cache for 58 minutes to avoid using an about-to-expire token
        cache.set(TOKEN_CACHE_KEY, token, timeout=58 * 60)
        return token

    def _get_headers(self) -> dict:
        return {
            'Authorization': f'Bearer {self._get_token()}',
            'Accept': 'application/json',
        }

    # ------------------------------------------------------------------
    # API calls
    # ------------------------------------------------------------------

    def get_eox_by_serial(self, serial_numbers: list[str]) -> list[dict]:
        """
        Look up EoX records for up to 20 serial numbers per chunk.

        Records where the API returned an error (e.g. serial not found) are
        silently filtered out.
        """
        if not serial_numbers:
            return []

        results = []
        for chunk in _chunks(serial_numbers, 20):
            serials_str = ','.join(chunk)
            url = f'{self._base_url}/EOXBySerialNumber/1/{serials_str}'
            results.extend(self._fetch_eox(url))
        return results

    def get_eox_by_product_id(self, product_ids: list[str]) -> list[dict]:
        """Look up EoX records for up to 20 Product IDs (part numbers) per chunk."""
        if not product_ids:
            return []

        results = []
        for chunk in _chunks(product_ids, 20):
            pids_str = ','.join(chunk)
            url = f'{self._base_url}/EOXByProductID/1/{pids_str}'
            results.extend(self._fetch_eox(url))
        return results

    def _fetch_eox(self, url: str) -> list[dict]:
        """Execute a GET against a pre-built EoX URL and return EoXRecord list."""
        try:
            response = requests.get(
                url,
                params={'responseencoding': 'json'},
                headers=self._get_headers(),
                timeout=30,
            )
        except requests.RequestException as exc:
            raise EoXAPIError(f'HTTP request failed: {exc}') from exc

        if response.status_code == 401:
            # Invalidate cached token and retry once
            cache.delete(TOKEN_CACHE_KEY)
            try:
                response = requests.get(
                    url,
                    params={'responseencoding': 'json'},
                    headers=self._get_headers(),
                    timeout=30,
                )
            except requests.RequestException as exc:
                raise EoXAPIError(f'HTTP request failed on retry: {exc}') from exc

        if response.status_code != 200:
            raise EoXAPIError(
                f'Cisco EoX API returned {response.status_code}: {response.text[:300]}'
            )

        data = response.json()
        raw_records = data.get('EOXRecord', [])

        # Filter out error records (no EoX data for this product/serial)
        return [
            r for r in raw_records if not r.get('EOXError') and r.get('EOLProductID')
        ]

    # ------------------------------------------------------------------
    # Parsing
    # ------------------------------------------------------------------

    @staticmethod
    def parse_eox_record(record: dict) -> dict:
        """
        Convert a raw Cisco EoX API record into a dict whose keys match
        HardwareLifecycle field names. Date values are ``datetime.date``
        instances or ``None`` when the API returns a sentinel/missing value.
        """

        def _date(field_name: str) -> date | None:
            obj = record.get(field_name, {})
            if isinstance(obj, dict):
                value = obj.get('value', '')
            else:
                value = str(obj) if obj else ''
            if not value or value == _CISCO_NULL_DATE:
                return None
            try:
                return date.fromisoformat(value)
            except ValueError:
                logger.debug('Cannot parse date %r for field %s', value, field_name)
                return None

        documentation = record.get('LinkToProductBulletinURL') or None
        # Truncate to the model's max_length of 500
        if documentation and len(documentation) > 500:
            documentation = documentation[:500]

        return {
            'end_of_sale': _date('EndOfSaleDate'),
            'end_of_maintenance': _date('EndOfSWMaintenanceReleases'),
            'end_of_security': _date('EndOfSecurityVulSupportDate'),
            'end_of_support': _date('LastDateOfSupport'),
            'last_contract_renewal': _date('EndOfServiceContractRenewal'),
            'documentation': documentation,
            # Informational extras (not stored directly, useful for logging)
            '_eol_product_id': record.get('EOLProductID', ''),
            '_product_description': record.get('ProductIDDescription', ''),
        }


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------


def _chunks(lst: list, size: int):
    """Yield successive ``size``-sized chunks from ``lst``."""
    for i in range(0, len(lst), size):
        yield lst[i : i + size]
