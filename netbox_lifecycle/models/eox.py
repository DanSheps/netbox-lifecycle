import base64
import hashlib

from core.choices import JobIntervalChoices
from cryptography.fernet import InvalidToken
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from netbox.models import JobsMixin, PrimaryModel

from netbox_lifecycle.choices.eox import DriverChoices

__all__ = ('EoXAPISettings',)


def _get_fernet():
    """Return a Fernet instance keyed from Django's SECRET_KEY."""
    from cryptography.fernet import Fernet

    key_material = settings.SECRET_KEY.encode()
    digest = hashlib.sha256(key_material).digest()
    fernet_key = base64.urlsafe_b64encode(digest)
    return Fernet(fernet_key)


class EoXAPISettings(JobsMixin, PrimaryModel):
    """
    Stores EoX API credentials, parameters, and sync configuration for a single
    vendor driver. Each row represents one configured EoX endpoint; multiple
    rows for the same driver (e.g. different URLs) are permitted.

    The OAuth client secret is stored Fernet-encrypted at rest using a key
    derived from Django's SECRET_KEY.
    """

    driver = models.CharField(
        choices=DriverChoices,
        default=DriverChoices.CISCO,
        verbose_name=_('Driver'),
        help_text=_('The EoX driver implementation used to query this endpoint.'),
    )

    url = models.URLField(
        max_length=300,
        verbose_name=_('API URL'),
        help_text=_('Base URL of the EoX API.'),
    )

    manufacturers = models.ManyToManyField(
        to='dcim.Manufacturer',
        related_name='eox_settings',
        verbose_name=_('Manufacturers'),
        help_text=_('DeviceTypes/ModuleTypes from these manufacturers are queried.'),
    )

    enabled = models.BooleanField(
        default=False,
        help_text=_('Enable automatic EoX API synchronization.'),
    )

    client_id = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_('OAuth Client ID'),
    )

    _client_secret = models.CharField(
        max_length=500,
        blank=True,
        db_column='client_secret',
        verbose_name=_('OAuth Client Secret'),
    )

    sync_interval = models.PositiveIntegerField(
        choices=JobIntervalChoices,
        default=JobIntervalChoices.INTERVAL_DAILY,
        verbose_name=_('Sync Interval'),
        help_text=_('How often the background sync job should run.'),
    )

    last_synced = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_('Last synced'),
        editable=False,
    )

    clone_fields = ('driver', 'url', 'sync_interval')

    class Meta:
        verbose_name = _('EoX API Settings')
        verbose_name_plural = _('EoX API Settings')
        ordering = ('driver', 'url', 'pk')
        constraints = (
            models.UniqueConstraint(
                fields=('driver', 'url'),
                name='%(app_label)s_%(class)s_unique_driver_url',
                violation_error_message=_(
                    'An EoX settings record for this driver and URL already exists.'
                ),
            ),
        )
        permissions = (('sync', _('Trigger an EoX sync')),)

    def __str__(self):
        return f'{self.get_driver_display()} — {self.url}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_lifecycle:eoxapisettings', args=[self.pk])

    # ------------------------------------------------------------------
    # Encrypted client secret
    # ------------------------------------------------------------------

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

    # ------------------------------------------------------------------
    # Recurring sync scheduling
    # ------------------------------------------------------------------

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.enabled and self.client_id and self._client_secret:
            from netbox_lifecycle.jobs import EoXSyncJob

            EoXSyncJob.enqueue_once(instance=self, interval=self.sync_interval)
