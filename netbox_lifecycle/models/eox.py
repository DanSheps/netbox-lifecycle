import base64
import hashlib

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from cryptography.fernet import InvalidToken
from netbox.models import JobsMixin, PrimaryModel
from utilities.choices import ChoiceSet

__all__ = ('EoXAPISettings',)


# START - MOVE THESE TO choices/eox.py
class SyncIntervalChoiceSet(ChoiceSet):
    HOURLY = 3600
    DAILY = 14400
    WEEKLY = 10080
    BIWEEKLY = 20160
    MONTHLY = 43200

    CHOICES = [
        (HOURLY, _('Hourly')),
        (DAILY, _('Daily')),
        (WEEKLY, _('Weekly')),
        (BIWEEKLY, _('Biweekly')),
        (MONTHLY, _('Monthly')),
    ]


class DriverChoiceSet(ChoiceSet):
    CISCO = 'cisco'
    CHOICES = [(CISCO, 'Cisco EoX'),]
# END MOVE


def _get_fernet():
    """Return a Fernet instance keyed from Django's SECRET_KEY."""

    from cryptography.fernet import Fernet
    key_material = settings.SECRET_KEY.encode()
    digest = hashlib.sha256(key_material).digest()
    fernet_key = base64.urlsafe_b64encode(digest)
    return Fernet(fernet_key)


class EoXAPISettings(JobsMixin, PrimaryModel):
    """
    Stores EoX API credentials, parameters, and sync configuration.
    The OAuth client secret is stored Fernet-encrypted at rest
    using a key derived from Django's SECRET_KEY.
    """

    url = models.URLField(
        max_length=300,
        verbose_name=_('API URL'),
        help_text='URL of the EoX API'
    )

    driver = models.CharField(
        choices=DriverChoiceSet,
        default=DriverChoiceSet.CISCO,
        verbose_name=_('Driver Type'),
        help_text=_('The EoX driver')
    )

    manufacturers = models.ManyToManyField(
        verbose_name=_("Manufacturer"),
        to='dcim.Manufacturer',
        related_name="eox"
    )

    enabled = models.BooleanField(
        default=False,
        help_text=_("Enable automatic EoX API synchronization.")
    )

    client_id = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_("OAuth Client ID"),
        help_text=_("Client ID Obtained from Cisco API Console (apiconsole.cisco.com).")
    )

    _client_secret = models.CharField(
        max_length=500,
        blank=True,
        db_column='client_secret',
        verbose_name=_("OAuth Client Secret")
    )

    sync_interval = models.PositiveIntegerField(
        choices=SyncIntervalChoiceSet,
        default=SyncIntervalChoiceSet.HOURLY,
        verbose_name=_('Sync Interval'),
        help_text=_('How often the background sync job should run.')
    )

    class Meta:
        verbose_name = _('EoX API Setting')
        verbose_name_plural = _('EoX API Settings')

        ordering = ('driver', 'url', 'pk',)
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'driver',
                ],

                name='%(app_label)s_%(class)s_unique_driver'
            )
        ]

    def __str__(self):
        return f'{self.url}'

    # ------------------------
    # Encrypted Client Secret
    # ------------------------

    @property
    def client_secret(self):
        if not self._client_secret:
            return ''
        try:
            return _get_fernet().decrypt(self._client_secret.encode()).decode()
        except InvalidToken:
            return ''

    @client_secret.setter
    def client_secret(self, value):
        if value:
            self._client_secret = _get_fernet().encrypt(value.encode()).decode()
        else:
            self._client_secret = ''

    @property
    def sync_interval_display(self):
        for value, label in SYNC_INTERVAL_CHOICES:
            if value == self.sync_interval:
                return label
        return f'{self.sync_interval} minutes'
