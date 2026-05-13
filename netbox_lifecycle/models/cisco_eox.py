import base64
import hashlib

from django.conf import settings
from django.db import models

__all__ = ('CiscoEoXSettings',)

SYNC_INTERVAL_CHOICES = [
    (60, 'Hourly'),
    (1440, 'Daily'),
    (10080, 'Weekly'),
    (20160, 'Biweekly'),
    (43200, 'Monthly'),
]


def _get_fernet():
    """Return a Fernet instance keyed from Django's SECRET_KEY."""
    from cryptography.fernet import Fernet

    key_material = settings.SECRET_KEY.encode()
    digest = hashlib.sha256(key_material).digest()
    fernet_key = base64.urlsafe_b64encode(digest)
    return Fernet(fernet_key)


class CiscoEoXSettings(models.Model):
    """
    Singleton model (pk=1) that stores Cisco EoX API credentials and sync
    configuration.  The OAuth client secret is stored Fernet-encrypted at rest
    using a key derived from Django's SECRET_KEY.

    A second source of truth is PLUGINS_CONFIG (see utilities/settings_loader.py);
    the database record takes precedence when present.
    """

    enabled = models.BooleanField(
        default=False,
        help_text='Enable automatic Cisco EoX API synchronisation.',
    )
    client_id = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='OAuth Client ID',
        help_text='Client ID obtained from Cisco API Console (apiconsole.cisco.com).',
    )
    _client_secret = models.CharField(
        max_length=500,
        blank=True,
        db_column='client_secret',
        verbose_name='OAuth Client Secret',
    )
    sync_interval = models.PositiveIntegerField(
        choices=SYNC_INTERVAL_CHOICES,
        default=10080,
        verbose_name='Sync Interval',
        help_text='How often the background sync job should run.',
    )
    manufacturer_names = models.CharField(
        max_length=500,
        default='Cisco',
        verbose_name='Manufacturer Names',
        help_text=(
            'Comma-separated list of manufacturer names whose device/module types '
            'will be queried against the Cisco EoX API.'
        ),
    )

    class Meta:
        verbose_name = 'Cisco EoX Settings'

    def __str__(self):
        return 'Cisco EoX Settings'

    # ------------------------------------------------------------------
    # Singleton helpers
    # ------------------------------------------------------------------

    @classmethod
    def get_or_create_settings(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    # ------------------------------------------------------------------
    # Encrypted client secret
    # ------------------------------------------------------------------

    @property
    def client_secret(self):
        if not self._client_secret:
            return ''
        try:
            return _get_fernet().decrypt(self._client_secret.encode()).decode()
        except Exception:
            # If decryption fails (e.g. SECRET_KEY rotated), return empty string
            return ''

    @client_secret.setter
    def client_secret(self, value):
        if value:
            self._client_secret = _get_fernet().encrypt(value.encode()).decode()
        else:
            self._client_secret = ''

    # ------------------------------------------------------------------
    # Convenience helpers
    # ------------------------------------------------------------------

    @property
    def manufacturer_names_list(self):
        """Return manufacturer names as a list of stripped strings."""
        return [n.strip() for n in self.manufacturer_names.split(',') if n.strip()]

    @property
    def sync_interval_display(self):
        for value, label in SYNC_INTERVAL_CHOICES:
            if value == self.sync_interval:
                return label
        return f'{self.sync_interval} minutes'
